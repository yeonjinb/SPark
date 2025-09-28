#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
통합 주차장 시스템 - 고급 스코어링 + 기존 시스템 통합
"""

from natural_language_processor import NaturalLanguageProcessor
from advanced_scoring_system import AdvancedScoringSystem
from typing import Dict, List, Any, Optional
import json

class IntegratedParkingSystem:
    def __init__(self):
        """통합 주차장 시스템 초기화"""
        self.nlp = NaturalLanguageProcessor()
        self.scoring = AdvancedScoringSystem()
        
        # 기본 사용자 프로필
        self.user_profile = {
            'vehicle_height': 1.8,  # 기본 차량 높이 (미터)
            'vehicle_type': '승용차',  # 기본 차량 타입
            'driving_experience': 'intermediate',  # 초급, 중급, 고급
            'preferences': {
                'price_weight': 0.4,
                'time_weight': 0.4,
                'convenience_weight': 0.2
            }
        }
    
    def update_user_profile(self, profile_updates: Dict):
        """사용자 프로필 업데이트"""
        if 'vehicle_height' in profile_updates:
            self.user_profile['vehicle_height'] = profile_updates['vehicle_height']
        if 'vehicle_type' in profile_updates:
            self.user_profile['vehicle_type'] = profile_updates['vehicle_type']
        if 'driving_experience' in profile_updates:
            self.user_profile['driving_experience'] = profile_updates['driving_experience']
        if 'preferences' in profile_updates:
            self.user_profile['preferences'].update(profile_updates['preferences'])
    
    def process_voice_command(self, voice_text: str) -> Dict:
        """음성 명령어 처리 - 통합 시스템"""
        
        # 1. 자연어 처리
        parsed_command = self.nlp.parse_complete_command(voice_text)
        
        # 2. 사용자 프로필 기반 차량 정보 추출
        vehicle_height = self.user_profile['vehicle_height']
        vehicle_type = self.user_profile['vehicle_type']
        
        # 음성 명령에서 차량 정보 추출 (있다면)
        if parsed_command['vehicle_types']:
            vehicle_type = parsed_command['vehicle_types'][0]
        
        # 3. 시간 정보 추출
        hours = parsed_command['time_info']['hours'] or 2  # 기본값 2시간
        
        # 4. 위치 정보 추출
        locations = parsed_command['locations']
        
        # 5. 가격 제한 추출
        price_limit = parsed_command['price_info']['max_price']
        
        # 6. 사용자 선호도 기반 가중치 설정
        preferences = self.user_profile['preferences'].copy()
        
        # 가격 제한이 있으면 가격 민감도 증가
        if price_limit:
            preferences['price_weight'] = 0.6
            preferences['time_weight'] = 0.3
            preferences['convenience_weight'] = 0.1
        
        # 7. 고급 스코어링으로 주차장 추천
        recommendations = self.scoring.get_top_recommendations(
            hours=hours,
            top_n=5,
            vehicle_height=vehicle_height,
            vehicle_type=vehicle_type,
            user_preferences=preferences
        )
        
        # 8. 가격 제한 필터링 (추가)
        if price_limit:
            recommendations = [lot for lot in recommendations if lot['total_cost'] <= price_limit]
        
        # 9. 경로 안내 정보 생성
        route_guidance = []
        for lot in recommendations[:3]:  # 상위 3개만
            route_info = self.scoring.generate_route_guidance(lot)
            route_guidance.append({
                'lot_id': lot['id'],
                'lot_name': lot['name'],
                'route': route_info
            })
        
        # 10. 결과 통합
        result = {
            'parsed_command': parsed_command,
            'user_profile': self.user_profile,
            'total_found': len(recommendations),
            'recommendations': recommendations,
            'route_guidance': route_guidance,
            'processing_info': {
                'scoring_method': 'advanced_weighted_scoring',
                'weights_used': preferences,
                'filters_applied': [
                    f'차량 높이: {vehicle_height}m 이하',
                    f'차량 타입: {vehicle_type}',
                    f'운영 시간: 현재 운영 중',
                    f'가용성: 빈 자리 있음'
                ]
            }
        }
        
        return result
    
    def get_recommendation_explanation(self, lot: Dict) -> str:
        """추천 이유 설명 생성"""
        score_info = lot['score_info']
        breakdown = score_info['breakdown']
        
        explanations = []
        
        # 가격 관련 설명
        if breakdown['price_component'] > 2.0:
            explanations.append(f"💰 저렴한 주차비 ({lot['total_cost']:,}원)")
        
        # 시간 관련 설명
        if breakdown['time_component'] > 20.0:
            explanations.append(f"⏱️ 빠른 접근성 ({lot['travel_time']}분)")
        
        # 편의성 관련 설명
        if breakdown['convenience_component'] > 0.15:
            explanations.append(f"🚗 쉬운 주차 ({lot['difficulty_level']})")
        
        # 편의시설 설명
        if lot['amenities']['elevator']:
            explanations.append("🛗 엘리베이터 이용 가능")
        if lot['amenities']['restroom']:
            explanations.append("🚻 화장실 이용 가능")
        if lot['amenities'].get('convenience_store'):
            explanations.append("🏪 편의점 이용 가능")
        
        return " | ".join(explanations) if explanations else "기본 추천 주차장"
    
    def generate_user_report(self, result: Dict) -> str:
        """사용자 리포트 생성"""
        report = []
        
        # 헤더
        report.append("🎯 주차장 추천 리포트")
        report.append("=" * 50)
        
        # 명령어 정보
        parsed = result['parsed_command']
        report.append(f"📝 처리된 명령어: \"{parsed['original_text']}\"")
        report.append(f"⏰ 주차 시간: {parsed['time_info']['hours']}시간")
        report.append(f"🚗 차량 정보: {result['user_profile']['vehicle_type']} ({result['user_profile']['vehicle_height']}m)")
        
        # 가중치 정보
        weights = result['processing_info']['weights_used']
        report.append(f"⚖️ 가중치 설정: 가격({weights['price_weight']:.1f}) 시간({weights['time_weight']:.1f}) 편의성({weights['convenience_weight']:.1f})")
        
        # 추천 결과
        report.append(f"\n🏆 추천 주차장 ({result['total_found']}개)")
        report.append("-" * 30)
        
        for i, lot in enumerate(result['recommendations'], 1):
            report.append(f"\n{i}. {lot['name']}")
            report.append(f"   💰 총 비용: {lot['total_cost']:,}원")
            report.append(f"   ⏱️ 도착 시간: {lot['travel_time']}분")
            report.append(f"   🚗 주차 난이도: {lot['difficulty_level']}")
            report.append(f"   ⭐ 종합 점수: {lot['final_score']:.2f}")
            report.append(f"   📍 주소: {lot['location']['address']}")
            
            # 추천 이유
            explanation = self.get_recommendation_explanation(lot)
            report.append(f"   💡 추천 이유: {explanation}")
            
            # 경로 안내
            route_info = next((r for r in result['route_guidance'] if r['lot_id'] == lot['id']), None)
            if route_info:
                report.append(f"   🗺️ 경로: {route_info['route']['route_info']['route_summary']}")
        
        return "\n".join(report)

# 테스트 함수
def test_integrated_system():
    """통합 시스템 테스트"""
    system = IntegratedParkingSystem()
    
    # 사용자 프로필 설정
    system.update_user_profile({
        'vehicle_height': 1.9,
        'vehicle_type': 'SUV',
        'preferences': {
            'price_weight': 0.3,
            'time_weight': 0.5,
            'convenience_weight': 0.2
        }
    })
    
    test_commands = [
        "2시간 주차장 찾아줘",
        "강남역에서 3시간 주차할 곳 찾아줘",
        "SUV 1시간 주차장 예약해줘",
        "5000원 이하로 4시간 주차할 곳 찾아줘"
    ]
    
    print("🎤 통합 주차장 시스템 테스트")
    print("=" * 60)
    
    for i, command in enumerate(test_commands, 1):
        print(f"\n{i}. 테스트 명령어: \"{command}\"")
        print("-" * 50)
        
        result = system.process_voice_command(command)
        
        # 간단한 결과 출력
        print(f"명령어 타입: {result['parsed_command']['command_type']}")
        print(f"시간: {result['parsed_command']['time_info']['hours']}시간")
        print(f"찾은 주차장: {result['total_found']}개")
        
        if result['recommendations']:
            print("추천 주차장:")
            for j, lot in enumerate(result['recommendations'][:2], 1):
                print(f"  {j}. {lot['name']} - {lot['total_cost']:,}원 ({lot['travel_time']}분, 점수: {lot['final_score']:.2f})")
    
    # 상세 리포트 생성
    print(f"\n📊 상세 리포트 예시:")
    print("=" * 60)
    detailed_result = system.process_voice_command("2시간 주차장 찾아줘")
    report = system.generate_user_report(detailed_result)
    print(report)

if __name__ == "__main__":
    test_integrated_system()


