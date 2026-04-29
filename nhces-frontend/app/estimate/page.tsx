'use client';
import { useState, useEffect } from 'react';
import { GS, COLOURS } from '@/lib/styles';
import Button from '@/components/ui/Button';
import { Input, Select } from '@/components/ui/Input';
import DataSourceBadge, { type DataSourceLevel } from '@/components/ui/DataSourceBadge';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import TemporalChart from '@/components/estimate/TemporalChart';
import { estimate, getMacroSnapshot, type EstimateResponse, type EstimateRequest, type ShapItem, type MacroSnapshot } from '@/lib/api';
import { formatNGN, formatNGNPerSqm } from '@/lib/formatters';

const BUILDING_TYPES = [
  { value: 'Residential',   label: 'Residential'   },
  { value: 'Commercial',    label: 'Commercial'    },
  { value: 'Industrial',    label: 'Industrial'    },
  { value: 'Institutional', label: 'Institutional' },
  { value: 'Mixed Use',     label: 'Mixed Use'     },
];
const CONSTRUCTION_TYPES = [
  { value: 'New Build',  label: 'New Build'  },
  { value: 'Renovation', label: 'Renovation' },
  { value: 'Extension',  label: 'Extension'  },
  { value: 'Fit-Out',    label: 'Fit-Out'    },
];
const ZONES = [
  { value: 'North Central', label: 'North Central' },
  { value: 'North East',    label: 'North East'    },
  { value: 'North West',    label: 'North West'    },
  { value: 'South East',    label: 'South East'    },
  { value: 'South South',   label: 'South South'   },
  { value: 'South West',    label: 'South West'    },
];

// Feature labels for the 14 derived model inputs (used in FeatureSnapshotPanel)
const FEATURE_LABELS: Record<string, [string, string]> = {
  d_gdp_growth_pct:        ['GDP Growth',    '\u0394 %pts YoY'],
  d_cpi_annual_pct:        ['CPI Inflation', '\u0394 %pts YoY'],
  d_lending_rate_pct:      ['Lending Rate',  '\u0394 %pts YoY'],
  d_brent_usd_barrel:      ['Brent Crude',   '\u0394 $/bbl YoY'],
  ret_ngn_usd:             ['NGN/USD',       '% chg YoY'],
  ret_ngn_eur:             ['NGN/EUR',       '% chg YoY'],
  ret_ngn_gbp:             ['NGN/GBP',       '% chg YoY'],
  lag1_d_gdp_growth_pct:   ['GDP Growth',    '\u0394 %pts (lag 1yr)'],
  lag1_d_cpi_annual_pct:   ['CPI Inflation', '\u0394 %pts (lag 1yr)'],
  lag1_d_lending_rate_pct: ['Lending Rate',  '\u0394 %pts (lag 1yr)'],
  lag1_d_brent_usd_barrel: ['Brent Crude',   '\u0394 $/bbl (lag 1yr)'],
  lag1_ret_ngn_usd:        ['NGN/USD',       '% chg (lag 1yr)'],
  lag1_ret_ngn_eur:        ['NGN/EUR',       '% chg (lag 1yr)'],
  lag1_ret_ngn_gbp:        ['NGN/GBP',       '% chg (lag 1yr)'],
};

