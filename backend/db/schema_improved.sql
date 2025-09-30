-- Improved Supabase schema with enhanced pricing, difficulty, and PostGIS support

-- Enable PostGIS extension for spatial queries
create extension if not exists postgis;

create table if not exists public.users (
  id uuid primary key default gen_random_uuid(),
  auth_user_id uuid unique not null,
  name text,
  age int,
  driving_years int,
  preferred_powertrain text check (preferred_powertrain in ('ICE','EV')),
  created_at timestamptz not null default now()
);

-- Car models reference table with height data
create table if not exists public.car_models (
  id uuid primary key default gen_random_uuid(),
  make text not null,
  model text not null,
  height_m numeric(4,2) not null,
  category text not null,
  created_at timestamptz not null default now(),
  unique(make, model)
);

create table if not exists public.vehicles (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references public.users(id) on delete cascade,
  make text,
  model text,
  plate_number text,
  powertrain text check (powertrain in ('ICE','EV')),
  height_m numeric(4,2),
  created_at timestamptz not null default now()
);

-- Enhanced parking_lots table with detailed pricing and difficulty
create table if not exists public.parking_lots (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  lat double precision not null,
  lng double precision not null,
  location geography(point, 4326), -- PostGIS geography column for spatial queries
  
  -- Basic info
  height_limit_m numeric(4,2),
  ev_charging boolean not null default false,
  open_24h boolean not null default true,
  
  -- Detailed pricing structure
  -- Weekday pricing
  weekday_base_price int not null default 0,        -- 기본요금 (원)
  weekday_additional_price int not null default 0,  -- 추가요금 (원/10분)
  weekday_daily_max int,                           -- 1일 최대요금 (원)
  weekday_night_price int,                         -- 심야요금 (원/10분, 22:00-06:00)
  
  -- Weekend pricing
  weekend_base_price int not null default 0,
  weekend_additional_price int not null default 0,
  weekend_daily_max int,
  weekend_night_price int,
  
  -- Holiday pricing
  holiday_base_price int not null default 0,
  holiday_additional_price int not null default 0,
  holiday_daily_max int,
  holiday_night_price int,
  
  -- Legacy field for backward compatibility
  price_per_hour int not null default 0,
  
  -- Difficulty and structure info
  difficulty_score numeric(3,2) check (difficulty_score >= 0 and difficulty_score <= 5), -- 0-5 난이도 점수
  structure_type text check (structure_type in ('GROUND', 'UNDERGROUND', 'ELEVATED', 'MIXED')), -- 구조 유형
  capacity int,                                    -- 수용 가능 차량 수
  entrance_width_m numeric(4,2),                  -- 진입로 폭 (m)
  exit_width_m numeric(4,2),                      -- 출구 폭 (m)
  turning_radius_m numeric(4,2),                  -- 회전 반경 (m)
  has_valet boolean not null default false,       -- 발렛파킹 여부
  has_attendant boolean not null default false,   -- 관리인 상주 여부
  
  -- Additional amenities
  has_cctv boolean not null default false,
  has_lighting boolean not null default true,
  has_roof boolean not null default false,
  has_elevator boolean not null default false,
  has_disabled_access boolean not null default false,
  
  created_at timestamptz not null default now()
);

create table if not exists public.favorites (
  user_id uuid not null references public.users(id) on delete cascade,
  parking_lot_id uuid not null references public.parking_lots(id) on delete cascade,
  created_at timestamptz not null default now(),
  primary key (user_id, parking_lot_id)
);

-- Enhanced search_logs with selection tracking
create table if not exists public.search_logs (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references public.users(id) on delete set null,
  user_lat double precision,
  user_lng double precision,
  is_ev boolean,
  vehicle_height_m numeric(4,2),
  max_price_per_hour int,
  results jsonb,
  selected_parking_lot_id uuid references public.parking_lots(id) on delete set null, -- 선택된 주차장
  selection_timestamp timestamptz, -- 선택 시점
  search_duration_ms int, -- 검색 소요 시간 (밀리초)
  created_at timestamptz not null default now()
);

