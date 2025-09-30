"""
할인율 시스템 - 다둥이 복지 카드 및 기타 할인 카드 지원
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, time
import json

class DiscountSystem:
    """할인 시스템 관리 클래스"""
    
    def __init__(self):
        """할인 시스템 초기화"""
        self.discount_cards = {
            # 다둥이 복지 카드
            "다둥이_복지_카드": {
                "name": "다둥이 복지 카드",
                "discount_rate": 0.50,  # 50% 할인
                "conditions": {
                    "min_children": 3,  # 3명 이상 자녀
                    "max_children": None,  # 제한 없음
                    "age_requirement": None,  # 나이 제한 없음
                    "income_limit": None,  # 소득 제한 없음
                    "area_restriction": None  # 지역 제한 없음
                },
                "description": "3명 이상 자녀가 있는 가정을 위한 주차 할인"
            },
            
            # 장애인 복지 카드
            "장애인_복지_카드": {
                "name": "장애인 복지 카드",
                "discount_rate": 0.30,  # 30% 할인
                "conditions": {
                    "disability_level": [1, 2, 3, 4, 5, 6],  # 1-6급 장애
                    "guardian_benefit": True,  # 보호자 혜택 포함
                },
                "description": "장애인 및 보호자를 위한 주차 할인"
            },
            
            # 경로우대 카드
            "경로우대_카드": {
                "name": "경로우대 카드",
                "discount_rate": 0.20,  # 20% 할인
                "conditions": {
                    "min_age": 65,  # 65세 이상
                    "max_age": None,
                },
                "description": "65세 이상 어르신을 위한 주차 할인"
            },
            
            # 국가유공자 카드
            "국가유공자_카드": {
                "name": "국가유공자 카드",
                "discount_rate": 0.40,  # 40% 할인
                "conditions": {
                    "merit_type": ["독립유공자", "애국지사", "참전유공자", "보훈대상자"],
                    "family_benefit": True,  # 가족 혜택 포함
                },
                "description": "국가유공자 및 가족을 위한 주차 할인"
            },
            
            # 저소득층 카드
            "저소득층_카드": {
                "name": "저소득층 복지 카드",
                "discount_rate": 0.60,  # 60% 할인
                "conditions": {
                    "income_level": "기초생활수급자",
                    "housing_type": ["임대주택", "공공임대", "영구임대"],
                },
                "description": "기초생활수급자를 위한 주차 할인"
            },
            
            # 청년 카드
            "청년_카드": {
                "name": "청년 복지 카드",
                "discount_rate": 0.25,  # 25% 할인
                "conditions": {
                    "min_age": 19,
                    "max_age": 34,
                    "income_limit": 80000000,  # 연소득 8천만원 이하
                },
                "description": "19-34세 청년을 위한 주차 할인"
            },
            
            # 신혼부부 카드
            "신혼부부_카드": {
                "name": "신혼부부 복지 카드",
                "discount_rate": 0.30,  # 30% 할인
                "conditions": {
                    "marriage_period": 7,  # 결혼 7년 이내
                    "age_limit": 39,  # 39세 이하
                    "income_limit": 70000000,  # 연소득 7천만원 이하
                },
                "description": "신혼부부를 위한 주차 할인"
            }
        }
        
        # 주차장별 할인 정책
        self.parking_lot_discount_policies = {
            "공영_주차장": {
                "all_discount_cards": True,  # 모든 할인 카드 적용 가능
                "max_discount_rate": 0.70,  # 최대 70% 할인
                "additional_benefits": ["주말_무료", "야간_할인"]
            },
            "민영_주차장": {
                "selected_cards_only": ["다둥이_복지_카드", "장애인_복지_카드"],  # 선택적 적용
                "max_discount_rate": 0.50,  # 최대 50% 할인
                "additional_benefits": []
            },
            "대형마트_주차장": {
                "shopping_discount": True,  # 쇼핑 금액에 따른 할인
                "base_discount": 0.20,  # 기본 20% 할인
                "max_discount_rate": 0.40,  # 최대 40% 할인
            }
        }
    
    def check_eligibility(self, user_info: Dict, card_type: str) -> bool:
        """사용자 자격 확인"""
        if card_type not in self.discount_cards:
            return False
        
        card_info = self.discount_cards[card_type]
        conditions = card_info["conditions"]
        
        # 다둥이 복지 카드 자격 확인
        if card_type == "다둥이_복지_카드":
            children_count = user_info.get("children_count", 0)
            min_children = conditions["min_children"]
            return children_count >= min_children
        
        # 장애인 복지 카드 자격 확인
        elif card_type == "장애인_복지_카드":
            disability_level = user_info.get("disability_level")
            return disability_level in conditions["disability_level"]
        
        # 경로우대 카드 자격 확인
        elif card_type == "경로우대_카드":
            age = user_info.get("age", 0)
            return age >= conditions["min_age"]
        
        # 국가유공자 카드 자격 확인
        elif card_type == "국가유공자_카드":
            merit_type = user_info.get("merit_type")
            return merit_type in conditions["merit_type"]
        
        # 저소득층 카드 자격 확인
        elif card_type == "저소득층_카드":
            income_level = user_info.get("income_level")
            return income_level == conditions["income_level"]
        
        # 청년 카드 자격 확인
        elif card_type == "청년_카드":
            age = user_info.get("age", 0)
            income = user_info.get("annual_income", 0)
            return (conditions["min_age"] <= age <= conditions["max_age"] and 
                   income <= conditions["income_limit"])
        
        # 신혼부부 카드 자격 확인
        elif card_type == "신혼부부_카드":
            marriage_years = user_info.get("marriage_years", 0)
            age = user_info.get("age", 0)
            income = user_info.get("annual_income", 0)
            return (marriage_years <= conditions["marriage_period"] and
                   age <= conditions["age_limit"] and
                   income <= conditions["income_limit"])
        
        return False
    
    def calculate_discounted_price(self, original_price: float, user_cards: List[str], 
                                 parking_lot_type: str = "공영_주차장") -> Dict:
        """할인 적용된 가격 계산"""
        
        # 사용 가능한 할인 카드 필터링
        applicable_cards = []
        for card in user_cards:
            if card in self.discount_cards:
                card_info = self.discount_cards[card]
                parking_policy = self.parking_lot_discount_policies.get(parking_lot_type, {})
                
                # 주차장 타입별 할인 카드 적용 가능 여부 확인
                if (parking_policy.get("all_discount_cards", False) or 
                    card in parking_policy.get("selected_cards_only", [])):
                    applicable_cards.append(card)
        
        if not applicable_cards:
            return {
                "original_price": original_price,
                "discounted_price": original_price,
                "discount_rate": 0.0,
                "discount_amount": 0.0,
                "applied_cards": [],
                "final_price": original_price
            }
        
        # 최대 할인율 찾기
        max_discount_rate = 0.0
        best_card = None
        
        for card in applicable_cards:
            card_discount_rate = self.discount_cards[card]["discount_rate"]
            if card_discount_rate > max_discount_rate:
                max_discount_rate = card_discount_rate
                best_card = card
        
        # 주차장별 최대 할인율 제한
        parking_policy = self.parking_lot_discount_policies.get(parking_lot_type, {})
        max_allowed_discount = parking_policy.get("max_discount_rate", 1.0)
        
        if max_discount_rate > max_allowed_discount:
            max_discount_rate = max_allowed_discount
        
        # 할인 적용
        discount_amount = original_price * max_discount_rate
        final_price = original_price - discount_amount
        
        return {
            "original_price": original_price,
            "discounted_price": final_price,
            "discount_rate": max_discount_rate,
            "discount_amount": discount_amount,
            "applied_cards": [best_card] if best_card else [],
            "final_price": final_price,
            "savings": discount_amount
        }
    
    def get_user_discount_info(self, user_info: Dict) -> Dict:
        """사용자별 적용 가능한 할인 정보 조회"""
        applicable_discounts = {}
        
        for card_type, card_info in self.discount_cards.items():
            if self.check_eligibility(user_info, card_type):
                applicable_discounts[card_type] = {
                    "name": card_info["name"],
                    "discount_rate": card_info["discount_rate"],
                    "description": card_info["description"]
                }
        
        return applicable_discounts
    
    def calculate_time_based_discount(self, base_price: float, parking_hours: int, 
                                    parking_lot_type: str) -> Dict:
        """시간대별 추가 할인 계산"""
        time_discounts = {}
        
        # 공영 주차장 시간대별 할인
        if parking_lot_type == "공영_주차장":
            if parking_hours >= 8:  # 장시간 주차
                time_discounts["장시간_할인"] = 0.10  # 10% 추가 할인
            elif parking_hours >= 4:  # 중시간 주차
                time_discounts["중시간_할인"] = 0.05  # 5% 추가 할인
        
        # 야간 할인 (22시~06시)
        current_hour = datetime.now().hour
        if current_hour >= 22 or current_hour <= 6:
            time_discounts["야간_할인"] = 0.15  # 15% 추가 할인
        
        # 주말 할인
        if datetime.now().weekday() >= 5:  # 토요일, 일요일
            time_discounts["주말_할인"] = 0.20  # 20% 추가 할인
        
        # 최대 시간 할인율 적용 (중복 할인 제한)
        max_time_discount = max(time_discounts.values()) if time_discounts else 0.0
        
        return {
            "time_discounts": time_discounts,
            "max_time_discount_rate": max_time_discount,
            "time_discount_amount": base_price * max_time_discount
        }


class DiscountedPricingSystem:
    """할인율이 적용된 가격 점수 계산 시스템"""
    
    def __init__(self):
        self.discount_system = DiscountSystem()
    
    def calculate_discounted_score(self, lot: Dict, hours: int, user_info: Dict, 
                                 user_cards: List[str]) -> Dict:
        """할인율을 반영한 점수 계산"""
        
        # 1. 기본 가격 계산
        hourly_rate = lot['pricing']['hourly_rate']
        original_total_cost = hourly_rate * hours
        
        # 2. 주차장 타입 확인
        parking_lot_type = self._get_parking_lot_type(lot)
        
        # 3. 카드 할인 적용
        card_discount_result = self.discount_system.calculate_discounted_price(
            original_total_cost, user_cards, parking_lot_type
        )
        
        # 4. 시간대별 추가 할인 적용
        time_discount_result = self.discount_system.calculate_time_based_discount(
            card_discount_result["final_price"], hours, parking_lot_type
        )
        
        # 5. 최종 할인 가격 계산
        final_discounted_price = (card_discount_result["final_price"] - 
                                time_discount_result["time_discount_amount"])
        
        # 6. 할인율 반영된 점수 계산
        # 기존 공식: score = α*(1/총요금) + β*(1/예상 소요시간) + γ*(운전 난이도)
        # 수정된 공식: score = α*(1/할인적용_총요금) + β*(1/예상 소요시간) + γ*(운전 난이도)
        
        # 할인 적용된 비용 점수 (낮을수록 좋음) - 역수 사용
        max_cost = 50000  # 최대 비용 기준
        discounted_cost_score = (max_cost / max(final_discounted_price, 1000))
        
        # 할인 혜택 점수 (추가 보너스)
        total_discount_rate = (card_discount_result["discount_rate"] + 
                             time_discount_result["max_time_discount_rate"])
        discount_bonus_score = min(total_discount_rate * 2, 1.0)  # 최대 1.0점
        
        return {
            "original_price": original_total_cost,
            "card_discount": card_discount_result,
            "time_discount": time_discount_result,
            "final_price": final_discounted_price,
            "total_discount_rate": total_discount_rate,
            "discounted_cost_score": discounted_cost_score,
            "discount_bonus_score": discount_bonus_score,
            "savings_amount": original_total_cost - final_discounted_price,
            "savings_percentage": (total_discount_rate * 100)
        }
    
    def _get_parking_lot_type(self, lot: Dict) -> str:
        """주차장 타입 판별"""
        name = lot.get("name", "").lower()
        
        if any(keyword in name for keyword in ["공영", "시설", "시청", "구청"]):
            return "공영_주차장"
        elif any(keyword in name for keyword in ["마트", "백화점", "쇼핑"]):
            return "대형마트_주차장"
        else:
            return "민영_주차장"
    
    def get_discount_recommendations(self, user_info: Dict, parking_lots: List[Dict]) -> Dict:
        """사용자별 할인 추천 정보"""
        
        # 사용자에게 적용 가능한 할인 카드 조회
        applicable_discounts = self.discount_system.get_user_discount_info(user_info)
        
        # 각 주차장별 할인 혜택 분석
        parking_lot_benefits = []
        for lot in parking_lots:
            lot_type = self._get_parking_lot_type(lot)
            parking_policy = self.discount_system.parking_lot_discount_policies.get(lot_type, {})
            
            # 이 주차장에서 적용 가능한 할인 카드
            available_cards = []
            if parking_policy.get("all_discount_cards", False):
                available_cards = list(applicable_discounts.keys())
            else:
                available_cards = [card for card in applicable_discounts.keys() 
                                 if card in parking_policy.get("selected_cards_only", [])]
            
            parking_lot_benefits.append({
                "lot_name": lot["name"],
                "lot_type": lot_type,
                "available_discount_cards": available_cards,
                "max_discount_rate": parking_policy.get("max_discount_rate", 0.0),
                "additional_benefits": parking_policy.get("additional_benefits", [])
            })
        
        return {
            "user_applicable_discounts": applicable_discounts,
            "parking_lot_benefits": parking_lot_benefits,
            "recommendations": self._generate_discount_recommendations(applicable_discounts, parking_lot_benefits)
        }
    
    def _generate_discount_recommendations(self, applicable_discounts: Dict, 
                                         parking_lot_benefits: List[Dict]) -> List[Dict]:
        """할인 추천 생성"""
        recommendations = []
        
        for lot_benefit in parking_lot_benefits:
            if lot_benefit["available_discount_cards"]:
                best_card = max(lot_benefit["available_discount_cards"], 
                              key=lambda card: applicable_discounts[card]["discount_rate"])
                
                recommendations.append({
                    "parking_lot": lot_benefit["lot_name"],
                    "recommended_card": best_card,
                    "discount_rate": applicable_discounts[best_card]["discount_rate"],
                    "estimated_savings": f"{applicable_discounts[best_card]['discount_rate'] * 100:.0f}% 할인 가능",
                    "priority": "high" if applicable_discounts[best_card]["discount_rate"] >= 0.5 else "medium"
                })
        
        # 할인율 순으로 정렬
        recommendations.sort(key=lambda x: x["discount_rate"], reverse=True)
        
        return recommendations


# 사용 예시
if __name__ == "__main__":
    # 할인 시스템 테스트
    discount_system = DiscountSystem()
    
    # 사용자 정보 (다둥이 가정)
    user_info = {
        "children_count": 4,  # 4명의 자녀
        "age": 35,
        "annual_income": 50000000,
        "marriage_years": 8
    }
    
    # 사용자 보유 카드
    user_cards = ["다둥이_복지_카드", "신혼부부_카드"]
    
    # 주차장 정보
    parking_lot = {
        "name": "능동공영 주차장",
        "pricing": {
            "hourly_rate": 3600
        }
    }
    
    # 4시간 주차 시나리오
    hours = 4
    original_cost = parking_lot["pricing"]["hourly_rate"] * hours
    
    print("=== 할인 시스템 테스트 ===")
    print(f"원래 비용: {original_cost:,}원")
    
    # 할인 적용
    discount_result = discount_system.calculate_discounted_price(
        original_cost, user_cards, "공영_주차장"
    )
    
    print(f"할인 적용 후: {discount_result['final_price']:,}원")
    print(f"할인율: {discount_result['discount_rate']*100:.0f}%")
    print(f"절약 금액: {discount_result['savings']:,}원")
    print(f"적용된 카드: {discount_result['applied_cards']}")
    
    # 시간대별 추가 할인
    time_discount = discount_system.calculate_time_based_discount(
        discount_result['final_price'], hours, "공영_주차장"
    )
    
    final_cost = discount_result['final_price'] - time_discount['time_discount_amount']
    print(f"시간대 할인 추가 적용 후: {final_cost:,}원")
    print(f"총 절약 금액: {original_cost - final_cost:,}원")
    print(f"총 할인율: {((original_cost - final_cost) / original_cost) * 100:.1f}%")