// Part A — Macro Context Panel
// Shows raw macro values (from GET /macro) before the user submits.
function MacroContextPanel({ snapshot }: { snapshot: MacroSnapshot | null }) {
  const [open, setOpen] = useState(false);
  if (!snapshot) return null;
  return (
    <div style={{ marginTop: 14, border: `1px solid ${COLOURS.border}`, borderRadius: 10, overflow: 'hidden' }}>
      <button
        type="button"
        onClick={() => setOpen(o => !o)}
        style={{
          width: '100%', display: 'flex', alignItems: 'center',
          justifyContent: 'space-between', padding: '9px 14px',
          background: COLOURS.accentBg, border: 'none', cursor: 'pointer',
        }}
      >
        <span style={{ fontFamily: 'var(--font-ui)', fontSize: 12, fontWeight: 600, color: COLOURS.accent }}>
          B. Macroeconomic Inputs (auto-loaded)
        </span>
        <span style={{ fontFamily: 'var(--font-ui)', fontSize: 11, color: COLOURS.accent }}>
          {open ? '\u25b2 Hide' : '\u25bc Show'}
        </span>
      </button>
      {open && (
        <div style={{ padding: '10px 14px 12px' }}>
          <p style={{ fontFamily: 'var(--font-ui)', fontSize: 11, color: COLOURS.textDim, margin: '0 0 8px', lineHeight: 1.5 }}>
            Automatically fetched from the iNHCES data pipeline and used for your prediction.
            To update, visit the <a href="/macro" style={{ color: COLOURS.accent }}>Macro Data</a> page.
          </p>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '4px 8px' }}>
            {snapshot.variables.map(v => (
              <div key={v.variable} style={{ background: COLOURS.surfaceAlt, borderRadius: 6, padding: '5px 8px' }}>
                <p style={{ fontFamily: 'var(--font-ui)', fontSize: 10, color: COLOURS.textDim, margin: '0 0 1px', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
                  {v.label}
                </p>
                <p style={{ fontFamily: 'var(--font-ui)', fontSize: 12, fontWeight: 600, color: COLOURS.textPrimary, margin: 0 }}>
                  {v.value.toLocaleString('en-NG', { maximumFractionDigits: 2 })}{' '}
                  <span style={{ fontWeight: 400, color: COLOURS.textDim }}>{v.unit}</span>
                </p>
              </div>
            ))}
          </div>
          <div style={{ marginTop: 8 }}>
            <DataSourceBadge level={(snapshot.overall_freshness ?? 'RED') as DataSourceLevel} />
          </div>
        </div>
      )}
    </div>
  );
}

