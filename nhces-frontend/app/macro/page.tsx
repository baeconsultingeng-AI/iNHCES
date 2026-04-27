'use client';
import { useEffect, useState } from 'react';
import { GS, COLOURS } from '@/lib/styles';
import Card from '@/components/ui/Card';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import DataSourceBadge, { type DataSourceLevel } from '@/components/ui/DataSourceBadge';
import { getMacroSnapshot, getMacroHistory, type MacroSnapshot, type MacroHistory } from '@/lib/api';

// Variable options
const VARIABLES = [
  { value: 'ngn_usd',          label: 'NGN / USD Exchange Rate',  unit: 'NGN per USD' },
  { value: 'ngn_eur',          label: 'NGN / EUR Exchange Rate',  unit: 'NGN per EUR' },
  { value: 'ngn_gbp',          label: 'NGN / GBP Exchange Rate',  unit: 'NGN per GBP' },
  { value: 'cpi_annual_pct',   label: 'CPI Inflation (Annual)',   unit: '% per annum' },
  { value: 'gdp_growth_pct',   label: 'GDP Growth Rate',          unit: '% per annum' },
  { value: 'lending_rate_pct', label: 'Lending Interest Rate',    unit: '% per annum' },
  { value: 'brent_usd_barrel', label: 'Brent Crude Oil Price',    unit: 'USD/barrel' },
];

// Simple SVG line chart
function LineChart({ data, unit }: { data: { year: number; value: number }[]; unit: string }) {
  if (!data.length) return null;
  const W = 520; const H = 180; const PAD = 40;
  const minV = Math.min(...data.map(d => d.value));
  const maxV = Math.max(...data.map(d => d.value));
  const range = maxV - minV || 1;

  const pts = data.map((d, i) => ({
    x: PAD + (i / Math.max(data.length - 1, 1)) * (W - 2 * PAD),
    y: PAD + (1 - (d.value - minV) / range) * (H - 2 * PAD),
    ...d,
  }));

  const pathD = pts.map((p, i) => `${i === 0 ? 'M' : 'L'} ${p.x.toFixed(1)} ${p.y.toFixed(1)}`).join(' ');
  const areaD = `${pathD} L ${pts[pts.length-1].x.toFixed(1)} ${H-PAD} L ${pts[0].x.toFixed(1)} ${H-PAD} Z`;

  return (
    <svg viewBox={`0 0 ${W} ${H}`} style={{ width: '100%', height: 180, display: 'block' }}>
      {/* Grid lines */}
      {[0, 0.25, 0.5, 0.75, 1].map(f => {
        const y = PAD + f * (H - 2 * PAD);
        const val = (maxV - f * range).toFixed(1);
        return (
          <g key={f}>
            <line x1={PAD} x2={W - PAD} y1={y} y2={y} stroke={COLOURS.border} strokeWidth={0.8} />
            <text x={PAD - 4} y={y + 4} textAnchor="end" fontSize={9} fill={COLOURS.textDim}>{val}</text>
          </g>
        );
      })}
      {/* Area */}
      <path d={areaD} fill={COLOURS.accentBg} />
      {/* Line */}
      <path d={pathD} fill="none" stroke={COLOURS.accent} strokeWidth={2} strokeLinejoin="round" />
      {/* Points + year labels */}
      {pts.map((p, i) => (
        <g key={i}>
          <circle cx={p.x} cy={p.y} r={3.5} fill={COLOURS.accent} />
          {i % Math.ceil(pts.length / 6) === 0 && (
            <text x={p.x} y={H - PAD + 14} textAnchor="middle" fontSize={9} fill={COLOURS.textDim}>
              {p.year}
            </text>
          )}
        </g>
      ))}
      {/* Unit label */}
      <text x={W - PAD} y={PAD - 6} textAnchor="end" fontSize={9} fill={COLOURS.textDim}>{unit}</text>
    </svg>
  );
}

