'use client';
import { useEffect, useState } from 'react';
import { GS, COLOURS } from '@/lib/styles';
import DataSourceBadge, { type DataSourceLevel } from '@/components/ui/DataSourceBadge';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import { getMacroSnapshot, type MacroSnapshot } from '@/lib/api';

export default function MacroSnapshotCard() {
  const [data,    setData]    = useState<MacroSnapshot | null>(null);
  const [loading, setLoading] = useState(true);
  const [error,   setError]   = useState<string | null>(null);

  useEffect(() => {
    getMacroSnapshot()
      .then(setData)
      .catch(e => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div style={{
      background:   COLOURS.surface,
      border:       `1px solid ${COLOURS.border}`,
      borderRadius: 12,
      display:      'flex',
      flexDirection:'column',
      height:       '100%',
      overflow:     'hidden',
    }}>
      {/* Header */}
      <div style={{
        ...GS.spaceBetween,
        padding:      '10px 14px 8px',
        borderBottom: `1px solid ${COLOURS.border}`,
        flexShrink:   0,
      }}>
        <span style={{ fontFamily: 'var(--font-display)', fontSize: 13, fontWeight: 700, color: COLOURS.textPrimary }}>
          Macro Snapshot
        </span>
        {data && <DataSourceBadge level={data.overall_freshness as DataSourceLevel} compact />}
      </div>

      {/* Body */}
      <div style={{ flex: 1, overflowY: 'auto', padding: '4px 0' }}>
        {loading && <LoadingSpinner size={20} label="Fetching..." style={{ padding: 16 }} />}
        {error   && (
          <div style={{ padding: '12px 14px', fontSize: 12, color: COLOURS.textDim }}>
            Connect to the FastAPI server to see live data.
          </div>
        )}
        {data && data.variables.map((v, i) => (
          <div key={v.variable} style={{
            display:       'grid',
            gridTemplateColumns: '1fr auto auto',
            alignItems:    'center',
            gap:           8,
            padding:       '7px 14px',
            borderBottom:  i < data.variables.length - 1 ? `1px solid ${COLOURS.border}` : 'none',
            background:    i % 2 === 0 ? 'transparent' : COLOURS.surfaceAlt,
          }}>
            <div>
              <p style={{ fontFamily: 'var(--font-ui)', fontSize: 12, color: COLOURS.textMuted, margin: 0 }}>
                {v.label}
              </p>
              {v.as_of_date && (
                <p style={{ fontFamily: 'var(--font-ui)', fontSize: 10, color: COLOURS.textDim, margin: 0 }}>
                  {v.as_of_date.slice(0, 7)}
                </p>
              )}
            </div>
            <span style={{ fontFamily: 'var(--font-ui)', fontSize: 13, fontWeight: 600, color: COLOURS.textPrimary }}>
              {v.value.toLocaleString('en-NG', { maximumFractionDigits: 2 })}
              <span style={{ fontSize: 10, fontWeight: 400, color: COLOURS.textDim, marginLeft: 4 }}>{v.unit}</span>
            </span>
            <DataSourceBadge level={v.data_level as DataSourceLevel} compact />
          </div>
        ))}
      </div>

      {data && (
        <div style={{ padding: '6px 14px', borderTop: `1px solid ${COLOURS.border}`, flexShrink: 0 }}>
          <span style={{ fontFamily: 'var(--font-ui)', fontSize: 10, color: COLOURS.textDim }}>
            Updated {new Date(data.as_of).toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' })}
          </span>
        </div>
      )}
    </div>
  );
}
