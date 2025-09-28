#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from vosk import Model, KaldiRecognizer

def test_vosk_installation():
    """Vosk 설치 및 모델 로드 테스트"""
    print("🎤 Vosk 음성인식 라이브러리 테스트 시작...")
    
    # 모델 경로 설정
    model_path = "models/vosk-model-small-ko-0.22"
    
    # 모델 파일 존재 확인
    if not os.path.exists(model_path):
        print(f"❌ 모델 파일을 찾을 수 없습니다: {model_path}")
        return False
    
    try:
        # 모델 로드 테스트
        print("📁 모델 로딩 중...")
        model = Model(model_path)
        print("✅ 모델 로드 성공!")
        
        # 인식기 초기화 테스트 (16kHz 샘플링 레이트)
        print("🎯 인식기 초기화 중...")
        rec = KaldiRecognizer(model, 16000)
        print("✅ 인식기 초기화 성공!")
        
        print("🎉 Vosk 설치가 완료되었습니다!")
        print(f"📊 모델 정보:")
        print(f"   - 경로: {model_path}")
        print(f"   - 언어: 한국어 (Korean)")
        print(f"   - 크기: Small (빠른 처리)")
        
        return True
        
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        return False

if __name__ == "__main__":
    test_vosk_installation()