create table if not exists public.user_settings (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references public.users(id) on delete cascade,
  weight_price int not null default 40,     -- 0..100
  weight_distance int not null default 60,  -- 0..100
  weight_difficulty int not null default 0, -- 0..100 (미사용시 0)
  created_at timestamptz not null default now()
);

-- PostGIS spatial indexes for optimized distance queries
create index if not exists idx_parking_lots_location_postgis on public.parking_lots using gist (location);
create index if not exists idx_parking_lots_location_btree on public.parking_lots (lat, lng);

-- Pricing indexes
create index if not exists idx_parking_lots_weekday_price on public.parking_lots (weekday_base_price, weekday_additional_price);
create index if not exists idx_parking_lots_weekend_price on public.parking_lots (weekend_base_price, weekend_additional_price);
create index if not exists idx_parking_lots_holiday_price on public.parking_lots (holiday_base_price, holiday_additional_price);

-- Difficulty and structure indexes
create index if not exists idx_parking_lots_difficulty on public.parking_lots (difficulty_score);
create index if not exists idx_parking_lots_structure on public.parking_lots (structure_type);
create index if not exists idx_parking_lots_capacity on public.parking_lots (capacity);

-- EV charging index
create index if not exists idx_parking_lots_ev on public.parking_lots (ev_charging) where ev_charging = true;

-- Search logs indexes
create index if not exists idx_search_logs_user on public.search_logs (user_id);
create index if not exists idx_search_logs_selected on public.search_logs (selected_parking_lot_id);
create index if not exists idx_search_logs_created on public.search_logs (created_at);

-- User settings index
create unique index if not exists uq_user_settings_user on public.user_settings(user_id);

-- Car models index for fast lookup
create index if not exists idx_car_models_make_model on public.car_models (make, model);

-- Insert Korean major car height data
insert into public.car_models (make, model, height_m, category) values
-- Hyundai
('Hyundai', 'Avante', 1.43, 'Mid-size Sedan'),
('Hyundai', 'Sonata', 1.45, 'Mid-size Sedan'),
('Hyundai', 'Grandeur', 1.47, 'Full-size Sedan'),
('Hyundai', 'Aslan', 1.47, 'Full-size Sedan'),
('Hyundai', 'i30', 1.47, 'Mid-size Hatchback'),
('Hyundai', 'Venue', 1.56, 'Compact SUV'),
('Hyundai', 'Kona', 1.57, 'Compact SUV'),
('Hyundai', 'Tucson', 1.65, 'Mid-size SUV'),
('Hyundai', 'Santa Fe', 1.68, 'Large SUV'),
('Hyundai', 'Palisade', 1.75, 'Full-size SUV'),
('Hyundai', 'Staria', 1.99, 'MPV'),

-- Kia
('Kia', 'K3', 1.45, 'Mid-size Sedan'),
('Kia', 'K5', 1.45, 'Mid-size Sedan'),
('Kia', 'K8', 1.47, 'Full-size Sedan'),
('Kia', 'K9', 1.49, 'Full-size Sedan'),
('Kia', 'Morning', 1.49, 'Microcar'),
('Kia', 'Picanto', 1.49, 'Microcar'),
('Kia', 'Ray', 1.72, 'Tall Microcar'),
('Kia', 'Niro', 1.55, 'Compact SUV'),
('Kia', 'Seltos', 1.62, 'Compact SUV'),
('Kia', 'Sportage', 1.65, 'Mid-size SUV'),
('Kia', 'Sorento', 1.70, 'Large SUV'),
('Kia', 'Mohave', 1.76, 'Full-size SUV'),
('Kia', 'Carnival', 1.75, 'MPV'),

-- Genesis
('Genesis', 'G70', 1.40, 'Mid-size Sedan'),
('Genesis', 'G80', 1.47, 'Full-size Sedan'),
('Genesis', 'G90', 1.49, 'Full-size Sedan'),
('Genesis', 'GV60', 1.58, 'Compact SUV'),
('Genesis', 'GV70', 1.63, 'Mid-size SUV'),
('Genesis', 'GV80', 1.71, 'Large SUV'),

