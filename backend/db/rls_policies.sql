-- Enable RLS
alter table public.users enable row level security;
alter table public.vehicles enable row level security;
alter table public.favorites enable row level security;
alter table public.search_logs enable row level security;
alter table public.user_settings enable row level security;

-- Users: a user can see/update only their row
create policy if not exists "Users: owner access"
  on public.users for all
  using (auth.uid() = auth_user_id)
  with check (auth.uid() = auth_user_id);

-- Vehicles: owner only
create policy if not exists "Vehicles: owner access"
  on public.vehicles for all
  using (exists (select 1 from public.users u where u.id = user_id and u.auth_user_id = auth.uid()))
  with check (exists (select 1 from public.users u where u.id = user_id and u.auth_user_id = auth.uid()));

-- Favorites: owner only
create policy if not exists "Favorites: owner access"
  on public.favorites for all
  using (exists (select 1 from public.users u where u.id = user_id and u.auth_user_id = auth.uid()))
  with check (exists (select 1 from public.users u where u.id = user_id and u.auth_user_id = auth.uid()));

-- Search logs: owner read, insert own
create policy if not exists "SearchLogs: owner read"
  on public.search_logs for select using (exists (
    select 1 from public.users u where u.id = user_id and u.auth_user_id = auth.uid()
  ));
create policy if not exists "SearchLogs: insert own"
  on public.search_logs for insert with check (exists (
    select 1 from public.users u where u.id = user_id and u.auth_user_id = auth.uid()
  ));

-- User settings: owner only
create policy if not exists "UserSettings: owner access"
  on public.user_settings for all
  using (exists (select 1 from public.users u where u.id = user_id and u.auth_user_id = auth.uid()))
  with check (exists (select 1 from public.users u where u.id = user_id and u.auth_user_id = auth.uid()));
