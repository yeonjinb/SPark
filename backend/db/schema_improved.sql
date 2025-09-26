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