-- Tesla
('Tesla', 'Model 3', 1.44, 'Mid-size Sedan'),
('Tesla', 'Model Y', 1.62, 'Mid-size SUV'),
('Tesla', 'Model S', 1.45, 'Full-size Sedan'),
('Tesla', 'Model X', 1.68, 'Large SUV'),

-- BMW
('BMW', '3 Series (G20)', 1.45, 'Mid-size Sedan'),
('BMW', '5 Series (G30)', 1.48, 'Full-size Sedan'),
('BMW', '7 Series (G70)', 1.54, 'Full-size Sedan'),
('BMW', 'X1', 1.61, 'Compact SUV'),
('BMW', 'X3', 1.67, 'Mid-size SUV'),
('BMW', 'X5', 1.75, 'Large SUV'),

-- Mercedes-Benz
('Mercedes-Benz', 'C-Class (W206)', 1.45, 'Mid-size Sedan'),
('Mercedes-Benz', 'E-Class (W213)', 1.47, 'Full-size Sedan'),
('Mercedes-Benz', 'S-Class (W223)', 1.50, 'Full-size Sedan'),
('Mercedes-Benz', 'GLC', 1.64, 'Mid-size SUV'),
('Mercedes-Benz', 'GLE', 1.77, 'Large SUV'),

-- Audi
('Audi', 'A4', 1.43, 'Mid-size Sedan'),
('Audi', 'A6', 1.46, 'Full-size Sedan'),
('Audi', 'A8', 1.48, 'Full-size Sedan'),
('Audi', 'Q3', 1.62, 'Compact SUV'),
('Audi', 'Q5', 1.65, 'Mid-size SUV'),
('Audi', 'Q7', 1.74, 'Large SUV'),

-- Other Popular Imports
('VW', 'Golf', 1.45, 'Hatchback'),
('VW', 'Tiguan', 1.67, 'Mid-size SUV'),
('Toyota', 'Camry', 1.45, 'Mid-size Sedan'),
('Toyota', 'RAV4', 1.69, 'Mid-size SUV'),
('Honda', 'Accord', 1.45, 'Mid-size Sedan'),
('Honda', 'CR-V', 1.68, 'Large SUV'),
('Ford', 'Explorer', 1.78, 'Large SUV'),
('Lincoln', 'Navigator', 1.76, 'Large SUV')
on conflict (make, model) do nothing;

-- Function to update location geography when lat/lng changes
create or replace function update_parking_lot_location()
returns trigger as $$
begin
  new.location = st_setsrid(st_makepoint(new.lng, new.lat), 4326)::geography;
  return new;
end;
$$ language plpgsql;

-- Trigger to automatically update geography column
create trigger trigger_update_parking_lot_location
  before insert or update of lat, lng on public.parking_lots
  for each row execute function update_parking_lot_location();

-- Trigger to automatically fill vehicle height
create trigger trigger_auto_fill_vehicle_height
  before insert or update of make, model, height_m on public.vehicles
  for each row execute function auto_fill_vehicle_height();

-- Function to calculate distance between two points (in meters)
create or replace function calculate_distance_meters(
  lat1 double precision, lng1 double precision,
  lat2 double precision, lng2 double precision
)
returns double precision as $$
begin
  return st_distance(
    st_setsrid(st_makepoint(lng1, lat1), 4326)::geography,
    st_setsrid(st_makepoint(lng2, lat2), 4326)::geography
  );
end;
$$ language plpgsql;

-- Function to auto-fill vehicle height based on make and model
create or replace function auto_fill_vehicle_height()
returns trigger as $$
declare
  car_height numeric(4,2);
begin
  -- Only auto-fill if height_m is null and both make and model are provided
  if new.height_m is null and new.make is not null and new.model is not null then
    -- Look up height from car_models table
    select height_m into car_height
    from public.car_models
    where make = new.make and model = new.model;
    
    -- If found, set the height
    if car_height is not null then
      new.height_m = car_height;
    end if;
  end if;
  
  return new;
end;
$$ language plpgsql;

-- Insert actual Seoul Gwangjin-gu parking lot data (20 locations)
-- Based on real Excel data with 30-minute base fare + 5-minute additional fare structure

