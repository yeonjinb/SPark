#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
웹 API 서버 - 음성 인식과 주차장 앱 연동
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import json
import re
from geopy.distance import geodesic

app = Flask(__name__)
CORS(app)  # CORS 허용 (웹 브라우저에서 API 호출 가능)

class ParkingAPI:
    def __init__(self):
        # 주차장 데이터 (실제로는 데이터베이스에서 가져옴)
        self.parking_lots = [
            {"id": 1, "name": "시청 주차장", "location": (37.5665, 126.9780), "price": 1000, "available": 15},
            {"id": 2, "name": "명동 주차장", "location": (37.5636, 126.9826), "price": 1500, "available": 8},
            {"id": 3, "name": "강남역 주차장", "location": (37.4979, 127.0276), "price": 2000, "available": 25},
            {"id": 4, "name": "홍대 주차장", "location": (37.5563, 126.9226), "price": 1200, "available": 12},
        ]
        
        # 현재 위치 (실제로는 GPS에서 가져옴)
        self.current_location = (37.5665, 126.9780)
    
    def extract_hours(self, text):
        """텍스트에서 시간 정보 추출"""
        hour_patterns = [
            r'(\d+)시간',
            r'(\d+)시간동안',
            r'(\d+)시간 동안',
            r'(\d+)시간만큼',
            r'(\d+)시간 정도'
        ]
        
        for pattern in hour_patterns:
            match = re.search(pattern, text)
            if match:
                hours = int(match.group(1))
                if 1 <= hours <= 24:
                    return hours
        
        return 2  # 기본값
    
    def identify_command_type(self, text):
        """명령어 타입 식별"""
        text_lower = text.lower()
        
        find_keywords = ["찾아", "찾아줘", "찾기", "검색", "어디", "위치", "추천", "알려줘", "보여줘"]
        reserve_keywords = ["예약", "예약해", "예약해줘", "예약하기", "빌리", "빌려줘"]
        info_keywords = ["정보", "알려줘", "어떤", "어디에", "얼마", "비용", "가격"]
        
        if any(keyword in text_lower for keyword in find_keywords):
            return "find_parking"
        elif any(keyword in text_lower for keyword in reserve_keywords):
            return "reserve_parking"
        elif any(keyword in text_lower for keyword in info_keywords):
            return "parking_info"
        else:
            return "find_parking"
    
    def find_optimal_parking(self, hours):
        """최적의 주차장 찾기"""
        optimal_lots = []
        
        for lot in self.parking_lots:
            if lot['available'] > 0:
                # 거리 계산
                distance = geodesic(self.current_location, lot['location']).kilometers
                
                # 총 비용 계산
                total_cost = lot['price'] * hours
                
                # 최적화 점수 계산
                score = self.calculate_optimality_score(distance, total_cost, lot['available'])
                
                optimal_lots.append({
                    **lot,
                    'distance': round(distance, 2),
                    'total_cost': total_cost,
                    'score': round(score, 2)
                })
        
        # 점수순으로 정렬
        optimal_lots.sort(key=lambda x: x['score'])
        
        return optimal_lots[:3]  # 상위 3개만 반환
    
    def calculate_optimality_score(self, distance, cost, availability):
        """최적화 점수 계산"""
        distance_score = distance * 40
        cost_score = cost * 0.001 * 40
        availability_score = (10 - availability) * 2
        
        return distance_score + cost_score + availability_score
    
    def get_parking_info(self):
        """주차장 정보 조회"""
        info_lots = []
        
        for lot in self.parking_lots:
            distance = geodesic(self.current_location, lot['location']).kilometers
            info_lots.append({
                **lot,
                'distance': round(distance, 2),
                'availability_rate': round((lot['available'] / (lot['available'] + 10)) * 100, 1)
            })
        
        return info_lots

# API 인스턴스 생성
parking_api = ParkingAPI()

@app.route('/')
def index():
    """메인 페이지"""
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>주차장 API 서버</title>
        <meta charset="UTF-8">
    </head>
    <body>
        <h1>🚗 주차장 API 서버</h1>
        <p>API 서버가 정상적으로 실행 중입니다.</p>
        <h2>사용 가능한 API:</h2>
        <ul>
            <li>POST /api/process_voice - 음성 명령어 처리</li>
            <li>GET /api/parking_lots - 주차장 목록 조회</li>
            <li>GET /api/health - 서버 상태 확인</li>
        </ul>
        <p><a href="/voice_parking_integration.html">음성 주차장 찾기 테스트</a></p>
    </body>
    </html>
    """)

@app.route('/api/process_voice', methods=['POST'])
def process_voice():
    """음성 명령어 처리 API"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': '텍스트가 제공되지 않았습니다.'}), 400
        
        # 시간 추출
        hours = parking_api.extract_hours(text)
        
        # 명령어 타입 식별
        command_type = parking_api.identify_command_type(text)
        
        result = {
            'text': text,
            'hours': hours,
            'command_type': command_type,
            'timestamp': str(pd.Timestamp.now())
        }
        
        # 명령어 타입에 따른 처리
        if command_type == 'find_parking':
            parking_results = parking_api.find_optimal_parking(hours)
            result['parking_results'] = parking_results
            result['message'] = f'{hours}시간 주차에 최적화된 주차장을 찾았습니다.'
            
        elif command_type == 'reserve_parking':
            result['message'] = f'{hours}시간 주차장 예약 기능 (구현 예정)'
            
        elif command_type == 'parking_info':
            parking_info = parking_api.get_parking_info()
            result['parking_info'] = parking_info
            result['message'] = '주차장 정보를 조회했습니다.'
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/parking_lots', methods=['GET'])
def get_parking_lots():
    """주차장 목록 조회 API"""
    try:
        return jsonify({
            'parking_lots': parking_api.parking_lots,
            'current_location': parking_api.current_location
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """서버 상태 확인 API"""
    return jsonify({
        'status': 'healthy',
        'message': '주차장 API 서버가 정상적으로 작동 중입니다.',
        'timestamp': str(pd.Timestamp.now())
    })

@app.route('/voice_parking_integration.html')
def voice_integration_page():
    """음성 주차장 찾기 페이지"""
    with open('voice_parking_integration.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/spark')
def spark_webapp():
    """SPARK 최종 알고리즘 웹앱"""
    with open('spark_final_algorithm.html', 'r', encoding='utf-8') as f:
        return f.read()

if __name__ == '__main__':
    print("주차장 API 서버 시작...")
    print("서버 주소: http://localhost:5000")
    print("SPARK 웹앱: http://localhost:5000/spark")
    print("음성 테스트: http://localhost:5000/voice_parking_integration.html")
    print("API 문서: http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

