"""
거리 기반 예상 소요시간 산출 시스템
다양한 방법을 조합하여 정확도를 높인 시간 추정
"""

import math
from typing import Dict, List, Tuple, Optional
from datetime import datetime, time
import json

class TravelTimeEstimator:
    """거리 기반 예상 소요시간 계산기"""
    
    def __init__(self):
        """초기화"""
        
        # 지역별 평균 속도 (km/h)
        self.average_speeds = {
            "서울_도심": {
                "평일_오전": 25,    # 7-10시
                "평일_점심": 35,    # 11-14시
                "평일_오후": 30,    # 15-18시
                "평일_저녁": 40,    # 19-22시
                "평일_심야": 50,    # 23-6시
                "주말_오전": 35,    # 7-12시
                "주말_오후": 40,    # 13-18시
                "주말_저녁": 45,    # 19-23시
                "주말_심야": 55,    # 24-6시
            },
            "서울_외곽": {
                "평일_오전": 35,
                "평일_점심": 45,
                "평일_오후": 40,
                "평일_저녁": 50,
                "평일_심야": 60,
                "주말_오전": 45,
                "주말_오후": 50,
                "주말_저녁": 55,
                "주말_심야": 65,
            },
            "고속도로": {
                "평일": 80,
                "주말": 90,
                "심야": 100
            }
        }
        
        # 도로 타입별 속도 보정 계수
        self.road_type_factors = {
            "고속도로": 1.0,
            "도시고속도로": 0.8,
            "주요도로": 0.6,
            "일반도로": 0.4,
            "단지내도로": 0.2
        }
        
        # 날씨/상황별 보정 계수
        self.condition_factors = {
            "맑음": 1.0,
            "흐림": 0.95,
            "비": 0.8,
            "눈": 0.6,
            "교통사고": 0.3,
            "공사": 0.7,
            "이벤트": 0.5
        }
        
        # 대중교통 시간표 (지하철/버스)
        self.public_transit_times = {
            "지하철": {
                "평균_속도": 35,  # km/h
                "대기시간": 3,    # 분
                "환승시간": 5     # 분
            },
            "버스": {
                "평균_속도": 25,  # km/h
                "대기시간": 8,    # 분
                "환승시간": 3,    # 분
                "정류장_시간": 1  # 분
            }
        }
    
    def haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Haversine 공식을 사용한 거리 계산 (km)"""
        R = 6371  # 지구 반지름 (km)
        
        # 위도, 경도를 라디안으로 변환
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        # Haversine 공식
        a = (math.sin(delta_lat / 2) ** 2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c
    
    def get_time_period(self, current_time: datetime) -> str:
        """현재 시간대 판별"""
        hour = current_time.hour
        is_weekend = current_time.weekday() >= 5  # 토요일(5), 일요일(6)
        
        if is_weekend:
            if 7 <= hour < 12:
                return "주말_오전"
            elif 12 <= hour < 18:
                return "주말_오후"
            elif 18 <= hour < 23:
                return "주말_저녁"
            else:
                return "주말_심야"
        else:  # 평일
            if 7 <= hour < 10:
                return "평일_오전"
            elif 10 <= hour < 15:
                return "평일_점심"
            elif 15 <= hour < 19:
                return "평일_오후"
            elif 19 <= hour < 23:
                return "평일_저녁"
            else:
                return "평일_심야"
    
    def get_area_type(self, lat: float, lon: float) -> str:
        """지역 타입 판별 (도심/외곽)"""
        # 서울 도심 지역 좌표 범위 (대략적)
        seoul_center = {
            "min_lat": 37.45,
            "max_lat": 37.65,
            "min_lon": 126.85,
            "max_lon": 127.15
        }
        
        # 도심 지역인지 확인
        if (seoul_center["min_lat"] <= lat <= seoul_center["max_lat"] and
            seoul_center["min_lon"] <= lon <= seoul_center["max_lon"]):
            return "서울_도심"
        else:
            return "서울_외곽"
    
    def estimate_car_travel_time(self, lat1: float, lon1: float, lat2: float, lon2: float,
                               current_time: Optional[datetime] = None,
                               road_type: str = "일반도로",
                               weather_condition: str = "맑음") -> Dict:
        """자동차 예상 소요시간 계산"""
        
        if current_time is None:
            current_time = datetime.now()
        
        # 1. 직선 거리 계산
        straight_distance = self.haversine_distance(lat1, lon1, lat2, lon2)
        
        # 2. 실제 도로 거리 추정 (직선 거리의 1.2-1.5배)
        road_distance_factor = 1.3  # 평균적으로 직선거리의 1.3배
        if road_type == "고속도로":
            road_distance_factor = 1.1  # 고속도로는 직선에 가까움
        elif road_type == "단지내도로":
            road_distance_factor = 1.5  # 단지내는 우회가 많음
        
        actual_distance = straight_distance * road_distance_factor
        
        # 3. 시간대별 평균 속도 계산
        time_period = self.get_time_period(current_time)
        area_type = self.get_area_type(lat1, lon1)  # 출발지 기준
        
        base_speed = self.average_speeds[area_type][time_period]
        
        # 4. 도로 타입별 속도 보정
        road_factor = self.road_type_factors.get(road_type, 0.6)
        adjusted_speed = base_speed * road_factor
        
        # 5. 날씨/상황별 보정
        condition_factor = self.condition_factors.get(weather_condition, 1.0)
        final_speed = adjusted_speed * condition_factor
        
        # 6. 예상 소요시간 계산 (분)
        travel_time_minutes = (actual_distance / final_speed) * 60
        
        # 7. 추가 시간 요소들
        additional_time = 0
        
        # 신호등 대기시간 (도심지역)
        if area_type == "서울_도심":
            traffic_lights = int(actual_distance * 2)  # km당 2개 신호등
            additional_time += traffic_lights * 1.5  # 신호등당 1.5분 대기
        
        # 주차장 진입 시간
        parking_time = 3  # 평균 3분
        
        # 총 소요시간
        total_time = travel_time_minutes + additional_time + parking_time
        
        return {
            "straight_distance_km": round(straight_distance, 2),
            "actual_distance_km": round(actual_distance, 2),
            "base_speed_kmh": base_speed,
            "adjusted_speed_kmh": round(final_speed, 1),
            "travel_time_minutes": round(travel_time_minutes, 1),
            "additional_time_minutes": round(additional_time, 1),
            "parking_time_minutes": parking_time,
            "total_time_minutes": round(total_time, 1),
            "time_period": time_period,
            "area_type": area_type,
            "road_type": road_type,
            "weather_condition": weather_condition
        }
    
    def estimate_public_transit_time(self, lat1: float, lon1: float, lat2: float, lon2: float,
                                   current_time: Optional[datetime] = None,
                                   transit_type: str = "지하철") -> Dict:
        """대중교통 예상 소요시간 계산"""
        
        if current_time is None:
            current_time = datetime.now()
        
        # 1. 직선 거리 계산
        distance = self.haversine_distance(lat1, lon1, lat2, lon2)
        
        # 2. 대중교통 정보
        transit_info = self.public_transit_times[transit_type]
        
        # 3. 이동 시간 계산
        travel_time = (distance / transit_info["평균_속도"]) * 60
        
        # 4. 대기 및 환승 시간
        waiting_time = transit_info["대기시간"]
        
        # 환승 횟수 추정 (거리 기반)
        if distance <= 2:
            transfer_count = 0
        elif distance <= 5:
            transfer_count = 1
        else:
            transfer_count = 2
        
        transfer_time = transfer_count * transit_info["환승시간"]
        
        # 5. 총 소요시간
        total_time = travel_time + waiting_time + transfer_time
        
        return {
            "distance_km": round(distance, 2),
            "transit_type": transit_type,
            "travel_time_minutes": round(travel_time, 1),
            "waiting_time_minutes": waiting_time,
            "transfer_count": transfer_count,
            "transfer_time_minutes": transfer_time,
            "total_time_minutes": round(total_time, 1)
        }
    
    def estimate_walking_time(self, lat1: float, lon1: float, lat2: float, lon2: float) -> Dict:
        """도보 예상 소요시간 계산"""
        
        # 1. 직선 거리 계산
        distance = self.haversine_distance(lat1, lon1, lat2, lon2)
        
        # 2. 도보 속도 (km/h)
        walking_speed = 4.0  # 평균 도보 속도 4km/h
        
        # 3. 예상 소요시간 (분)
        walking_time = (distance / walking_speed) * 60
        
        return {
            "distance_km": round(distance, 2),
            "walking_speed_kmh": walking_speed,
            "walking_time_minutes": round(walking_time, 1)
        }
    
    def get_comprehensive_travel_time(self, lat1: float, lon1: float, lat2: float, lon2: float,
                                    current_time: Optional[datetime] = None,
                                    preferences: Optional[Dict] = None) -> Dict:
        """종합적인 이동수단별 예상 소요시간"""
        
        if current_time is None:
            current_time = datetime.now()
        
        if preferences is None:
            preferences = {
                "road_type": "일반도로",
                "weather_condition": "맑음",
                "include_public_transit": True,
                "include_walking": True
            }
        
        results = {}
        
        # 1. 자동차 이동시간
        car_result = self.estimate_car_travel_time(
            lat1, lon1, lat2, lon2, current_time,
            preferences["road_type"], preferences["weather_condition"]
        )
        results["car"] = car_result
        
        # 2. 대중교통 이동시간 (옵션)
        if preferences.get("include_public_transit", True):
            subway_result = self.estimate_public_transit_time(
                lat1, lon1, lat2, lon2, current_time, "지하철"
            )
            results["subway"] = {
                "total_time_minutes": subway_result["total_time_minutes"],
                **subway_result
            }
            
            bus_result = self.estimate_public_transit_time(
                lat1, lon1, lat2, lon2, current_time, "버스"
            )
            results["bus"] = {
                "total_time_minutes": bus_result["total_time_minutes"],
                **bus_result
            }
        
        # 3. 도보 이동시간 (옵션)
        if preferences.get("include_walking", True):
            walking_result = self.estimate_walking_time(lat1, lon1, lat2, lon2)
            results["walking"] = {
                "total_time_minutes": walking_result["walking_time_minutes"],
                **walking_result
            }
        
        # 4. 최적 이동수단 추천
        best_transport = min(results.items(), key=lambda x: x[1]["total_time_minutes"])
        
        return {
            "travel_options": results,
            "recommended_transport": {
                "type": best_transport[0],
                "time_minutes": best_transport[1]["total_time_minutes"]
            },
            "distance_km": round(self.haversine_distance(lat1, lon1, lat2, lon2), 2),
            "calculation_time": current_time.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def get_traffic_conditions(self, current_time: Optional[datetime] = None) -> Dict:
        """현재 교통상황 분석"""
        
        if current_time is None:
            current_time = datetime.now()
        
        hour = current_time.hour
        is_weekend = current_time.weekday() >= 5
        
        # 교통체증 구간 분석
        congestion_levels = {
            "매우_혼잡": [7, 8, 9, 18, 19, 20],  # 출퇴근 시간
            "혼잡": [10, 11, 17, 21],
            "보통": [12, 13, 14, 15, 16, 22],
            "원활": [23, 0, 1, 2, 3, 4, 5, 6]
        }
        
        current_congestion = "보통"
        for level, hours in congestion_levels.items():
            if hour in hours:
                current_congestion = level
                break
        
        # 주말 보정
        if is_weekend and current_congestion in ["매우_혼잡", "혼잡"]:
            current_congestion = "보통"
        
        return {
            "congestion_level": current_congestion,
            "hour": hour,
            "is_weekend": is_weekend,
            "time_period": self.get_time_period(current_time),
            "recommendation": self._get_traffic_recommendation(current_congestion, is_weekend)
        }
    
    def _get_traffic_recommendation(self, congestion_level: str, is_weekend: bool) -> str:
        """교통상황별 추천사항"""
        
        recommendations = {
            "매우_혼잡": "대중교통 이용 권장, 자동차 이용시 30-50% 시간 추가 소요 예상",
            "혼잡": "자동차 이용 가능, 20-30% 시간 추가 소요 예상",
            "보통": "자동차 이용 적합, 정상적인 이동시간",
            "원활": "자동차 이용 최적, 평소보다 빠른 이동 가능"
        }
        
        return recommendations.get(congestion_level, "정상적인 이동시간")


class AdvancedTravelTimeEstimator:
    """고급 예상 소요시간 계산기 (실제 API 연동 준비)"""
    
    def __init__(self):
        self.basic_estimator = TravelTimeEstimator()
        
        # 실제 API 연동을 위한 설정 (향후 구현)
        self.api_keys = {
            "google_maps": None,
            "naver_maps": None,
            "kakao_maps": None,
            "tmap": None
        }
    
    def estimate_with_real_time_traffic(self, lat1: float, lon1: float, lat2: float, lon2: float,
                                      current_time: Optional[datetime] = None,
                                      api_provider: str = "google") -> Dict:
        """실시간 교통정보를 활용한 예상 소요시간"""
        
        # 현재는 기본 계산 + 교통상황 보정
        basic_result = self.basic_estimator.estimate_car_travel_time(
            lat1, lon1, lat2, lon2, current_time
        )
        
        # 실시간 교통상황 분석
        traffic_conditions = self.basic_estimator.get_traffic_conditions(current_time)
        
        # 교통상황에 따른 추가 시간 보정
        traffic_multipliers = {
            "매우_혼잡": 1.5,
            "혼잡": 1.3,
            "보통": 1.0,
            "원활": 0.8
        }
        
        traffic_multiplier = traffic_multipliers.get(
            traffic_conditions["congestion_level"], 1.0
        )
        
        # 최종 시간 계산
        final_time = basic_result["total_time_minutes"] * traffic_multiplier
        
        return {
            **basic_result,
            "real_time_adjusted_minutes": round(final_time, 1),
            "traffic_conditions": traffic_conditions,
            "traffic_multiplier": traffic_multiplier,
            "api_provider": api_provider,
            "note": "실제 API 연동시 더 정확한 시간 제공 가능"
        }
    
    def get_route_alternatives(self, lat1: float, lon1: float, lat2: float, lon2: float,
                             current_time: Optional[datetime] = None) -> Dict:
        """경로 대안별 예상 소요시간"""
        
        if current_time is None:
            current_time = datetime.now()
        
        # 다양한 경로 옵션 시뮬레이션
        route_options = [
            {
                "name": "최단경로",
                "road_type": "일반도로",
                "description": "직선거리 기준 최단 경로"
            },
            {
                "name": "고속도로경로",
                "road_type": "고속도로",
                "description": "고속도로 우선 경로"
            },
            {
                "name": "회피경로",
                "road_type": "일반도로",
                "description": "혼잡구간 회피 경로"
            }
        ]
        
        route_results = {}
        
        for route in route_options:
            result = self.basic_estimator.estimate_car_travel_time(
                lat1, lon1, lat2, lon2, current_time, route["road_type"]
            )
            
            route_results[route["name"]] = {
                "time_minutes": result["total_time_minutes"],
                "distance_km": result["actual_distance_km"],
                "description": route["description"],
                "road_type": route["road_type"]
            }
        
        # 최적 경로 추천
        best_route = min(route_results.items(), key=lambda x: x[1]["time_minutes"])
        
        return {
            "route_options": route_results,
            "recommended_route": {
                "name": best_route[0],
                "time_minutes": best_route[1]["time_minutes"]
            },
            "calculation_time": current_time.strftime("%Y-%m-%d %H:%M:%S")
        }


# 사용 예시
if __name__ == "__main__":
    print("=== 거리 기반 예상 소요시간 계산 테스트 ===")
    
    # 기본 예상 소요시간 계산기
    estimator = TravelTimeEstimator()
    
    # 테스트 좌표 (건대입구역 → 능동공영 주차장)
    start_lat, start_lon = 37.5407, 127.0692  # 건대입구역
    end_lat, end_lon = 37.5507, 127.0745      # 능동공영 주차장
    
    print(f"\n📍 출발지: 건대입구역 ({start_lat}, {start_lon})")
    print(f"📍 도착지: 능동공영 주차장 ({end_lat}, {end_lon})")
    
    # 1. 자동차 예상 소요시간
    print("\n🚗 자동차 예상 소요시간:")
    car_result = estimator.estimate_car_travel_time(start_lat, start_lon, end_lat, end_lon)
    
    print(f"  직선거리: {car_result['straight_distance_km']}km")
    print(f"  실제거리: {car_result['actual_distance_km']}km")
    print(f"  평균속도: {car_result['adjusted_speed_kmh']}km/h")
    print(f"  이동시간: {car_result['travel_time_minutes']}분")
    print(f"  추가시간: {car_result['additional_time_minutes']}분 (신호등 등)")
    print(f"  주차시간: {car_result['parking_time_minutes']}분")
    print(f"  총 소요시간: {car_result['total_time_minutes']}분")
    print(f"  시간대: {car_result['time_period']}")
    print(f"  지역: {car_result['area_type']}")
    
    # 2. 대중교통 예상 소요시간
    print("\n🚇 지하철 예상 소요시간:")
    subway_result = estimator.estimate_public_transit_time(start_lat, start_lon, end_lat, end_lon)
    
    print(f"  거리: {subway_result['distance_km']}km")
    print(f"  이동시간: {subway_result['travel_time_minutes']}분")
    print(f"  대기시간: {subway_result['waiting_time_minutes']}분")
    print(f"  환승횟수: {subway_result['transfer_count']}회")
    print(f"  환승시간: {subway_result['transfer_time_minutes']}분")
    print(f"  총 소요시간: {subway_result['total_time_minutes']}분")
    
    # 3. 도보 예상 소요시간
    print("\n🚶 도보 예상 소요시간:")
    walking_result = estimator.estimate_walking_time(start_lat, start_lon, end_lat, end_lon)
    
    print(f"  거리: {walking_result['distance_km']}km")
    print(f"  도보속도: {walking_result['walking_speed_kmh']}km/h")
    print(f"  소요시간: {walking_result['walking_time_minutes']}분")
    
    # 4. 종합 비교
    print("\n📊 이동수단별 종합 비교:")
    comprehensive_result = estimator.get_comprehensive_travel_time(start_lat, start_lon, end_lat, end_lon)
    
    print(f"  직선거리: {comprehensive_result['distance_km']}km")
    print(f"  추천 이동수단: {comprehensive_result['recommended_transport']['type']}")
    print(f"  추천 소요시간: {comprehensive_result['recommended_transport']['time_minutes']}분")
    
    print("\n  상세 비교:")
    for transport, details in comprehensive_result['travel_options'].items():
        print(f"    {transport}: {details['total_time_minutes']}분")
    
    # 5. 교통상황 분석
    print("\n🚦 현재 교통상황:")
    traffic_conditions = estimator.get_traffic_conditions()
    
    print(f"  혼잡도: {traffic_conditions['congestion_level']}")
    print(f"  시간대: {traffic_conditions['time_period']}")
    print(f"  추천사항: {traffic_conditions['recommendation']}")
    
    # 6. 고급 예상 소요시간 (실시간 교통정보 반영)
    print("\n⚡ 실시간 교통정보 반영 예상 소요시간:")
    advanced_estimator = AdvancedTravelTimeEstimator()
    
    real_time_result = advanced_estimator.estimate_with_real_time_traffic(
        start_lat, start_lon, end_lat, end_lon
    )
    
    print(f"  기본 계산시간: {real_time_result['total_time_minutes']}분")
    print(f"  실시간 보정시간: {real_time_result['real_time_adjusted_minutes']}분")
    print(f"  교통상황: {real_time_result['traffic_conditions']['congestion_level']}")
    print(f"  보정계수: {real_time_result['traffic_multiplier']}")
    
    # 7. 경로 대안별 비교
    print("\n🗺️ 경로 대안별 예상 소요시간:")
    route_alternatives = advanced_estimator.get_route_alternatives(start_lat, start_lon, end_lat, end_lon)
    
    print(f"  추천 경로: {route_alternatives['recommended_route']['name']}")
    print(f"  추천 시간: {route_alternatives['recommended_route']['time_minutes']}분")
    
    print("\n  경로별 상세:")
    for route_name, details in route_alternatives['route_options'].items():
        print(f"    {route_name}: {details['time_minutes']}분 ({details['distance_km']}km)")
