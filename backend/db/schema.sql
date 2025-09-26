-- Supabase schema: users, vehicles, parking_lots, favorites, search_logs

create table if not exists public.users (
  id uuid primary key default gen_random_uuid(),
  email text unique not null,
  password_hash text not null,
  name text not null,
  age int,
  driving_years int,
  preferred_powertrain text check (preferred_powertrain in ('ICE','EV')),
  created_at timestamptz not null default now()
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

create table if not exists public.parking_lots (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  lat double precision not null,
  lng double precision not null,
  price_per_hour int not null,
  height_limit_m numeric(4,2),
  ev_charging boolean not null default false,
  open_24h boolean not null default true,
  created_at timestamptz not null default now()
);

create table if not exists public.favorites (
  user_id uuid not null references public.users(id) on delete cascade,
  parking_lot_id uuid not null references public.parking_lots(id) on delete cascade,
  created_at timestamptz not null default now(),
  primary key (user_id, parking_lot_id)
);

create table if not exists public.search_logs (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references public.users(id) on delete set null,
  user_lat double precision,
  user_lng double precision,
  is_ev boolean,
  vehicle_height_m numeric(4,2),
  max_price_per_hour int,
  results jsonb,
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

create index if not exists idx_parking_lots_location on public.parking_lots (lat, lng);
create index if not exists idx_parking_lots_price on public.parking_lots (price_per_hour);
create unique index if not exists uq_user_settings_user on public.user_settings(user_id);
