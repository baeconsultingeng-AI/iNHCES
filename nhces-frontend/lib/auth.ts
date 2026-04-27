'use client';
import { createBrowserClient } from '@supabase/ssr';
import { setAuthToken } from './api';

const supabaseUrl  = process.env.NEXT_PUBLIC_SUPABASE_URL  ?? '';
const supabaseAnon = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY ?? '';

// True when real Supabase credentials are configured
export const SUPABASE_CONFIGURED =
  supabaseUrl.length > 0 &&
  !supabaseUrl.includes('placeholder') &&
  supabaseAnon.length > 0 &&
  !supabaseAnon.includes('placeholder');

export function createClient() {
  // Provide safe fallback values so the client can be created without crashing.
  // Actual API calls will fail — SUPABASE_CONFIGURED flag tells the UI to show
  // a "not configured" notice instead of submitting the form.
  const url  = supabaseUrl  || 'https://placeholder.supabase.co';
  const anon = supabaseAnon || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.placeholder.sig';
  return createBrowserClient(url, anon);
}

export async function getSession() {
  if (!SUPABASE_CONFIGURED) return null;
  const supabase = createClient();
  const { data: { session } } = await supabase.auth.getSession();
  if (session?.access_token) setAuthToken(session.access_token);
  return session;
}

export async function signIn(email: string, password: string) {
  if (!SUPABASE_CONFIGURED) {
    throw new Error('Supabase is not configured. Add NEXT_PUBLIC_SUPABASE_URL and NEXT_PUBLIC_SUPABASE_ANON_KEY to .env.local.');
  }
  const supabase = createClient();
  const { data, error } = await supabase.auth.signInWithPassword({ email, password });
  if (error) throw new Error(error.message);
  if (data.session?.access_token) setAuthToken(data.session.access_token);
  return data.session;
}

export async function signUp(
  email: string,
  password: string,
  fullName: string,
  institution: string,
  role: 'qsprofessional' | 'researcher',
) {
  if (!SUPABASE_CONFIGURED) {
    throw new Error('Supabase is not configured. Add NEXT_PUBLIC_SUPABASE_URL and NEXT_PUBLIC_SUPABASE_ANON_KEY to .env.local.');
  }
  const supabase = createClient();
  const { data, error } = await supabase.auth.signUp({
    email,
    password,
    options: {
      data: { full_name: fullName, institution, role },
    },
  });
  if (error) throw new Error(error.message);
  if (data.session?.access_token) setAuthToken(data.session.access_token);
  return data;
}

export async function signOut() {
  if (!SUPABASE_CONFIGURED) return;
  const supabase = createClient();
  setAuthToken(null);
  await supabase.auth.signOut();
}

export async function getCurrentUser() {
  if (!SUPABASE_CONFIGURED) return null;
  const supabase = createClient();
  const { data: { user } } = await supabase.auth.getUser();
  return user;
}
