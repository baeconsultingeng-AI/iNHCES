import Link from 'next/link';
import { GS, COLOURS } from '@/lib/styles';

// Everything fits in one viewport — no scrolling required
export default function HomePage() {
  return (
    <div style={{
      height:         'calc(100vh - 60px)',
      background:     COLOURS.background,
      display:        'grid',
      gridTemplateRows: '1fr auto',
      overflow:       'hidden',
    }}>

      {/* ── MAIN HERO AREA ─────────────────────────────────────────────── */}
      <div style={{
        display:             'grid',
        gridTemplateColumns: '1fr 1fr',
        gap:                 0,
        overflow:            'hidden',
      }}>

        {/* LEFT — Brand + CTA */}
        <div style={{
          padding:        '52px 48px 40px',
          display:        'flex',
          flexDirection:  'column',
          justifyContent: 'center',
          borderRight:    `1px solid ${COLOURS.border}`,
        }}
             className="anim">

          {/* Pill badge */}
          <span style={{
            ...GS.tag,
            background:  COLOURS.accentBg,
            color:       COLOURS.accent,
            border:      `1px solid ${COLOURS.accentBorder}`,
            marginBottom: 20,
            alignSelf:   'flex-start',
            fontSize:    13,
          }}>
            TETFund NRF 2025 &nbsp;·&nbsp; ABU Zaria, Nigeria
          </span>

          <h1 style={{
            fontFamily: 'var(--font-display)',
            fontSize:   'clamp(28px, 3.5vw, 46px)',
            fontWeight: 900,
            color:      COLOURS.textPrimary,
            lineHeight: 1.15,
            margin:     '0 0 18px',
          }}>
            Intelligent Housing
            <br />
            <span style={{ color: COLOURS.accent }}>Cost Estimation</span>
            <br />
            for Nigeria
          </h1>

          <p style={{
            fontFamily: 'var(--font-body)',
            fontSize:   16,
            color:      COLOURS.textMuted,
            lineHeight: 1.6,
            margin:     '0 0 30px',
            maxWidth:   420,
          }}>
            AI-powered construction cost prediction per sqm.
            Live macroeconomic data · SHAP explainability · PDF reports.
            Built for Nigerian Quantity Surveyors.
          </p>

          {/* CTA buttons */}
          <div style={{ display: 'flex', gap: 12, marginBottom: 36 }}>
            <Link href="/estimate" style={{ ...GS.btn, padding: '12px 28px', fontSize: 15 }}>
              Get an Estimate
            </Link>
            <Link href="/dashboard" style={{ ...GS.btnGhost, padding: '12px 28px', fontSize: 15 }}>
              Dashboard
            </Link>
          </div>

          {/* Inline stats */}
          <div style={{ display: 'flex', gap: 24 }}>
            {[
              { v: '13.66%', l: 'LOO-CV MAPE' },
              { v: '7',      l: 'Macro Variables' },
              { v: '9',      l: 'Data Pipelines' },
              { v: '9',      l: 'Publications' },
            ].map(s => (
              <div key={s.l}>
                <div style={{
                  fontFamily: 'var(--font-display)',
                  fontSize:   22,
                  fontWeight: 700,
                  color:      COLOURS.accent,
                  lineHeight: 1,
                }}>
                  {s.v}
                </div>
                <div style={{ fontFamily: 'var(--font-ui)', fontSize: 11, color: COLOURS.textDim, marginTop: 3 }}>
                  {s.l}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* RIGHT — Feature cards */}
        <div style={{
          padding:       '52px 40px 40px',
          display:       'flex',
          flexDirection: 'column',
          justifyContent:'center',
          gap:           16,
          background:    COLOURS.surface,
        }}
             className="anim">

          {/* How it works — compact 3 steps */}
          <p style={{ ...GS.label, marginBottom: 4 }}>How it works</p>
          {[
            { n:'01', t:'Enter Project Details', d:'Building type, floor area, location and zone.' },
            { n:'02', t:'AI Predicts the Cost',  d:'LightGBM champion model returns NGN/sqm with confidence interval.' },
            { n:'03', t:'Download PDF Report',   d:'Professional 4-page report with SHAP feature chart.' },
          ].map(step => (
            <div key={step.n} style={{
              display:      'flex',
              gap:          14,
              padding:      '14px 16px',
              background:   COLOURS.background,
              borderRadius: 10,
              border:       `1px solid ${COLOURS.border}`,
              alignItems:   'flex-start',
            }}>
              <span style={{
                fontFamily: 'var(--font-display)',
                fontSize:   22,
                fontWeight: 700,
                color:      COLOURS.accentBg,
                lineHeight: 1,
                minWidth:   32,
              }}>{step.n}</span>
              <div>
                <p style={{ fontFamily: 'var(--font-display)', fontSize: 15, fontWeight: 700, color: COLOURS.textPrimary, margin: '0 0 3px' }}>
                  {step.t}
                </p>
                <p style={{ fontFamily: 'var(--font-body)', fontSize: 13, color: COLOURS.textMuted, margin: 0 }}>
                  {step.d}
                </p>
              </div>
            </div>
          ))}

          {/* Data quality badges — compact row */}
          <div style={{ marginTop: 8 }}>
            <p style={{ ...GS.label, marginBottom: 8 }}>Data Transparency</p>
            <div style={{ display: 'flex', gap: 8 }}>
              {([
                { level: 'GREEN', label: 'Live Data',       bg: COLOURS.green },
                { level: 'AMBER', label: 'AI Template',     bg: COLOURS.amber },
                { level: 'RED',   label: 'Synthetic Data',  bg: COLOURS.red   },
              ] as const).map(b => (
                <div key={b.level} style={{
                  flex:        1,
                  background:  b.bg,
                  color:       COLOURS.white,
                  borderRadius: 8,
                  padding:     '8px 10px',
                  textAlign:   'center',
                }}>
                  <p style={{ fontFamily: 'var(--font-ui)', fontSize: 11, fontWeight: 700, margin: 0, letterSpacing: '0.05em' }}>{b.level}</p>
                  <p style={{ fontFamily: 'var(--font-ui)', fontSize: 11, opacity: 0.85, margin: '2px 0 0' }}>{b.label}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* ── FOOTER STRIP ──────────────────────────────────────────────── */}
      <div style={{
        borderTop:      `1px solid ${COLOURS.border}`,
        background:     COLOURS.surface,
        padding:        '12px 40px',
        display:        'flex',
        alignItems:     'center',
        justifyContent: 'space-between',
      }}>
        <span style={{ fontFamily: 'var(--font-ui)', fontSize: 12, color: COLOURS.textDim }}>
          iNHCES · TETFund National Research Fund 2025 · Dept. of Quantity Surveying, ABU Zaria
        </span>
        <div style={{ display: 'flex', gap: 12 }}>
          {[
            { href: '/estimate',  label: 'Estimate'  },
            { href: '/dashboard', label: 'Dashboard' },
            { href: '/macro',     label: 'Macro Data'},
          ].map(l => (
            <Link key={l.href} href={l.href} style={{
              fontFamily: 'var(--font-ui)', fontSize: 12,
              color: COLOURS.accent, textDecoration: 'none',
            }}>
              {l.label}
            </Link>
          ))}
        </div>
      </div>

    </div>
  );
}
