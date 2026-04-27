'use client';
import { useEffect, useState } from 'react';
import { GS, COLOURS } from '@/lib/styles';
import DataSourceBadge, { type DataSourceLevel } from '@/components/ui/DataSourceBadge';
import { getPipelineStatus, type PipelineStatus } from '@/lib/api';

function StateIcon({ state }: { state?: string }) {
  if (state === 'success') return <span style={{ color: COLOURS.green,  fontSize: 13, fontWeight: 700 }}>✓</span>;
  if (state === 'failed')  return <span style={{ color: COLOURS.red,    fontSize: 13, fontWeight: 700 }}>✗</span>;
  if (state === 'running') return <span style={{ color: COLOURS.accent, fontSize: 11 }}>▶</span>;
  return <span style={{ color: COLOURS.textDim, fontSize: 12 }}>–</span>;
}

function HealthPill({ health }: { health: string }) {
  const cols: Record<string, { bg: string; color: string }> = {
    OK:       { bg: COLOURS.greenLight, color: COLOURS.green },
    DEGRADED: { bg: COLOURS.amberLight, color: COLOURS.amber },
    DOWN:     { bg: COLOURS.redLight,   color: COLOURS.red },
  };
  const s = cols[health] ?? cols.DOWN;
  return (
    <span style={{ ...GS.tag, background: s.bg, color: s.color, fontSize: 11, fontWeight: 700 }}>
      {health}
    </span>
  );
}

export default function PipelineHealthCard() {
  const [data,    setData]    = useState<PipelineStatus | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getPipelineStatus()
      .then(setData)
      .catch(() => setData(null))
      .finally(() => setLoading(false));
  }, []);

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
          Pipeline Health
        </span>
        {data ? <HealthPill health={data.overall_health} /> : (
          <span style={{ ...GS.tag, background: COLOURS.redLight, color: COLOURS.red, fontSize: 11 }}>
            {loading ? '...' : 'DOWN'}
          </span>
        )}
      </div>

      {/* DAG rows */}
      {!data ? (
        <div style={{ padding: '10px 14px', fontSize: 12, color: COLOURS.textDim }}>
          {loading ? 'Checking Airflow...' : 'Airflow not running — deploy to Railway to see DAG status.'}
        </div>
      ) : (
        data.dags.map((dag, i) => (
          <div key={dag.dag_id} style={{
            display:      'grid',
            gridTemplateColumns: 'auto 1fr auto',
            alignItems:   'center',
            gap:          8,
            padding:      '5px 14px',
            borderBottom: i < data.dags.length - 1 ? `1px solid ${COLOURS.border}` : 'none',
            background:   i % 2 === 0 ? 'transparent' : COLOURS.surfaceAlt,
          }}>
            <StateIcon state={dag.last_run_state} />
            <div style={{ minWidth: 0 }}>
              <p style={{
                fontFamily:   'var(--font-ui)', fontSize: 11, color: COLOURS.textPrimary,
                margin: 0, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis',
              }}>
                {dag.dag_id.replace('nhces_', '')}
              </p>
              <p style={{ fontFamily: 'var(--font-ui)', fontSize: 10, color: COLOURS.textDim, margin: 0 }}>
                {dag.schedule === 'manual' ? 'Manual' : dag.schedule}
              </p>
            </div>
            <DataSourceBadge level={dag.data_level as DataSourceLevel} compact />
          </div>
        ))
      )}
    </div>
  );
}