insert into public.parking_lots (
  name, lat, lng, height_limit_m, ev_charging, open_24h,
  weekday_base_price, weekday_additional_price, weekday_daily_max,
  weekend_base_price, weekend_additional_price, weekend_daily_max,
  price_per_hour, difficulty_score, structure_type, capacity,
  has_roof, has_elevator, has_disabled_access, has_cctv, has_lighting
) values

-- 1. 능동공영 (EV charging available, 24h, discounts for disabled/children)
('능동공영', 37.554161, 127.080178, 2.1, true, true,
 1800, 300, null,  -- Weekday: 30min=1800원, 5min=300원
 1800, 300, null,  -- Weekend: same as weekday
 3600, 2.0, 'GROUND', 77,
 true, false, true, true, true),

-- 2. 자양전통시장 공영 (No EV, limited hours, no discounts)
('자양전통시장 공영', 37.536635, 127.06509, 2.2, false, false,
 2250, 375, null,  -- Weekday: 30min=2250원, 5min=375원
 2250, 375, null,  -- Weekend: same as weekday
 4500, 2.0, 'GROUND', 24,
 true, false, false, true, true),

-- 3. 자양4동 공영 (EV charging, 24h)
('자양4동 공영', 37.538793, 127.068189, null, true, true,
 2250, 375, null,  -- Weekday: 30min=2250원, 5min=375원
 2250, 375, null,  -- Weekend: same as weekday
 4500, 1.0, 'GROUND', 83,
 false, false, false, true, true),

-- 4. 화양동 공영 (EV charging, 24h, multiple discounts)
('화양동 공영', 37.545499, 127.071053, 2.1, true, true,
 1800, 300, null,  -- Weekday: 30min=1800원, 5min=300원
 1800, 300, null,  -- Weekend: same as weekday
 3600, 3.0, 'GROUND', 44,
 true, false, true, true, true),

-- 5. 광진광장 공영 (No EV, 24h)
('광진광장 공영', 37.547903, 127.073174, 2.0, false, true,
 2250, 375, null,  -- Weekday: 30min=2250원, 5min=375원
 2250, 375, null,  -- Weekend: same as weekday
 4500, 1.0, 'GROUND', 36,
 false, false, false, true, true),

-- 6. 어린이대공원 정문 주차장 (No EV, limited hours, discounts)
('어린이대공원 정문 주차장', 37.552059, 127.076285, null, false, false,
 1350, 225, null,  -- Weekday: 30min=1350원, 5min=225원
 1350, 225, null,  -- Weekend: same as weekday
 2700, 1.0, 'GROUND', 335,
 false, false, true, true, true),

-- 7. 어린이대공원 후문 주차장 (EV charging, limited hours, discounts)
('어린이대공원 후문 주차장', 37.551929, 127.087462, null, true, false,
 1350, 225, null,  -- Weekday: 30min=1350원, 5min=225원
 1350, 225, null,  -- Weekend: same as weekday
 2700, 1.0, 'GROUND', 250,
 false, false, true, true, true),

-- 8. 광진정보도서관 주차장 (EV charging, 24h, discounts)
('광진정보도서관 주차장', 37.55118, 127.110693, 2.1, true, true,
 1350, 225, null,  -- Weekday: 30min=1350원, 5min=225원
 1350, 225, null,  -- Weekend: same as weekday
 2700, 2.0, 'UNDERGROUND', 14,
 true, true, true, true, true),

-- 9. 송림 기사식당길 공영주차장 (EV charging, limited hours, discounts)
('송림 기사식당길 공영주차장', 37.534678, 127.076117, null, true, false,
 1800, 300, null,  -- Weekday: 30min=1800원, 5min=300원
 1800, 300, null,  -- Weekend: same as weekday
 3600, 2.0, 'GROUND', 1,
 false, false, true, true, true),

-- 10. 송림기사식당길(B) 공영주차장 (EV charging, limited hours, discounts)
('송림기사식당길(B) 공영주차장', 37.537368, 127.076519, null, true, false,
 1800, 300, null,  -- Weekday: 30min=1800원, 5min=300원
 1800, 300, null,  -- Weekend: same as weekday
 3600, 2.0, 'GROUND', 1,
 false, false, true, true, true),

