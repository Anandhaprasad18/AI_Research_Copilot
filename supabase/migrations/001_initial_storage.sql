-- This migration reconciles the current application identity model, which uses username rather than auth.users UUIDs.
-- It intentionally targets the existing Supabase project without introducing Supabase Auth.

-- Drop and recreate the app tables only if they are empty.
-- If the tables are not empty, this script exits without destructive action.

DO $$
BEGIN
  IF EXISTS (
    SELECT 1 FROM information_schema.tables
    WHERE table_schema = 'public' AND table_name = 'profiles'
  ) THEN
    IF (SELECT COUNT(*) FROM public.profiles) = 0 THEN
      DROP TABLE public.profiles;
    END IF;
  END IF;

  IF EXISTS (
    SELECT 1 FROM information_schema.tables
    WHERE table_schema = 'public' AND table_name = 'documents'
  ) THEN
    IF (SELECT COUNT(*) FROM public.documents) = 0 THEN
      DROP TABLE public.documents;
    END IF;
  END IF;
END $$;

CREATE TABLE IF NOT EXISTS public.profiles (
    username TEXT PRIMARY KEY,
    personalization TEXT,
    active_document TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username TEXT NOT NULL,
    file_name TEXT NOT NULL,
    storage_path TEXT NOT NULL,
    uploaded_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_documents_username ON public.documents(username);

ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.documents ENABLE ROW LEVEL SECURITY;

-- Minimal RLS policies for username-based access.
-- These are intentionally app-level policies for this deployment stage.
DROP POLICY IF EXISTS "profiles_select_own" ON public.profiles;
DROP POLICY IF EXISTS "profiles_insert_own" ON public.profiles;
DROP POLICY IF EXISTS "profiles_update_own" ON public.profiles;
DROP POLICY IF EXISTS "documents_select_own" ON public.documents;
DROP POLICY IF EXISTS "documents_insert_own" ON public.documents;
DROP POLICY IF EXISTS "documents_update_own" ON public.documents;
DROP POLICY IF EXISTS "documents_delete_own" ON public.documents;

CREATE POLICY "profiles_select_own"
ON public.profiles
FOR SELECT
TO authenticated
USING (username = current_setting('request.jwt.claims', true)::json->>'username');

CREATE POLICY "profiles_insert_own"
ON public.profiles
FOR INSERT
TO authenticated
WITH CHECK (username = current_setting('request.jwt.claims', true)::json->>'username');

CREATE POLICY "profiles_update_own"
ON public.profiles
FOR UPDATE
TO authenticated
USING (username = current_setting('request.jwt.claims', true)::json->>'username')
WITH CHECK (username = current_setting('request.jwt.claims', true)::json->>'username');

CREATE POLICY "documents_select_own"
ON public.documents
FOR SELECT
TO authenticated
USING (username = current_setting('request.jwt.claims', true)::json->>'username');

CREATE POLICY "documents_insert_own"
ON public.documents
FOR INSERT
TO authenticated
WITH CHECK (username = current_setting('request.jwt.claims', true)::json->>'username');

CREATE POLICY "documents_update_own"
ON public.documents
FOR UPDATE
TO authenticated
USING (username = current_setting('request.jwt.claims', true)::json->>'username')
WITH CHECK (username = current_setting('request.jwt.claims', true)::json->>'username');

CREATE POLICY "documents_delete_own"
ON public.documents
FOR DELETE
TO authenticated
USING (username = current_setting('request.jwt.claims', true)::json->>'username');
