# Vosk 음성인식 사용법 가이드

## 📚 목차
1. [기본 사용법](#기본-사용법)
2. [실시간 음성인식](#실시간-음성인식)
3. [파일에서 음성인식](#파일에서-음성인식)
4. [고급 기능](#고급-기능)
5. [문제해결](#문제해결)

## 기본 사용법

### 1. 모델 로드
```python
from vosk import Model, KaldiRecognizer
import json

# 한국어 모델 로드
model = Model("models/vosk-model-small-ko-0.22")

# 인식기 초기화 (16kHz 샘플링 레이트)
recognizer = KaldiRecognizer(model, 16000)
```

### 2. 음성 데이터 처리
```python
# 음성 데이터를 청크 단위로 처리
while True:
    data = wf.readframes(4000)  # 4000 바이트씩 읽기
    if len(data) == 0:
        break
    
    # 음성 인식 수행
    if recognizer.AcceptWaveform(data):
        result = json.loads(recognizer.Result())
        print("인식 결과:", result['text'])
    
    # 최종 결과 가져오기
    final_result = json.loads(recognizer.FinalResult())
    print("최종 결과:", final_result['text'])
```

## 실시간 음성인식

### 마이크로부터 실시간 인식
```python
import pyaudio

# 오디오 설정
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

# PyAudio 초기화
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT,
                   channels=CHANNELS,
                   rate=RATE,
                   input=True,
                   frames_per_buffer=CHUNK)

print("🎤 음성인식 시작... (종료하려면 Ctrl+C)")

try:
    while True:
        data = stream.read(CHUNK)
        
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            if result['text']:
                print(f"인식: {result['text']}")
                
except KeyboardInterrupt:
    print("\n음성인식 종료")

# 정리
stream.stop_stream()
stream.close()
audio.terminate()
```

## 파일에서 음성인식

### WAV 파일 처리
```python
import wave

def recognize_wav_file(file_path):
    wf = wave.open(file_path, 'rb')
    
    # 파일의 샘플링 레이트에 맞춰 인식기 초기화
    recognizer = KaldiRecognizer(model, wf.getframerate())
    
    results = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
            
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            if result['text']:
                results.append(result['text'])
    
    # 최종 결과
    final_result = json.loads(recognizer.FinalResult())
    if final_result['text']:
        results.append(final_result['text'])
    
    wf.close()
    return ' '.join(results)

# 사용 예제
text = recognize_wav_file("audio.wav")
print("인식된 텍스트:", text)
```

## 고급 기능

### 1. 부분 결과와 최종 결과
```python
# 부분 결과 (실시간으로 나오는 중간 결과)
if recognizer.AcceptWaveform(data):
    partial_result = json.loads(recognizer.Result())
    print("부분 결과:", partial_result['text'])

# 최종 결과 (완전한 문장이 끝났을 때)
final_result = json.loads(recognizer.FinalResult())
print("최종 결과:", final_result['text'])
```

### 2. 신뢰도 점수 확인
```python
result = json.loads(recognizer.Result())
if 'confidence' in result:
    confidence = result['confidence']
    print(f"신뢰도: {confidence:.2f}")
```

### 3. 여러 언어 모델 사용
```python
# 영어 모델
english_model = Model("models/vosk-model-en-us-0.22")

# 한국어 모델
korean_model = Model("models/vosk-model-small-ko-0.22")

# 상황에 따라 모델 선택
def select_model(language):
    if language == "en":
        return english_model
    elif language == "ko":
        return korean_model
    else:
        return korean_model  # 기본값
```

## 문제해결

### 1. 마이크 권한 문제
```python
# 마이크 접근 권한 확인
import pyaudio

audio = pyaudio.PyAudio()
print("사용 가능한 오디오 장치:")
for i in range(audio.get_device_count()):
    info = audio.get_device_info_by_index(i)
    if info['maxInputChannels'] > 0:
        print(f"장치 {i}: {info['name']}")
```

### 2. 샘플링 레이트 문제
```python
# 파일의 실제 샘플링 레이트 확인
import wave

wf = wave.open("audio.wav", 'rb')
print(f"샘플링 레이트: {wf.getframerate()}")
print(f"채널 수: {wf.getnchannels()}")
print(f"비트 깊이: {wf.getsampwidth() * 8}")
wf.close()
```

### 3. 메모리 최적화
```python
# 큰 파일을 청크 단위로 처리
def process_large_file(file_path, chunk_size=16000):
    wf = wave.open(file_path, 'rb')
    recognizer = KaldiRecognizer(model, wf.getframerate())
    
    # 파일을 작은 청크로 나누어 처리
    while True:
        data = wf.readframes(chunk_size)
        if len(data) == 0:
            break
        
        recognizer.AcceptWaveform(data)
        
        # 메모리 정리
        del data
    
    wf.close()
    return json.loads(recognizer.FinalResult())
```

## 성능 최적화 팁

1. **적절한 청크 크기 사용**: 4000 바이트가 일반적으로 좋음
2. **샘플링 레이트**: 16kHz 권장 (더 높으면 정확도 향상, 속도 저하)
3. **모델 크기**: Small(빠름), Medium(균형), Large(정확함)
4. **실시간 처리**: AcceptWaveform()으로 부분 결과 확인

## 지원 형식

- **오디오 형식**: WAV, MP3, FLAC
- **샘플링 레이트**: 8kHz, 16kHz, 48kHz
- **비트 깊이**: 16bit 권장
- **채널**: 모노(1채널) 권장

