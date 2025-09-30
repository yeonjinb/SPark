#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
자연어 처리 및 시간 정보 추출 시스템
"""

import re
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

class NaturalLanguageProcessor:
    def __init__(self):
        """자연어 처리기 초기화"""
        # 시간 관련 패턴 정의
        self.time_patterns = {
            # 직접적인 시간 표현
            'hours': [
                r'(\d+)시간',
                r'(\d+)시간동안',
                r'(\d+)시간 동안',
                r'(\d+)시간만큼',
                r'(\d+)시간 정도',
                r'(\d+)시간짜리'
            ],
            'minutes': [
                r'(\d+)분',
                r'(\d+)분동안',
                r'(\d+)분 동안',
                r'(\d+)분만큼'
            ],
            'days': [
                r'(\d+)일',
                r'(\d+)일동안',
                r'(\d+)일 동안',
                r'(\d+)일만큼'
            ],
            # 상대적 시간 표현
            'relative': [
                r'하루',
                r'이틀',
                r'삼일',
                r'한 시간',
                r'두 시간',
                r'세 시간',
                r'네 시간',
                r'다섯 시간',
                r'반나절',
                r'하루종일'
            ],
            # 시간대 표현
            'time_range': [
                r'오전 (\d+)시부터',
                r'오후 (\d+)시까지',
                r'(\d+)시부터 (\d+)시까지',
                r'(\d+):(\d+)부터 (\d+):(\d+)까지'
            ]
        }
        
        # 명령어 타입 패턴
        self.command_patterns = {
            'find_parking': [
                '찾아', '찾아줘', '찾기', '검색', '어디', '위치', 
                '추천', '알려줘', '보여줘', '제안', '선택'
            ],
            'reserve_parking': [
                '예약', '예약해', '예약해줘', '예약하기', '예약하고',
                '빌리', '빌려줘', '사용', '이용', '계약'
            ],
            'parking_info': [
                '정보', '알려줘', '어떤', '어디에', '얼마', '비용',
                '가격', '요금', '현재', '상황', '상태'
            ],
            'cancel_reservation': [
                '취소', '취소해', '취소해줘', '해제', '해제해줘'
            ]
        }
        
        # 위치 관련 키워드
        self.location_keywords = [
            '강남', '강북', '서초', '송파', '마포', '홍대', '명동', '시청',
            '잠실', '건대', '신촌', '이대', '여의도', '종로', '을지로',
            '압구정', '청담', '신사', '논현', '역삼', '삼성', '봉은사'
        ]
        
        # 차량 타입 키워드
        self.vehicle_keywords = {
            '승용차': ['승용차', '소형차', '경차', '세단'],
            'SUV': ['SUV', '지프', '크로스오버'],
            '승합차': ['승합차', '밴', '미니밴'],
            '화물차': ['화물차', '트럭', '픽업']
        }
    
    def extract_time_info(self, text: str) -> Dict:
        """텍스트에서 시간 정보 추출"""
        result = {
            'hours': None,
            'minutes': None,
            'days': None,
            'start_time': None,
            'end_time': None,
            'duration_type': 'hours',  # 기본값
            'raw_text': text
        }
        
        text_lower = text.lower()
        
        # 시간 추출 (시간 단위)
        for pattern in self.time_patterns['hours']:
            match = re.search(pattern, text_lower)
            if match:
                hours = int(match.group(1))
                if 1 <= hours <= 24:
                    result['hours'] = hours
                    result['duration_type'] = 'hours'
                    break
        
        # 분 추출
        for pattern in self.time_patterns['minutes']:
            match = re.search(pattern, text_lower)
            if match:
                minutes = int(match.group(1))
                if 1 <= minutes <= 59:
                    result['minutes'] = minutes
                    result['duration_type'] = 'minutes'
                    break
        
        # 일 추출
        for pattern in self.time_patterns['days']:
            match = re.search(pattern, text_lower)
            if match:
                days = int(match.group(1))
                if 1 <= days <= 7:
                    result['days'] = days
                    result['duration_type'] = 'days'
                    break
        
        # 상대적 시간 표현 처리
        relative_mappings = {
            '한 시간': 1, '두 시간': 2, '세 시간': 3, '네 시간': 4, '다섯 시간': 5,
            '하루': 24, '이틀': 48, '삼일': 72, '반나절': 12, '하루종일': 24
        }
        
        for korean, hours in relative_mappings.items():
            if korean in text_lower:
                result['hours'] = hours
                result['duration_type'] = 'hours'
                break
        
        # 시간대 추출
        time_range_patterns = [
            r'(\d+)시부터 (\d+)시까지',
            r'오전 (\d+)시부터 오후 (\d+)시까지',
            r'(\d+):(\d+)부터 (\d+):(\d+)까지'
        ]
        
        for pattern in time_range_patterns:
            match = re.search(pattern, text_lower)
            if match:
                groups = match.groups()
                if len(groups) == 2:  # 3시부터 5시까지
                    start_hour, end_hour = int(groups[0]), int(groups[1])
                    result['start_time'] = f"{start_hour:02d}:00"
                    result['end_time'] = f"{end_hour:02d}:00"
                    result['hours'] = end_hour - start_hour
                elif len(groups) == 4:  # 09:30부터 17:30까지
                    start_hour, start_min, end_hour, end_min = map(int, groups)
                    result['start_time'] = f"{start_hour:02d}:{start_min:02d}"
                    result['end_time'] = f"{end_hour:02d}:{end_min:02d}"
                    start_time = datetime.strptime(result['start_time'], '%H:%M')
                    end_time = datetime.strptime(result['end_time'], '%H:%M')
                    duration = end_time - start_time
                    result['hours'] = duration.total_seconds() / 3600
        
        return result
    
    def identify_command_type(self, text: str) -> str:
        """명령어 타입 식별"""
        text_lower = text.lower()
        
        # 주차장 관련 키워드 확인
        parking_keywords = ['주차장', '주차', '주차공간', '주차공간', '파킹']
        if not any(keyword in text_lower for keyword in parking_keywords):
            return 'unknown'
        
        # 명령어 타입 판별
        for command_type, keywords in self.command_patterns.items():
            if any(keyword in text_lower for keyword in keywords):
                return command_type
        
        # 기본값은 찾기로 설정
        return 'find_parking'
    
    def extract_location_info(self, text: str) -> List[str]:
        """위치 정보 추출"""
        found_locations = []
        text_lower = text.lower()
        
        for location in self.location_keywords:
            if location in text_lower:
                found_locations.append(location)
        
        return found_locations
    
    def extract_vehicle_type(self, text: str) -> List[str]:
        """차량 타입 추출"""
        found_vehicles = []
        text_lower = text.lower()
        
        for vehicle_type, keywords in self.vehicle_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    found_vehicles.append(vehicle_type)
                    break
        
        return found_vehicles
    
    def extract_price_info(self, text: str) -> Dict:
        """가격 정보 추출"""
        result = {
            'max_price': None,
            'price_range': None,
            'budget': None
        }
        
        # 가격 패턴
        price_patterns = [
            r'(\d+)원 이하',
            r'(\d+)원까지',
            r'(\d+)원 미만',
            r'(\d+)원에서 (\d+)원',
            r'(\d+)원대'
        ]
        
        for pattern in price_patterns:
            match = re.search(pattern, text)
            if match:
                groups = match.groups()
                if len(groups) == 1:
                    result['max_price'] = int(groups[0])
                elif len(groups) == 2:
                    result['price_range'] = (int(groups[0]), int(groups[1]))
        
        return result
    
    def parse_complete_command(self, text: str) -> Dict:
        """완전한 명령어 파싱"""
        result = {
            'original_text': text,
            'time_info': self.extract_time_info(text),
            'command_type': self.identify_command_type(text),
            'locations': self.extract_location_info(text),
            'vehicle_types': self.extract_vehicle_type(text),
            'price_info': self.extract_price_info(text),
            'confidence': 0.0
        }
        
        # 신뢰도 계산
        confidence_factors = []
        
        if result['time_info']['hours'] or result['time_info']['minutes'] or result['time_info']['days']:
            confidence_factors.append(0.3)
        
        if result['command_type'] != 'unknown':
            confidence_factors.append(0.4)
        
        if result['locations']:
            confidence_factors.append(0.2)
        
        if result['vehicle_types']:
            confidence_factors.append(0.1)
        
        result['confidence'] = sum(confidence_factors)
        
        return result
    
    def process_document(self, document: str) -> List[Dict]:
        """문서에서 주차장 관련 명령어들을 추출하고 처리"""
        # 문장 단위로 분리 (간단한 분리)
        sentences = re.split(r'[.!?]\s*', document)
        
        results = []
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and any(keyword in sentence.lower() for keyword in ['주차장', '주차', '파킹']):
                parsed = self.parse_complete_command(sentence)
                if parsed['confidence'] > 0.3:  # 신뢰도 임계값
                    results.append(parsed)
        
        return results

# 테스트 함수
def test_nlp_processor():
    """NLP 처리기 테스트"""
    nlp = NaturalLanguageProcessor()
    
    test_commands = [
        "2시간동안 주차할 주차장 찾아줘",
        "3시간 주차장 예약해줘",
        "강남역에서 4시간 주차할 곳 찾아줘",
        "명동 주차장 정보 알려줘",
        "SUV 1시간 주차할 곳 추천해줘",
        "5000원 이하로 2시간 주차장 찾아줘"
    ]
    
    print("🧠 자연어 처리 테스트")
    print("=" * 50)
    
    for i, command in enumerate(test_commands, 1):
        print(f"\n{i}. 테스트 명령어: '{command}'")
        result = nlp.parse_complete_command(command)
        
        print(f"   명령어 타입: {result['command_type']}")
        print(f"   시간 정보: {result['time_info']}")
        print(f"   위치: {result['locations']}")
        print(f"   차량 타입: {result['vehicle_types']}")
        print(f"   가격 정보: {result['price_info']}")
        print(f"   신뢰도: {result['confidence']:.2f}")

if __name__ == "__main__":
    test_nlp_processor()









