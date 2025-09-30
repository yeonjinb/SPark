#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
간단한 음성 인식 테스트 - Python 버전
"""

import json
import time
from vosk import Model, KaldiRecognizer
import pyaudio

def test_microphone_access():
    """마이크 접근 테스트"""
    print("🎤 마이크 접근 테스트...")
    
    try:
        audio = pyaudio.PyAudio()
        
        # 마이크 장치 확인
        device_count = audio.get_device_count()
        input_devices = []
        
        for i in range(device_count):
            info = audio.get_device_info_by_index(i)
            if info['maxInputChannels'] > 0:
                input_devices.append(f"장치 {i}: {info['name']}")
        
        print(f"✅ 마이크 장치 {len(input_devices)}개 발견:")
        for device in input_devices:
            print(f"   - {device}")
        
        audio.terminate()
        return True
        
    except Exception as e:
        print(f"❌ 마이크 접근 실패: {e}")
        return False

def test_vosk_recognition():
    """Vosk 음성 인식 테스트"""
    print("\n🎯 Vosk 음성 인식 테스트...")
    
    try:
        # 모델 로드
        model = Model("models/vosk-model-small-ko-0.22")
        recognizer = KaldiRecognizer(model, 16000)
        
        # 오디오 설정
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        
        audio = pyaudio.PyAudio()
        stream = audio.open(format=FORMAT,
                          channels=CHANNELS,
                          rate=RATE,
                          input=True,
                          frames_per_buffer=CHUNK)
        
        print("🎤 5초간 음성을 녹음합니다...")
        print("💡 다음 중 하나를 말해보세요:")
        print("   - '안녕하세요'")
        print("   - '2시간 주차장 찾아줘'")
        print("   - '주차장 정보 알려줘'")
        
        # 5초간 녹음
        results = []
        for i in range(0, int(RATE / CHUNK * 5)):
            data = stream.read(CHUNK)
            
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                if result['text']:
                    results.append(result['text'])
                    print(f"인식: {result['text']}")
        
        # 최종 결과
        final_result = json.loads(recognizer.FinalResult())
        if final_result['text']:
            results.append(final_result['text'])
        
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        # 결과 출력
        if results:
            full_text = ' '.join(results)
            print(f"\n✅ 최종 인식 결과: '{full_text}'")
            
            # 주차장 관련 키워드 체크
            parking_keywords = ['주차', '주차장', '찾아', '정보', '예약']
            found_keywords = [kw for kw in parking_keywords if kw in full_text]
            
            if found_keywords:
                print(f"🎯 주차장 관련 키워드 발견: {found_keywords}")
            else:
                print("ℹ️ 주차장 관련 키워드가 없습니다")
        else:
            print("❌ 인식된 음성이 없습니다")
        
        return True
        
    except Exception as e:
        print(f"❌ Vosk 테스트 실패: {e}")
        return False

def main():
    """메인 테스트 함수"""
    print("🚗 SPark 음성 인식 테스트")
    print("=" * 50)
    
    # 1. 마이크 테스트
    mic_ok = test_microphone_access()
    
    if mic_ok:
        # 2. Vosk 테스트
        input("\nEnter를 눌러 Vosk 테스트를 시작하세요...")
        vosk_ok = test_vosk_recognition()
        
        if vosk_ok:
            print("\n🎉 모든 테스트 완료!")
            print("✅ 음성 인식이 정상적으로 작동합니다!")
        else:
            print("\n❌ Vosk 테스트 실패")
    else:
        print("\n❌ 마이크 테스트 실패")
    
    print("\n💡 웹 브라우저 테스트도 해보세요:")
    print("   voice_test.html 파일을 크롬에서 열어보세요!")

if __name__ == "__main__":
    main()









