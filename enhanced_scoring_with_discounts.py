"""
할인율이 적용된 향상된 가중치 점수 계산 시스템
기존 공식: score = α*(1/총요금) + β*(1/예상 소요시간) + γ*(운전 난이도)
수정 공식: score = α*(1/할인적용_총요금) + β*(1/예상 소요시간) + γ*(운전 난이도) + δ*(할인혜택점수)
"""

from typing import Dict, List, Optional, Any
from discount_system import DiscountSystem, DiscountedPricingSystem
import math

class EnhancedScoringWithDiscounts:
    """할인율이 적용된 향상된 점수 계산 시스템"""
    
    def __init__(self):
        """초기화"""
        self.discount_system = DiscountSystem()
        self.discount_pricing = DiscountedPricingSystem()
        
        # 기본 가중치 설정
        self.weights = {
            'price_sensitivity': 0.35,        # α - 가격 민감도 (35%)
            'time_sensitivity': 0.35,         # β - 시간 민감도 (35%)  
            'convenience_sensitivity': 0.20,  # γ - 편의성 민감도 (20%)
            'discount_sensitivity': 0.10      # δ - 할인 혜택 민감도 (10%)
        }
        
        # 사용자 프로필별 가중치 조정
        self.user_profile_weights = {
            "가격민감형": {
                'price_sensitivity': 0.50,
                'time_sensitivity': 0.25,
                'convenience_sensitivity': 0.15,
                'discount_sensitivity': 0.10
            },
            "시간민감형": {
                'price_sensitivity': 0.20,
                'time_sensitivity': 0.50,
                'convenience_sensitivity': 0.20,
                'discount_sensitivity': 0.10
            },
            "편의성민감형": {
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
    
    def calculate_enhanced_score(self, lot: Dict, hours: int, user_info: Dict, 
                               user_cards: List[str]) -> Dict:
        """할인율을 반영한 향상된 점수 계산"""
        
        # 1. 할인 적용된 가격 정보 계산
        discount_info = self.discount_pricing.calculate_discounted_score(
            lot, hours, user_info, user_cards
        )
        
        # 2. 예상 소요시간 계산
        travel_time = self._calculate_travel_time(lot)
        
        # 3. 운전 난이도 점수 계산
        difficulty_score = self._calculate_driving_difficulty_score(lot)
        
        # 4. 각 요소별 점수 계산
        
        # 가격 점수 (할인 적용된 가격 기준)
        max_cost = 50000
        price_score = (max_cost / max(discount_info['final_price'], 1000))
        
        # 시간 점수
        max_time = 120
        time_score = (max_time / max(travel_time, 1))
        
        # 편의성 점수 (운전 난이도의 역수)
        convenience_score = 1 - difficulty_score
        
        # 할인 혜택 점수 (새로 추가)
        discount_benefit_score = self._calculate_discount_benefit_score(discount_info)
        
        # 5. 최종 가중치 점수 계산
        final_score = (
            self.weights['price_sensitivity'] * price_score +
            self.weights['time_sensitivity'] * time_score +
            self.weights['convenience_sensitivity'] * convenience_score +
            self.weights['discount_sensitivity'] * discount_benefit_score
        )
        
        # 6. 보너스 점수 (추가 혜택)
        bonus_score = self._calculate_bonus_score(lot, user_info, discount_info)
        
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
            'travel_time': travel_time,
            'difficulty_score': round(difficulty_score, 4),
            'weights_used': self.weights.copy()
        }
    
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
    
    def _calculate_bonus_score(self, lot: Dict, user_info: Dict, discount_info: Dict) -> float:
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
        
        return min(bonus, 0.2)  # 최대 0.2점 보너스
    
    def _calculate_travel_time(self, lot: Dict) -> float:
        """주차장까지 예상 소요시간 계산 (분)"""
        # 실제로는 지도 API를 사용해야 하지만, 여기서는 거리 기반 추정
        
        # 현재 위치 (건대입구역)
        current_location = {"latitude": 37.5407, "longitude": 127.0692}
        
        # 간단한 거리 계산 (실제로는 지도 API 사용)
        lat_diff = abs(lot['location']['latitude'] - current_location['latitude'])
        lng_diff = abs(lot['location']['longitude'] - current_location['longitude'])
        distance_km = (lat_diff + lng_diff) * 111  # 대략적인 km 변환
        
        # 도시 평균 속도 30km/h 가정
        travel_time_minutes = (distance_km / 30) * 60
        
        # 교통상황 보정 (기본 20% 추가)
        travel_time_minutes *= 1.2
        
        return round(travel_time_minutes, 1)
    
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
    
    def rank_parking_lots_with_discounts(self, parking_lots: List[Dict], hours: int, 
                                       user_info: Dict, user_cards: List[str]) -> List[Dict]:
        """할인율을 반영한 주차장 랭킹"""
        
        ranked_lots = []
        
        for lot in parking_lots:
            # 향상된 점수 계산
            score_result = self.calculate_enhanced_score(lot, hours, user_info, user_cards)
            
            # 랭킹 정보 추가
            lot_with_score = lot.copy()
            lot_with_score.update({
                'enhanced_score': score_result['final_score'],
                'score_breakdown': score_result['component_scores'],
                'discount_info': score_result['discount_info'],
                'travel_time': score_result['travel_time'],
                'difficulty_score': score_result['difficulty_score'],
                'ranking_factors': {
                    'original_price': score_result['discount_info']['original_price'],
                    'final_price': score_result['discount_info']['final_price'],
                    'total_savings': score_result['discount_info']['savings_amount'],
                    'discount_rate': score_result['discount_info']['total_discount_rate'],
                    'applied_cards': score_result['discount_info']['card_discount']['applied_cards']
                }
            })
            
            ranked_lots.append(lot_with_score)
        
        # 점수순으로 정렬 (높을수록 좋음)
        ranked_lots.sort(key=lambda x: x['enhanced_score'], reverse=True)
        
        return ranked_lots
    
    def get_discount_impact_analysis(self, parking_lots: List[Dict], hours: int, 
                                   user_info: Dict, user_cards: List[str]) -> Dict:
        """할인율이 랭킹에 미치는 영향 분석"""
        
        # 할인 적용 전후 점수 비교
        comparison_results = []
        
        for lot in parking_lots:
            # 할인 적용된 점수
            with_discount = self.calculate_enhanced_score(lot, hours, user_info, user_cards)
            
            # 할인 적용 안된 점수 (빈 카드 리스트로 계산)
            without_discount = self.calculate_enhanced_score(lot, hours, user_info, [])
            
            comparison_results.append({
                'lot_name': lot['name'],
                'score_with_discount': with_discount['final_score'],
                'score_without_discount': without_discount['final_score'],
                'score_difference': with_discount['final_score'] - without_discount['final_score'],
                'rank_improvement': 0,  # 나중에 계산
                'savings_amount': with_discount['discount_info']['savings_amount'],
                'discount_rate': with_discount['discount_info']['total_discount_rate']
            })
        
        # 할인 적용 전후 랭킹 계산
        lots_with_discount = [(i, lot['score_with_discount']) for i, lot in enumerate(comparison_results)]
        lots_without_discount = [(i, lot['score_without_discount']) for i, lot in enumerate(comparison_results)]
        
        lots_with_discount.sort(key=lambda x: x[1], reverse=True)
        lots_without_discount.sort(key=lambda x: x[1], reverse=True)
        
        # 랭킹 개선도 계산
        for i, (original_idx, _) in enumerate(lots_with_discount):
            original_rank = next(j for j, (idx, _) in enumerate(lots_without_discount) if idx == original_idx)
            comparison_results[original_idx]['rank_improvement'] = original_rank - i
        
        return {
            'comparison_results': comparison_results,
            'total_savings': sum(lot['savings_amount'] for lot in comparison_results),
            'average_discount_rate': sum(lot['discount_rate'] for lot in comparison_results) / len(comparison_results),
            'lots_with_discount_benefit': len([lot for lot in comparison_results if lot['score_difference'] > 0])
        }


# 사용 예시
if __name__ == "__main__":
    # 향상된 점수 계산 시스템 테스트
    enhanced_scoring = EnhancedScoringWithDiscounts()
    
    # 사용자 정보
    user_info = {
        "children_count": 4,  # 다둥이 가정
        "age": 35,
        "annual_income": 50000000,
        "vehicle_type": "승용차"
    }
    
    # 사용자 보유 카드
    user_cards = ["다둥이_복지_카드"]
    
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
    
    print("=== 할인율이 적용된 향상된 점수 계산 시스템 테스트 ===")
    
    # 4시간 주차 시나리오
    hours = 4
    
    # 각 주차장별 점수 계산
    for lot in test_lots:
        print(f"\n📍 {lot['name']}")
        print("-" * 50)
        
        score_result = enhanced_scoring.calculate_enhanced_score(
            lot, hours, user_info, user_cards
        )
        
        print(f"최종 점수: {score_result['final_score']:.4f}")
        print(f"원래 가격: {score_result['discount_info']['original_price']:,}원")
        print(f"할인 적용 후: {score_result['discount_info']['final_price']:,}원")
        print(f"절약 금액: {score_result['discount_info']['savings_amount']:,}원")
        print(f"할인율: {score_result['discount_info']['total_discount_rate']*100:.1f}%")
        
        print("\n컴포넌트 점수:")
        for component, score in score_result['component_scores'].items():
            print(f"  {component}: {score:.4f}")
        
        print("\n가중치 적용 점수:")
        for component, score in score_result['weighted_components'].items():
            print(f"  {component}: {score:.4f}")
    
    # 랭킹 결과
    print("\n" + "="*60)
    print("🏆 할인율 반영 랭킹 결과")
    print("="*60)
    
    ranked_lots = enhanced_scoring.rank_parking_lots_with_discounts(
        test_lots, hours, user_info, user_cards
    )
    
    for i, lot in enumerate(ranked_lots, 1):
        print(f"{i}위: {lot['name']}")
        print(f"   점수: {lot['enhanced_score']:.4f}")
        print(f"   가격: {lot['ranking_factors']['final_price']:,}원 "
              f"(할인율: {lot['ranking_factors']['discount_rate']*100:.1f}%)")
        print(f"   절약: {lot['ranking_factors']['total_savings']:,}원")
        print(f"   적용카드: {lot['ranking_factors']['applied_cards']}")
        print()
    
    # 할인 영향 분석
    print("📊 할인율이 랭킹에 미치는 영향 분석")
    print("-" * 50)
    
    impact_analysis = enhanced_scoring.get_discount_impact_analysis(
        test_lots, hours, user_info, user_cards
    )
    
    print(f"총 절약 금액: {impact_analysis['total_savings']:,}원")
    print(f"평균 할인율: {impact_analysis['average_discount_rate']*100:.1f}%")
    print(f"할인 혜택을 받는 주차장: {impact_analysis['lots_with_discount_benefit']}개")
    
    for result in impact_analysis['comparison_results']:
        print(f"\n{result['lot_name']}:")
        print(f"  할인 적용 전 점수: {result['score_without_discount']:.4f}")
        print(f"  할인 적용 후 점수: {result['score_with_discount']:.4f}")
        print(f"  점수 향상: {result['score_difference']:.4f}")
        print(f"  랭킹 개선: {result['rank_improvement']}단계 상승")
        print(f"  절약 금액: {result['savings_amount']:,}원")


