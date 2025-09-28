#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
고급 스코어링 및 랭킹 시스템
가중치 기반 최적화 점수 계산
"""

import math
from typing import Dict, List, Tuple, Optional
from datetime import datetime, time
import json

class AdvancedScoringSystem:
    def __init__(self):
        """고급 스코어링 시스템 초기화"""
        
        # 가중치 설정 (사용자 설정 가능)
        self.weights = {
            'price_sensitivity': 0.4,    # α - 가격 민감도 (기본값)
            'time_sensitivity': 0.4,     # β - 시간 민감도 (기본값)  
            'convenience_sensitivity': 0.2  # γ - 편의성 민감도 (기본값)
        }
        
        # 주차장 데이터 (운전 난이도 정보 추가)
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
                "reviews_count": 156,
                # 운전 난이도 관련 정보
                "driving_difficulty": {
                    "parking_type": "자주식",  # 자주식, 기계식, 발렛파킹
                    "access_road_width": 4.5,  # 진입로 폭 (미터)
                    "turning_radius": 8.0,     # 회전 반경 (미터)
                    "slope_angle": 5,          # 경사각 (도)
                    "obstacles": ["없음"],     # 장애물
                    "lighting": "우수",        # 조명 상태
                    "security": "우수"         # 보안 상태
                }
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
                "reviews_count": 234,
                "driving_difficulty": {
                    "parking_type": "기계식",
                    "access_road_width": 3.5,
                    "turning_radius": 7.0,
                    "slope_angle": 8,
                    "obstacles": ["기둥", "화분"],
                    "lighting": "우수",
                    "security": "우수"
                }
            }
        ]
        
        # 현재 위치 (실제로는 GPS에서 가져옴)
        self.current_location = {"latitude": 37.5665, "longitude": 126.9780, "address": "서울특별시 중구 세종대로 110"}
        
        # 목적지 위치 (사용자 입력 또는 기본값)
        self.destination = {"latitude": 37.5665, "longitude": 126.9780}
    
    def set_user_preferences(self, price_weight: float = None, time_weight: float = None, convenience_weight: float = None):
        """사용자 가중치 설정"""
        if price_weight is not None:
            self.weights['price_sensitivity'] = price_weight
        if time_weight is not None:
            self.weights['time_sensitivity'] = time_weight
        if convenience_weight is not None:
            self.weights['convenience_sensitivity'] = convenience_weight
        
        # 가중치 정규화 (합이 1이 되도록)
        total = sum(self.weights.values())
        for key in self.weights:
            self.weights[key] = self.weights[key] / total
    
    def calculate_driving_difficulty_score(self, lot: Dict) -> float:
        """운전 난이도 점수 계산 (0-1, 낮을수록 좋음)"""
        difficulty = lot['driving_difficulty']
        score = 0.0
        
        # 주차 타입 점수 (자주식이 가장 쉬움)
        parking_type_scores = {
            "자주식": 0.0,
            "기계식": 0.3,
            "발렛파킹": 0.1
        }
        score += parking_type_scores.get(difficulty['parking_type'], 0.5)
        
        # 진입로 폭 점수 (넓을수록 좋음)
        if difficulty['access_road_width'] >= 4.0:
            score += 0.0
        elif difficulty['access_road_width'] >= 3.0:
            score += 0.1
        else:
            score += 0.3
        
        # 회전 반경 점수 (클수록 좋음)
        if difficulty['turning_radius'] >= 8.0:
            score += 0.0
        elif difficulty['turning_radius'] >= 6.0:
            score += 0.1
        else:
            score += 0.2
        
        # 경사각 점수 (평평할수록 좋음)
        slope_penalty = min(difficulty['slope_angle'] * 0.02, 0.3)
        score += slope_penalty
        
        # 장애물 점수
        obstacle_count = len(difficulty['obstacles']) - difficulty['obstacles'].count("없음")
        score += obstacle_count * 0.1
        
        # 조명 점수
        lighting_scores = {"우수": 0.0, "양호": 0.1, "보통": 0.2, "나쁨": 0.3}
        score += lighting_scores.get(difficulty['lighting'], 0.2)
        
        # 최대 1.0으로 제한
        return min(score, 1.0)
    
    def calculate_travel_time(self, lot: Dict) -> float:
        """주차장까지 예상 소요시간 계산 (분)"""
        # 실제로는 지도 API를 사용해야 하지만, 여기서는 거리 기반 추정
        
        # 간단한 거리 계산 (실제로는 지도 API 사용)
        lat_diff = abs(lot['location']['latitude'] - self.current_location['latitude'])
        lng_diff = abs(lot['location']['longitude'] - self.current_location['longitude'])
        distance_km = (lat_diff + lng_diff) * 111  # 대략적인 km 변환
        
        # 도시 평균 속도 30km/h 가정
        travel_time_minutes = (distance_km / 30) * 60
        
        # 교통상황 보정 (기본 20% 추가)
        travel_time_minutes *= 1.2
        
        return round(travel_time_minutes, 1)
    
    def calculate_total_cost(self, lot: Dict, hours: int) -> float:
        """총 주차 비용 계산"""
        hourly_rate = lot['pricing']['hourly_rate']
        daily_rate = lot['pricing']['daily_rate']
        
        # 일일 요금이 더 저렴한 경우
        if hours >= 8 and daily_rate < hourly_rate * hours:
            return daily_rate
        
        return hourly_rate * hours
    
    def calculate_advanced_score(self, lot: Dict, hours: int) -> Dict:
        """고급 점수 계산"""
        
        # 1. 총 비용 계산
        total_cost = self.calculate_total_cost(lot, hours)
        
        # 2. 예상 소요시간 계산
        travel_time = self.calculate_travel_time(lot)
        
        # 3. 운전 난이도 점수 계산
        difficulty_score = self.calculate_driving_difficulty_score(lot)
        
        # 4. 가중치 적용 점수 계산
        # α*(1/총요금) + β*(1/예상 소요시간) + γ*(운전 난이도)
        
        # 비용 점수 (낮을수록 좋음) - 역수 사용
        max_cost = 50000  # 최대 비용 기준
        cost_score = (max_cost / max(total_cost, 1000))  # 최소 1000원으로 나눗셈 방지
        
        # 시간 점수 (짧을수록 좋음) - 역수 사용
        max_time = 120  # 최대 120분
        time_score = (max_time / max(travel_time, 1))  # 최소 1분으로 나눗셈 방지
        
        # 편의성 점수 (높을수록 좋음) - 운전 난이도의 역수
        convenience_score = 1 - difficulty_score
        
        # 최종 가중치 점수 계산
        final_score = (
            self.weights['price_sensitivity'] * cost_score +
            self.weights['time_sensitivity'] * time_score +
            self.weights['convenience_sensitivity'] * convenience_score
        )
        
        return {
            'final_score': round(final_score, 3),
            'cost_score': round(cost_score, 3),
            'time_score': round(time_score, 3),
            'convenience_score': round(convenience_score, 3),
            'total_cost': total_cost,
            'travel_time': travel_time,
            'difficulty_score': round(difficulty_score, 3),
            'breakdown': {
                'price_component': round(self.weights['price_sensitivity'] * cost_score, 3),
                'time_component': round(self.weights['time_sensitivity'] * time_score, 3),
                'convenience_component': round(self.weights['convenience_sensitivity'] * convenience_score, 3)
            }
        }
    
    def filter_candidates(self, vehicle_height: float = None, vehicle_type: str = None, operating_now: bool = True) -> List[Dict]:
        """후보군 필터링"""
        filtered_lots = []
        
        for lot in self.parking_lots:
            # 1. 차량 높이 필터링
            if vehicle_height is not None:
                if lot['restrictions']['height_limit'] < vehicle_height:
                    continue
            
            # 2. 차종 제한 기준 필터링
            if vehicle_type is not None:
                if vehicle_type not in lot['restrictions']['vehicle_types']:
                    continue
            
            # 3. 운영 시간 필터링
            if operating_now:
                if not self._is_operating_now(lot):
                    continue
            
            # 4. 가용성 필터링
            if lot['capacity']['available_spaces'] <= 0:
                continue
            
            filtered_lots.append(lot)
        
        return filtered_lots
    
    def _is_operating_now(self, lot: Dict) -> bool:
        """현재 운영 중인지 확인"""
        current_time = datetime.now()
        current_hour = current_time.hour
        
        operating_hours = lot['operating_hours']
        
        if current_time.weekday() < 5:  # 평일
            hours_str = operating_hours['weekday']
        else:  # 주말
            hours_str = operating_hours['weekend']
        
        if '-' in hours_str:
            start_time, end_time = hours_str.split('-')
            start_hour = int(start_time.split(':')[0])
            end_hour = int(end_time.split(':')[0])
            
            if start_hour == 0 and end_hour == 23:
                return True
            
            return start_hour <= current_hour <= end_hour
        
        return True
    
    def get_top_recommendations(self, hours: int, top_n: int = 5, 
                               vehicle_height: float = None, vehicle_type: str = None,
                               user_preferences: Dict = None) -> List[Dict]:
        """Top N 주차장 추천"""
        
        # 사용자 가중치 설정
        if user_preferences:
            self.set_user_preferences(
                user_preferences.get('price_weight'),
                user_preferences.get('time_weight'), 
                user_preferences.get('convenience_weight')
            )
        
        # 1. 후보군 필터링
        candidates = self.filter_candidates(vehicle_height, vehicle_type)
        
        # 2. 각 후보에 대해 점수 계산
        scored_lots = []
        
        for lot in candidates:
            score_info = self.calculate_advanced_score(lot, hours)
            
            result = {
                **lot,
                'score_info': score_info,
                'final_score': score_info['final_score'],
                'total_cost': score_info['total_cost'],
                'travel_time': score_info['travel_time'],
                'difficulty_level': self._get_difficulty_level(score_info['difficulty_score'])
            }
            
            scored_lots.append(result)
        
        # 3. 점수순으로 정렬 (높을수록 좋음)
        scored_lots.sort(key=lambda x: x['final_score'], reverse=True)
        
        # 4. Top N 반환
        return scored_lots[:top_n]
    
    def _get_difficulty_level(self, difficulty_score: float) -> str:
        """난이도 점수를 레벨로 변환"""
        if difficulty_score <= 0.2:
            return "매우 쉬움"
        elif difficulty_score <= 0.4:
            return "쉬움"
        elif difficulty_score <= 0.6:
            return "보통"
        elif difficulty_score <= 0.8:
            return "어려움"
        else:
            return "매우 어려움"
    
    def generate_route_guidance(self, lot: Dict) -> Dict:
        """지도 경로 안내 정보 생성 (실제로는 지도 API 연동)"""
        return {
            "start_location": self.current_location,
            "end_location": lot['location'],
            "route_info": {
                "distance_km": round(self.calculate_travel_time(lot) * 0.5, 1),  # 대략적 거리
                "estimated_time_minutes": self.calculate_travel_time(lot),
                "traffic_condition": "보통",
                "toll_roads": [],
                "route_summary": f"{self.current_location['address']} → {lot['location']['address']}"
            },
            "turn_by_turn": [
                "현재 위치에서 출발",
                "주요 도로로 진입",
                f"{lot['name']} 도착"
            ]
        }

# 테스트 함수
def test_advanced_scoring():
    """고급 스코어링 시스템 테스트"""
    scoring = AdvancedScoringSystem()
    
    print("🎯 고급 스코어링 시스템 테스트")
    print("=" * 60)
    
    # 기본 설정으로 테스트
    print("\n1. 기본 가중치 설정 테스트:")
    print(f"가격 민감도 (α): {scoring.weights['price_sensitivity']}")
    print(f"시간 민감도 (β): {scoring.weights['time_sensitivity']}")
    print(f"편의성 민감도 (γ): {scoring.weights['convenience_sensitivity']}")
    
    # 2시간 주차 추천
    recommendations = scoring.get_top_recommendations(hours=2, top_n=3)
    
    print(f"\n2. 2시간 주차 추천 결과:")
    for i, lot in enumerate(recommendations, 1):
        print(f"\n{i}. {lot['name']}")
        print(f"   💰 총 비용: {lot['total_cost']:,}원")
        print(f"   ⏱️ 예상 소요시간: {lot['travel_time']}분")
        print(f"   🚗 운전 난이도: {lot['difficulty_level']}")
        print(f"   ⭐ 최종 점수: {lot['final_score']}")
        
        # 점수 구성 요소
        breakdown = lot['score_info']['breakdown']
        print(f"   📊 점수 구성:")
        print(f"      - 가격 점수: {breakdown['price_component']}")
        print(f"      - 시간 점수: {breakdown['time_component']}")
        print(f"      - 편의성 점수: {breakdown['convenience_component']}")
    
    # 사용자 가중치 변경 테스트
    print(f"\n3. 가격 민감도 높은 설정 테스트:")
    price_sensitive_recommendations = scoring.get_top_recommendations(
        hours=2, 
        top_n=3,
        user_preferences={'price_weight': 0.7, 'time_weight': 0.2, 'convenience_weight': 0.1}
    )
    
    for i, lot in enumerate(price_sensitive_recommendations, 1):
        print(f"\n{i}. {lot['name']} - {lot['total_cost']:,}원 (점수: {lot['final_score']})")

if __name__ == "__main__":
    test_advanced_scoring()