-- 11. 자양유수지 공영주차장 (EV charging, 24h)
('자양유수지 공영주차장', 37.529884, 127.077604, null, true, true,
 1800, 300, null,  -- Weekday: 30min=1800원, 5min=300원
 1800, 300, null,  -- Weekend: same as weekday
 3600, 1.0, 'GROUND', 281,
 false, false, false, true, true),

-- 12. 동서울호텔길 노상공영주차장 (EV charging, 24h, premium pricing)
('동서울호텔길 노상공영주차장', 37.533539, 127.091273, null, true, true,
 2700, 450, null,  -- Weekday: 30min=2700원, 5min=450원 (premium)
 2700, 450, null,  -- Weekend: same as weekday
 5400, 2.0, 'GROUND', 1,
 false, false, false, true, true),

-- 13. 건국대병원주차장 (EV charging, limited hours, disabled discount)
('건국대병원주차장', 37.540604, 127.072128, 2.1, true, false,
 2250, 375, null,  -- Weekday: 30min=2250원, 5min=375원
 2250, 375, null,  -- Weekend: same as weekday
 4500, 1.0, 'UNDERGROUND', 655,
 true, true, true, true, true),

-- 14. 한림타워민영주차장 (EV charging, 24h, premium)
('한림타워민영주차장', 37.540943, 127.069157, 2.2, true, true,
 2250, 375, null,  -- Weekday: 30min=2250원, 5min=375원
 2250, 375, null,  -- Weekend: same as weekday
 4500, 2.0, 'UNDERGROUND', null,
 true, true, false, true, true),

-- 15. 건국대서울캠퍼스주차장 (No EV, 24h, high pricing)
('건국대서울캠퍼스주차장', 37.542575, 127.07376, 2.3, false, true,
 3000, 500, null,  -- Weekday: 30min=3000원, 5min=500원 (high)
 3000, 500, null,  -- Weekend: same as weekday
 6000, 1.0, 'GROUND', null,
 false, false, false, true, true),

-- 16. 가나주차장 (No EV, 24h, premium)
('가나주차장', 37.541302, 127.069866, 2.4, false, true,
 2998, 500, null,  -- Weekday: 30min=2998원, 5min=500원
 2998, 500, null,  -- Weekend: same as weekday
 5996, 2.0, 'UNDERGROUND', 30,
 true, true, false, true, true),

-- 17. 스타시티주차장 (No EV, 24h, premium pricing, large capacity)
('스타시티주차장', 37.537964, 127.072702, 2.5, false, true,
 4500, 750, null,  -- Weekday: 30min=4500원, 5min=750원 (premium)
 4500, 750, null,  -- Weekend: same as weekday
 9000, 1.0, 'UNDERGROUND', 1452,
 true, true, false, true, true),

-- 18. 한아름민영주차장 (No EV, 24h, mid-range pricing)
('한아름민영주차장', 37.543689, 127.069895, null, false, true,
 2500, 417, null,  -- Weekday: 30min=2500원, 5min=417원
 2500, 417, null,  -- Weekend: same as weekday
 5000, 2.0, 'GROUND', null,
 false, false, false, true, true),

-- 19. 동신민영주차장 (No EV, limited hours, mid-range pricing)
('동신민영주차장', 37.542558, 127.06471, null, false, false,
 2250, 375, null,  -- Weekday: 30min=2250원, 5min=375원
 2250, 375, null,  -- Weekend: same as weekday
 4500, 2.0, 'UNDERGROUND', null,
 true, true, false, true, true),

-- 20. 아이파킹 동도센트리움캠퍼스파크 주차장 (No EV, 24h, height restricted)
('아이파킹 동도센트리움캠퍼스파크 주차장', 37.54781, 127.07091, 1.55, false, true,
 2250, 375, null,  -- Weekday: 30min=2250원, 5min=375원
 2250, 375, null,  -- Weekend: same as weekday
 4500, 3.0, 'UNDERGROUND', 132,
 true, true, false, true, true)

