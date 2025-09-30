#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
실제 주차장 데이터를 사용한 추천 시스템
이미지에서 추출한 실제 주차장 데이터 통합
"""

from advanced_scoring_system import AdvancedScoringSystem
from natural_language_processor import NaturalLanguageProcessor
from map_api_integration import MapAPIIntegration
from typing import Dict, List, Any, Optional
import json

class RealParkingDataSystem(AdvancedScoringSystem):
    def __init__(self):
        """실제 주차장 데이터로 시스템 초기화"""
        super().__init__()
        
        # 실제 주차장 데이터 (이미지에서 추출)
        self.parking_lots = [
            {
                "id": 1,
                "name": "아이파킹 동도센트리움캠퍼스파크 주차장",
                "location": {
                    "latitude": 37.5507,  # 능동 지역 좌표 (추정)
                    "longitude": 127.0745,
                    "address": "동도센트리움캠퍼스파크"
                },
                "pricing": {
                    "hourly_rate": 4500,
                    "daily_rate": None,
                    "night_rate": None,
                    # 상세 요금 정보
                    "weekday_base": 1500,
                    "weekday_additional": 250,
                    "weekday_cap": None,
                    "weekend_base": 1500,
                    "holiday_base": 1500,
                    "holiday_additional": 250
                },
                "capacity": {
                    "total_spaces": 132,
                    "available_spaces": 85  # 예상 가용 공간
                },
                "facilities": ["24시간 운영", "지붕 보호"],
                "operating_hours": {
                    "weekday": "00:00-23:59",
                    "weekend": "00:00-23:59"
                },
                "restrictions": {
                    "max_duration": 24,
                    "vehicle_types": ["승용차"],
                    "height_limit": 1.55
                },
                "amenities": {
                    "elevator": False,
                    "restroom": False,
                    "atm": False,
                    "convenience_store": False,
                    "ev_charging": False,
                    "roof": True,
                    "cctv": False,
                    "lighting": False
                },
                "rating": 3.8,
                "reviews_count": 42,
                # 운전 난이도 정보 (추정)
                "driving_difficulty": {
                    "parking_type": "자주식",
                    "access_road_width": 4.0,  # 추정값
                    "turning_radius": 8.0,     # 추정값
                    "slope_angle": 3,          # 추정값
                    "obstacles": ["없음"],
                    "lighting": "보통",
                    "security": "양호"
                }
            },
            {
                "id": 2,
                "name": "능동공영 주차장",
                "location": {
                    "latitude": 37.5507,
                    "longitude": 127.0745,
                    "address": "능동 205"
                },
                "pricing": {
                    "hourly_rate": 3600,
                    "daily_rate": 50000,
                    "night_rate": None,
                    # 상세 요금 정보
                    "weekday_base": 1200,
                    "weekday_additional": 200,
                    "weekday_cap": 50000,
                    "weekend_base": 1200,
                    "holiday_base": 1200,
                    "holiday_additional": 200
                },
                "capacity": {
                    "total_spaces": 77,
                    "available_spaces": 52  # 예상 가용 공간
                },
                "facilities": ["24시간 운영", "전기차 충전", "지붕 보호"],
                "operating_hours": {
                    "weekday": "00:00-23:59",
                    "weekend": "00:00-23:59"
                },
                "restrictions": {
                    "max_duration": 24,
                    "vehicle_types": ["승용차", "SUV"],
                    "height_limit": 2.1
                },
                "amenities": {
                    "elevator": False,
                    "restroom": False,
                    "atm": False,
                    "convenience_store": False,
                    "ev_charging": True,
                    "roof": True,
                    "cctv": False,
                    "lighting": False
                },
                "rating": 4.1,
                "reviews_count": 28,
                # 운전 난이도 정보 (추정)
                "driving_difficulty": {
                    "parking_type": "자주식",
                    "access_road_width": 4.5,  # 추정값
                    "turning_radius": 8.5,     # 추정값
                    "slope_angle": 2,          # 추정값
                    "obstacles": ["없음"],
                    "lighting": "양호",
                    "security": "우수"
                }
            }
        ]
        
        # 추가 주차장 데이터 (기존 샘플 데이터와 함께)
        self.parking_lots.extend([
            {
                "id": 3,
                "name": "서울시청 주차장",
                "location": {
                    "latitude": 37.5665,
                    "longitude": 126.9780,
                    "address": "서울특별시 중구 세종대로 110"
                },
                "pricing": {
                    "hourly_rate": 1000,
                    "daily_rate": 15000,
                    "night_rate": 500,
                    "weekday_base": 1000,
                    "weekday_additional": 0,
                    "weekday_cap": 15000,
                    "weekend_base": 1000,
                    "holiday_base": 1000,
                    "holiday_additional": 0
                },
                "capacity": {
                    "total_spaces": 300,
                    "available_spaces": 15
                },
                "facilities": ["24시간 운영", "장애인 주차공간", "전기차 충전시설"],
                "operating_hours": {
                    "weekday": "00:00-23:59",
                    "weekend": "00:00-23:59"
                },
                "restrictions": {
                    "max_duration": 24,
                    "vehicle_types": ["승용차", "SUV", "승합차"],
                    "height_limit": 2.1
                },
                "amenities": {
                    "elevator": True,
                    "restroom": True,
                    "atm": True,
                    "convenience_store": False,
                    "ev_charging": True,
                    "roof": True,
                    "cctv": True,
                    "lighting": True
                },
                "rating": 4.2,
                "reviews_count": 156,
                "driving_difficulty": {
                    "parking_type": "자주식",
                    "access_road_width": 4.5,
                    "turning_radius": 8.0,
                    "slope_angle": 5,
                    "obstacles": ["없음"],
                    "lighting": "우수",
                    "security": "우수"
                }
            },
            {
                "id": 4,
                "name": "명동 중앙 주차장",
                "location": {
                    "latitude": 37.5636,
                    "longitude": 126.9826,
                    "address": "서울특별시 중구 명동길 26"
                },
                "pricing": {
                    "hourly_rate": 1500,
                    "daily_rate": 20000,
                    "night_rate": 800,
                    "weekday_base": 1500,
                    "weekday_additional": 0,
                    "weekday_cap": 20000,
                    "weekend_base": 1500,
                    "holiday_base": 1500,
                    "holiday_additional": 0
                },
                "capacity": {
                    "total_spaces": 200,
                    "available_spaces": 8
                },
                "facilities": ["24시간 운영", "장애인 주차공간", "발렛파킹"],
                "operating_hours": {
                    "weekday": "06:00-23:00",
                    "weekend": "08:00-22:00"
                },
                "restrictions": {
                    "max_duration": 12,
                    "vehicle_types": ["승용차", "SUV"],
                    "height_limit": 2.0
                },
                "amenities": {
                    "elevator": True,
                    "restroom": True,
                    "atm": True,
                    "convenience_store": False,
                    "ev_charging": False,
                    "roof": True,
                    "cctv": True,
                    "lighting": True
                },
                "rating": 4.5,
                "reviews_count": 89,
                "driving_difficulty": {
                    "parking_type": "발렛파킹",
                    "access_road_width": 3.0,
                    "turning_radius": 6.0,
                    "slope_angle": 0,
                    "obstacles": ["없음"],
                    "lighting": "양호",
                    "security": "우수"
                }
            }
        ])
        
        # 현재 위치 설정 (능동 지역으로 변경)
        self.current_location = {
            "latitude": 37.5507,
            "longitude": 127.0745,
            "address": "서울특별시 강동구 능동"
        }
        
        # NLP 및 지도 API 초기화
        self.nlp = NaturalLanguageProcessor()
        self.map_api = MapAPIIntegration()
    
    def calculate_advanced_pricing(self, lot: Dict, hours: int) -> float:
        """상세 요금 계산 (실제 데이터 기반)"""
        pricing = lot['pricing']
        
        # 일일 최대 요금이 있고, 시간이 충분히 길면 일일 요금 사용
        if hours >= 8 and pricing.get('daily_rate'):
            daily_cost = pricing['daily_rate']
            hourly_cost = pricing['hourly_rate'] * hours
            return min(daily_cost, hourly_cost)
        
        # 주말/공휴일 구분 (간단히 시간으로 구분)
        import datetime
        now = datetime.datetime.now()
        
        # 기본 시간당 요금
        base_hourly_rate = pricing['hourly_rate']
        
        # 상세 요금 계산 (추가 요금 포함)
        if hours <= 1:
            # 첫 시간은 기본 요금
            total_cost = base_hourly_rate
        else:
            # 첫 시간 + 추가 시간 요금
            base_cost = pricing.get('weekday_base', base_hourly_rate)
            additional_cost = (hours - 1) * pricing.get('weekday_additional', 0)
            total_cost = base_cost + additional_cost
        
        return total_cost
    
    def get_ev_charging_lots(self) -> List[Dict]:
        """전기차 충전 가능한 주차장 목록"""
        return [lot for lot in self.parking_lots if lot['amenities']['ev_charging']]
    
    def get_roofed_lots(self) -> List[Dict]:
        """지붕이 있는 주차장 목록"""
        return [lot for lot in self.parking_lots if lot['amenities']['roof']]
    
    def get_lots_by_price_range(self, min_price: int, max_price: int, hours: int) -> List[Dict]:
        """가격대별 주차장 필터링"""
        filtered_lots = []
        
        for lot in self.parking_lots:
            total_cost = self.calculate_advanced_pricing(lot, hours)
            if min_price <= total_cost <= max_price:
                filtered_lots.append(lot)
        
        return filtered_lots
    
    def get_lots_by_vehicle_height(self, vehicle_height: float) -> List[Dict]:
        """차량 높이별 주차장 필터링"""
        return [lot for lot in self.parking_lots if lot['restrictions']['height_limit'] >= vehicle_height]
    
    def process_real_data_request(self, voice_command: str) -> Dict:
        """실제 데이터 기반 요청 처리"""
        
        # 자연어 처리
        parsed_command = self.nlp.parse_complete_command(voice_command)
        
        # 시간 정보
        hours = parsed_command['time_info']['hours'] or 2
        
        # 가격 제한
        price_limit = parsed_command['price_info']['max_price']
        
        # 위치 정보
        locations = parsed_command['locations']
        
        # 차량 타입 (기본값 설정)
        vehicle_height = 1.8  # 기본 승용차 높이
        vehicle_type = '승용차'
        
        if 'SUV' in parsed_command['vehicle_types'] or 'suv' in voice_command.lower():
            vehicle_height = 2.0
            vehicle_type = 'SUV'
        
        # 필터링된 후보군
        candidates = self.filter_candidates(vehicle_height, vehicle_type)
        
        # 가격 제한이 있으면 추가 필터링
        if price_limit:
            candidates = [lot for lot in candidates 
                         if self.calculate_advanced_pricing(lot, hours) <= price_limit]
        
        # 각 후보에 대해 점수 계산
        scored_lots = []
        
        for lot in candidates:
            # 실제 요금 계산
            total_cost = self.calculate_advanced_pricing(lot, hours)
            
            # 기존 점수 계산 시스템 사용
            score_info = self.calculate_advanced_score(lot, hours)
            
            # 실제 요금으로 업데이트
            score_info['total_cost'] = total_cost
            
            result = {
                **lot,
                'score_info': score_info,
                'final_score': score_info['final_score'],
                'total_cost': total_cost,
                'travel_time': score_info['travel_time'],
                'difficulty_level': self._get_difficulty_level(score_info['difficulty_score']),
                'detailed_pricing': self._generate_pricing_breakdown(lot, hours)
            }
            
            scored_lots.append(result)
        
        # 점수순으로 정렬
        scored_lots.sort(key=lambda x: x['final_score'], reverse=True)
        
        return {
            'parsed_command': parsed_command,
            'total_found': len(scored_lots),
            'recommendations': scored_lots,
            'data_source': 'real_parking_data',
            'processing_info': {
                'vehicle_height_filter': vehicle_height,
                'vehicle_type_filter': vehicle_type,
                'price_limit_filter': price_limit,
                'hours_requested': hours
            }
        }
    
    def _generate_pricing_breakdown(self, lot: Dict, hours: int) -> Dict:
        """요금 상세 내역 생성"""
        pricing = lot['pricing']
        
        breakdown = {
            'base_rate': pricing['hourly_rate'],
            'total_hours': hours,
            'calculation_method': 'detailed_pricing'
        }
        
        if hours <= 1:
            breakdown['cost_breakdown'] = f"첫 1시간: {pricing['hourly_rate']:,}원"
        else:
            base_cost = pricing.get('weekday_base', pricing['hourly_rate'])
            additional_cost = (hours - 1) * pricing.get('weekday_additional', 0)
            breakdown['cost_breakdown'] = f"기본요금: {base_cost:,}원 + 추가요금: {additional_cost:,}원"
        
        # 일일 최대 요금 적용 여부
        if hours >= 8 and pricing.get('daily_rate'):
            breakdown['daily_rate_applied'] = True
            breakdown['daily_rate'] = pricing['daily_rate']
        else:
            breakdown['daily_rate_applied'] = False
        
        return breakdown

# 테스트 함수
def test_real_data_system():
    """실제 데이터 시스템 테스트"""
    system = RealParkingDataSystem()
    
    print("🏢 실제 주차장 데이터 시스템 테스트")
    print("=" * 60)
    
    # 주차장 데이터 확인
    print(f"\n📊 등록된 주차장: {len(system.parking_lots)}개")
    for lot in system.parking_lots:
        print(f"   - {lot['name']}")
        print(f"     위치: {lot['location']['address']}")
        print(f"     시간당 요금: {lot['pricing']['hourly_rate']:,}원")
        print(f"     높이 제한: {lot['restrictions']['height_limit']}m")
        print(f"     전기차 충전: {'가능' if lot['amenities']['ev_charging'] else '불가능'}")
        print(f"     지붕: {'있음' if lot['amenities']['roof'] else '없음'}")
        print()
    
    # 테스트 명령어들
    test_commands = [
        "2시간 주차장 찾아줘",
        "전기차 충전 가능한 주차장 찾아줘",
        "SUV 3시간 주차할 곳 찾아줘",
        "5000원 이하로 4시간 주차할 곳 찾아줘"
    ]
    
    print("🎤 음성 명령어 테스트:")
    print("-" * 40)
    
    for i, command in enumerate(test_commands, 1):
        print(f"\n{i}. 명령어: \"{command}\"")
        
        result = system.process_real_data_request(command)
        
        print(f"   📝 파싱 결과:")
        parsed = result['parsed_command']
        print(f"      - 명령어 타입: {parsed['command_type']}")
        print(f"      - 시간: {parsed['time_info']['hours']}시간")
        print(f"      - 위치: {parsed['locations']}")
        print(f"      - 차량: {parsed['vehicle_types']}")
        print(f"      - 가격 제한: {parsed['price_info']['max_price']}")
        
        print(f"   🎯 추천 결과: {result['total_found']}개")
        
        if result['recommendations']:
            for j, lot in enumerate(result['recommendations'][:3], 1):
                print(f"      {j}. {lot['name']}")
                print(f"         💰 비용: {lot['total_cost']:,}원 ({result['parsed_command']['time_info']['hours']}시간)")
                print(f"         ⏱️ 도착시간: {lot['travel_time']}분")
                print(f"         🚗 난이도: {lot['difficulty_level']}")
                print(f"         ⭐ 점수: {lot['final_score']:.2f}")
                
                # 상세 요금 내역
                pricing = lot['detailed_pricing']
                print(f"         📋 요금 내역: {pricing['cost_breakdown']}")
                
                # 특별 기능
                amenities = []
                if lot['amenities']['ev_charging']:
                    amenities.append("전기차충전")
                if lot['amenities']['roof']:
                    amenities.append("지붕보호")
                if lot['amenities']['elevator']:
                    amenities.append("엘리베이터")
                
                if amenities:
                    print(f"         🏪 편의시설: {', '.join(amenities)}")
        else:
            print("      조건에 맞는 주차장이 없습니다.")

if __name__ == "__main__":
    test_real_data_system()









