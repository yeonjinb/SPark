#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
문서 파싱 시스템 - 자연어 문서에서 주차장 관련 정보 추출
"""

import re
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from natural_language_processor import NaturalLanguageProcessor
from data_filtering_system import DataFilteringSystem

class DocumentParser:
    def __init__(self):
        """문서 파서 초기화"""
        self.nlp = NaturalLanguageProcessor()
        self.filtering_system = DataFilteringSystem()
        
        # 문서 타입별 파싱 규칙
        self.document_patterns = {
            'email': {
                'subject_pattern': r'제목[:\s]*([^\n]+)',
                'content_pattern': r'내용[:\s]*([\s\S]+)',
                'time_pattern': r'(\d{4}[-/]\d{2}[-/]\d{2}|\d{2}:\d{2})'
            },
            'chat': {
                'message_pattern': r'(\d{2}:\d{2})\s*([^:]+):\s*(.+)',
                'system_pattern': r'시스템[:\s]*([^\n]+)'
            },
            'report': {
                'section_pattern': r'([가-힣\s]+)[:\s]*\n([\s\S]+?)(?=\n[가-힣\s]+[:\s]*\n|\Z)',
                'bullet_pattern': r'[-•]\s*(.+)',
                'number_pattern': r'\d+\.\s*(.+)'
            },
            'general': {
                'paragraph_pattern': r'([^\n]+(?:\n[^\n]+)*)',
                'sentence_pattern': r'([^.!?]+[.!?])'
            }
        }
    
    def detect_document_type(self, document: str) -> str:
        """문서 타입 자동 감지"""
        document_lower = document.lower()
        
        # 이메일 패턴
        if any(keyword in document_lower for keyword in ['제목:', '발신자:', '수신자:', 'cc:', 'bcc:']):
            return 'email'
        
        # 채팅 패턴
        if re.search(r'\d{2}:\d{2}\s+[^:]+:', document):
            return 'chat'
        
        # 보고서 패턴
        if any(keyword in document_lower for keyword in ['목차', '요약', '결론', '참고문헌']):
            return 'report'
        
        return 'general'
    
    def parse_email(self, document: str) -> Dict:
        """이메일 문서 파싱"""
        result = {
            'type': 'email',
            'subject': '',
            'content': '',
            'extracted_commands': [],
            'metadata': {}
        }
        
        # 제목 추출
        subject_match = re.search(self.document_patterns['email']['subject_pattern'], document)
        if subject_match:
            result['subject'] = subject_match.group(1).strip()
        
        # 내용 추출
        content_match = re.search(self.document_patterns['email']['content_pattern'], document)
        if content_match:
            result['content'] = content_match.group(1).strip()
        
        # 시간 정보 추출
        time_matches = re.findall(self.document_patterns['email']['time_pattern'], document)
        result['metadata']['times'] = time_matches
        
        # 주차장 관련 명령어 추출
        full_text = f"{result['subject']} {result['content']}"
        result['extracted_commands'] = self.nlp.process_document(full_text)
        
        return result
    
    def parse_chat(self, document: str) -> Dict:
        """채팅 문서 파싱"""
        result = {
            'type': 'chat',
            'messages': [],
            'extracted_commands': [],
            'participants': set()
        }
        
        lines = document.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 메시지 패턴 매칭
            message_match = re.match(self.document_patterns['chat']['message_pattern'], line)
            if message_match:
                time, sender, content = message_match.groups()
                
                message = {
                    'time': time,
                    'sender': sender,
                    'content': content
                }
                
                result['messages'].append(message)
                result['participants'].add(sender)
                
                # 주차장 관련 명령어 추출
                if any(keyword in content.lower() for keyword in ['주차장', '주차', '파킹']):
                    parsed_command = self.nlp.parse_complete_command(content)
                    if parsed_command['confidence'] > 0.3:
                        parsed_command['message_info'] = {
                            'time': time,
                            'sender': sender
                        }
                        result['extracted_commands'].append(parsed_command)
            
            # 시스템 메시지 처리
            system_match = re.search(self.document_patterns['chat']['system_pattern'], line)
            if system_match:
                result['messages'].append({
                    'time': '',
                    'sender': 'SYSTEM',
                    'content': system_match.group(1)
                })
        
        result['participants'] = list(result['participants'])
        
        return result
    
    def parse_report(self, document: str) -> Dict:
        """보고서 문서 파싱"""
        result = {
            'type': 'report',
            'sections': {},
            'extracted_commands': [],
            'summary': ''
        }
        
        # 섹션별 파싱
        sections = re.findall(self.document_patterns['report']['section_pattern'], document)
        
        for section_title, section_content in sections:
            section_title = section_title.strip()
            section_content = section_content.strip()
            
            result['sections'][section_title] = {
                'content': section_content,
                'bullets': re.findall(self.document_patterns['report']['bullet_pattern'], section_content),
                'numbered_items': re.findall(self.document_patterns['report']['number_pattern'], section_content)
            }
            
            # 주차장 관련 명령어 추출
            section_commands = self.nlp.process_document(section_content)
            for command in section_commands:
                command['section'] = section_title
                result['extracted_commands'].append(command)
        
        # 전체 문서에서 주차장 관련 명령어 추출
        all_commands = self.nlp.process_document(document)
        result['extracted_commands'].extend(all_commands)
        
        # 요약 생성
        result['summary'] = self._generate_summary(result['extracted_commands'])
        
        return result
    
    def parse_general(self, document: str) -> Dict:
        """일반 문서 파싱"""
        result = {
            'type': 'general',
            'paragraphs': [],
            'sentences': [],
            'extracted_commands': [],
            'statistics': {}
        }
        
        # 문단별 분리
        paragraphs = re.findall(self.document_patterns['general']['paragraph_pattern'], document)
        result['paragraphs'] = [p.strip() for p in paragraphs if p.strip()]
        
        # 문장별 분리
        sentences = re.findall(self.document_patterns['general']['sentence_pattern'], document)
        result['sentences'] = [s.strip() for s in sentences if s.strip()]
        
        # 주차장 관련 명령어 추출
        result['extracted_commands'] = self.nlp.process_document(document)
        
        # 통계 정보
        result['statistics'] = {
            'total_paragraphs': len(result['paragraphs']),
            'total_sentences': len(result['sentences']),
            'total_commands': len(result['extracted_commands']),
            'avg_confidence': sum(cmd['confidence'] for cmd in result['extracted_commands']) / max(len(result['extracted_commands']), 1)
        }
        
        return result
    
    def parse_document(self, document: str, document_type: Optional[str] = None) -> Dict:
        """문서 파싱 메인 함수"""
        if document_type is None:
            document_type = self.detect_document_type(document)
        
        # 문서 타입별 파싱
        if document_type == 'email':
            return self.parse_email(document)
        elif document_type == 'chat':
            return self.parse_chat(document)
        elif document_type == 'report':
            return self.parse_report(document)
        else:
            return self.parse_general(document)
    
    def _generate_summary(self, commands: List[Dict]) -> str:
        """명령어 목록에서 요약 생성"""
        if not commands:
            return "주차장 관련 명령어가 없습니다."
        
        summary_parts = []
        
        # 명령어 타입별 집계
        command_types = {}
        time_requirements = []
        locations = set()
        
        for cmd in commands:
            cmd_type = cmd['command_type']
            command_types[cmd_type] = command_types.get(cmd_type, 0) + 1
            
            if cmd['time_info']['hours']:
                time_requirements.append(f"{cmd['time_info']['hours']}시간")
            
            locations.update(cmd['locations'])
        
        # 요약 생성
        if command_types:
            type_summary = ", ".join([f"{cmd_type}({count}개)" for cmd_type, count in command_types.items()])
            summary_parts.append(f"명령어 유형: {type_summary}")
        
        if time_requirements:
            time_summary = ", ".join(set(time_requirements))
            summary_parts.append(f"시간 요구사항: {time_summary}")
        
        if locations:
            location_summary = ", ".join(locations)
            summary_parts.append(f"관련 위치: {location_summary}")
        
        return " | ".join(summary_parts)
    
    def process_document_with_filtering(self, document: str, document_type: Optional[str] = None) -> Dict:
        """문서 파싱 + 필터링 결과 생성"""
        # 1. 문서 파싱
        parsed_doc = self.parse_document(document, document_type)
        
        # 2. 각 명령어에 대해 필터링 적용
        processed_commands = []
        
        for command in parsed_doc['extracted_commands']:
            if command['confidence'] > 0.3:  # 신뢰도 임계값
                # 필터링 시스템으로 주차장 검색
                filtering_result = self.filtering_system.process_voice_command(command['original_text'])
                
                processed_command = {
                    'original_command': command,
                    'filtering_result': filtering_result,
                    'recommendations': filtering_result['results'][:3]  # 상위 3개만
                }
                
                processed_commands.append(processed_command)
        
        # 3. 결과 통합
        result = parsed_doc.copy()
        result['processed_commands'] = processed_commands
        result['total_recommendations'] = sum(len(cmd['recommendations']) for cmd in processed_commands)
        
        return result

# 테스트 함수
def test_document_parser():
    """문서 파서 테스트"""
    parser = DocumentParser()
    
    # 테스트 문서들
    test_documents = {
        'email': """
