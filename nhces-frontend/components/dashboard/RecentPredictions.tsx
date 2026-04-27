import { GS, COLOURS } from '@/lib/styles';
import Link from 'next/link';

export default function RecentPredictions() {
  return (
    <div style={{
      background:   COLOURS.surface,
      border:       `1px solid ${COLOURS.border}`,
      borderRadius: 12,
      overflow:     'hidden',
      display:      'flex',
      flexDirection:'column',
    }}>
      <div style={{
        ...GS.spaceBetween,
        padding:      '10px 14px 8px',
        borderBottom: `1px solid ${COLOURS.border}`,
        flexShrink:   0,
      }}>
        <span style={{ fontFamily: 'var(--font-display)', fontSize: 13, fontWeight: 700, color: COLOURS.textPrimary }}>
          Recent Estimates
        </span>
        <Link href="/estimate" style={{
          fontFamily:   'var(--font-ui)', fontSize: 12, color: COLOURS.accent,
          textDecoration: 'none', fontWeight: 600,
        }}>
          + New
        </Link>
      </div>

      {/* Empty state */}
      <div style={{
        flex:        1,
        display:     'flex',
        flexDirection:'column',
        alignItems:  'center',
        justifyContent:'center',
        padding:     '20px 16px',
        textAlign:   'center',
      }}>
        <div style={{
          width:        40,
          height:       40,
          borderRadius: '50%',
          background:   COLOURS.accentBg,
          border:       `1px solid ${COLOURS.accentBorder}`,
          display:      'flex',
          alignItems:   'center',
          justifyContent:'center',
          marginBottom: 10,
          fontSize:     18,
        }}>
          📊
        </div>
        <p style={{ fontFamily: 'var(--font-body)', fontSize: 13, color: COLOURS.textMuted, margin: '0 0 12px' }}>
          No estimates yet.
          <br />Run your first estimate to see history here.
        </p>
        <Link href="/estimate" style={{ ...GS.btn, padding: '8px 18px', fontSize: 13 }}>
          Get an Estimate
        </Link>
      </div>
    </div>
  );
}