// Part B — Feature Snapshot Panel
// Shows the exact 14 derived model inputs used for a completed prediction.
function FeatureSnapshotPanel({ snapshot }: { snapshot: Record<string, number> }) {
  const [open, setOpen] = useState(false);
  const entries = Object.entries(snapshot);
  if (entries.length === 0) return null;
  return (
    <div style={{ background: COLOURS.surface, border: `1px solid ${COLOURS.border}`, borderRadius: 10, overflow: 'hidden' }}>
      <button
        type="button"
        onClick={() => setOpen(o => !o)}
        style={{
          width: '100%', display: 'flex', alignItems: 'center',
          justifyContent: 'space-between', padding: '9px 14px',
          background: COLOURS.surfaceAlt, border: 'none', cursor: 'pointer',
          borderBottom: open ? `1px solid ${COLOURS.border}` : 'none',
        }}
      >
        <span style={{ fontFamily: 'var(--font-ui)', fontSize: 12, fontWeight: 600, color: COLOURS.textMuted }}>
          All Model Inputs Used (14 features)
        </span>
        <span style={{ fontFamily: 'var(--font-ui)', fontSize: 11, color: COLOURS.textDim }}>
          {open ? '\u25b2 Hide' : '\u25bc Show'}
        </span>
      </button>
      {open && (
        <div style={{ padding: '10px 14px 12px' }}>
          <p style={{ fontFamily: 'var(--font-ui)', fontSize: 11, color: COLOURS.textDim, margin: '0 0 8px', lineHeight: 1.5 }}>
            Exact derived features fed into the LightGBM champion model for this prediction.
          </p>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '4px 8px' }}>
            {entries.map(([key, val]) => {
              const [name, unit] = FEATURE_LABELS[key] ?? [key, ''];
              const pos = val >= 0;
              return (
                <div key={key} style={{ background: COLOURS.surfaceAlt, borderRadius: 6, padding: '5px 8px' }}>
                  <p style={{ fontFamily: 'var(--font-ui)', fontSize: 10, color: COLOURS.textDim, margin: '0 0 1px' }}>
                    {name} <span style={{ fontStyle: 'italic' }}>({unit})</span>
                  </p>
                  <p style={{ fontFamily: 'var(--font-ui)', fontSize: 12, fontWeight: 600, color: pos ? COLOURS.textPrimary : COLOURS.red, margin: 0 }}>
                    {pos ? '+' : ''}{val.toFixed(2)}
                  </p>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}

// Compact SHAP chart
function ShapBars({ items }: { items: ShapItem[] }) {
  const maxAbs = Math.max(...items.map(i => Math.abs(i.value)), 1);
  return (
    <div>
      {items.slice(0, 5).map(item => {
        const pct = Math.abs(item.value) / maxAbs * 100;
        const pos = item.value >= 0;
        return (
          <div key={item.feature} style={{ marginBottom: 8 }}>
            <div style={{ ...GS.spaceBetween, marginBottom: 3 }}>
              <span style={{ fontFamily: 'var(--font-ui)', fontSize: 11, color: COLOURS.textMuted }}>
                {item.label}
              </span>
              <span style={{ fontFamily: 'var(--font-ui)', fontSize: 11, fontWeight: 600, color: pos ? COLOURS.green : COLOURS.red }}>
                {pos ? '+' : ''}{item.value.toLocaleString('en-NG', { maximumFractionDigits: 0 })}
              </span>
            </div>
            <div style={{ height: 6, background: COLOURS.surfaceAlt, borderRadius: 3 }}>
              <div style={{ height: '100%', width: `${pct}%`, background: pos ? COLOURS.green : COLOURS.red, borderRadius: 3, transition: 'width 0.5s ease' }} />
            </div>
          </div>
        );
      })}
    </div>
  );
}

// Result panel
function ResultPanel({ result }: { result: EstimateResponse }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 10, height: '100%' }}>
      {/* Primary figure */}
      <div style={{
        background:   COLOURS.accentBg,
        border:       `1px solid ${COLOURS.accentBorder}`,
        borderRadius: 10,
        padding:      '14px 16px',
      }}>
        <p style={{ ...GS.label, margin: '0 0 4px' }}>Predicted Cost Per Sqm</p>
        <p style={{
          fontFamily: 'var(--font-display)',
          fontSize:   28,
          fontWeight: 700,
          color:      COLOURS.accent,
          margin:     '0 0 4px',
          lineHeight: 1.1,
        }}>
          {formatNGNPerSqm(result.predicted_cost_per_sqm)}
        </p>
        <p style={{ fontFamily: 'var(--font-ui)', fontSize: 12, color: COLOURS.textMuted, margin: 0 }}>
          90% CI: {formatNGN(result.confidence_lower)} – {formatNGN(result.confidence_upper)}/sqm
        </p>
      </div>

      {/* Total cost */}
      <div style={{
        background:     COLOURS.textPrimary,
        borderRadius:   10,
        padding:        '12px 16px',
        display:        'flex',
        justifyContent: 'space-between',
        alignItems:     'center',
      }}>
        <span style={{ fontFamily: 'var(--font-ui)', fontSize: 12, color: COLOURS.surfaceAlt }}>Total Estimated Cost</span>
        <span style={{ fontFamily: 'var(--font-display)', fontSize: 18, fontWeight: 700, color: COLOURS.white }}>
          {formatNGN(result.total_predicted_cost_ngn)}
        </span>
      </div>

      {/* Model meta */}
      <div style={{
        display:      'grid',
        gridTemplateColumns: '1fr 1fr',
        gap:          '4px 12px',
        background:   COLOURS.surface,
        border:       `1px solid ${COLOURS.border}`,
        borderRadius: 10,
        padding:      '10px 14px',
      }}>
        {[
          ['Model',   result.model_name],
          ['MAPE',    `${result.mape_at_prediction.toFixed(2)}%`],
          ['Version', result.model_version],
          ['Time',    `${result.api_response_ms ?? '--'} ms`],
        ].map(([k, v]) => (
          <div key={k}>
            <p style={{ fontFamily: 'var(--font-ui)', fontSize: 10, color: COLOURS.textDim, margin: '0 0 1px', textTransform: 'uppercase', letterSpacing: '0.04em' }}>{k}</p>
            <p style={{ fontFamily: 'var(--font-ui)', fontSize: 12, fontWeight: 600, color: COLOURS.textPrimary, margin: 0 }}>{v}</p>
          </div>
        ))}
      </div>

      {/* Data freshness */}
      <DataSourceBadge level={(result.data_freshness ?? 'RED') as DataSourceLevel} />

      {/* Temporal Cost Projection Chart */}
      {result.projections && result.projections.length > 1 && (
        <div style={{
          background:   COLOURS.surface,
          border:       `1px solid ${COLOURS.border}`,
          borderRadius: 10,
          padding:      '12px 14px',
        }}>
          <TemporalChart
            projections={result.projections}
            annualInflationRate={result.annual_inflation_rate ?? 12}
          />
        </div>
      )}

      {/* SHAP */}
      {result.shap_top_features?.length > 0 && (
        <div style={{
          background:   COLOURS.surface,
          border:       `1px solid ${COLOURS.border}`,
          borderRadius: 10,
          padding:      '10px 14px',
        }}>
          <p style={{ ...GS.label, margin: '0 0 10px' }}>Feature Importance (SHAP)</p>
          <ShapBars items={result.shap_top_features} />
        </div>
      )}

      {/* Part B: All model inputs — full feature snapshot with human-readable labels */}
      {result.feature_snapshot && Object.keys(result.feature_snapshot).length > 0 && (
        <FeatureSnapshotPanel snapshot={result.feature_snapshot} />
      )}
    </div>
  );
}

// Placeholder for right panel before submission
function PlaceholderPanel() {
  return (
    <div style={{
      display:        'flex',
      flexDirection:  'column',
      alignItems:     'center',
      justifyContent: 'center',
      height:         '100%',
      background:     COLOURS.surface,
      border:         `1px dashed ${COLOURS.border2}`,
      borderRadius:   12,
      padding:        32,
      textAlign:      'center',
    }}>
      <div style={{
        width:        56,
        height:       56,
        borderRadius: '50%',
        background:   COLOURS.accentBg,
        border:       `2px solid ${COLOURS.accentBorder}`,
        display:      'flex',
        alignItems:   'center',
        justifyContent:'center',
        fontSize:     24,
        marginBottom: 16,
      }}>
        🏗️
      </div>
      <h3 style={{ fontFamily: 'var(--font-display)', fontSize: 16, color: COLOURS.textPrimary, margin: '0 0 8px' }}>
        Your estimate will appear here
      </h3>
      <p style={{ fontFamily: 'var(--font-body)', fontSize: 13, color: COLOURS.textMuted, margin: 0, lineHeight: 1.6 }}>
        Fill in the project details on the left and click
        <strong> Calculate Cost</strong> to get an AI-powered
        cost prediction with SHAP explainability.
      </p>
    </div>
  );
}

// ── Main page ─────────────────────────────────────────────────────────────────
export default function EstimatePage() {
  const [form,    setForm]    = useState<Partial<EstimateRequest>>({
    building_type: 'Residential', construction_type: 'New Build',
    location_zone: 'North West',  num_floors: 1,
  });
  const [loading,       setLoading]       = useState(false);
  const [result,        setResult]        = useState<EstimateResponse | null>(null);
  const [error,         setError]         = useState<string | null>(null);
  const [macroSnapshot, setMacroSnapshot] = useState<MacroSnapshot | null>(null);

  // Part A: load macro context on mount so values are visible before submission
  useEffect(() => {
    getMacroSnapshot()
      .then(setMacroSnapshot)
      .catch(() => { /* silent — panel simply won't render if API is unavailable */ });
  }, []);

  function set(k: keyof EstimateRequest, v: string | number) {
    setForm(p => ({ ...p, [k]: v }));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    if (!form.floor_area_sqm || !form.location_state) {
      setError('Floor area and location state are required.'); return;
    }
    setLoading(true);
    try {
      setResult(await estimate(form as EstimateRequest));
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Estimation failed.');
    } finally { setLoading(false); }
  }

  return (
    // Full-height, centered, no scroll
    <div style={{
      height:         'calc(100vh - 60px)',
      display:        'flex',
      flexDirection:  'column',
      overflow:       'hidden',
      background:     COLOURS.background,
    }}>
      {/* Page title bar */}
      <div style={{
        padding:      '12px 40px 10px',
        borderBottom: `1px solid ${COLOURS.border}`,
        background:   COLOURS.surface,
        flexShrink:   0,
      }}>
        <h1 style={{ fontFamily: 'var(--font-display)', fontSize: 18, fontWeight: 700, color: COLOURS.textPrimary, margin: 0 }}>
          Cost Estimation
        </h1>
        <p style={{ fontFamily: 'var(--font-ui)', fontSize: 12, color: COLOURS.textDim, margin: '2px 0 0' }}>
          AI-powered construction cost per sqm · LightGBM champion · TETFund NRF 2025
        </p>
      </div>

      {/* Two-column body */}
      <div style={{
        flex:                1,
        display:             'grid',
        gridTemplateColumns: '420px 1fr',
        gap:                 20,
        padding:             '20px 40px',
        overflow:            'hidden',
        maxWidth:            1100,
        margin:              '0 auto',
        width:               '100%',
        boxSizing:           'border-box',
      }}>

        {/* ── LEFT: Form ──────────────────────────────────────────────── */}
        <div style={{
          background:   COLOURS.surface,
          border:       `1px solid ${COLOURS.border}`,
          borderRadius: 12,
          padding:      '18px 20px',
          overflowY:    'auto',
          display:      'flex',
          flexDirection:'column',
          gap:          0,
        }}>
          <h2 style={{ fontFamily: 'var(--font-display)', fontSize: 15, fontWeight: 700, margin: '0 0 3px', color: COLOURS.textPrimary }}>
            Project Details
          </h2>
          <p style={{ fontFamily: 'var(--font-ui)', fontSize: 11, color: COLOURS.textDim, margin: '0 0 12px' }}>
            A. User-provided project inputs
          </p>

          <form onSubmit={handleSubmit}>
            {/* Row 1: Building type + Construction type */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10, marginBottom: 10 }}>
              <Select label="Building Type" options={BUILDING_TYPES}
                value={form.building_type ?? 'Residential'}
                onChange={e => set('building_type', e.target.value)} />
              <Select label="Construction Type" options={CONSTRUCTION_TYPES}
                value={form.construction_type ?? 'New Build'}
                onChange={e => set('construction_type', e.target.value)} />
            </div>

            {/* Row 2: Floor area + Floors */}
            <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: 10, marginBottom: 10 }}>
              <Input label="Floor Area (sqm) *" type="number" min={1} placeholder="e.g. 120"
                value={form.floor_area_sqm ?? ''}
                onChange={e => set('floor_area_sqm', parseFloat(e.target.value))} />
              <Input label="Floors" type="number" min={1} placeholder="1"
                value={form.num_floors ?? 1}
                onChange={e => set('num_floors', parseInt(e.target.value))} />
            </div>

            {/* Row 3: State + Zone */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10, marginBottom: 14 }}>
              <Input label="State *" placeholder="e.g. Kaduna"
                value={form.location_state ?? ''}
                onChange={e => set('location_state', e.target.value)} />
              <Select label="Zone" options={ZONES}
                value={form.location_zone ?? 'North West'}
                onChange={e => set('location_zone', e.target.value)} />
            </div>

            {error && (
              <div style={{ ...GS.alertDanger, marginBottom: 12, fontSize: 13 }}>{error}</div>
            )}

            <Button type="submit" loading={loading} style={{ width: '100%', marginTop: 2 }}>
              {loading ? 'Consulting champion model...' : '⚡  Calculate Cost'}
            </Button>

            <p style={{ fontFamily: 'var(--font-ui)', fontSize: 11, color: COLOURS.textDim, textAlign: 'center', margin: '10px 0 0' }}>
              LightGBM · 13.66% LOO-CV MAPE · No login required
            </p>
          </form>

          {/* Part A: Macro context — raw values auto-loaded from iNHCES pipeline */}
          <MacroContextPanel snapshot={macroSnapshot} />
        </div>

        {/* ── RIGHT: Result or Placeholder ────────────────────────────── */}
        <div style={{ overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
          {loading && !result ? (
            <div style={{
              flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center',
              background: COLOURS.surface, border: `1px solid ${COLOURS.border}`, borderRadius: 12,
            }}>
              <LoadingSpinner label="Consulting champion model..." />
            </div>
          ) : result ? (
            <div style={{ flex: 1, overflowY: 'auto' }} className="anim">
              <ResultPanel result={result} />
            </div>
          ) : (
            <PlaceholderPanel />
          )}
        </div>

      </div>
    </div>
  );
}