제목: 2시간 주차장 예약 요청
발신자: 홍길동 <hong@example.com>
수신자: 주차장 관리팀 <parking@example.com>

내용:
안녕하세요. 내일 오전 10시부터 12시까지 2시간 동안 주차장을 예약하고 싶습니다.
강남역 근처 주차장 중에서 5000원 이하로 이용 가능한 곳이 있나요?
SUV 차량입니다.

감사합니다.
홍길동
        """,
        
        'chat': """
09:30 김철수: 안녕하세요! 3시간 주차할 곳 찾아주세요
09:31 시스템: 주차장 검색을 시작합니다
09:32 이영희: 명동 주차장 정보 알려주세요
09:33 박민수: SUV 1시간 주차장 예약해줘
09:34 시스템: 검색 완료되었습니다
        """,
        
        'report': """
주차장 이용 현황 보고서

요약:
본 보고서는 2024년 1월 주차장 이용 현황을 분석한 결과입니다.

주요 발견사항:
- 2시간 주차장 이용률이 가장 높음
- 강남역 주차장의 만족도가 4.5점으로 최고
- 명동 지역 주차장은 주말 이용률이 높음

권장사항:
- 3시간 주차장 시설 확충 필요
- 전기차 충전시설 추가 설치 권장
        """
    }
    
    print("📄 문서 파서 테스트")
    print("=" * 60)
    
    for doc_type, document in test_documents.items():
        print(f"\n📋 {doc_type.upper()} 문서 테스트")
        print("-" * 40)
        
        result = parser.process_document_with_filtering(document, doc_type)
        
        print(f"문서 타입: {result['type']}")
        print(f"추출된 명령어 수: {len(result['extracted_commands'])}")
        print(f"처리된 명령어 수: {len(result['processed_commands'])}")
        print(f"총 추천 주차장 수: {result['total_recommendations']}")
        
        if result['processed_commands']:
            print("\n처리된 명령어:")
            for i, cmd in enumerate(result['processed_commands'], 1):
                original = cmd['original_command']['original_text']
                recommendations = len(cmd['recommendations'])
                print(f"  {i}. '{original}' → {recommendations}개 추천")

if __name__ == "__main__":
    test_document_parser()


