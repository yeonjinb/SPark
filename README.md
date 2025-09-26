# SPark - 스마트 주차장 검색 앱

SPark는 AI 음성 인식과 카카오맵을 활용한 스마트 주차장 검색 및 추천 서비스입니다.

## 주요 기능

- 🎤 **Vosk 음성 인식**: 오프라인 한국어 음성 인식으로 "2시간 이용 가능한 주차장 찾아줘"와 같은 자연어 검색
- 🗺️ **카카오맵 연동**: 실시간 지도 표시 및 길찾기 기능
- 🔍 **AI 추천**: 사용자 선호도 기반 주차장 추천 알고리즘
- 👤 **사용자 인증**: 회원가입/로그인 및 개인화 설정
- ⭐ **즐겨찾기**: 자주 이용하는 주차장 저장
- 📱 **반응형 UI**: 직관적이고 현대적인 사용자 인터페이스

## 기술 스택

### Frontend (Flutter)
- **Flutter 3.8+**: 크로스 플랫폼 모바일 앱
- **카카오맵 SDK**: 지도 표시 및 길찾기
- **Vosk 음성 인식**: 오프라인 한국어 음성 인식
- **상태 관리**: Riverpod
- **HTTP 통신**: Dio

### Backend (Python)
- **FastAPI**: 고성능 REST API 서버
- **Supabase**: PostgreSQL 데이터베이스 및 인증
- **PostGIS**: 공간 데이터 처리
- **JWT**: 토큰 기반 인증

## Quickstart

### Backend
1. Create venv and install deps:
```bash
cd backend
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
```
2. Run server:
```bash
python -m backend.main
# or
uvicorn backend.main:app --reload
```
3. Test endpoints:
```bash
GET http://localhost:8000/ping
POST http://localhost:8000/recommend
{
  "user_lat": 37.5665,
  "user_lng": 126.9780,
  "is_ev": true,
  "vehicle_height_m": 1.6,
  "max_price_per_hour": 4000,
  "limit": 5
}
```

### Supabase
1. Apply schema and RLS in SQL editor:
   - `backend/db/schema.sql`
   - `backend/db/rls_policies.sql`
2. Create service role policies as needed.

### Flutter
1. Create `.env` at project root:
```env
# API 설정
API_BASE_URL=http://localhost:8000

# 카카오 API 키 (카카오 개발자 콘솔에서 발급)
KAKAO_REST_API_KEY=your_kakao_rest_api_key_here

# Supabase 설정 (백엔드용)
SUPABASE_URL=your_supabase_url_here
SUPABASE_SERVICE_KEY=your_supabase_service_key_here
```

2. Setup Vosk model:
```bash
# Vosk 한국어 모델 다운로드 및 설정
python scripts/setup_vosk_model.py
```

3. Install dependencies:
```bash
flutter pub get
```

4. Run app:
```bash
flutter run
```

## API 엔드포인트

### 인증
- `POST /auth/signup` - 회원가입
- `POST /auth/login` - 로그인
- `GET /auth/me` - 현재 사용자 정보 조회

### 주차장 추천
- `POST /recommend` - 주차장 추천 조회
- `POST /log_selection` - 선택한 주차장 로깅

### 즐겨찾기
- `GET /favorites` - 즐겨찾기 목록 조회
- `POST /favorites` - 즐겨찾기 추가
- `DELETE /favorites/{id}` - 즐겨찾기 제거

## 카카오 API 설정

1. [카카오 개발자 콘솔](https://developers.kakao.com/)에서 앱 등록
2. REST API 키 발급
3. `.env` 파일에 `KAKAO_REST_API_KEY` 설정

## 데이터베이스 설정

1. Supabase 프로젝트 생성
2. `backend/db/schema.sql` 실행하여 테이블 생성
3. `backend/db/rls_policies.sql` 실행하여 RLS 정책 설정
4. `.env` 파일에 Supabase 설정 추가

## 개발 환경 설정

### 필수 도구
- Flutter SDK 3.8+
- Python 3.8+
- Android Studio / Xcode
- Git

### 권장 IDE
- Android Studio (Flutter 개발)
- VS Code (백엔드 개발)
- Cursor (AI 코드 어시스턴트)
