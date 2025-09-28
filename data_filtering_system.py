#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
데이터 필터링 시스템
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, time
import json
from natural_language_processor import NaturalLanguageProcessor

class DataFilteringSystem:
    def __init__(self):
        """데이터 필터링 시스템 초기화"""
        self.nlp = NaturalLanguageProcessor()
        
        # 주차장 데이터 (실제로는 API나 DB에서 가져옴)
        self.parking_lots = [
            {
                "id": 1,
                "name": "서울시청 주차장",
                "location": {"latitude": 37.5665, "longitude": 126.9780, "address": "서울특별시 중구 세종대로 110"},
                "pricing": {"hourly_rate": 1000, "daily_rate": 15000, "night_rate": 500},
                "capacity": {"total_spaces": 300, "available_spaces": 15},
                "facilities": ["24시간 운영", "장애인 주차공간", "전기차 충전시설"],
                "operating_hours": {"weekday": "00:00-23:59", "weekend": "00:00-23:59"},
                "restrictions": {"max_duration": 24, "vehicle_types": ["승용차", "SUV", "승합차"], "height_limit": 2.1},
                "amenities": {"elevator": True, "restroom": True, "atm": True},
                "rating": 4.2,
                "reviews_count": 156
            },
            {
                "id": 2,
                "name": "명동 중앙 주차장",
                "location": {"latitude": 37.5636, "longitude": 126.9826, "address": "서울특별시 중구 명동길 26"},
                "pricing": {"hourly_rate": 1500, "daily_rate": 20000, "night_rate": 800},
                "capacity": {"total_spaces": 200, "available_spaces": 8},
                "facilities": ["24시간 운영", "장애인 주차공간", "발렛파킹"],
                "operating_hours": {"weekday": "06:00-23:00", "weekend": "08:00-22:00"},
                "restrictions": {"max_duration": 12, "vehicle_types": ["승용차", "SUV"], "height_limit": 2.0},
                "amenities": {"elevator": True, "restroom": True, "atm": True},
                "rating": 4.5,
                "reviews_count": 89
            },
            {
                "id": 3,
                "name": "강남역 지하 주차장",
                "location": {"latitude": 37.4979, "longitude": 127.0276, "address": "서울특별시 강남구 강남대로 396"},
                "pricing": {"hourly_rate": 2000, "daily_rate": 25000, "night_rate": 1000},
                "capacity": {"total_spaces": 500, "available_spaces": 25},
                "facilities": ["24시간 운영", "장애인 주차공간", "전기차 충전시설", "무료 WiFi"],
                "operating_hours": {"weekday": "05:30-24:00", "weekend": "06:00-23:30"},
                "restrictions": {"max_duration": 48, "vehicle_types": ["승용차", "SUV", "승합차", "화물차"], "height_limit": 2.3},
                "amenities": {"elevator": True, "restroom": True, "convenience_store": True, "atm": True},
                "rating": 4.7,
                "reviews_count": 234
            }
        ]
        
        # 현재 위치 (실제로는 GPS에서 가져옴)
        self.current_location = {"latitude": 37.5665, "longitude": 126.9780}
    
    def filter_by_time_requirement(self, parking_lots: List[Dict], time_info: Dict) -> List[Dict]:
        """시간 요구사항에 따른 필터링"""
        filtered_lots = []
        
        required_hours = time_info.get('hours', 0) or 0
        required_minutes = time_info.get('minutes', 0) or 0
        required_days = time_info.get('days', 0) or 0
        
        # 총 필요 시간 계산 (시간 단위)
        total_required_hours = required_hours + (required_minutes / 60) + (required_days * 24)
        
        for lot in parking_lots:
            max_duration = lot['restrictions']['max_duration']
            
            # 최대 주차 시간 체크
            if max_duration >= total_required_hours:
                # 운영 시간 체크
                if self._is_operating_now(lot, time_info):
                    filtered_lots.append(lot)
        
        return filtered_lots
    
    def filter_by_location(self, parking_lots: List[Dict], locations: List[str]) -> List[Dict]:
        """위치에 따른 필터링"""
        if not locations:
            return parking_lots
        
        filtered_lots = []
        
        for lot in parking_lots:
            lot_address = lot['location']['address'].lower()
            lot_name = lot['name'].lower()
            
            for location in locations:
                if location.lower() in lot_address or location.lower() in lot_name:
                    filtered_lots.append(lot)
                    break
        
        return filtered_lots
    
    def filter_by_vehicle_type(self, parking_lots: List[Dict], vehicle_types: List[str]) -> List[Dict]:
        """차량 타입에 따른 필터링"""
        if not vehicle_types:
            return parking_lots
        
        filtered_lots = []
        
        for lot in parking_lots:
            allowed_vehicles = lot['restrictions']['vehicle_types']
            
            # 요청된 차량 타입이 허용되는지 확인
            if any(vehicle in allowed_vehicles for vehicle in vehicle_types):
                filtered_lots.append(lot)
        
        return filtered_lots
    
    def filter_by_price(self, parking_lots: List[Dict], price_info: Dict) -> List[Dict]:
        """가격에 따른 필터링"""
        max_price = price_info.get('max_price')
        price_range = price_info.get('price_range')
        
        if not max_price and not price_range:
            return parking_lots
        
        filtered_lots = []
        
        for lot in parking_lots:
            hourly_rate = lot['pricing']['hourly_rate']
            
            # 최대 가격 체크
            if max_price and hourly_rate <= max_price:
                filtered_lots.append(lot)
            # 가격 범위 체크
            elif price_range:
                min_price, max_price_range = price_range
                if min_price <= hourly_rate <= max_price_range:
                    filtered_lots.append(lot)
        
        return filtered_lots
    
    def filter_by_availability(self, parking_lots: List[Dict], min_availability: int = 1) -> List[Dict]:
        """가용성에 따른 필터링"""
        return [lot for lot in parking_lots if lot['capacity']['available_spaces'] >= min_availability]
    
    def filter_by_facilities(self, parking_lots: List[Dict], required_facilities: List[str]) -> List[Dict]:
        """편의시설에 따른 필터링"""
        if not required_facilities:
            return parking_lots
        
        filtered_lots = []
        
        for lot in parking_lots:
            lot_facilities = lot['facilities']
            
            # 요청된 모든 편의시설이 있는지 확인
            if all(facility in lot_facilities for facility in required_facilities):
                filtered_lots.append(lot)
        
        return filtered_lots
    
    def filter_by_rating(self, parking_lots: List[Dict], min_rating: float = 0.0) -> List[Dict]:
        """평점에 따른 필터링"""
        return [lot for lot in parking_lots if lot['rating'] >= min_rating]
    
    def _is_operating_now(self, lot: Dict, time_info: Dict) -> bool:
        """현재 운영 중인지 확인"""
        current_time = datetime.now()
        current_hour = current_time.hour
        
        # 운영 시간 파싱
        operating_hours = lot['operating_hours']
        
        # 요일별 운영 시간 확인
        if current_time.weekday() < 5:  # 평일
            hours_str = operating_hours['weekday']
        else:  # 주말
            hours_str = operating_hours['weekend']
        
        # "HH:MM-HH:MM" 형식 파싱
        if '-' in hours_str:
            start_time, end_time = hours_str.split('-')
            start_hour = int(start_time.split(':')[0])
            end_hour = int(end_time.split(':')[0])
            
            # 24시간 운영 체크
            if start_hour == 0 and end_hour == 23:
                return True
            
            # 시간대 체크
            return start_hour <= current_hour <= end_hour
        
        return True
    
    def apply_all_filters(self, parsed_command: Dict) -> List[Dict]:
        """모든 필터를 적용하여 주차장 검색"""
        filtered_lots = self.parking_lots.copy()
        
        # 1. 가용성 필터링
        filtered_lots = self.filter_by_availability(filtered_lots)
        
        # 2. 시간 요구사항 필터링
        if parsed_command['time_info']['hours'] or parsed_command['time_info']['minutes'] or parsed_command['time_info']['days']:
            filtered_lots = self.filter_by_time_requirement(filtered_lots, parsed_command['time_info'])
        
        # 3. 위치 필터링
        if parsed_command['locations']:
            filtered_lots = self.filter_by_location(filtered_lots, parsed_command['locations'])
        
        # 4. 차량 타입 필터링
        if parsed_command['vehicle_types']:
            filtered_lots = self.filter_by_vehicle_type(filtered_lots, parsed_command['vehicle_types'])
        
        # 5. 가격 필터링
        if parsed_command['price_info']['max_price'] or parsed_command['price_info']['price_range']:
            filtered_lots = self.filter_by_price(filtered_lots, parsed_command['price_info'])
        
        # 6. 평점 필터링 (기본값: 3.0 이상)
        filtered_lots = self.filter_by_rating(filtered_lots, 3.0)
        
        return filtered_lots
    
    def rank_results(self, parking_lots: List[Dict], parsed_command: Dict) -> List[Dict]:
        """결과 랭킹 및 정렬"""
        ranked_lots = []
        
        time_info = parsed_command['time_info']
        required_hours = time_info.get('hours', 2) or 2  # 기본값 2시간
        
        for lot in parking_lots:
            # 점수 계산
            score = self._calculate_score(lot, required_hours)
            
            ranked_lot = lot.copy()
            ranked_lot['score'] = score
            ranked_lot['total_cost'] = lot['pricing']['hourly_rate'] * required_hours
            ranked_lots.append(ranked_lot)
        
        # 점수순으로 정렬 (낮을수록 좋음)
        ranked_lots.sort(key=lambda x: x['score'])
        
        return ranked_lots
    
    def _calculate_score(self, lot: Dict, required_hours: int) -> float:
        """주차장 점수 계산"""
        # 거리 점수 (현재 위치 기준)
        distance = self._calculate_distance(lot)
        
        # 비용 점수
        cost = lot['pricing']['hourly_rate'] * required_hours
        
        # 가용성 점수 (적을수록 좋음)
        availability = lot['capacity']['available_spaces']
        
        # 평점 점수 (낮을수록 좋음)
        rating = lot['rating']
        
        # 가중치 적용
        score = (
            distance * 40 +           # 거리 40%
            cost * 0.001 * 30 +       # 비용 30%
            (10 - availability) * 2 + # 가용성 20%
            (5 - rating) * 2          # 평점 10%
        )
        
        return round(score, 2)
    
    def _calculate_distance(self, lot: Dict) -> float:
        """현재 위치에서 주차장까지의 거리 계산 (간단한 유클리드 거리)"""
        lat_diff = abs(lot['location']['latitude'] - self.current_location['latitude'])
        lon_diff = abs(lot['location']['longitude'] - self.current_location['longitude'])
        return (lat_diff + lon_diff) * 111  # 대략적인 km 변환
    
    def process_voice_command(self, voice_text: str) -> Dict:
        """음성 명령어 처리 및 필터링"""
        # 1. 자연어 처리
        parsed_command = self.nlp.parse_complete_command(voice_text)
        
        # 2. 필터링 적용
        filtered_lots = self.apply_all_filters(parsed_command)
        
        # 3. 랭킹 및 정렬
        ranked_results = self.rank_results(filtered_lots, parsed_command)
        
        # 4. 결과 반환
        return {
            'parsed_command': parsed_command,
            'total_found': len(ranked_results),
            'results': ranked_results[:5],  # 상위 5개만 반환
            'processing_time': datetime.now().isoformat()
        }

# 테스트 함수
def test_filtering_system():
    """필터링 시스템 테스트"""
    filtering_system = DataFilteringSystem()
    
    test_commands = [
        "2시간 주차장 찾아줘",
        "강남역에서 3시간 주차할 곳 찾아줘",
        "SUV 1시간 주차장 예약해줘",
        "5000원 이하로 4시간 주차할 곳 찾아줘",
        "명동 주차장 정보 알려줘"
    ]
    
    print("🔍 데이터 필터링 시스템 테스트")
    print("=" * 60)
    
    for i, command in enumerate(test_commands, 1):
        print(f"\n{i}. 테스트 명령어: '{command}'")
        result = filtering_system.process_voice_command(command)
        
        print(f"   파싱된 명령어: {result['parsed_command']['command_type']}")
        print(f"   시간 정보: {result['parsed_command']['time_info']}")
        print(f"   찾은 주차장 수: {result['total_found']}")
        
        if result['results']:
            print("   추천 주차장:")
            for j, lot in enumerate(result['results'][:3], 1):
                print(f"     {j}. {lot['name']} (점수: {lot['score']}, 비용: {lot['total_cost']:,}원)")

if __name__ == "__main__":
    test_filtering_system()
