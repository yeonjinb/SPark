#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
주차장 찾기 앱 - Vosk 음성인식 통합 예제
"""

import json
import time
from vosk import Model, KaldiRecognizer
import pyaudio
import requests
import geopy
from geopy.distance import geodesic

class ParkingApp:
    def __init__(self, model_path="models/vosk-model-small-ko-0.22"):
        """
        주차장 찾기 앱 초기화
        
        Vosk의 역할:
        1. 음성을 텍스트로 변환 (STT - Speech to Text)
        2. 사용자 명령어 인식
        3. 자연어 처리의 입력 단계
        """
        try:
            self.model = Model(model_path)
            print(f"✅ Vosk 모델 로드 성공: {model_path}")
        except Exception as e:
            print(f"❌ 모델 로드 실패: {e}")
            raise
        
        self.recognizer = None
        self.is_listening = False
        
        # 주차장 데이터 (실제로는 API에서 가져옴)
        self.parking_lots = [
            {"name": "시청 주차장", "location": (37.5665, 126.9780), "price": 1000, "available": 15},
            {"name": "명동 주차장", "location": (37.5636, 126.9826), "price": 1500, "available": 8},
            {"name": "강남역 주차장", "location": (37.4979, 127.0276), "price": 2000, "available": 25},
            {"name": "홍대 주차장", "location": (37.5563, 126.9226), "price": 1200, "available": 12},
        ]
        
        # 현재 위치 (실제로는 GPS에서 가져옴)
        self.current_location = (37.5665, 126.9780)  # 서울시청
    
    def start_voice_recognition(self):
        """음성 인식 시작"""
        print("🎤 음성 인식을 시작합니다...")
        print("말씀하세요: 'n시간동안 주차할 주차장 찾아줘'")
        
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        
        try:
            audio = pyaudio.PyAudio()
            
            # 마이크 장치 확인
            device_count = audio.get_device_count()
            input_devices = []
            for i in range(device_count):
                info = audio.get_device_info_by_index(i)
                if info['maxInputChannels'] > 0:
                    input_devices.append(info['name'])
            
            if not input_devices:
                print("❌ 입력 가능한 마이크 장치를 찾을 수 없습니다.")
                return
            
            print(f"🎤 사용 가능한 마이크: {len(input_devices)}개")
            
            recognizer = KaldiRecognizer(self.model, RATE)
            
            stream = audio.open(format=FORMAT,
                              channels=CHANNELS,
                              rate=RATE,
                              input=True,
                              frames_per_buffer=CHUNK)
        except Exception as e:
            print(f"❌ 오디오 초기화 실패: {e}")
            return
        
        self.is_listening = True
        
        try:
            while self.is_listening:
                data = stream.read(CHUNK)
                
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    if result['text']:
                        print(f"인식된 음성: {result['text']}")
                        self.process_voice_command(result['text'])
        
        except KeyboardInterrupt:
            print("\n음성 인식을 종료합니다.")
        except Exception as e:
            print(f"❌ 음성 인식 중 오류: {e}")
        finally:
            # 리소스 정리
            if 'stream' in locals():
                stream.stop_stream()
                stream.close()
            if 'audio' in locals():
                audio.terminate()
    
    def process_voice_command(self, text):
        """음성 명령어 처리 - Vosk의 핵심 역할"""
        
        # Vosk의 역할: 음성 → 텍스트 변환 완료
        # 이제 텍스트를 분석해서 명령어 추출
        
        print(f"🔍 명령어 분석 중: {text}")
        
        # 1. 시간 정보 추출
        hours = self.extract_hours(text)
        
        # 2. 명령어 타입 확인 - 개선된 버전
        command_type = self.identify_command_type(text)
        
        if command_type == "find_parking":
            print(f"📍 {hours}시간 주차용 주차장을 찾습니다...")
            self.find_parking_lots(hours)
        elif command_type == "reserve_parking":
            print(f"📅 {hours}시간 주차장 예약을 처리합니다...")
            self.reserve_parking(hours)
        elif command_type == "parking_info":
            print(f"ℹ️ 주차장 정보를 제공합니다...")
            self.show_parking_info()
        else:
            print("❌ 주차장 관련 명령어를 인식하지 못했습니다.")
            print("💡 사용 가능한 명령어:")
            print("   - '2시간 주차장 찾아줘'")
            print("   - '3시간 주차장 예약해줘'")
            print("   - '주차장 정보 알려줘'")
    
    def identify_command_type(self, text):
        """명령어 타입을 더 정확하게 식별"""
        text_lower = text.lower()
        
        # 주차장 찾기 관련 키워드
        find_keywords = [
            "찾아", "찾아줘", "찾기", "검색", "어디", "위치", 
            "추천", "알려줘", "보여줘", "제안"
        ]
        
        # 예약 관련 키워드
        reserve_keywords = [
            "예약", "예약해", "예약해줘", "예약하기", "예약하고",
            "빌리", "빌려줘", "사용", "이용"
        ]
        
        # 정보 요청 관련 키워드
        info_keywords = [
            "정보", "알려줘", "어떤", "어디에", "얼마", "비용",
            "가격", "요금", "현재", "상황"
        ]
        
        # 주차장 관련 키워드 확인
        parking_keywords = ["주차장", "주차", "주차공간", "주차공간"]
        
        if not any(keyword in text_lower for keyword in parking_keywords):
            return "unknown"
        
        # 명령어 타입 판별
        if any(keyword in text_lower for keyword in find_keywords):
            return "find_parking"
        elif any(keyword in text_lower for keyword in reserve_keywords):
            return "reserve_parking"
        elif any(keyword in text_lower for keyword in info_keywords):
            return "parking_info"
        else:
            # 기본값은 찾기로 설정
            return "find_parking"
    
    def extract_hours(self, text):
        """텍스트에서 시간 정보 추출 - 개선된 버전"""
        import re
        
        # 다양한 시간 패턴 지원
        hour_patterns = [
            r'(\d+)시간',
            r'(\d+)시간동안',
            r'(\d+)시간 동안',
            r'(\d+)시간만큼',
            r'(\d+)시간 정도',
            r'(\d+)시간짜리'
        ]
        
        for pattern in hour_patterns:
            match = re.search(pattern, text)
            if match:
                hours = int(match.group(1))
                # 유효한 시간 범위 체크 (1-24시간)
                if 1 <= hours <= 24:
                    return hours
                else:
                    print(f"⚠️ 시간 범위 초과: {hours}시간 (1-24시간만 가능)")
                    return min(max(hours, 1), 24)  # 범위 내로 제한
        
        # 기본값
        print("⚠️ 시간 정보를 찾을 수 없어 기본값 2시간을 사용합니다.")
        return 2
    
    def find_parking_lots(self, hours):
        """최적의 주차장 찾기 - Vosk 이후 처리"""
        print(f"🎯 {hours}시간 주차에 최적화된 주차장을 찾는 중...")
        
        # 거리 계산 및 최적화
        optimal_lots = []
        
        for lot in self.parking_lots:
            if lot['available'] > 0:
                # 거리 계산
                distance = geodesic(self.current_location, lot['location']).kilometers
                
                # 총 비용 계산 (시간 * 시간당 요금)
                total_cost = lot['price'] * hours
                
                # 최적화 점수 계산 (거리 + 비용 + 가용성)
                score = self.calculate_optimality_score(distance, total_cost, lot['available'])
                
                optimal_lots.append({
                    **lot,
                    'distance': distance,
                    'total_cost': total_cost,
                    'score': score
                })
        
        # 점수순으로 정렬
        optimal_lots.sort(key=lambda x: x['score'])
        
        # 결과 출력
        print("\n🏆 최적의 주차장 추천:")
        print("-" * 60)
        
        for i, lot in enumerate(optimal_lots[:3], 1):
            print(f"{i}. {lot['name']}")
            print(f"   📍 거리: {lot['distance']:.2f}km")
            print(f"   💰 총 비용: {lot['total_cost']:,}원 ({hours}시간)")
            print(f"   🅿️  남은 자리: {lot['available']}개")
            print(f"   ⭐ 점수: {lot['score']:.2f}")
            print()
    
    def calculate_optimality_score(self, distance, cost, availability):
        """최적화 점수 계산"""
        # 가중치: 거리(40%), 비용(40%), 가용성(20%)
        distance_score = distance * 40
        cost_score = cost * 0.001 * 40  # 원을 천원 단위로 변환
        availability_score = (10 - availability) * 2  # 적을수록 좋음
        
        return distance_score + cost_score + availability_score
    
    def show_parking_info(self):
        """주차장 정보 표시"""
        print("\n📋 등록된 주차장 정보:")
        print("-" * 50)
        
        for i, lot in enumerate(self.parking_lots, 1):
            distance = geodesic(self.current_location, lot['location']).kilometers
            print(f"{i}. {lot['name']}")
            print(f"   📍 거리: {distance:.2f}km")
            print(f"   💰 시간당 요금: {lot['price']:,}원")
            print(f"   🅿️  남은 자리: {lot['available']}개")
            print(f"   📊 가용률: {(lot['available'] / (lot['available'] + 10)) * 100:.1f}%")
            print()
    
    def reserve_parking(self, hours):
        """주차장 예약 처리"""
        print(f"📅 {hours}시간 주차장 예약 기능 (구현 예정)")
        print("💡 예약 기능은 추후 구현될 예정입니다.")
    
    def stop_listening(self):
        """음성 인식 중지"""
        self.is_listening = False

class VoiceCommandProcessor:
    """음성 명령어 처리기 - Vosk와 비즈니스 로직 연결"""
    
    def __init__(self, parking_app):
        self.parking_app = parking_app
    
    def process_continuous_voice(self):
        """연속 음성 인식"""
        print("🎤 연속 음성 인식 모드")
        print("명령어 예시:")
        print("- '2시간동안 주차할 주차장 찾아줘'")
        print("- '3시간 주차장 예약해줘'")
        print("- '종료' (프로그램 종료)")
        
        self.parking_app.start_voice_recognition()

def main():
    """메인 함수"""
    print("🚗 스마트 주차장 찾기 앱")
    print("=" * 50)
    
    # 앱 초기화
    app = ParkingApp()
    
    # 음성 처리기
    voice_processor = VoiceCommandProcessor(app)
    
    print("옵션을 선택하세요:")
    print("1. 음성으로 주차장 찾기")
    print("2. 테스트 명령어 실행")
    print("3. 종료")
    
    choice = input("\n선택 (1-3): ").strip()
    
    if choice == "1":
        voice_processor.process_continuous_voice()
    elif choice == "2":
        # 테스트 명령어 - 다양한 패턴 테스트
        test_commands = [
            "2시간동안 주차할 주차장 찾아줘",
            "3시간 주차장 예약해줘",
            "1시간 주차할 곳 찾아줘",
            "주차장 정보 알려줘",
            "4시간 주차공간 검색해줘",
            "주차장 추천해줘"
        ]
        
        for cmd in test_commands:
            print(f"\n테스트: {cmd}")
            app.process_voice_command(cmd)
            time.sleep(1)
    elif choice == "3":
        print("👋 프로그램을 종료합니다.")
    else:
        print("❌ 잘못된 선택입니다.")

if __name__ == "__main__":
    main()
