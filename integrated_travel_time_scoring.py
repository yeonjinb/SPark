"""
거리 기반 예상 소요시간을 적용한 통합 가중치 점수 계산 시스템
"""

from typing import Dict, List, Optional, Any
from travel_time_estimation import TravelTimeEstimator, AdvancedTravelTimeEstimator
from discount_system import DiscountSystem, DiscountedPricingSystem
import math

class IntegratedTravelTimeScoring:
    """거리 기반 예상 소요시간을 적용한 통합 점수 계산 시스템"""
    
    def __init__(self):
        """초기화"""
        self.travel_estimator = TravelTimeEstimator()
        self.advanced_estimator = AdvancedTravelTimeEstimator()
        self.discount_system = DiscountSystem()
        self.discount_pricing = DiscountedPricingSystem()
        
        # 기본 가중치 설정 (예상 소요시간 반영)
        self.weights = {
            'price_sensitivity': 0.30,        # α - 가격 민감도 (30%)
            'time_sensitivity': 0.40,         # β - 시간 민감도 (40%) - 예상 소요시간 기반
            'convenience_sensitivity': 0.20,  # γ - 편의성 민감도 (20%)
            'discount_sensitivity': 0.10      # δ - 할인 혜택 민감도 (10%)
        }
        
        # 사용자 프로필별 가중치 조정
        self.user_profile_weights = {
            "시간우선형": {
                'price_sensitivity': 0.20,
                'time_sensitivity': 0.50,      # 시간 민감도 최대
                'convenience_sensitivity': 0.20,
                'discount_sensitivity': 0.10
            },
            "가격우선형": {
                'price_sensitivity': 0.45,
                'time_sensitivity': 0.25,
                'convenience_sensitivity': 0.20,
                'discount_sensitivity': 0.10
            },
            "편의성우선형": {
                'price_sensitivity': 0.25,
                'time_sensitivity': 0.25,
                'convenience_sensitivity': 0.40,
                'discount_sensitivity': 0.10
            },
            "할인추구형": {
                'price_sensitivity': 0.25,
                'time_sensitivity': 0.25,
                'convenience_sensitivity': 0.20,
                'discount_sensitivity': 0.30
            }
        }
    
    def set_user_profile(self, profile_type: str):
        """사용자 프로필에 따른 가중치 설정"""
        if profile_type in self.user_profile_weights:
            self.weights.update(self.user_profile_weights[profile_type])
    
    def calculate_integrated_score(self, lot: Dict, hours: int, user_info: Dict, 
                                 user_cards: List[str], current_location: Dict,
                                 transport_preference: str = "car") -> Dict:
        """거리 기반 예상 소요시간을 반영한 통합 점수 계산"""
        
        # 1. 할인 적용된 가격 정보 계산
        discount_info = self.discount_pricing.calculate_discounted_score(
            lot, hours, user_info, user_cards
        )
        
        # 2. 거리 기반 예상 소요시간 계산
        travel_time_info = self._calculate_enhanced_travel_time(
            current_location, lot['location'], transport_preference
        )
        
        # 3. 운전 난이도 점수 계산
        difficulty_score = self._calculate_driving_difficulty_score(lot)
        
        # 4. 각 요소별 점수 계산
        
        # 가격 점수 (할인 적용된 가격 기준)
        max_cost = 50000
        price_score = (max_cost / max(discount_info['final_price'], 1000))
        
        # 시간 점수 (거리 기반 예상 소요시간 사용)
        max_time = 120  # 최대 120분
        estimated_time = travel_time_info['total_time_minutes']
        time_score = (max_time / max(estimated_time, 1))
        
        # 편의성 점수 (운전 난이도의 역수)
        convenience_score = 1 - difficulty_score
        
        # 할인 혜택 점수
        discount_benefit_score = self._calculate_discount_benefit_score(discount_info)
        
        # 5. 최종 가중치 점수 계산
        final_score = (
            self.weights['price_sensitivity'] * price_score +
            self.weights['time_sensitivity'] * time_score +
            self.weights['convenience_sensitivity'] * convenience_score +
            self.weights['discount_sensitivity'] * discount_benefit_score
        )
        
        # 6. 보너스 점수 (추가 혜택)
        bonus_score = self._calculate_bonus_score(lot, user_info, discount_info, travel_time_info)
        
        # 최종 점수에 보너스 추가
        final_score += bonus_score
        
        # 0-1 범위로 정규화
        final_score = max(0.0, min(final_score, 1.0))
        
        return {
            'final_score': round(final_score, 4),
            'component_scores': {
                'price_score': round(price_score, 4),
                'time_score': round(time_score, 4),
                'convenience_score': round(convenience_score, 4),
                'discount_benefit_score': round(discount_benefit_score, 4),
                'bonus_score': round(bonus_score, 4)
            },
            'weighted_components': {
                'price_component': round(self.weights['price_sensitivity'] * price_score, 4),
                'time_component': round(self.weights['time_sensitivity'] * time_score, 4),
                'convenience_component': round(self.weights['convenience_sensitivity'] * convenience_score, 4),
                'discount_component': round(self.weights['discount_sensitivity'] * discount_benefit_score, 4)
            },
            'discount_info': discount_info,
            'travel_time_info': travel_time_info,
            'difficulty_score': round(difficulty_score, 4),
            'weights_used': self.weights.copy(),
            'transport_preference': transport_preference
        }
    
    def _calculate_enhanced_travel_time(self, current_location: Dict, lot_location: Dict, 
                                      transport_preference: str) -> Dict:
        """향상된 예상 소요시간 계산"""
        
        # 현재 위치와 주차장 위치
        current_lat, current_lon = current_location['latitude'], current_location['longitude']
        lot_lat, lot_lon = lot_location['latitude'], lot_location['longitude']
        
        # 기본 예상 소요시간 계산
        if transport_preference == "car":
            # 자동차 - 실시간 교통정보 반영
            travel_result = self.advanced_estimator.estimate_with_real_time_traffic(
                current_lat, current_lon, lot_lat, lot_lon
            )
            
            return {
                'transport_type': 'car',
                'total_time_minutes': travel_result['real_time_adjusted_minutes'],
                'base_time_minutes': travel_result['total_time_minutes'],
                'traffic_adjustment': travel_result['traffic_multiplier'],
                'distance_km': travel_result['actual_distance_km'],
                'estimated_speed_kmh': travel_result['adjusted_speed_kmh'],
                'traffic_conditions': travel_result['traffic_conditions'],
                'route_info': {
                    'straight_distance': travel_result['straight_distance_km'],
                    'actual_distance': travel_result['actual_distance_km'],
                    'time_period': travel_result['time_period'],
                    'area_type': travel_result['area_type']
                }
            }
        
        elif transport_preference == "public_transit":
            # 대중교통 - 지하철 우선
            subway_result = self.travel_estimator.estimate_public_transit_time(
                current_lat, current_lon, lot_lat, lot_lon, transit_type="지하철"
            )
            
            return {
                'transport_type': 'public_transit',
                'total_time_minutes': subway_result['total_time_minutes'],
                'distance_km': subway_result['distance_km'],
                'waiting_time_minutes': subway_result['waiting_time_minutes'],
                'transfer_count': subway_result['transfer_count'],
                'route_info': {
                    'transit_type': '지하철',
                    'average_speed': 35
                }
            }
        
        elif transport_preference == "walking":
            # 도보
            walking_result = self.travel_estimator.estimate_walking_time(
                current_lat, current_lon, lot_lat, lot_lon
            )
            
            return {
                'transport_type': 'walking',
                'total_time_minutes': walking_result['walking_time_minutes'],
                'distance_km': walking_result['distance_km'],
                'walking_speed_kmh': walking_result['walking_speed_kmh'],
                'route_info': {
                    'transport_type': 'walking'
                }
            }
        
        else:
            # 종합 비교 (모든 이동수단)
            comprehensive_result = self.travel_estimator.get_comprehensive_travel_time(
                current_lat, current_lon, lot_lat, lot_lon
            )
            
            return {
                'transport_type': 'comprehensive',
                'total_time_minutes': comprehensive_result['recommended_transport']['time_minutes'],
                'recommended_transport': comprehensive_result['recommended_transport']['type'],
                'all_options': comprehensive_result['travel_options'],
                'route_info': {
                    'distance_km': comprehensive_result['distance_km']
                }
            }
    
    def _calculate_driving_difficulty_score(self, lot: Dict) -> float:
        """운전 난이도 점수 계산 (0-1, 낮을수록 쉬움)"""
        score = 0.0
        
        # 주차장 타입별 난이도
        parking_type_scores = {
            "자주식": 0.0,
            "기계식": 0.3,
            "발렛파킹": 0.1
        }
        
        difficulty = lot.get('difficulty', {})
        parking_type = difficulty.get('type', '자주식')
        score += parking_type_scores.get(parking_type, 0.5)
        
        # 높이 제한 점수
        height_limit = lot.get('restrictions', {}).get('height_limit_m', 2.5)
        if height_limit < 1.8:
            score += 0.2
        elif height_limit < 2.0:
            score += 0.1
        
        # 진입로 폭 점수
        access_width = difficulty.get('entrance_width_m', 4.0)
        if access_width < 3.0:
            score += 0.2
        elif access_width < 4.0:
            score += 0.1
        
        # 회전 반경 점수
        turning_radius = difficulty.get('turning_radius_m', 8.0)
        if turning_radius < 6.0:
            score += 0.15
        elif turning_radius < 8.0:
            score += 0.05
        
        # 경사각 점수
        slope_grade = difficulty.get('slope_grade', 0)
        score += min(slope_grade * 0.02, 0.2)
        
        # 장애물 점수
        obstacles = difficulty.get('obstacles', False)
        if obstacles:
            score += 0.1
        
        # 조명 점수
        lighting = difficulty.get('lighting_level', '보통')
        lighting_scores = {"우수": 0.0, "양호": 0.05, "보통": 0.1, "나쁨": 0.2}
        score += lighting_scores.get(lighting, 0.1)
        
        return min(score, 1.0)
    
    def _calculate_discount_benefit_score(self, discount_info: Dict) -> float:
        """할인 혜택 점수 계산"""
        
        # 기본 할인 혜택 점수
        total_discount_rate = discount_info['total_discount_rate']
        
        # 할인율에 따른 점수 (할인율이 높을수록 높은 점수)
        if total_discount_rate >= 0.5:  # 50% 이상 할인
            base_score = 0.9
        elif total_discount_rate >= 0.3:  # 30% 이상 할인
            base_score = 0.7
        elif total_discount_rate >= 0.1:  # 10% 이상 할인
            base_score = 0.5
        else:  # 할인 없음
            base_score = 0.1
        
        # 절약 금액에 따른 추가 점수
        savings_amount = discount_info['savings_amount']
        if savings_amount >= 10000:  # 1만원 이상 절약
            savings_bonus = 0.1
        elif savings_amount >= 5000:  # 5천원 이상 절약
            savings_bonus = 0.05
        else:
            savings_bonus = 0.0
        
        return min(base_score + savings_bonus, 1.0)
    
    def _calculate_bonus_score(self, lot: Dict, user_info: Dict, discount_info: Dict, 
                             travel_time_info: Dict) -> float:
        """추가 보너스 점수 계산"""
        bonus = 0.0
        
        # 24시간 운영 보너스
        if lot.get('operating_hours', {}).get('24_7', False):
            bonus += 0.05
        
        # 전기차 충전소 보너스 (전기차 사용자만)
        if user_info.get('vehicle_type') == '전기차' and lot.get('amenities', {}).get('ev_charging', False):
            bonus += 0.08
        
        # 발렛 파킹 보너스
        if lot.get('amenities', {}).get('valet', False):
            bonus += 0.06
        
        # CCTV 보안 보너스
        if lot.get('amenities', {}).get('cctv', False):
            bonus += 0.03
        
        # 조명 시설 보너스
        if lot.get('amenities', {}).get('lighting', False):
            bonus += 0.02
        
        # 높은 할인율 보너스
        if discount_info['total_discount_rate'] >= 0.4:
            bonus += 0.05
        
        # 공영 주차장 보너스 (신뢰성)
        if '공영' in lot.get('name', ''):
            bonus += 0.03
        
        # 빠른 접근성 보너스 (예상 소요시간이 짧을 때)
        if travel_time_info['total_time_minutes'] <= 10:
            bonus += 0.05
        elif travel_time_info['total_time_minutes'] <= 15:
            bonus += 0.03
        
        # 교통상황이 좋을 때 보너스
        if travel_time_info.get('traffic_conditions', {}).get('congestion_level') == '원활':
            bonus += 0.02
        
        return min(bonus, 0.2)  # 최대 0.2점 보너스
    
    def rank_parking_lots_with_travel_time(self, parking_lots: List[Dict], hours: int, 
                                         user_info: Dict, user_cards: List[str],
                                         current_location: Dict,
                                         transport_preference: str = "car") -> List[Dict]:
        """거리 기반 예상 소요시간을 반영한 주차장 랭킹"""
        
        ranked_lots = []
        
        for lot in parking_lots:
            # 통합 점수 계산
            score_result = self.calculate_integrated_score(
                lot, hours, user_info, user_cards, current_location, transport_preference
            )
            
            # 랭킹 정보 추가
            lot_with_score = lot.copy()
            lot_with_score.update({
                'integrated_score': score_result['final_score'],
                'score_breakdown': score_result['component_scores'],
                'discount_info': score_result['discount_info'],
                'travel_time_info': score_result['travel_time_info'],
                'difficulty_score': score_result['difficulty_score'],
                'transport_preference': transport_preference,
                'ranking_factors': {
                    'original_price': score_result['discount_info']['original_price'],
                    'final_price': score_result['discount_info']['final_price'],
                    'total_savings': score_result['discount_info']['savings_amount'],
                    'discount_rate': score_result['discount_info']['total_discount_rate'],
                    'estimated_travel_time': score_result['travel_time_info']['total_time_minutes'],
                    'travel_distance': score_result['travel_time_info'].get('distance_km', 0),
                    'applied_cards': score_result['discount_info']['card_discount']['applied_cards']
                }
            })
            
            ranked_lots.append(lot_with_score)
        
        # 점수순으로 정렬 (높을수록 좋음)
        ranked_lots.sort(key=lambda x: x['integrated_score'], reverse=True)
        
        return ranked_lots
    
    def get_transport_recommendation(self, parking_lots: List[Dict], current_location: Dict) -> Dict:
        """이동수단별 추천 분석"""
        
        transport_analysis = {
            'car': [],
            'public_transit': [],
            'walking': []
        }
        
        for lot in parking_lots:
            lot_lat, lot_lon = lot['location']['latitude'], lot['location']['longitude']
            current_lat, current_lon = current_location['latitude'], current_location['longitude']
            
            # 각 이동수단별 예상 소요시간 계산
            car_time = self.advanced_estimator.estimate_with_real_time_traffic(
                current_lat, current_lon, lot_lat, lot_lon
            )['real_time_adjusted_minutes']
            
            subway_time = self.travel_estimator.estimate_public_transit_time(
                current_lat, current_lon, lot_lat, lot_lon, transit_type="지하철"
            )['total_time_minutes']
            
            walking_time = self.travel_estimator.estimate_walking_time(
                current_lat, current_lon, lot_lat, lot_lon
            )['walking_time_minutes']
            
            transport_analysis['car'].append({
                'lot_name': lot['name'],
                'time_minutes': car_time
            })
            
            transport_analysis['public_transit'].append({
                'lot_name': lot['name'],
                'time_minutes': subway_time
            })
            
            transport_analysis['walking'].append({
                'lot_name': lot['name'],
                'time_minutes': walking_time
            })
        
        # 각 이동수단별 최적 주차장 찾기
        best_transports = {}
        for transport, lots in transport_analysis.items():
            best_lot = min(lots, key=lambda x: x['time_minutes'])
            best_transports[transport] = best_lot
        
        return {
            'transport_analysis': transport_analysis,
            'best_transports': best_transports,
            'recommendation': min(best_transports.items(), key=lambda x: x[1]['time_minutes'])
        }