on conflict (name, lat, lng) do nothing;

-- Create discount policies table for parking lots
create table if not exists public.parking_discounts (
  id uuid primary key default gen_random_uuid(),
  parking_lot_id uuid not null references public.parking_lots(id) on delete cascade,
  discount_type text not null check (discount_type in ('DISABLED', 'ECO_CAR', 'TWO_CHILDREN', 'THREE_CHILDREN')),
  discount_rate int not null check (discount_rate >= 0 and discount_rate <= 100), -- 할인율 (%)
  description text,
  created_at timestamptz not null default now(),
  unique(parking_lot_id, discount_type)
);

-- Insert discount policies for parking lots
insert into public.parking_discounts (parking_lot_id, discount_type, discount_rate, description) 
select 
  pl.id,
  discount_type,
  discount_rate,
  description
from public.parking_lots pl,
(values
  ('DISABLED', 80, '장애인 할인'),
  ('TWO_CHILDREN', 30, '2자녀 할인'),
  ('THREE_CHILDREN', 50, '3자녀 이상 할인')
) as discounts(discount_type, discount_rate, description)
where pl.name in ('능동공영');

insert into public.parking_discounts (parking_lot_id, discount_type, discount_rate, description) 
select 
  pl.id,
  discount_type,
  discount_rate,
  description
from public.parking_lots pl,
(values
  ('DISABLED', 80, '장애인 할인'),
  ('ECO_CAR', 50, '친환경차 할인'),
  ('TWO_CHILDREN', 30, '2자녀 할인'),
  ('THREE_CHILDREN', 50, '3자녀 이상 할인')
) as discounts(discount_type, discount_rate, description)
where pl.name in ('화양동 공영');

insert into public.parking_discounts (parking_lot_id, discount_type, discount_rate, description) 
select 
  pl.id,
  discount_type,
  discount_rate,
  description
from public.parking_lots pl,
(values
  ('DISABLED', 80, '장애인 할인'),
  ('ECO_CAR', 50, '친환경차 할인'),
  ('THREE_CHILDREN', 50, '3자녀 이상 할인')
) as discounts(discount_type, discount_rate, description)
where pl.name in ('어린이대공원 정문 주차장', '어린이대공원 후문 주차장');

insert into public.parking_discounts (parking_lot_id, discount_type, discount_rate, description) 
select 
  pl.id,
  discount_type,
  discount_rate,
  description
from public.parking_lots pl,
(values
  ('DISABLED', 80, '장애인 할인'),
  ('ECO_CAR', 50, '친환경차 할인'),
  ('TWO_CHILDREN', 30, '2자녀 할인'),
  ('THREE_CHILDREN', 50, '3자녀 이상 할인')
) as discounts(discount_type, discount_rate, description)
where pl.name in ('광진정보도서관 주차장', '송림 기사식당길 공영주차장', '송림기사식당길(B) 공영주차장');

insert into public.parking_discounts (parking_lot_id, discount_type, discount_rate, description) 
select 
  pl.id,
  discount_type,
  discount_rate,
  description
from public.parking_lots pl,
(values
  ('DISABLED', 50, '장애인 할인')
) as discounts(discount_type, discount_rate, description)
where pl.name in ('건국대병원주차장');

-- Create indexes for discount queries
create index if not exists idx_parking_discounts_lot on public.parking_discounts (parking_lot_id);
create index if not exists idx_parking_discounts_type on public.parking_discounts (discount_type);

-- Create monthly pass table for parking lots
create table if not exists public.monthly_passes (
  id uuid primary key default gen_random_uuid(),
  parking_lot_id uuid not null references public.parking_lots(id) on delete cascade,
  pass_type text not null check (pass_type in ('MONTHLY', 'QUARTERLY', 'YEARLY')),
  price int not null check (price > 0), -- 정기권 가격 (원)
  description text,
  is_active boolean not null default true,
  created_at timestamptz not null default now(),
  unique(parking_lot_id, pass_type)
);

