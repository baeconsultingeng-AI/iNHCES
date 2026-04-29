'use client';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import {
  Calculator,
  LayoutDashboard,
  FolderOpen,
  FileText,
  TrendingUp,
  LogIn,
  LogOut,
  UserPlus,
} from 'lucide-react';
import { GS, COLOURS } from '@/lib/styles';
import Logo from '@/components/ui/Logo';
import { createClient, signOut, SUPABASE_CONFIGURED } from '@/lib/auth';
import type { User } from '@supabase/supabase-js';

const NAV_LINKS = [
  { href: '/estimate',  label: 'Estimate',   Icon: Calculator      },
  { href: '/dashboard', label: 'Dashboard',  Icon: LayoutDashboard },
  { href: '/projects',  label: 'Projects',   Icon: FolderOpen      },
  { href: '/reports',   label: 'Reports',    Icon: FileText        },
  { href: '/macro',     label: 'Macro Data', Icon: TrendingUp      },
];

export default function Navbar() {
  const pathname = usePathname();
  const router   = useRouter();
  const [user,         setUser]         = useState<User | null>(null);
  const [loadingAuth,  setLoadingAuth]  = useState(true);
  const [loggingOut,   setLoggingOut]   = useState(false);

  useEffect(() => {
    // Skip auth subscription when Supabase is not configured (dev mode)
    if (!SUPABASE_CONFIGURED) {
      setLoadingAuth(false);
      return;
    }

    const supabase = createClient();

    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null);
      setLoadingAuth(false);
    });

    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user ?? null);
    });

    return () => subscription.unsubscribe();
  }, []);

  async function handleSignOut() {
    setLoggingOut(true);
    try {
      await signOut();
      router.push('/');
      router.refresh();
    } catch {
      // silent
    } finally {
      setLoggingOut(false);
    }
  }

  const displayName = user?.user_metadata?.full_name
    ? (user.user_metadata.full_name as string).split(' ')[0]
    : user?.email?.split('@')[0] ?? '';

  return (
    <nav style={GS.navBar}>
      {/* Brand */}
      <Link href="/" style={{ ...GS.navBrand, display: 'flex', alignItems: 'center', textDecoration: 'none' }}>
        <Logo size={28} textSize={18} />
      </Link>

      {/* Divider */}
      <span style={{ width: 1, height: 24, background: COLOURS.border, margin: '0 8px' }} />

      {/* Navigation links */}
      {NAV_LINKS.map(({ href, label, Icon }) => {
        const active = pathname === href || pathname.startsWith(href + '/');
        return (
          <Link
            key={href}
            href={href}
            style={{ ...GS.navBtn, ...(active ? GS.navBtnActive : {}), display: 'flex', alignItems: 'center', gap: 5 }}
          >
            <Icon size={14} strokeWidth={1.8} />
            {label}
          </Link>
        );
      })}

      {/* Spacer */}
      <span style={{ flex: 1 }} />

      {/* Auth section */}
      {loadingAuth ? (
        <span style={{ ...GS.metaText, fontSize: 12 }}>...</span>
      ) : user ? (
        /* Logged in state */
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <div style={{
            display:       'flex',
            alignItems:    'center',
            gap:           8,
            padding:       '6px 12px',
            background:    COLOURS.accentBg,
            border:        `1px solid ${COLOURS.accentBorder}`,
            borderRadius:  20,
          }}>
            <div style={{
              width:        26,
              height:       26,
              borderRadius: '50%',
              background:   COLOURS.accent,
              display:      'flex',
              alignItems:   'center',
              justifyContent: 'center',
              fontFamily:   'var(--font-ui)',
              fontSize:     12,
              fontWeight:   700,
              color:        COLOURS.white,
            }}>
              {displayName.charAt(0).toUpperCase()}
            </div>
            <span style={{ fontFamily: 'var(--font-ui)', fontSize: 13, fontWeight: 500, color: COLOURS.accent }}>
              {displayName}
            </span>
          </div>
          <button
            onClick={handleSignOut}
            disabled={loggingOut}
            style={{
              ...GS.navBtn,
              color:  COLOURS.red,
              cursor: loggingOut ? 'not-allowed' : 'pointer',
              opacity: loggingOut ? 0.6 : 1,
              display: 'flex',
              alignItems: 'center',
              gap: 5,
            }}
          >
            <LogOut size={14} strokeWidth={1.8} />
            {loggingOut ? 'Signing out...' : 'Log Out'}
          </button>
        </div>
      ) : (
        /* Logged out state */
        <>
          <Link href="/login" style={{ ...GS.navBtn, display: 'flex', alignItems: 'center', gap: 5 }}>
            <LogIn size={14} strokeWidth={1.8} />
            Log In
          </Link>
          <Link
            href="/register"
            style={{ ...GS.btn, padding: '7px 16px', fontSize: 13, display: 'flex', alignItems: 'center', gap: 5 }}
          >
            <UserPlus size={14} strokeWidth={1.8} />
            Get Started
          </Link>
        </>
      )}
    </nav>
  );
}
