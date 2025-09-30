#!/usr/bin/env python3
"""
주차장 JSON 데이터를 CSV로 변환하는 스크립트
"""

import json
import pandas as pd
from pathlib import Path
import sys

def convert_parking_json_to_csv(json_file_path: str):
    """주차장 JSON 데이터를 CSV로 변환합니다."""
    
    # JSON 파일 읽기
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"JSON 파일 읽기 오류: {e}")
        return None
    
    # 주차장 결과 데이터 추출
    if 'parking_results' not in data or 'recommendations' not in data['parking_results']:
        print("주차장 추천 데이터를 찾을 수 없습니다.")
        return None
    
    recommendations = data['parking_results']['recommendations']
    
    # DataFrame으로 변환할 데이터 준비
    parking_data = []
    
    for rec in recommendations:
        parking_info = {
            # 기본 정보
            'name': rec.get('name', ''),
            'address': rec.get('address', ''),
            'latitude': rec.get('latitude', 0),
            'longitude': rec.get('longitude', 0),
            'distance_km': rec.get('distance_km', 0),
            'walking_time_min': rec.get('walking_time_min', 0),
            'total_spots': rec.get('total_spots', 0),
            'available_spots': rec.get('available_spots', 0),
            
            # 요금 정보
            'base_fee': rec.get('base_fee', 0),
            'unit_fee': rec.get('unit_fee', 0),
            'unit_time': rec.get('unit_time', 0),
            'max_fee': rec.get('max_fee', 0),
            'free_time': rec.get('free_time', 0),
            
            # 운영 시간
            'operation_start': rec.get('operation_start', ''),
            'operation_end': rec.get('operation_end', ''),
            'weekend_operation': rec.get('weekend_operation', True),
            
            # 차량 제한
            'height_limit': rec.get('height_limit', 0),
            'weight_limit': rec.get('weight_limit', 0),
            
            # 편의시설
            'facilities': ', '.join(rec.get('facilities', [])),
            'payment_methods': ', '.join(rec.get('payment_methods', [])),
            
            # 스코어 정보
            'total_score': rec.get('total_score', 0),
            'price_score': rec.get('scores', {}).get('price_score', 0),
            'distance_score': rec.get('scores', {}).get('distance_score', 0),
            'availability_score': rec.get('scores', {}).get('availability_score', 0),
            'convenience_score': rec.get('scores', {}).get('convenience_score', 0),
            
            # 계산된 비용
            'estimated_cost': rec.get('estimated_cost', 0),
            'discount_applied': rec.get('discount_applied', 0),
            'final_cost': rec.get('final_cost', 0),
        }
        
        parking_data.append(parking_info)
    
    # DataFrame 생성
    df = pd.DataFrame(parking_data)
    
    # CSV 파일명 생성
    json_path = Path(json_file_path)
    csv_file_path = json_path.parent / f"{json_path.stem}_parking_data.csv"
    
    # CSV로 저장
    df.to_csv(csv_file_path, index=False, encoding='utf-8')
    
    print(f"CSV 변환 완료!")
    print(f"입력: {json_file_path}")
    print(f"출력: {csv_file_path}")
    print(f"데이터: {len(df)}개 주차장 정보")
    print(f"컬럼: {len(df.columns)}개")
    
    return str(csv_file_path)

def main():
    # JSON 파일들 확인
    json_files = [
        "parking_recommendation_20250927_163309.json",
        "real_parking_recommendation_20250927_170033.json"
    ]
    
    print("주차장 JSON 데이터를 CSV로 변환합니다...\n")
    
    converted_files = []
    
    for json_file in json_files:
        if Path(json_file).exists():
            print(f"변환 중: {json_file}")
            csv_file = convert_parking_json_to_csv(json_file)
            if csv_file:
                converted_files.append(csv_file)
            print()
        else:
            print(f"파일을 찾을 수 없음: {json_file}")
    
    if converted_files:
        print("=" * 50)
        print("변환된 CSV 파일들:")
        for csv_file in converted_files:
            print(f"  - {csv_file}")
        
        print("\n다음 명령어로 Supabase에 업로드할 수 있습니다:")
        for csv_file in converted_files:
            table_name = Path(csv_file).stem.replace('_parking_data', '')
            print(f"  python upload_csv_to_supabase.py {csv_file} {table_name}")

if __name__ == "__main__":
    main()