# 사용 예시
if __name__ == "__main__":
    print("=== 거리 기반 예상 소요시간을 적용한 통합 점수 계산 시스템 테스트 ===")
    
    # 통합 점수 계산 시스템
    integrated_scoring = IntegratedTravelTimeScoring()
    
    # 사용자 정보
    user_info = {
        "children_count": 4,  # 다둥이 가정
        "age": 35,
        "annual_income": 50000000,
        "vehicle_type": "승용차"
    }
    
    # 사용자 보유 카드
    user_cards = ["다둥이_복지_카드"]
    
    # 현재 위치 (건대입구역)
    current_location = {
        "latitude": 37.5407,
        "longitude": 127.0692,
        "address": "건대입구역"
    }
    
    # 테스트용 주차장 데이터
    test_lots = [
        {
            "id": 1,
            "name": "능동공영 주차장",
            "location": {"latitude": 37.5507, "longitude": 127.0745},
            "pricing": {"hourly_rate": 3600},
            "operating_hours": {"24_7": True},
            "amenities": {"ev_charging": True, "cctv": True, "lighting": True},
            "difficulty": {"type": "자주식", "entrance_width_m": 4.0, "turning_radius_m": 8.0},
            "restrictions": {"height_limit_m": 2.1}
        },
        {
            "id": 2,
            "name": "아이파킹 동도센트리움캠퍼스파크 주차장",
            "location": {"latitude": 37.5507, "longitude": 127.0745},
            "pricing": {"hourly_rate": 4500},
            "operating_hours": {"24_7": True},
            "amenities": {"ev_charging": False, "cctv": False, "lighting": False},
            "difficulty": {"type": "자주식", "entrance_width_m": 3.5, "turning_radius_m": 7.0},
            "restrictions": {"height_limit_m": 1.55}
        }
    ]
    
    # 4시간 주차 시나리오
    hours = 4
    
    print(f"\n📍 출발지: {current_location['address']}")
    print(f"📍 목적지: 주차장들")
    print(f"🕐 주차 시간: {hours}시간")
    print(f"🚗 이동수단: 자동차")
    
    # 이동수단별 추천 분석
    print("\n🚗 이동수단별 추천 분석:")
    transport_recommendation = integrated_scoring.get_transport_recommendation(
        test_lots, current_location
    )
    
    print(f"  자동차 최적: {transport_recommendation['best_transports']['car']['lot_name']} "
          f"({transport_recommendation['best_transports']['car']['time_minutes']}분)")
    print(f"  대중교통 최적: {transport_recommendation['best_transports']['public_transit']['lot_name']} "
          f"({transport_recommendation['best_transports']['public_transit']['time_minutes']}분)")
    print(f"  도보 최적: {transport_recommendation['best_transports']['walking']['lot_name']} "
          f"({transport_recommendation['best_transports']['walking']['time_minutes']}분)")
    
    # 통합 점수 계산 및 랭킹
    print(f"\n🏆 거리 기반 예상 소요시간을 반영한 통합 랭킹:")
    ranked_lots = integrated_scoring.rank_parking_lots_with_travel_time(
        test_lots, hours, user_info, user_cards, current_location, "car"
    )
    
    for i, lot in enumerate(ranked_lots, 1):
        print(f"\n{i}위: {lot['name']}")
        print(f"   통합 점수: {lot['integrated_score']:.4f}")
        print(f"   가격: {lot['ranking_factors']['final_price']:,}원 "
              f"(할인율: {lot['ranking_factors']['discount_rate']*100:.1f}%)")
        print(f"   예상 소요시간: {lot['ranking_factors']['estimated_travel_time']:.1f}분")
        print(f"   거리: {lot['ranking_factors']['travel_distance']:.2f}km")
        print(f"   절약: {lot['ranking_factors']['total_savings']:,}원")
        print(f"   적용카드: {lot['ranking_factors']['applied_cards']}")
        
        # 상세 점수 분석
        print(f"   상세 점수:")
        for component, score in lot['score_breakdown'].items():
            print(f"     {component}: {score:.4f}")
    
    # 시간우선형 사용자 프로필 테스트
    print(f"\n⏰ 시간우선형 사용자 프로필 테스트:")
    integrated_scoring.set_user_profile("시간우선형")
    
    time_priority_ranking = integrated_scoring.rank_parking_lots_with_travel_time(
        test_lots, hours, user_info, user_cards, current_location, "car"
    )
    
    print(f"  시간우선형 가중치: {integrated_scoring.weights}")
    print(f"  1위: {time_priority_ranking[0]['name']} "
          f"(점수: {time_priority_ranking[0]['integrated_score']:.4f}, "
          f"시간: {time_priority_ranking[0]['ranking_factors']['estimated_travel_time']:.1f}분)")
    
    # 이동수단별 비교
    print(f"\n🚌 이동수단별 점수 비교 (능동공영 주차장):")
    lot = test_lots[0]  # 능동공영 주차장
    
    for transport in ["car", "public_transit", "walking"]:
        score_result = integrated_scoring.calculate_integrated_score(
            lot, hours, user_info, user_cards, current_location, transport
        )
        print(f"  {transport}: 점수 {score_result['final_score']:.4f}, "
              f"시간 {score_result['travel_time_info']['total_time_minutes']:.1f}분")









