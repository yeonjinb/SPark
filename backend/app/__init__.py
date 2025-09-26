from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Any, Dict
import math
from datetime import datetime, timedelta
import jwt
import hashlib
import secrets

def create_app() -> FastAPI:
    app = FastAPI(title="SPark Backend", version="0.2.0")

    @app.get("/")
    def root():
        return {"ok": True, "data": {"service": "SPark API", "docs": "/docs", "health": "/ping"}}

    @app.get("/ping")
    def ping():
        return {"ok": True, "data": {"status": "ok"}}

    class RecommendRequest(BaseModel):
        user_lat: float = Field(..., description="사용자 위도")
        user_lng: float = Field(..., description="사용자 경도")
        is_ev: bool = Field(False, description="전기차 여부")
        vehicle_height_m: Optional[float] = Field(None, description="차량 높이(m)")
        max_price_per_hour: Optional[int] = Field(None, description="시간당 최대 요금")
        limit: int = Field(5, ge=1, le=20, description="추천 개수")
        auth_user_id: Optional[str] = Field(None, description="Supabase auth user id (선호 가중치 조회용)")
        search_radius_km: float = Field(5.0, ge=0.1, le=50.0, description="검색 반경(km)")
        include_difficulty: bool = Field(True, description="난이도 점수 포함 여부")
        preferred_structure: Optional[str] = Field(None, description="선호 구조 유형")

    class DetailedPricing(BaseModel):
        weekday_base: int
        weekday_additional: int
        weekday_daily_max: Optional[int]
        weekday_night: Optional[int]
        weekend_base: int
        weekend_additional: int
        weekend_daily_max: Optional[int]
        weekend_night: Optional[int]
        holiday_base: int
        holiday_additional: int
        holiday_daily_max: Optional[int]
        holiday_night: Optional[int]

    class ParkingLot(BaseModel):
        id: str
        name: str
        lat: float
        lng: float
        height_limit_m: Optional[float] = None
        ev_charging: bool = False
        open_24h: bool = True
        
        # Detailed pricing
        pricing: DetailedPricing
        
        # Difficulty and structure
        difficulty_score: Optional[float] = None
        structure_type: Optional[str] = None
        capacity: Optional[int] = None
        entrance_width_m: Optional[float] = None
        exit_width_m: Optional[float] = None
        turning_radius_m: Optional[float] = None
        has_valet: bool = False
        has_attendant: bool = False
        
        # Amenities
        has_cctv: bool = False
        has_lighting: bool = True
        has_roof: bool = False
        has_elevator: bool = False
        has_disabled_access: bool = False
        
        # Legacy field for backward compatibility
        price_per_hour: int = 0

    class RecommendResponseItem(BaseModel):
        lot: ParkingLot
        score: float
        distance_km: float
        estimated_price: Optional[int] = None

    class Envelope(BaseModel):
        ok: bool
        data: Optional[Any] = None
        error: Optional[Dict[str, Any]] = None

    # 인증 관련 모델
    class UserSignup(BaseModel):
        email: EmailStr
        password: str = Field(..., min_length=8)
        name: str = Field(..., min_length=2)
        age: Optional[int] = Field(None, ge=18, le=100)
        driving_years: Optional[int] = Field(None, ge=0, le=50)
        preferred_powertrain: Optional[str] = Field(None, pattern="^(ICE|EV)$")

    class UserLogin(BaseModel):
        email: EmailStr
        password: str

    class KakaoLoginRequest(BaseModel):
        kakao_id: str = Field(..., description="카카오 사용자 ID")
        email: Optional[str] = Field(None, description="이메일")
        nickname: Optional[str] = Field(None, description="닉네임")
        profile_image: Optional[str] = Field(None, description="프로필 이미지 URL")
        access_token: str = Field(..., description="카카오 액세스 토큰")

    class UserResponse(BaseModel):
        id: str
        email: str
        name: str
        age: Optional[int]
        driving_years: Optional[int]
        preferred_powertrain: Optional[str]
        created_at: str

    class AuthResponse(BaseModel):
        user: UserResponse
        access_token: str
        token_type: str = "bearer"

    # JWT 설정
    SECRET_KEY = "your-secret-key-here"  # 실제 환경에서는 환경변수로 관리
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    security = HTTPBearer()

    def create_access_token(data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
        try:
            payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id is None:
                raise HTTPException(status_code=401, detail="Invalid authentication credentials")
            return user_id
        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        R = 6371.0
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(math.radians(lat1))
            * math.cos(math.radians(lat2))
            * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    def calculate_current_pricing(pricing: DetailedPricing, is_weekend: bool = False, is_holiday: bool = False) -> tuple[int, int]:
        """현재 시간대에 맞는 요금 계산"""
        if is_holiday:
            return pricing.holiday_base, pricing.holiday_additional
        elif is_weekend:
            return pricing.weekend_base, pricing.weekend_additional
        else:
            return pricing.weekday_base, pricing.weekday_additional

    def calculate_estimated_price(pricing: DetailedPricing, hours: float, is_weekend: bool = False, is_holiday: bool = False) -> int:
        """예상 요금 계산"""
        base_price, additional_price = calculate_current_pricing(pricing, is_weekend, is_holiday)
        
        if hours <= 1.0:
            return base_price
        else:
            additional_hours = hours - 1.0
            additional_10min_units = math.ceil(additional_hours * 6)  # 10분 단위로 계산
            return base_price + (additional_10min_units * additional_price)

    def base_scores(req: RecommendRequest, lot: ParkingLot) -> Optional[Dict[str, float]]:
        distance_km = haversine_km(req.user_lat, req.user_lng, lot.lat, lot.lng)
        
        # 반경 체크
        if distance_km > req.search_radius_km:
            return None
            
        distance_score = max(0.0, 1.0 - min(distance_km / req.search_radius_km, 1.0))
        
        # 현재 시간대 요금으로 계산
        now = datetime.now()
        is_weekend = now.weekday() >= 5  # 토요일(5), 일요일(6)
        is_holiday = False  # 공휴일 체크 로직 추가 가능
        
        base_price, additional_price = calculate_current_pricing(lot.pricing, is_weekend, is_holiday)
        price_score = max(0.0, 1.0 - min(base_price / 6000.0, 1.0))
        
        # Hard filters
        if req.is_ev and not lot.ev_charging:
            return None
        if req.vehicle_height_m is not None and lot.height_limit_m is not None:
            if req.vehicle_height_m > lot.height_limit_m:
                return None
        if req.max_price_per_hour is not None and base_price > req.max_price_per_hour:
            return None
        if req.preferred_structure and lot.structure_type and lot.structure_type != req.preferred_structure:
            return None
            
        scores = {"distance": distance_score, "price": price_score}
        
        # 난이도 점수 추가
        if req.include_difficulty and lot.difficulty_score is not None:
            # 난이도가 낮을수록 높은 점수 (1 - difficulty_score/5)
            difficulty_score = max(0.0, 1.0 - (lot.difficulty_score / 5.0))
            scores["difficulty"] = difficulty_score
            
        return scores

    def compose_score(scores: Dict[str, float], is_ev: bool, lot: ParkingLot, 
                      w_distance: float, w_price: float, w_difficulty: float = 0.0) -> float:
        """개선된 점수 계산"""
        # 가중치 정규화
        total = max(w_distance + w_price + w_difficulty, 1e-6)
        wd = w_distance / total
        wp = w_price / total
        wdiff = w_difficulty / total
        
        # 기본 점수 계산
        score = wd * scores["distance"] + wp * scores["price"]
        if "difficulty" in scores:
            score += wdiff * scores["difficulty"]
            
        # 보너스 점수
        if lot.open_24h:
            score += 0.05
        if is_ev and lot.ev_charging:
            score += 0.1
        if lot.has_valet:
            score += 0.08
        if lot.has_attendant:
            score += 0.05
        if lot.has_cctv:
            score += 0.03
        if lot.has_lighting:
            score += 0.02
            
        return max(0.0, min(score, 1.0))

    try:
        from .supabase_client import get_supabase  # type: ignore
        supabase_client = get_supabase()
    except Exception:
        supabase_client = None

    @app.post("/recommend", response_model=Envelope)
    def recommend(req: RecommendRequest):
        try:
            # Default weights if user_settings not found
            weight_distance = 60.0
            weight_price = 40.0
            weight_difficulty = 0.0

            # Load user_settings by auth_user_id
            if supabase_client is not None and req.auth_user_id:
                try:
                    u_res = (
                        supabase_client
                        .table("users").select("id").eq("auth_user_id", req.auth_user_id).limit(1)
                        .execute()
                    )
                    u_list = u_res.data or []
                    user_id = u_list[0]["id"] if isinstance(u_list, list) and len(u_list) > 0 else None
                    if user_id:
                        s_res = (
                            supabase_client
                            .table("user_settings").select("weight_distance,weight_price,weight_difficulty").eq("user_id", user_id).limit(1)
                            .execute()
                        )
                        s_list = s_res.data or []
                        if isinstance(s_list, list) and len(s_list) > 0:
                            s0 = s_list[0]
                            weight_distance = float(s0.get("weight_distance", weight_distance))
                            weight_price = float(s0.get("weight_price", weight_price))
                            weight_difficulty = float(s0.get("weight_difficulty", weight_difficulty))
                except Exception:
                    pass

            candidates: List[ParkingLot] = []
            if supabase_client is not None:
                # PostGIS를 사용한 공간 쿼리
                query = supabase_client.table("parking_lots").select("*")
                
                # 반경 내 검색 (PostGIS 사용)
                radius_meters = req.search_radius_km * 1000
                query = query.filter("location", "st_dwithin", f"ST_GeogFromText('POINT({req.user_lng} {req.user_lat})'),{radius_meters}")
                
                if req.max_price_per_hour is not None:
                    query = query.lte("weekday_base_price", req.max_price_per_hour)
                if req.is_ev:
                    query = query.eq("ev_charging", True)
                if req.preferred_structure:
                    query = query.eq("structure_type", req.preferred_structure)
                    
                data = query.limit(200).execute().data or []
                
                for row in data:
                    try:
                        # 상세 요금 정보 구성
                        pricing = DetailedPricing(
                            weekday_base=row.get("weekday_base_price", 0),
                            weekday_additional=row.get("weekday_additional_price", 0),
                            weekday_daily_max=row.get("weekday_daily_max"),
                            weekday_night=row.get("weekday_night_price"),
                            weekend_base=row.get("weekend_base_price", 0),
                            weekend_additional=row.get("weekend_additional_price", 0),
                            weekend_daily_max=row.get("weekend_daily_max"),
                            weekend_night=row.get("weekend_night_price"),
                            holiday_base=row.get("holiday_base_price", 0),
                            holiday_additional=row.get("holiday_additional_price", 0),
                            holiday_daily_max=row.get("holiday_daily_max"),
                            holiday_night=row.get("holiday_night_price")
                        )
                        
                        candidates.append(
                            ParkingLot(
                                id=str(row.get("id")),
                                name=row.get("name") or "",
                                lat=float(row.get("lat")),
                                lng=float(row.get("lng")),
                                height_limit_m=(
                                    float(row.get("height_limit_m")) if row.get("height_limit_m") is not None else None
                                ),
                                ev_charging=bool(row.get("ev_charging")),
                                open_24h=bool(row.get("open_24h", True)),
                                pricing=pricing,
                                difficulty_score=(
                                    float(row.get("difficulty_score")) if row.get("difficulty_score") is not None else None
                                ),
                                structure_type=row.get("structure_type"),
                                capacity=row.get("capacity"),
                                entrance_width_m=(
                                    float(row.get("entrance_width_m")) if row.get("entrance_width_m") is not None else None
                                ),
                                exit_width_m=(
                                    float(row.get("exit_width_m")) if row.get("exit_width_m") is not None else None
                                ),
                                turning_radius_m=(
                                    float(row.get("turning_radius_m")) if row.get("turning_radius_m") is not None else None
                                ),
                                has_valet=bool(row.get("has_valet", False)),
                                has_attendant=bool(row.get("has_attendant", False)),
                                has_cctv=bool(row.get("has_cctv", False)),
                                has_lighting=bool(row.get("has_lighting", True)),
                                has_roof=bool(row.get("has_roof", False)),
                                has_elevator=bool(row.get("has_elevator", False)),
                                has_disabled_access=bool(row.get("has_disabled_access", False)),
                                price_per_hour=int(row.get("price_per_hour", 0))  # Legacy field
                            )
                        )
                    except Exception as e:
                        print(f"Error processing parking lot: {e}")
                        continue
            else:
                # 데이터베이스 연결 실패 시 빈 결과 반환
                candidates = []

            scored: List[RecommendResponseItem] = []
            for lot in candidates:
                s = base_scores(req, lot)
                if s is None:
                    continue
                    
                final_score = compose_score(s, req.is_ev, lot, weight_distance, weight_price, weight_difficulty)
                
                if final_score > 0:
                    distance_km = haversine_km(req.user_lat, req.user_lng, lot.lat, lot.lng)
                    estimated_price = calculate_estimated_price(lot.pricing, 2.0)  # 2시간 기준
                    
                    scored.append(RecommendResponseItem(
                        lot=lot,
                        score=final_score,
                        distance_km=distance_km,
                        estimated_price=estimated_price
                    ))

            scored.sort(key=lambda x: x.score, reverse=True)
            topk = scored[: req.limit]

            if supabase_client is not None:
                try:
                    supabase_client.table("search_logs").insert({
                        "user_id": None,
                        "user_lat": req.user_lat,
                        "user_lng": req.user_lng,
                        "is_ev": req.is_ev,
                        "vehicle_height_m": req.vehicle_height_m,
                        "max_price_per_hour": req.max_price_per_hour,
                        "results": [
                            {
                                "id": item.lot.id, 
                                "score": item.score, 
                                "distance_km": item.distance_km,
                                "estimated_price": item.estimated_price,
                                "price_per_hour": item.lot.price_per_hour
                            }
                            for item in topk
                        ],
                    }).execute()
                except Exception as e:
                    print(f"Error saving search log: {e}")

            return {"ok": True, "data": [item.model_dump() for item in topk]}
        except Exception as e:
            return {"ok": False, "error": {"message": str(e)}}

    @app.post("/log_selection", response_model=Envelope)
    def log_selection(search_log_id: str, selected_parking_lot_id: str):
        """사용자가 선택한 주차장 로깅"""
        try:
            if supabase_client is not None:
                supabase_client.table("search_logs").update({
                    "selected_parking_lot_id": selected_parking_lot_id,
                    "selection_timestamp": datetime.now().isoformat()
                }).eq("id", search_log_id).execute()
                
            return {"ok": True, "data": {"message": "Selection logged successfully"}}
        except Exception as e:
            return {"ok": False, "error": {"message": str(e)}}

    # 회원가입 API
    @app.post("/auth/signup", response_model=Envelope)
    def signup(user_data: UserSignup):
        """사용자 회원가입"""
        try:
            if supabase_client is None:
                return {"ok": False, "error": {"message": "Database connection failed"}}

            # 이메일 중복 체크
            existing_user = supabase_client.table("users").select("id").eq("email", user_data.email).execute()
            if existing_user.data:
                return {"ok": False, "error": {"message": "Email already registered"}}

            # 비밀번호 해시화
            hashed_password = hash_password(user_data.password)
            
            # 사용자 생성
            user_result = supabase_client.table("users").insert({
                "email": user_data.email,
                "password_hash": hashed_password,
                "name": user_data.name,
                "age": user_data.age,
                "driving_years": user_data.driving_years,
                "preferred_powertrain": user_data.preferred_powertrain,
                "created_at": datetime.now().isoformat()
            }).execute()

            if not user_result.data:
                return {"ok": False, "error": {"message": "Failed to create user"}}

            user = user_result.data[0]
            
            # JWT 토큰 생성
            access_token = create_access_token(data={"sub": str(user["id"])})
            
            # 사용자 설정 기본값 생성
            supabase_client.table("user_settings").insert({
                "user_id": user["id"],
                "weight_distance": 60,
                "weight_price": 40,
                "weight_difficulty": 0
            }).execute()

            return {
                "ok": True, 
                "data": {
                    "user": {
                        "id": user["id"],
                        "email": user["email"],
                        "name": user["name"],
                        "age": user["age"],
                        "driving_years": user["driving_years"],
                        "preferred_powertrain": user["preferred_powertrain"],
                        "created_at": user["created_at"]
                    },
                    "access_token": access_token,
                    "token_type": "bearer"
                }
            }
        except Exception as e:
            return {"ok": False, "error": {"message": str(e)}}

    # 로그인 API
    @app.post("/auth/login", response_model=Envelope)
    def login(login_data: UserLogin):
        """사용자 로그인"""
        try:
            if supabase_client is None:
                return {"ok": False, "error": {"message": "Database connection failed"}}

            # 사용자 조회
            user_result = supabase_client.table("users").select("*").eq("email", login_data.email).execute()
            
            if not user_result.data:
                return {"ok": False, "error": {"message": "Invalid email or password"}}

            user = user_result.data[0]
            
            # 비밀번호 확인
            hashed_password = hash_password(login_data.password)
            if user["password_hash"] != hashed_password:
                return {"ok": False, "error": {"message": "Invalid email or password"}}

            # JWT 토큰 생성
            access_token = create_access_token(data={"sub": str(user["id"])})

            return {
                "ok": True,
                "data": {
                    "user": {
                        "id": user["id"],
                        "email": user["email"],
                        "name": user["name"],
                        "age": user["age"],
                        "driving_years": user["driving_years"],
                        "preferred_powertrain": user["preferred_powertrain"],
                        "created_at": user["created_at"]
                    },
                    "access_token": access_token,
                    "token_type": "bearer"
                }
            }
        except Exception as e:
            return {"ok": False, "error": {"message": str(e)}}

    # 카카오 로그인 API
    @app.post("/auth/kakao", response_model=Envelope)
    def kakao_login(kakao_data: KakaoLoginRequest):
        """카카오 로그인/회원가입"""
        try:
            if supabase_client is None:
                return {"ok": False, "error": {"message": "Database connection failed"}}

            # 카카오 ID로 기존 사용자 조회
            existing_user = supabase_client.table("users").select("*").eq("kakao_id", kakao_data.kakao_id).execute()
            
            if existing_user.data:
                # 기존 사용자 로그인
                user = existing_user.data[0]
                access_token = create_access_token(data={"sub": str(user["id"])})
                
                return {
                    "ok": True,
                    "data": {
                        "user": {
                            "id": user["id"],
                            "email": user["email"],
                            "name": user["name"],
                            "nickname": user.get("nickname"),
                            "profile_image": user.get("profile_image"),
                            "age": user["age"],
                            "driving_years": user["driving_years"],
                            "preferred_powertrain": user["preferred_powertrain"],
                            "created_at": user["created_at"]
                        },
                        "access_token": access_token,
                        "token_type": "bearer"
                    }
                }
            else:
                # 새 사용자 회원가입
                user_result = supabase_client.table("users").insert({
                    "kakao_id": kakao_data.kakao_id,
                    "email": kakao_data.email,
                    "name": kakao_data.nickname or "카카오 사용자",
                    "nickname": kakao_data.nickname,
                    "profile_image": kakao_data.profile_image,
                    "created_at": datetime.now().isoformat()
                }).execute()

                if not user_result.data:
                    return {"ok": False, "error": {"message": "Failed to create user"}}

                user = user_result.data[0]
                access_token = create_access_token(data={"sub": str(user["id"])})
                
                # 사용자 설정 기본값 생성
                supabase_client.table("user_settings").insert({
                    "user_id": user["id"],
                    "weight_distance": 60,
                    "weight_price": 40,
                    "weight_difficulty": 0
                }).execute()

                return {
                    "ok": True,
                    "data": {
                        "user": {
                            "id": user["id"],
                            "email": user["email"],
                            "name": user["name"],
                            "nickname": user.get("nickname"),
                            "profile_image": user.get("profile_image"),
                            "age": user["age"],
                            "driving_years": user["driving_years"],
                            "preferred_powertrain": user["preferred_powertrain"],
                            "created_at": user["created_at"]
                        },
                        "access_token": access_token,
                        "token_type": "bearer"
                    }
                }
        except Exception as e:
            return {"ok": False, "error": {"message": str(e)}}

    # 사용자 정보 조회 API
    @app.get("/auth/me", response_model=Envelope)
    def get_current_user(user_id: str = Depends(verify_token)):
        """현재 로그인한 사용자 정보 조회"""
        try:
            if supabase_client is None:
                return {"ok": False, "error": {"message": "Database connection failed"}}

            user_result = supabase_client.table("users").select("*").eq("id", user_id).execute()
            
            if not user_result.data:
                return {"ok": False, "error": {"message": "User not found"}}

            user = user_result.data[0]
            
            return {
                "ok": True,
                "data": {
                    "id": user["id"],
                    "email": user["email"],
                    "name": user["name"],
                    "age": user["age"],
                    "driving_years": user["driving_years"],
                    "preferred_powertrain": user["preferred_powertrain"],
                    "created_at": user["created_at"]
                }
            }
        except Exception as e:
            return {"ok": False, "error": {"message": str(e)}}

    return app


app = create_app()

