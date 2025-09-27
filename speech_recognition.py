#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import pyaudio
import wave
import os
from vosk import Model, KaldiRecognizer

class SpeechRecognizer:
    def __init__(self, model_path="models/vosk-model-small-ko-0.22"):
        """음성 인식기 초기화"""
        self.model_path = model_path
        self.model = Model(model_path)
        self.recognizer = None
        
    def recognize_from_file(self, audio_file_path):
        """음성 파일에서 텍스트 추출"""
        if not os.path.exists(audio_file_path):
            return "음성 파일을 찾을 수 없습니다."
            
        wf = wave.open(audio_file_path, 'rb')
        self.recognizer = KaldiRecognizer(self.model, wf.getframerate())
        
        results = []
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if self.recognizer.AcceptWaveform(data):
                result = json.loads(self.recognizer.Result())
                if result['text']:
                    results.append(result['text'])
        
        final_result = json.loads(self.recognizer.FinalResult())
        if final_result['text']:
            results.append(final_result['text'])
            
        wf.close()
        return ' '.join(results)
    
    def recognize_from_microphone(self, duration=5):
        """마이크로부터 실시간 음성 인식"""
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        
        audio = pyaudio.PyAudio()
        self.recognizer = KaldiRecognizer(self.model, RATE)
        
        print(f"🎤 {duration}초 동안 음성을 녹음합니다...")
        
        stream = audio.open(format=FORMAT,
                          channels=CHANNELS,
                          rate=RATE,
                          input=True,
                          frames_per_buffer=CHUNK)
        
        frames = []
        for i in range(0, int(RATE / CHUNK * duration)):
            data = stream.read(CHUNK)
            frames.append(data)
            
            if self.recognizer.AcceptWaveform(data):
                result = json.loads(self.recognizer.Result())
                if result['text']:
                    print(f"인식: {result['text']}")
        
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        final_result = json.loads(self.recognizer.FinalResult())
        return final_result.get('text', '')

# 사용 예제
if __name__ == "__main__":
    recognizer = SpeechRecognizer()
    
    print("🎤 음성 인식 테스트")
    print("1. 마이크로부터 음성 인식")
    print("2. 음성 파일에서 인식")
    
    choice = input("선택하세요 (1 또는 2): ")
    
    if choice == "1":
        result = recognizer.recognize_from_microphone(duration=5)
        print(f"결과: {result}")
    elif choice == "2":
        file_path = input("음성 파일 경로를 입력하세요: ")
        result = recognizer.recognize_from_file(file_path)
        print(f"결과: {result}")
    else:
        print("잘못된 선택입니다.")
