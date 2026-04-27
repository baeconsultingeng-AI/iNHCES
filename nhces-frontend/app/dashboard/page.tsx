import { GS, COLOURS } from '@/lib/styles';
import MacroSnapshotCard from '@/components/dashboard/MacroSnapshot';
import ModelStatusCard from '@/components/dashboard/ModelStatus';
import PipelineHealthCard from '@/components/dashboard/PipelineHealth';
import RecentPredictions from '@/components/dashboard/RecentPredictions';
import Link from 'next/link';

// Compact stat pill for header row
function StatPill({ value, label, accent }: { value: string; label: string; accent?: boolean }) {
  return (
    <div style={{
      background:   accent ? COLOURS.accentBg : COLOURS.surface,
      border:       `1px solid ${accent ? COLOURS.accentBorder : COLOURS.border}`,
      borderRadius: 10,
      padding:      '10px 16px',
      textAlign:    'center',
      flex:         1,
    }}>
      <p style={{
        fontFamily: 'var(--font-display)',
        fontSize:   20,
        fontWeight: 700,
        color:      accent ? COLOURS.accent : COLOURS.textPrimary,
        margin:     '0 0 2px',
        lineHeight: 1,
      }}>{value}</p>
      <p style={{ fontFamily: 'var(--font-ui)', fontSize: 11, color: COLOURS.textMuted, margin: 0 }}>{label}</p>
    </div>
  );
}

export default function DashboardPage() {
  const now = new Date().toLocaleDateString('en-GB', {
    weekday: 'long', day: 'numeric', month: 'long', year: 'numeric',
  });

  return (
    // Full-height layout — no scrolling
    <div style={{
      height:        'calc(100vh - 60px)',
      display:       'grid',
      gridTemplateRows: 'auto auto 1fr',
      gap:           0,
      overflow:      'hidden',
      background:    COLOURS.background,
    }}>

      {/* ── HEADER ROW ─────────────────────────────────────────────────── */}
      <div style={{
        display:        'flex',
        alignItems:     'center',
        justifyContent: 'space-between',
        padding:        '14px 24px 10px',
        borderBottom:   `1px solid ${COLOURS.border}`,
        background:     COLOURS.surface,
      }}>
        <div>
          <h1 style={{
            fontFamily: 'var(--font-display)',
            fontSize:   20,
            fontWeight: 700,
            color:      COLOURS.textPrimary,
            margin:     0,
          }}>
            Dashboard
          </h1>
          <p style={{ fontFamily: 'var(--font-ui)', fontSize: 12, color: COLOURS.textDim, margin: '2px 0 0' }}>
            {now}
          </p>
        </div>
        <Link href="/estimate" style={{ ...GS.btn, padding: '8px 18px', fontSize: 13 }}>
          + New Estimate
        </Link>
      </div>

      {/* ── STATS STRIP ────────────────────────────────────────────────── */}
      <div style={{
        display:    'flex',
        gap:        10,
        padding:    '10px 24px',
        background: COLOURS.background,
        borderBottom: `1px solid ${COLOURS.border}`,
      }}>
        <StatPill value="13.66%"    label="Champion MAPE"    accent />
        <StatPill value="LightGBM"  label="Champion Model" />
        <StatPill value="7"         label="Macro Variables" />
        <StatPill value="9"         label="Airflow DAGs" />
        <StatPill value="O1–O5"     label="Research Complete" />
        <StatPill value="9"         label="Publications" />
      </div>

      {/* ── MAIN 3-COLUMN GRID — fills remaining height ─────────────────── */}
      <div style={{
        display:             'grid',
        gridTemplateColumns: '1.1fr 0.85fr 1.05fr',
        gap:                 12,
        padding:             '12px 24px 14px',
        overflow:            'hidden',
        minHeight:           0,
      }}>

        {/* Column 1: Macro Snapshot */}
        <div style={{ display: 'flex', flexDirection: 'column', minHeight: 0, overflow: 'hidden' }}>
          <MacroSnapshotCard />
        </div>

        {/* Column 2: Model Status */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 12, minHeight: 0, overflow: 'hidden' }}>
          <ModelStatusCard />
        </div>

        {/* Column 3: Pipeline + Recent */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 12, minHeight: 0, overflow: 'hidden' }}>
          <div style={{ flex: '0 0 auto', overflow: 'hidden' }}>
            <PipelineHealthCard />
          </div>
          <div style={{ flex: '1 1 auto', overflow: 'hidden' }}>
            <RecentPredictions />
          </div>
        </div>

      </div>
    </div>
  );
}
