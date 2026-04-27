import { GS, COLOURS } from '@/lib/styles';
import Badge from '@/components/ui/Badge';

const CHAMPION = {
  name:        'LightGBM',
  looCvMape:   13.66,
  trainedDate: '2026-04-26',
  features:    14,
  trainRows:   18,
};

export default function ModelStatusCard() {
  const ok = CHAMPION.looCvMape <= 15;
  return (
    <div style={{
      background:   COLOURS.surface,
      border:       `1px solid ${COLOURS.border}`,
      borderRadius: 12,
      overflow:     'hidden',
    }}>
      {/* Header */}
      <div style={{
        ...GS.spaceBetween,
        padding:      '10px 14px 8px',
        borderBottom: `1px solid ${COLOURS.border}`,
      }}>
        <span style={{ fontFamily: 'var(--font-display)', fontSize: 13, fontWeight: 700, color: COLOURS.textPrimary }}>
          Champion Model
        </span>
        <Badge variant={ok ? 'success' : 'warning'} style={{ fontSize: 11 }}>
          {ok ? '✓ Target Met' : '⚠ Below Target'}
        </Badge>
      </div>

      {/* MAPE highlight */}
      <div style={{
        display:        'flex',
        alignItems:     'center',
        justifyContent: 'space-between',
        padding:        '10px 14px',
        background:     COLOURS.accentBg,
        borderBottom:   `1px solid ${COLOURS.accentBorder}`,
      }}>
        <div>
          <p style={{ fontFamily: 'var(--font-ui)', fontSize: 10, color: COLOURS.accent, margin: 0, letterSpacing: '0.05em', textTransform: 'uppercase' }}>
            LOO-CV MAPE
          </p>
          <p style={{ fontFamily: 'var(--font-display)', fontSize: 26, fontWeight: 700, color: COLOURS.accent, margin: 0, lineHeight: 1.1 }}>
            {CHAMPION.looCvMape}%
          </p>
        </div>
        <div style={{ textAlign: 'right' }}>
          <p style={{ fontFamily: 'var(--font-ui)', fontSize: 10, color: COLOURS.textDim, margin: 0 }}>Target</p>
          <p style={{ fontFamily: 'var(--font-ui)', fontSize: 14, fontWeight: 600, color: COLOURS.green, margin: 0 }}>≤ 15%</p>
        </div>
      </div>

      {/* Stat rows */}
      {[
        ['Algorithm',   CHAMPION.name],
        ['Features',    `${CHAMPION.features} engineered`],
        ['Train rows',  `${CHAMPION.trainRows} annual obs.`],
        ['Trained',     CHAMPION.trainedDate],
        ['Data source', 'RED — synthetic proxy'],
      ].map(([k, v], i) => (
        <div key={k} style={{
          display:        'flex',
          justifyContent: 'space-between',
          padding:        '6px 14px',
          borderBottom:   i < 4 ? `1px solid ${COLOURS.border}` : 'none',
          background:     i % 2 === 0 ? 'transparent' : COLOURS.surfaceAlt,
        }}>
          <span style={{ fontFamily: 'var(--font-ui)', fontSize: 12, color: COLOURS.textMuted }}>{k}</span>
          <span style={{ fontFamily: 'var(--font-ui)', fontSize: 12, fontWeight: 500, color: COLOURS.textPrimary }}>{v}</span>
        </div>
      ))}
    </div>
  );
}
