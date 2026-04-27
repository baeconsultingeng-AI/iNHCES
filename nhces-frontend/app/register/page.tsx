'use client';
import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { GS, COLOURS } from '@/lib/styles';
import Button from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { signUp, SUPABASE_CONFIGURED } from '@/lib/auth';

type Role = 'qsprofessional' | 'researcher';

const ROLES: { value: Role; label: string; desc: string }[] = [
  {
    value: 'qsprofessional',
    label: 'QS Professional',
    desc:  'Estimate project costs, manage projects, download reports',
  },
  {
    value: 'researcher',
    label: 'Researcher / PI',
    desc:  'Access aggregate data, macro series, and model metrics',
  },
];

export default function RegisterPage() {
  const router = useRouter();
  const [form, setForm] = useState({
    fullName:    '',
    email:       '',
    password:    '',
    confirm:     '',
    institution: '',
    role:        'qsprofessional' as Role,
  });
  const [loading, setLoading] = useState(false);
  const [error,   setError]   = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  function set(k: keyof typeof form, v: string) {
    setForm(p => ({ ...p, [k]: v }));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);

    if (!form.fullName || !form.email || !form.password) {
      setError('Name, email, and password are required.'); return;
    }
    if (form.password.length < 8) {
      setError('Password must be at least 8 characters.'); return;
    }
    if (form.password !== form.confirm) {
      setError('Passwords do not match.'); return;
    }

    setLoading(true);
    try {
      const result = await signUp(
        form.email, form.password, form.fullName,
        form.institution, form.role,
      );
      // If no session returned, Supabase sent a verification email
      if (!result.session) {
        setSuccess(true);
      } else {
        router.push('/dashboard');
        router.refresh();
      }
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Registration failed.');
    } finally {
      setLoading(false);
    }
  }

  // Success state — email verification pending
  if (success) {
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
          maxWidth:     420,
          textAlign:    'center',
          boxShadow:    '0 4px 24px rgba(26,20,16,0.08)',
        }}
             className="anim">
          <div style={{
            width: 56, height: 56, borderRadius: '50%',
            background: COLOURS.greenLight, border: `2px solid ${COLOURS.green}`,
            margin: '0 auto 16px', display: 'flex',
            alignItems: 'center', justifyContent: 'center', fontSize: 24,
          }}>
            ✉️
          </div>
          <h2 style={{ fontFamily: 'var(--font-display)', fontSize: 22, fontWeight: 700, color: COLOURS.textPrimary, margin: '0 0 10px' }}>
            Check your email
          </h2>
          <p style={{ fontFamily: 'var(--font-body)', fontSize: 14, color: COLOURS.textMuted, margin: '0 0 24px', lineHeight: 1.6 }}>
            We sent a verification link to{' '}
            <strong style={{ color: COLOURS.textPrimary }}>{form.email}</strong>.
            Click the link to activate your account, then log in.
          </p>
          <Link href="/login" style={{ ...GS.btn, display: 'inline-flex', textDecoration: 'none' }}>
            Go to Login
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div style={{
      height:         'calc(100vh - 60px)',
      background:     COLOURS.background,
      display:        'flex',
      alignItems:     'center',
      justifyContent: 'center',
      padding:        24,
      overflowY:      'auto',
    }}>
      <div style={{
        background:   COLOURS.surface,
        border:       `1px solid ${COLOURS.border}`,
        borderRadius: 16,
        padding:      '36px 44px',
        width:        '100%',
        maxWidth:     460,
        boxShadow:    '0 4px 24px rgba(26,20,16,0.08)',
        margin:       'auto',
      }}
           className="anim">

        {/* Dev mode notice */}
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
            To enable real registration, add your Supabase project credentials
            to <code>nhces-frontend/.env.local</code>.
          </div>
        )}

        {/* Header */}
        <div style={{ textAlign: 'center', marginBottom: 28 }}>
          <h1 style={{
            fontFamily: 'var(--font-display)',
            fontSize:   24,
            fontWeight: 700,
            color:      COLOURS.textPrimary,
            margin:     '0 0 6px',
          }}>
            Create your account
          </h1>
          <p style={{ fontFamily: 'var(--font-body)', fontSize: 14, color: COLOURS.textMuted, margin: 0 }}>
            iNHCES · TETFund NRF 2025 · ABU Zaria
          </p>
        </div>

        <form onSubmit={handleSubmit}>
          {/* Name + Email */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
            <Input label="Full Name *" placeholder="Dr. Amina Bello"
              value={form.fullName} onChange={e => set('fullName', e.target.value)} />
            <Input label="Institution" placeholder="ABU Zaria"
              value={form.institution} onChange={e => set('institution', e.target.value)} />
          </div>

          <Input label="Email Address *" type="email" placeholder="you@institution.ng"
            value={form.email} onChange={e => set('email', e.target.value)}
            autoComplete="email" />

          {/* Passwords */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
            <Input label="Password *" type="password" placeholder="Min. 8 characters"
              value={form.password} onChange={e => set('password', e.target.value)}
              autoComplete="new-password" />
            <Input label="Confirm Password *" type="password" placeholder="Repeat password"
              value={form.confirm} onChange={e => set('confirm', e.target.value)}
              autoComplete="new-password" />
          </div>

          {/* Role selector */}
          <div style={{ marginBottom: 16 }}>
            <label style={GS.label}>Account Role *</label>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              {ROLES.map(r => {
                const active = form.role === r.value;
                return (
                  <button
                    key={r.value}
                    type="button"
                    onClick={() => set('role', r.value)}
                    style={{
                      display:      'flex',
                      alignItems:   'flex-start',
                      gap:          12,
                      padding:      '10px 14px',
                      borderRadius: 10,
                      border:       active
                        ? `2px solid ${COLOURS.accent}`
                        : `1px solid ${COLOURS.border}`,
                      background:   active ? COLOURS.accentBg : COLOURS.surface,
                      cursor:       'pointer',
                      textAlign:    'left',
                      transition:   'all 0.15s ease',
                    }}
                  >
                    {/* Radio dot */}
                    <div style={{
                      width:        16,
                      height:       16,
                      borderRadius: '50%',
                      border:       `2px solid ${active ? COLOURS.accent : COLOURS.border2}`,
                      background:   active ? COLOURS.accent : 'transparent',
                      flexShrink:   0,
                      marginTop:    2,
                      display:      'flex',
                      alignItems:   'center',
                      justifyContent: 'center',
                    }}>
                      {active && (
                        <div style={{ width: 6, height: 6, borderRadius: '50%', background: COLOURS.white }} />
                      )}
                    </div>
                    <div>
                      <p style={{
                        fontFamily: 'var(--font-ui)', fontSize: 13, fontWeight: 600,
                        color:      active ? COLOURS.accent : COLOURS.textPrimary,
                        margin:     '0 0 2px',
                      }}>
                        {r.label}
                      </p>
                      <p style={{ fontFamily: 'var(--font-body)', fontSize: 12, color: COLOURS.textMuted, margin: 0 }}>
                        {r.desc}
                      </p>
                    </div>
                  </button>
                );
              })}
            </div>
          </div>

          {error && (
            <div style={{ ...GS.alertDanger, marginBottom: 14, fontSize: 13 }}>{error}</div>
          )}

          <Button type="submit" loading={loading} style={{ width: '100%' }}>
            {loading ? 'Creating account...' : 'Create Account'}
          </Button>
        </form>

        {/* Login link */}
        <div style={{ textAlign: 'center', marginTop: 20 }}>
          <span style={{ fontFamily: 'var(--font-body)', fontSize: 14, color: COLOURS.textMuted }}>
            Already have an account?{' '}
          </span>
          <Link href="/login" style={{
            fontFamily: 'var(--font-ui)', fontSize: 14,
            color: COLOURS.accent, fontWeight: 600, textDecoration: 'none',
          }}>
            Sign in
          </Link>
        </div>
      </div>
    </div>
  );
}