-- Insert monthly pass data for public parking lots with realistic pricing
insert into public.monthly_passes (parking_lot_id, pass_type, price, description) 
select 
  pl.id,
  'MONTHLY',
  price,
  description
from public.parking_lots pl,
(values
  ('능동공영',NULL,'월정기권(공영할인)')
  ('자양전통시장 공영',50000, '월정기권 (공영할인)'),
  ('화양동 공영', 100000, '월정기권 (공영할인)'),
  ('자양유수지 공영주차장', 100000, '월정기권 (공영할인)'),
  ('광진정보도서관 주차장', 90000, '월정기권 (도서관할인)'),
  ('어린이대공원 정문 주차장', 100000, '월정기권 (공원할인)'),
  ('어린이대공원 후문 주차장', 100000, '월정기권 (공원할인)'),
  ('자양4동 공영주차장',130000,'월정기권(공영할인)'),
  ('광진광장',NULL,'월정기권(공영할인)'),
  ('송림 기사식당길 공영주차장(구)',90000,'월정기권(공영할인)')
  ('송림기사식당길(B) 공영주차장',90000,'월정기권(공영할인)')  
  ('건국대병원주차장',110000,'월정기권(병원할인)'),
  ('한림타워민영주차장',NULL,'월정기권(민영할인)'),
  ('건국대서울캠퍼스주차장',110000,'월정기권(대학교할인)'),
  ('스타시티주차장',NULL,'월정기권(프리미엄할인)'),
  ('한아름민영주차장',99000,'월정기권(민영할인)'),
  ('동신민영주차장',NULL,'월정기권(민영할인)'),
  ('아이파킹 동도센트리움캠퍼스파크 주차장',99000,'월정기권(프리미엄할인)')


) as passes(parking_name, price, description)
where pl.name = passes.parking_name;

-- Create indexes for monthly pass queries
create index if not exists idx_monthly_passes_lot on public.monthly_passes (parking_lot_id);
create index if not exists idx_monthly_passes_type on public.monthly_passes (pass_type);
create index if not exists idx_monthly_passes_active on public.monthly_passes (is_active) where is_active = true;

-- Summary of inserted data:
/*
INSERTED PARKING LOT DATA (20 locations):

1. 능동공영 - EV ✓, 24h ✓, 장애인/다자녀 할인
2. 자양전통시장 공영 - No EV, 시간제한, 할인 없음
3. 자양4동 공영 - EV ✓, 24h ✓
4. 화양동 공영 - EV ✓, 24h ✓, 모든 할인
5. 광진광장 공영 - No EV, 24h ✓
6. 어린이대공원 정문 - No EV, 시간제한, 장애인/친환경/3자녀 할인
7. 어린이대공원 후문 - EV ✓, 시간제한, 장애인/친환경/3자녀 할인
8. 광진정보도서관 - EV ✓, 24h ✓, 모든 할인
9. 송림 기사식당길 - EV ✓, 시간제한, 모든 할인
10. 송림기사식당길(B) - EV ✓, 시간제한, 모든 할인
11. 자양유수지 공영 - EV ✓, 24h ✓
12. 동서울호텔길 - EV ✓, 24h ✓, 프리미엄 요금
13. 건국대병원 - EV ✓, 시간제한, 장애인 할인
14. 한림타워민영 - EV ✓, 24h ✓
15. 건국대서울캠퍼스 - No EV, 24h ✓, 고가
16. 가나주차장 - No EV, 24h ✓, 프리미엄
17. 스타시티주차장 - No EV, 24h ✓, 최고가, 대용량
18. 한아름민영 - No EV, 24h ✓
19. 동신민영 - No EV, 시간제한
20. 아이파킹 동도센트리움 - No EV, 24h ✓, 높이제한 1.55m

PRICING STRUCTURE:
- 모든 주차장: 30분 기본요금 + 5분당 추가요금
- 요금대: 1,350원~4,500원 (30분 기준)
- 추가요금: 225원~750원 (5분당)

FEATURES:
- 전기차 충전: 12개소 (60%)
- 24시간 운영: 13개소 (65%)
- 지하주차장: 8개소 (40%)
- 할인 혜택: 8개소 (40%)
*/