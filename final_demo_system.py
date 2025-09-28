#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
최종 통합 데모 시스템
음성 인식 → 자연어 처리 → 고급 스코어링 → 지도 연동 → 결과 출력
"""

from integrated_parking_system import IntegratedParkingSystem
from map_api_integration import MapAPIIntegration
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

class FinalDemoSystem:
    def __init__(self):
        """최종 데모 시스템 초기화"""
        self.parking_system = IntegratedParkingSystem()
        self.map_api = MapAPIIntegration()
        
        # 사용자 설정
        self.user_settings = {
            'current_location': {
                'latitude': 37.5665,
                'longitude': 126.9780,
                'address': '서울특별시 중구 세종대로 110'
            },
            'vehicle_info': {
                'height': 1.8,
                'type': '승용차',
                'length': 4.5,
                'width': 1.8
            },
            'preferences': {
                'price_weight': 0.4,
                'time_weight': 0.4,
                'convenience_weight': 0.2,
                'max_walking_distance': 0.5  # km
            }
        }
        
        # 시스템 정보
        self.system_info = {
            'version': '1.0.0',
            'features': [
                '음성 인식',
                '자연어 처리',
                '고급 스코어링',
                '지도 API 연동',
                '실시간 추천'
            ],
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def process_complete_request(self, voice_command: str, 
                               user_location: Dict = None,
                               user_preferences: Dict = None) -> Dict:
        """완전한 요청 처리"""
        
        # 1. 사용자 설정 업데이트
        if user_location:
            self.user_settings['current_location'].update(user_location)
        
        if user_preferences:
            self.user_settings['preferences'].update(user_preferences)
        
        # 2. 사용자 프로필 업데이트
        self.parking_system.update_user_profile({
            'vehicle_height': self.user_settings['vehicle_info']['height'],
            'vehicle_type': self.user_settings['vehicle_info']['type'],
            'preferences': self.user_settings['preferences']
        })
        
        # 3. 음성 명령어 처리
        result = self.parking_system.process_voice_command(voice_command)
        
        # 4. 지도 API 연동으로 실제 거리/시간 계산
        enhanced_recommendations = []
        for lot in result['recommendations']:
            # 실제 거리/시간 계산
            route_info = self.map_api.calculate_distance_and_time(
                self.user_settings['current_location'],
                lot['location']
            )
            
            # 기존 정보 업데이트
            lot['actual_distance_km'] = route_info['distance_km']
            lot['actual_travel_time_minutes'] = route_info['travel_time_minutes']
            lot['map_url'] = self.map_api.generate_map_url(
                self.user_settings['current_location'],
                lot['location']
            )
            lot['route_guidance'] = self.map_api.get_route_guidance(
                self.user_settings['current_location'],
                lot['location']
            )
            
            enhanced_recommendations.append(lot)
        
        result['recommendations'] = enhanced_recommendations
        
        # 5. 최종 결과 구성
        final_result = {
            'system_info': self.system_info,
            'user_settings': self.user_settings,
            'request_info': {
                'voice_command': voice_command,
                'processed_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'processing_time_ms': 150  # 실제로는 측정
            },
            'parking_results': result,
            'summary': self._generate_summary(result)
        }
        
        return final_result
    
    def _generate_summary(self, result: Dict) -> Dict:
        """결과 요약 생성"""
        recommendations = result['recommendations']
        
        if not recommendations:
            return {
                'status': 'no_results',
                'message': '조건에 맞는 주차장을 찾을 수 없습니다.'
            }
        
        best_lot = recommendations[0]
        
        summary = {
            'status': 'success',
            'total_found': result['total_found'],
            'best_recommendation': {
                'name': best_lot['name'],
                'cost': best_lot['total_cost'],
                'distance': best_lot['actual_distance_km'],
                'travel_time': best_lot['actual_travel_time_minutes'],
                'score': best_lot['final_score'],
                'difficulty': best_lot['difficulty_level']
            },
            'price_range': {
                'min': min(lot['total_cost'] for lot in recommendations),
                'max': max(lot['total_cost'] for lot in recommendations),
                'avg': sum(lot['total_cost'] for lot in recommendations) / len(recommendations)
            },
            'time_range': {
                'min': min(lot['actual_travel_time_minutes'] for lot in recommendations),
                'max': max(lot['actual_travel_time_minutes'] for lot in recommendations),
                'avg': sum(lot['actual_travel_time_minutes'] for lot in recommendations) / len(recommendations)
            }
        }
        
        return summary
    
    def generate_detailed_report(self, result: Dict) -> str:
        """상세 리포트 생성"""
        report = []
        
        # 헤더
        report.append("🎯 SPark 주차장 추천 시스템 - 상세 리포트")
        report.append("=" * 60)
        report.append(f"📅 생성 시간: {result['request_info']['processed_at']}")
        report.append(f"🎤 음성 명령: \"{result['request_info']['voice_command']}\"")
        
        # 시스템 정보
        report.append(f"\n🔧 시스템 정보:")
        report.append(f"   버전: {result['system_info']['version']}")
        report.append(f"   기능: {', '.join(result['system_info']['features'])}")
        
        # 사용자 설정
        user_settings = result['user_settings']
        report.append(f"\n👤 사용자 설정:")
        report.append(f"   현재 위치: {user_settings['current_location']['address']}")
        report.append(f"   차량 정보: {user_settings['vehicle_info']['type']} ({user_settings['vehicle_info']['height']}m)")
        report.append(f"   가중치: 가격({user_settings['preferences']['price_weight']:.1f}) 시간({user_settings['preferences']['time_weight']:.1f}) 편의성({user_settings['preferences']['convenience_weight']:.1f})")
        
        # 요약 정보
        summary = result['summary']
        if summary['status'] == 'success':
            report.append(f"\n📊 추천 요약:")
            report.append(f"   총 찾은 주차장: {summary['total_found']}개")
            report.append(f"   최고 추천: {summary['best_recommendation']['name']}")
            report.append(f"   비용 범위: {summary['price_range']['min']:,}원 ~ {summary['price_range']['max']:,}원")
            report.append(f"   거리 범위: {summary['time_range']['min']:.1f}분 ~ {summary['time_range']['max']:.1f}분")
        
        # 상세 추천 결과
        report.append(f"\n🏆 상세 추천 결과:")
        report.append("-" * 40)
        
        for i, lot in enumerate(result['parking_results']['recommendations'], 1):
            report.append(f"\n{i}. {lot['name']}")
            report.append(f"   💰 총 비용: {lot['total_cost']:,}원")
            report.append(f"   📍 실제 거리: {lot['actual_distance_km']:.2f}km")
            report.append(f"   ⏱️ 실제 소요시간: {lot['actual_travel_time_minutes']:.1f}분")
            report.append(f"   🚗 주차 난이도: {lot['difficulty_level']}")
            report.append(f"   ⭐ 종합 점수: {lot['final_score']:.2f}")
            report.append(f"   📍 주소: {lot['location']['address']}")
            report.append(f"   🅿️ 남은 자리: {lot['capacity']['available_spaces']}개")
            
            # 점수 구성
            breakdown = lot['score_info']['breakdown']
            report.append(f"   📊 점수 구성:")
            report.append(f"      - 가격 점수: {breakdown['price_component']:.2f}")
            report.append(f"      - 시간 점수: {breakdown['time_component']:.2f}")
            report.append(f"      - 편의성 점수: {breakdown['convenience_component']:.2f}")
            
            # 편의시설
            amenities = []
            if lot['amenities']['elevator']:
                amenities.append("엘리베이터")
            if lot['amenities']['restroom']:
                amenities.append("화장실")
            if lot['amenities'].get('convenience_store'):
                amenities.append("편의점")
            if lot['amenities'].get('atm'):
                amenities.append("ATM")
            
            if amenities:
                report.append(f"   🏪 편의시설: {', '.join(amenities)}")
            
            # 지도 링크
            report.append(f"   🗺️ 지도 보기: {lot['map_url']}")
        
        # 처리 정보
        report.append(f"\n🔍 처리 정보:")
        processing_info = result['parking_results']['processing_info']
        report.append(f"   스코어링 방법: {processing_info['scoring_method']}")
        report.append(f"   적용된 필터: {', '.join(processing_info['filters_applied'])}")
        
        return "\n".join(report)
    
    def save_results_to_file(self, result: Dict, filename: str = None):
        """결과를 파일로 저장"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"parking_recommendation_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"📁 결과가 {filename}에 저장되었습니다.")
        return filename

