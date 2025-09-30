#!/usr/bin/env python3
"""
CSV 파일을 Supabase 데이터베이스에 업로드하는 스크립트

사용법:
    python upload_csv_to_supabase.py <csv_file_path> <table_name> [--batch_size=1000]

예시:
    python upload_csv_to_supabase.py parking_data.csv parking_spots
    python upload_csv_to_supabase.py users.csv users --batch_size=500
"""

import os
import sys
import csv
import argparse
from typing import List, Dict, Any
from pathlib import Path

try:
    from supabase import create_client, Client
    import pandas as pd
except ImportError as e:
    print(f"필요한 라이브러리가 설치되지 않았습니다: {e}")
    print("다음 명령어로 설치하세요:")
    print("pip install supabase pandas")
    sys.exit(1)


def get_supabase_client() -> Client:
    """Supabase 클라이언트를 생성하고 반환합니다."""
    supabase_url = os.environ.get('SUPABASE_URL')
    supabase_key = os.environ.get('SUPABASE_KEY') or os.environ.get('SUPABASE_ANON_KEY')
    
    if not supabase_url or not supabase_key:
        print("오류: Supabase 환경변수가 설정되지 않았습니다.")
        print("다음 명령어로 환경변수를 설정하세요:")
        print("$env:SUPABASE_URL = \"your-supabase-url\"")
        print("$env:SUPABASE_KEY = \"your-supabase-key\"")
        sys.exit(1)
    
    return create_client(supabase_url, supabase_key)


def validate_csv_file(file_path: str) -> bool:
    """CSV 파일의 유효성을 검사합니다."""
    if not Path(file_path).exists():
        print(f"오류: 파일을 찾을 수 없습니다: {file_path}")
        return False
    
    if not file_path.lower().endswith('.csv'):
        print(f"오류: CSV 파일이 아닙니다: {file_path}")
        return False
    
    try:
        # CSV 파일이 올바르게 읽히는지 테스트
        with open(file_path, 'r', encoding='utf-8') as f:
            csv.Sniffer().sniff(f.read(1024))
        return True
    except Exception as e:
        print(f"오류: CSV 파일을 읽을 수 없습니다: {e}")
        return False


def read_csv_data(file_path: str) -> List[Dict[str, Any]]:
    """CSV 파일을 읽어서 딕셔너리 리스트로 반환합니다."""
    try:
        # pandas를 사용해 CSV 읽기 (자동으로 데이터 타입 추론)
        df = pd.read_csv(file_path)
        
        # NaN 값을 None으로 변환 (JSON에서 null로 처리됨)
        df = df.where(pd.notnull(df), None)
        
        # 딕셔너리 리스트로 변환
        data = df.to_dict('records')
        
        print(f"CSV 파일 읽기 완료: {len(data)}개 행, {len(df.columns)}개 열")
        print(f"컬럼명: {list(df.columns)}")
        
        return data
    
    except Exception as e:
        print(f"오류: CSV 파일 읽기 실패: {e}")
        sys.exit(1)


def upload_to_supabase(supabase: Client, table_name: str, data: List[Dict[str, Any]], batch_size: int = 1000):
    """데이터를 Supabase 테이블에 배치로 업로드합니다."""
    total_rows = len(data)
    uploaded_rows = 0
    
    print(f"Supabase 테이블 '{table_name}'에 데이터 업로드 시작...")
    print(f"총 {total_rows}개 행을 {batch_size}개씩 배치로 업로드합니다.")
    
    try:
        for i in range(0, total_rows, batch_size):
            batch = data[i:i + batch_size]
            
            # Supabase에 데이터 삽입
            result = supabase.table(table_name).insert(batch).execute()
            
            uploaded_rows += len(batch)
            progress = (uploaded_rows / total_rows) * 100
            
            print(f"진행률: {uploaded_rows}/{total_rows} ({progress:.1f}%) - 배치 {i//batch_size + 1}")
        
        print(f"✅ 업로드 완료! 총 {uploaded_rows}개 행이 성공적으로 업로드되었습니다.")
        
    except Exception as e:
        print(f"❌ 업로드 중 오류 발생: {e}")
        print(f"업로드된 행 수: {uploaded_rows}/{total_rows}")
        
        # 상세 오류 정보 출력
        if hasattr(e, 'details'):
            print(f"상세 오류: {e.details}")
        
        sys.exit(1)


def show_sample_data(data: List[Dict[str, Any]], sample_size: int = 3):
    """샘플 데이터를 보여줍니다."""
    if not data:
        print("데이터가 없습니다.")
        return
    
    print(f"\n샘플 데이터 (처음 {min(sample_size, len(data))}개 행):")
    print("-" * 50)
    
    for i, row in enumerate(data[:sample_size]):
        print(f"행 {i+1}:")
        for key, value in row.items():
            print(f"  {key}: {value}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description='CSV 파일을 Supabase 데이터베이스에 업로드합니다.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  python upload_csv_to_supabase.py data.csv my_table
  python upload_csv_to_supabase.py parking_data.csv parking_spots --batch_size=500
  python upload_csv_to_supabase.py users.csv users --preview-only
        """
    )
    
    parser.add_argument('csv_file', help='업로드할 CSV 파일 경로')
    parser.add_argument('table_name', help='Supabase 테이블 이름')
    parser.add_argument('--batch_size', type=int, default=1000, 
                       help='배치 크기 (기본값: 1000)')
    parser.add_argument('--preview-only', action='store_true',
                       help='데이터 미리보기만 하고 업로드하지 않음')
    parser.add_argument('--sample-size', type=int, default=3,
                       help='미리보기할 샘플 데이터 개수 (기본값: 3)')
    
    args = parser.parse_args()
    
    # CSV 파일 유효성 검사
    if not validate_csv_file(args.csv_file):
        sys.exit(1)
    
    # CSV 데이터 읽기
    data = read_csv_data(args.csv_file)
    
    # 샘플 데이터 보여주기
    show_sample_data(data, args.sample_size)
    
    # 미리보기만 하는 경우
    if args.preview_only:
        print("--preview-only 옵션이 설정되어 업로드를 건너뜁니다.")
        return
    
    # 사용자 확인
    response = input(f"\n'{args.table_name}' 테이블에 {len(data)}개 행을 업로드하시겠습니까? (y/N): ")
    if response.lower() not in ['y', 'yes']:
        print("업로드가 취소되었습니다.")
        return
    
    # Supabase 클라이언트 생성
    supabase = get_supabase_client()
    
    # 데이터 업로드
    upload_to_supabase(supabase, args.table_name, data, args.batch_size)


if __name__ == "__main__":
    main()




