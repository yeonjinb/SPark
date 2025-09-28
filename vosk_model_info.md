# Vosk 모델 및 성능 최적화 가이드

## 🤖 Vosk 모델 방식

Vosk는 **사전 훈련된 모델**을 사용하는 방식입니다:
- ✅ **추가 학습 불필요** - 이미 훈련된 모델 사용
- ✅ **즉시 사용 가능** - 다운로드만 하면 바로 사용
- ✅ **오프라인 작동** - 인터넷 연결 없이도 동작

## 📊 사용 가능한 한국어 모델

### 현재 설치된 모델: `vosk-model-small-ko-0.22`
- **크기**: ~87MB
- **특징**: 빠른 처리, 적은 메모리 사용
- **정확도**: 기본적인 한국어 인식
- **용도**: 실시간 처리, 임베디드 시스템

### 더 나은 성능을 위한 모델 옵션:

#### 1. Medium 모델 (정확도 향상)
```bash
# 더 큰 한국어 모델 다운로드
Invoke-WebRequest -Uri "https://alphacephei.com/vosk/models/vosk-model-ko-0.24.zip" -OutFile "vosk-model-ko-0.24.zip"
```
- **크기**: ~1.8GB
- **정확도**: Small 모델보다 높음
- **처리속도**: 상대적으로 느림

#### 2. Large 모델 (최고 정확도)
```bash
# 대용량 한국어 모델
Invoke-WebRequest -Uri "https://alphacephei.com/vosk/models/vosk-model-ko-0.25.zip" -OutFile "vosk-model-ko-0.25.zip"
```
- **크기**: ~3GB+
- **정확도**: 가장 높음
- **처리속도**: 가장 느림

## 🎯 성능 최적화 방법

### 1. 오디오 품질 개선
```python
# 권장 오디오 설정
RECOMMENDED_SETTINGS = {
    "sample_rate": 16000,  # 16kHz (표준)
    "channels": 1,         # 모노 (1채널)
    "bit_depth": 16,       # 16bit
    "format": "wav"        # WAV 형식
}
```

### 2. 전처리 (Preprocessing)
```python
import librosa
import soundfile as sf

def preprocess_audio(input_file, output_file):
    """오디오 전처리"""
    # 노이즈 제거
    y, sr = librosa.load(input_file, sr=16000)
    
    # 정규화
    y = librosa.util.normalize(y)
    
    # 저장
    sf.write(output_file, y, 16000)
```

### 3. 후처리 (Post-processing)
```python
def post_process_text(text):
    """인식 결과 후처리"""
    # 불필요한 공백 제거
    text = ' '.join(text.split())
    
    # 자주 틀리는 단어 교정
    corrections = {
        '안녕하세요': '안녕하세요',
        '감사합니다': '감사합니다',
        # 필요한 교정 사전 추가
    }
    
    for wrong, correct in corrections.items():
        text = text.replace(wrong, correct)
    
    return text
```

## 🔧 커스텀 모델 생성 (고급)

### 1. Kaldi 기반 커스텀 모델
```bash
# Kaldi 툴킷 설치 필요
# 자체 데이터로 모델 훈련 (복잡함)
```

### 2. 도메인 특화 모델
```python
# 특정 분야 단어 사전 추가
DOMAIN_VOCABULARY = {
    "의료": ["혈압", "맥박", "체온", "증상"],
    "법률": ["법조문", "판결", "소송", "계약"],
    "기술": ["알고리즘", "데이터베이스", "API", "프레임워크"]
}

def enhance_recognition(text, domain="일반"):
    """도메인별 단어 강화"""
    if domain in DOMAIN_VOCABULARY:
        # 도메인 단어 우선 인식 로직
        pass
    return text
```

## 📈 성능 비교

| 모델 | 크기 | 정확도 | 속도 | 메모리 | 용도 |
|------|------|--------|------|--------|------|
| Small | 87MB | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 실시간, 임베디드 |
| Medium | 1.8GB | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | 일반적인 용도 |
| Large | 3GB+ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ | 정확도 중시 |

## 🚀 추천 설정

### 개발/테스트 환경
```python
# 현재 설정 (Small 모델)
model_path = "models/vosk-model-small-ko-0.22"
```

### 프로덕션 환경
```python
# 더 나은 정확도 필요시
model_path = "models/vosk-model-ko-0.24"  # Medium 모델
```

## 💡 성능 향상 팁

1. **오디오 품질**: 깨끗한 녹음 환경
2. **마이크 품질**: 고품질 마이크 사용
3. **샘플링 레이트**: 16kHz 이상 권장
4. **노이즈 제거**: 전처리로 배경음 제거
5. **도메인 사전**: 특정 분야 단어 사전 구축

## ❌ 학습 데이터가 필요한 경우

일반적으로 **추가 학습 불필요**하지만, 다음 경우에만 고려:
- 특수한 도메인 (의료, 법률, 기술 전문용어)
- 특정 방언이나 억양
- 극도로 높은 정확도 요구
- 실시간 처리가 아닌 배치 처리

