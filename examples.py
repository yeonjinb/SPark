#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Vosk 음성인식 예제 모음
"""

import json
import pyaudio
import wave
import os
from vosk import Model, KaldiRecognizer

class VoskExamples:
    def __init__(self, model_path="models/vosk-model-small-ko-0.22"):
        self.model = Model(model_path)
        self.recognizer = None
    
    def example_1_basic_file_recognition(self, audio_file):
        """예제 1: 기본 파일 음성인식"""
        print("=== 예제 1: 파일에서 음성인식 ===")
        
        if not os.path.exists(audio_file):
            print(f"파일을 찾을 수 없습니다: {audio_file}")
            return
        
        wf = wave.open(audio_file, 'rb')
        recognizer = KaldiRecognizer(self.model, wf.getframerate())
        
        print("음성인식 중...")
        results = []
        
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                if result['text']:
                    results.append(result['text'])
                    print(f"부분 결과: {result['text']}")
        
        # 최종 결과
        final_result = json.loads(recognizer.FinalResult())
        if final_result['text']:
            results.append(final_result['text'])
        
        wf.close()
        
        full_text = ' '.join(results)
        print(f"최종 결과: {full_text}")
        return full_text
    
    def example_2_realtime_microphone(self, duration=10):
        """예제 2: 실시간 마이크 음성인식"""
        print("=== 예제 2: 실시간 마이크 음성인식 ===")
        
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        
        audio = pyaudio.PyAudio()
        recognizer = KaldiRecognizer(self.model, RATE)
        
        print(f"🎤 {duration}초 동안 음성을 녹음합니다...")
        
        stream = audio.open(format=FORMAT,
                          channels=CHANNELS,
                          rate=RATE,
                          input=True,
                          frames_per_buffer=CHUNK)
        
        try:
            for i in range(0, int(RATE / CHUNK * duration)):
                data = stream.read(CHUNK)
                
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    if result['text']:
                        print(f"실시간 인식: {result['text']}")
        
        except KeyboardInterrupt:
            print("\n녹음 중단됨")
        
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        # 최종 결과
        final_result = json.loads(recognizer.FinalResult())
        print(f"최종 결과: {final_result.get('text', '')}")
        return final_result.get('text', '')
    
    def example_3_continuous_listening(self):
        """예제 3: 연속 듣기 (키워드 감지)"""
        print("=== 예제 3: 연속 듣기 ===")
        print("'종료'라고 말하면 프로그램이 끝납니다.")
        
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        
        audio = pyaudio.PyAudio()
        recognizer = KaldiRecognizer(self.model, RATE)
        
        stream = audio.open(format=FORMAT,
                          channels=CHANNELS,
                          rate=RATE,
                          input=True,
                          frames_per_buffer=CHUNK)
        
        print("🎤 음성인식 시작... (종료하려면 '종료'라고 말하세요)")
        
        try:
            while True:
                data = stream.read(CHUNK)
                
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    if result['text']:
                        print(f"인식: {result['text']}")
                        
                        # 종료 키워드 감지
                        if "종료" in result['text']:
                            print("종료 키워드 감지! 프로그램을 종료합니다.")
                            break
        
        except KeyboardInterrupt:
            print("\n프로그램 종료")
        
        stream.stop_stream()
        stream.close()
        audio.terminate()
    
    def example_4_batch_processing(self, audio_files):
        """예제 4: 여러 파일 일괄 처리"""
        print("=== 예제 4: 여러 파일 일괄 처리 ===")
        
        results = {}
        
        for audio_file in audio_files:
            if os.path.exists(audio_file):
                print(f"처리 중: {audio_file}")
                result = self.example_1_basic_file_recognition(audio_file)
                results[audio_file] = result
            else:
                print(f"파일을 찾을 수 없습니다: {audio_file}")
                results[audio_file] = None
        
        return results
    
    def example_5_confidence_scoring(self, audio_file):
        """예제 5: 신뢰도 점수 확인"""
        print("=== 예제 5: 신뢰도 점수 확인 ===")
        
        if not os.path.exists(audio_file):
            print(f"파일을 찾을 수 없습니다: {audio_file}")
            return
        
        wf = wave.open(audio_file, 'rb')
        recognizer = KaldiRecognizer(self.model, wf.getframerate())
        
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                if result['text']:
                    confidence = result.get('confidence', 'N/A')
                    print(f"텍스트: {result['text']}")
                    print(f"신뢰도: {confidence}")
                    print("-" * 40)
        
        wf.close()

def main():
    """메인 함수 - 예제 실행"""
    examples = VoskExamples()
    
    print("🎤 Vosk 음성인식 예제 모음")
    print("1. 파일에서 음성인식")
    print("2. 실시간 마이크 음성인식")
    print("3. 연속 듣기")
    print("4. 여러 파일 일괄 처리")
    print("5. 신뢰도 점수 확인")
    
    choice = input("\n실행할 예제를 선택하세요 (1-5): ")
    
    if choice == "1":
        file_path = input("음성 파일 경로를 입력하세요: ")
        examples.example_1_basic_file_recognition(file_path)
    
    elif choice == "2":
        duration = int(input("녹음 시간(초)을 입력하세요 (기본값: 10): ") or "10")
        examples.example_2_realtime_microphone(duration)
    
    elif choice == "3":
        examples.example_3_continuous_listening()
    
    elif choice == "4":
        files = input("처리할 파일들을 쉼표로 구분하여 입력하세요: ").split(',')
        files = [f.strip() for f in files]
        results = examples.example_4_batch_processing(files)
        print("\n=== 일괄 처리 결과 ===")
        for file, result in results.items():
            print(f"{file}: {result}")
    
    elif choice == "5":
        file_path = input("음성 파일 경로를 입력하세요: ")
        examples.example_5_confidence_scoring(file_path)
    
    else:
        print("잘못된 선택입니다.")

if __name__ == "__main__":
    main()

