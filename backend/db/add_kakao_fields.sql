-- Add Kakao login fields to users table
ALTER TABLE public.users 
ADD COLUMN IF NOT EXISTS kakao_id text unique,
ADD COLUMN IF NOT EXISTS nickname text,
ADD COLUMN IF NOT EXISTS profile_image text;

-- Make email and password_hash nullable for Kakao users
ALTER TABLE public.users 
ALTER COLUMN email DROP NOT NULL,
ALTER COLUMN password_hash DROP NOT NULL;

-- Add constraint to ensure either email/password or kakao_id is provided
ALTER TABLE public.users 
ADD CONSTRAINT check_auth_method 
CHECK (
  (email IS NOT NULL AND password_hash IS NOT NULL) OR 
  kakao_id IS NOT NULL
);

-- Create index for kakao_id lookups
CREATE INDEX IF NOT EXISTS idx_users_kakao_id ON public.users (kakao_id);
