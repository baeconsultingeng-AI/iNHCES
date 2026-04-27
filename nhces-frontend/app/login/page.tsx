'use client';
import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { GS, COLOURS } from '@/lib/styles';
import Button from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { signIn, SUPABASE_CONFIGURED } from '@/lib/auth';

export default function LoginPage() {
  const router = useRouter();
  const [email,    setEmail]    = useState('');
  const [password, setPassword] = useState('');
  const [loading,  setLoading]  = useState(false);
  const [error,    setError]    = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    if (!email || !password) { setError('Email and password are required.'); return; }
    setLoading(true);
    try {
      await signIn(email, password);
      router.push('/dashboard');
      router.refresh();
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Login failed.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{
      height:         'calc(100vh - 60px)',
      background:     COLOURS.background,
      display:        'flex',
      alignItems:     'center',
      justifyContent: 'center',
      padding:        24,
    }}>
      <div style={{
        background:   COLOURS.surface,
        border:       `1px solid ${COLOURS.border}`,
        borderRadius: 16,
        padding:      '40px 44px',
        width:        '100%',
        maxWidth:     420,
        boxShadow:    '0 4px 24px rgba(26,20,16,0.08)',
      }}
           className="anim">

        {/* Dev mode notice when Supabase not configured */}
        {!SUPABASE_CONFIGURED && (
          <div style={{
            background:   COLOURS.amberLight,
            border:       `1px solid ${COLOURS.amber}`,
            borderRadius: 10,
            padding:      '10px 14px',
            marginBottom: 20,
            fontSize:     13,
            color:        COLOURS.amber,
            fontFamily:   'var(--font-ui)',
            lineHeight:   1.5,
          }}>
            <strong>Development mode</strong> — Supabase not configured.
            Add real credentials to <code>.env.local</code> to enable authentication.
            <br />
            <span style={{ fontSize: 11, opacity: 0.85 }}>
              The form will show the error message — this is expected.
            </span>
          </div>
        )}

        {/* Header */}
        <div style={{ textAlign: 'center', marginBottom: 32 }}>
          <div style={{
            width:        52,
            height:       52,
            borderRadius: '50%',
            background:   COLOURS.accentBg,
            border:       `2px solid ${COLOURS.accentBorder}`,
            margin:       '0 auto 16px',
            display:      'flex',
            alignItems:   'center',
            justifyContent: 'center',
            fontSize:     22,
          }}>
            🏗️
          </div>
          <h1 style={{
            fontFamily: 'var(--font-display)',
            fontSize:   26,
            fontWeight: 700,
            color:      COLOURS.textPrimary,
            margin:     '0 0 6px',
          }}>
            Welcome back
          </h1>
          <p style={{ fontFamily: 'var(--font-body)', fontSize: 14, color: COLOURS.textMuted, margin: 0 }}>
            Sign in to your iNHCES account
          </p>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit}>
          <Input
            label="Email address"
            type="email"
            placeholder="you@institution.ng"
            value={email}
            onChange={e => setEmail(e.target.value)}
            autoComplete="email"
          />
          <Input
            label="Password"
            type="password"
            placeholder="Your password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            autoComplete="current-password"
          />

          {error && (
            <div style={{ ...GS.alertDanger, marginBottom: 16, fontSize: 13 }}>
              {error}
            </div>
          )}

          <Button type="submit" loading={loading} style={{ width: '100%', marginTop: 4 }}>
            {loading ? 'Signing in...' : 'Sign In'}
          </Button>
        </form>

        {/* Divider */}
        <div style={{
          display:    'flex',
          alignItems: 'center',
          gap:        12,
          margin:     '20px 0',
        }}>
          <div style={{ flex: 1, height: 1, background: COLOURS.border }} />
          <span style={{ fontFamily: 'var(--font-ui)', fontSize: 12, color: COLOURS.textDim }}>
            or
          </span>
          <div style={{ flex: 1, height: 1, background: COLOURS.border }} />
        </div>

        {/* Register link */}
        <div style={{ textAlign: 'center' }}>
          <span style={{ fontFamily: 'var(--font-body)', fontSize: 14, color: COLOURS.textMuted }}>
            Don&apos;t have an account?{' '}
          </span>
          <Link href="/register" style={{
            fontFamily:     'var(--font-ui)',
            fontSize:       14,
            color:          COLOURS.accent,
            fontWeight:     600,
            textDecoration: 'none',
          }}>
            Create one
          </Link>
        </div>

        {/* Note about Supabase */}
        <p style={{
          fontFamily: 'var(--font-ui)',
          fontSize:   11,
          color:      COLOURS.textDim,
          textAlign:  'center',
          marginTop:  20,
          lineHeight: 1.5,
        }}>
          Authentication is provided by Supabase. Your credentials are never
          stored by iNHCES directly. Configure NEXT_PUBLIC_SUPABASE_URL
          and NEXT_PUBLIC_SUPABASE_ANON_KEY to enable full auth.
        </p>
      </div>
    </div>
  );
}
