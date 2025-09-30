# VOSK를 리액트 웹앱에 통합하는 방법

## 🎯 개요
이 폴더에는 SPark 주차장 앱에서 사용된 VOSK 음성 인식 기능을 리액트 웹앱으로 옮기기 위한 모든 파일들이 포함되어 있습니다.

## 📁 파일 구조
```
vosk_copy/
├── README_REACT_INTEGRATION.md     # 이 파일 (리액트 통합 가이드)
├── vosk_guide.md                   # VOSK 기본 사용법
├── vosk_integration_guide.md       # 주차장 앱 통합 가이드
├── vosk_model_info.md              # VOSK 모델 정보
├── voice_test.html                 # 웹 음성 테스트 예제
├── simple_voice_test.html          # 간단한 웹 음성 테스트
└── voice_parking_integration.html   # 주차장 음성 통합 예제
```

## 🚀 리액트 웹앱 통합 단계

### 1단계: VOSK 모델 확인
```bash
# VOSK 모델이 이미 설치되어 있는지 확인
# models/vosk-model-small-ko-0.22 폴더가 있는지 확인
```

### 2단계: 리액트 프로젝트 설정
```bash
# 필요한 패키지 설치 (이미 설치되어 있다면 생략)
npm install vosk
npm install @types/vosk  # TypeScript 사용시
```

### 3단계: 웹 워커를 사용한 VOSK 통합
```javascript
// src/workers/voskWorker.js
import { createWorker } from 'vosk';

let worker = null;

self.onmessage = async (e) => {
  const { type, data } = e.data;
  
  switch (type) {
    case 'INIT':
      worker = await createWorker();
      await worker.loadModel('path/to/vosk-model-small-ko-0.22');
      self.postMessage({ type: 'INIT_COMPLETE' });
      break;
      
    case 'RECOGNIZE':
      const result = await worker.recognize(data);
      self.postMessage({ type: 'RESULT', data: result });
      break;
      
    case 'TERMINATE':
      if (worker) {
        worker.terminate();
      }
      break;
  }
};
```

### 4단계: 리액트 컴포넌트 구현
```jsx
// src/components/VoiceRecognition.jsx
import React, { useState, useEffect, useRef } from 'react';

const VoiceRecognition = ({ onResult }) => {
  const [isListening, setIsListening] = useState(false);
  const [status, setStatus] = useState('준비');
  const workerRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const streamRef = useRef(null);

  useEffect(() => {
    // 웹 워커 초기화
    workerRef.current = new Worker('/workers/voskWorker.js');
    
    workerRef.current.onmessage = (e) => {
      const { type, data } = e.data;
      
      switch (type) {
        case 'INIT_COMPLETE':
          setStatus('음성 인식 준비 완료');
          break;
        case 'RESULT':
          onResult(data.text);
          break;
      }
    };

    return () => {
      if (workerRef.current) {
        workerRef.current.postMessage({ type: 'TERMINATE' });
      }
    };
  }, []);

  const startListening = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;
      
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      
      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          workerRef.current.postMessage({
            type: 'RECOGNIZE',
            data: event.data
          });
        }
      };
      
      mediaRecorder.start(1000); // 1초마다 데이터 전송
      setIsListening(true);
      setStatus('음성 인식 중...');
      
    } catch (error) {
      console.error('마이크 접근 실패:', error);
      setStatus('마이크 접근 실패');
    }
  };

  const stopListening = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
    }
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
    }
    setIsListening(false);
    setStatus('음성 인식 중지');
  };

  return (
    <div className="voice-recognition">
      <h3>음성 인식</h3>
      <p>상태: {status}</p>
      
      {!isListening ? (
        <button onClick={startListening}>
          🎤 음성 인식 시작
        </button>
      ) : (
        <button onClick={stopListening}>
          ⏹️ 음성 인식 중지
        </button>
      )}
    </div>
  );
};

export default VoiceRecognition;
```

### 5단계: 지도 연동
```jsx
// src/components/MapWithVoice.jsx
import React, { useState } from 'react';
import VoiceRecognition from './VoiceRecognition';

const MapWithVoice = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [parkingResults, setParkingResults] = useState([]);

  const handleVoiceResult = (text) => {
    console.log('음성 인식 결과:', text);
    
    // 주차장 관련 키워드 체크
    const parkingKeywords = ['주차', '주차장', '찾아', '정보', '예약'];
    const hasParkingKeyword = parkingKeywords.some(keyword => 
      text.includes(keyword)
    );
    
    if (hasParkingKeyword) {
      setSearchQuery(text);
      // 여기서 지도 API 호출
      searchParkingSpots(text);
    }
  };

  const searchParkingSpots = async (query) => {
    // 지도 API를 사용한 주차장 검색 로직
    console.log('주차장 검색:', query);
  };

  return (
    <div className="map-with-voice">
      <VoiceRecognition onResult={handleVoiceResult} />
      
      <div className="search-results">
        <h3>검색 결과: {searchQuery}</h3>
        {/* 지도 컴포넌트 */}
      </div>
    </div>
  );
};

export default MapWithVoice;
```

## 🔧 주요 기능

### 1. 실시간 음성 인식
- 마이크로부터 실시간 음성 입력
- 웹 워커를 사용한 백그라운드 처리
- 부분 결과와 최종 결과 제공

### 2. 주차장 관련 키워드 인식
- "주차장 찾아줘"
- "2시간 주차할 곳"
- "주차 정보 알려줘"

### 3. 지도 연동
- 음성 명령 → 지도 검색
- 실시간 주차장 정보 표시
- 위치 기반 추천

## 📋 체크리스트

- [ ] VOSK 모델 다운로드 완료
- [ ] 리액트 프로젝트에 VOSK 패키지 설치
- [ ] 웹 워커 구현
- [ ] 음성 인식 컴포넌트 구현
- [ ] 지도 API 연동
- [ ] 주차장 검색 로직 구현
- [ ] UI/UX 디자인 적용

## 🚨 주의사항

1. **HTTPS 필수**: 웹에서 마이크 접근은 HTTPS에서만 가능
2. **모델 크기**: VOSK 모델은 50MB+ 크기로 CDN 사용 권장
3. **브라우저 지원**: Chrome, Firefox, Safari 최신 버전
4. **권한 요청**: 사용자에게 마이크 권한 요청 필요

## 📚 참고 파일

- `voice_test.html`: 기본 웹 음성 인식 예제
- `simple_voice_test.html`: 간단한 웹 음성 테스트
- `voice_parking_integration.html`: 주차장 앱 통합 예제
- `vosk_guide.md`: VOSK 상세 사용법
- `vosk_integration_guide.md`: 앱 통합 아키텍처
- `vosk_model_info.md`: VOSK 모델 정보

## 🎯 다음 단계

1. 이 가이드를 참고하여 리액트 프로젝트에 VOSK 통합
2. 지도 API (Google Maps, Kakao Map 등) 연동
3. 주차장 데이터베이스 연동
4. UI/UX 개선 및 테스트