export default function MacroPage() {
  const [snapshot, setSnapshot] = useState<MacroSnapshot | null>(null);
  const [selected, setSelected] = useState('ngn_usd');
  const [history,  setHistory]  = useState<MacroHistory | null>(null);
  const [loadingSnap, setLoadingSnap] = useState(true);
  const [loadingHist, setLoadingHist] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Load snapshot
  useEffect(() => {
    getMacroSnapshot()
      .then(setSnapshot)
      .catch(e => setError(e.message))
      .finally(() => setLoadingSnap(false));
  }, []);

  // Load history whenever variable changes
  useEffect(() => {
    setLoadingHist(true);
    setHistory(null);
    getMacroHistory(selected, 10)
      .then(setHistory)
      .catch(() => setHistory(null))
      .finally(() => setLoadingHist(false));
  }, [selected]);

  const selectedMeta = VARIABLES.find(v => v.value === selected)!;
  const snapshotVar  = snapshot?.variables.find(v => v.variable === selected);

  return (
    <div style={{ ...GS.page, paddingTop: 40 }}>
      <div style={{ marginBottom: 32 }} className="anim">
        <h1 style={GS.pageTitle}>Macroeconomic Data</h1>
        <p style={GS.pageSub}>
          Live and historical macro indicators used by the iNHCES ML model.
          Each series shows its current data freshness level.
        </p>
      </div>

      {error && (
        <div style={{ ...GS.alertDanger, marginBottom: 24 }}>
          Backend unavailable — start FastAPI to see live data.
          <p style={{ ...GS.metaText, margin: '4px 0 0', fontSize: 12 }}>{error}</p>
        </div>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: 24, alignItems: 'start' }} className="anim">

        {/* Variable selector + snapshot values */}
        <Card>
          <h2 style={{ ...GS.sectionTitle, fontSize: 16, marginBottom: 14 }}>Variables</h2>
          {loadingSnap ? (
            <LoadingSpinner size={20} label="Fetching..." style={{ padding: 16 }} />
          ) : (
            <div>
              {VARIABLES.map(v => {
                const sv = snapshot?.variables.find(sv => sv.variable === v.value);
                const active = selected === v.value;
                return (
                  <button key={v.value} onClick={() => setSelected(v.value)} style={{
                    width:       '100%',
                    textAlign:   'left',
                    padding:     '10px 12px',
                    borderRadius: 8,
                    border:      active ? `1.5px solid ${COLOURS.accentBorder}` : `1px solid ${COLOURS.border}`,
                    background:  active ? COLOURS.accentBg : 'transparent',
                    cursor:      'pointer',
                    marginBottom: 6,
                    display:     'flex',
                    justifyContent: 'space-between',
                    alignItems:  'center',
                    gap:         8,
                  }}>
                    <div>
                      <p style={{ fontFamily: 'var(--font-ui)', fontSize: 13, fontWeight: active ? 600 : 400, color: active ? COLOURS.accent : COLOURS.textPrimary, margin: 0 }}>
                        {v.label}
                      </p>
                      {sv && (
                        <p style={{ ...GS.metaText, margin: 0, fontSize: 11 }}>
                          {sv.value.toLocaleString('en-NG', { maximumFractionDigits: 2 })} {v.unit}
                        </p>
                      )}
                    </div>
                    {sv && <DataSourceBadge level={sv.data_level as DataSourceLevel} compact />}
                  </button>
                );
              })}
            </div>
          )}
        </Card>

        {/* Chart + detail */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
          {/* Current value card */}
          {snapshotVar && (
            <Card style={{ borderLeft: `4px solid ${COLOURS.accent}` }}>
              <p style={GS.label}>{selectedMeta.label}</p>
              <div style={GS.spaceBetween}>
                <p style={{
                  fontFamily: 'var(--font-display)', fontSize: 32, fontWeight: 700,
                  color: COLOURS.accent, margin: 0,
                }}>
                  {snapshotVar.value.toLocaleString('en-NG', { maximumFractionDigits: 2 })}
                  <span style={{ fontFamily: 'var(--font-ui)', fontSize: 15, fontWeight: 400, marginLeft: 8 }}>
                    {selectedMeta.unit}
                  </span>
                </p>
                <DataSourceBadge level={snapshotVar.data_level as DataSourceLevel} />
              </div>
              <p style={{ ...GS.metaText, margin: '8px 0 0', fontSize: 12 }}>
                Source: {snapshotVar.source}
                {snapshotVar.as_of_date ? ` · As of ${snapshotVar.as_of_date.slice(0, 7)}` : ''}
              </p>
            </Card>
          )}

          {/* Historical chart */}
          <Card>
            <h3 style={{ ...GS.sectionTitle, fontSize: 15, marginBottom: 4 }}>
              Historical Trend — {selectedMeta.label}
            </h3>
            <p style={{ ...GS.metaText, marginBottom: 12 }}>Last 10 annual observations</p>
            {loadingHist && <LoadingSpinner size={20} label="Loading history..." style={{ padding: 24 }} />}
            {history && history.data.length > 0 ? (
              <>
                <LineChart data={history.data} unit={selectedMeta.unit} />
                <DataSourceBadge level={history.data_level as DataSourceLevel} style={{ marginTop: 10 }} />
              </>
            ) : !loadingHist && (
              <div style={{
                padding: 32, textAlign: 'center', background: COLOURS.surfaceAlt,
                borderRadius: 8, border: `1px dashed ${COLOURS.border2}`,
              }}>
                <p style={{ ...GS.metaText, margin: 0 }}>
                  No historical data — populate the macro tables via the Airflow DAGs or seed data.
                </p>
              </div>
            )}
          </Card>
        </div>
      </div>
    </div>
  );
}