# 데모 테스트 함수
def run_complete_demo():
    """완전한 데모 실행"""
    demo = FinalDemoSystem()
    
    print("🚀 SPark 주차장 추천 시스템 - 완전한 데모")
    print("=" * 60)
    
    # 테스트 시나리오들
    test_scenarios = [
        {
            'command': "2시간 주차장 찾아줘",
            'description': "기본 주차장 검색"
        },
        {
            'command': "강남역에서 3시간 주차할 곳 찾아줘",
            'description': "지역 지정 검색"
        },
        {
            'command': "5000원 이하로 4시간 주차할 곳 찾아줘",
            'description': "가격 제한 검색"
        },
        {
            'command': "SUV 1시간 주차장 예약해줘",
            'description': "차량 타입 지정"
        }
    ]
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n{i}. {scenario['description']}")
        print(f"   명령어: \"{scenario['command']}\"")
        print("-" * 50)
        
        # 완전한 요청 처리
        result = demo.process_complete_request(scenario['command'])
        
        # 요약 정보 출력
        summary = result['summary']
        if summary['status'] == 'success':
            best = summary['best_recommendation']
            print(f"   ✅ {summary['total_found']}개 주차장 발견")
            print(f"   🏆 최고 추천: {best['name']}")
            print(f"   💰 비용: {best['cost']:,}원")
            print(f"   📍 거리: {best['distance']:.1f}km ({best['travel_time']:.1f}분)")
            print(f"   ⭐ 점수: {best['score']:.2f}")
        else:
            print(f"   ❌ {summary['message']}")
    
    # 상세 리포트 생성 및 저장
    print(f"\n📊 상세 리포트 생성 중...")
    detailed_result = demo.process_complete_request("2시간 주차장 찾아줘")
    report = demo.generate_detailed_report(detailed_result)
    
    # 리포트를 파일로 저장
    report_filename = f"parking_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"📁 상세 리포트가 {report_filename}에 저장되었습니다.")
    
    # JSON 결과도 저장
    json_filename = demo.save_results_to_file(detailed_result)
    
    print(f"\n🎉 데모 완료!")
    print(f"   - 상세 리포트: {report_filename}")
    print(f"   - JSON 결과: {json_filename}")
    print(f"   - 시스템 버전: {demo.system_info['version']}")

if __name__ == "__main__":
    run_complete_demo()
