#!/usr/bin/env python3
"""
Vosk 모델을 assets 폴더에 복사하는 스크립트
"""

import os
import shutil
import zipfile
import requests
from pathlib import Path

def download_vosk_model():
    """Vosk 한국어 모델 다운로드"""
    model_url = "https://alphacephei.com/vosk/models/vosk-model-small-ko-0.22.zip"
    model_zip = "vosk-model-small-ko-0.22.zip"
    model_dir = "vosk-model-small-ko-0.22"
    assets_dir = "assets/models"
    
    # assets 디렉토리 생성
    os.makedirs(assets_dir, exist_ok=True)
    
    # 모델이 이미 있는지 확인
    if os.path.exists(os.path.join(assets_dir, model_dir)):
        print(f"모델이 이미 존재합니다: {os.path.join(assets_dir, model_dir)}")
        return
    
    print("Vosk 한국어 모델을 다운로드 중...")
    
    try:
        # 모델 다운로드
        response = requests.get(model_url, stream=True)
        response.raise_for_status()
        
        with open(model_zip, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print("모델 다운로드 완료")
        
        # 압축 해제
        print("모델 압축 해제 중...")
        with zipfile.ZipFile(model_zip, 'r') as zip_ref:
            zip_ref.extractall(".")
        
        # assets 폴더로 이동
        if os.path.exists(model_dir):
            shutil.move(model_dir, os.path.join(assets_dir, model_dir))
            print(f"모델을 {os.path.join(assets_dir, model_dir)}로 이동했습니다")
        
        # 임시 파일 삭제
        os.remove(model_zip)
        print("설정 완료!")
        
    except Exception as e:
        print(f"오류 발생: {e}")
        print("수동으로 모델을 다운로드하여 assets/models/ 폴더에 넣어주세요")
        print(f"다운로드 URL: {model_url}")

if __name__ == "__main__":
    download_vosk_model()
