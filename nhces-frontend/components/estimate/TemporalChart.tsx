/**
 * TemporalChart — iNHCES Cost Projection Chart
 *
 * Displays construction cost projections at 4 horizons
 * (Current, <1yr, <3yrs, <5yrs) with widening confidence bands.
 *
 * Design: Warm Ivory palette, SVG-based (no external charting library).
 * Confidence band grows with horizon to honestly represent increasing uncertainty.
 */

import { COLOURS } from '@/lib/styles';
import { type ProjectionPoint } from '@/lib/api';
import { formatNGN } from '@/lib/formatters';

interface TemporalChartProps {
  projections:         ProjectionPoint[];
  annualInflationRate: number;
}

const W = 520;
const H = 200;
const PAD_L = 70;
const PAD_R = 20;
const PAD_T = 20;
const PAD_B = 48;
const CHART_W = W - PAD_L - PAD_R;
const CHART_H = H - PAD_T - PAD_B;

export default function TemporalChart({ projections, annualInflationRate }: TemporalChartProps) {
  if (!projections || projections.length === 0) return null;

  // Compute chart bounds
  const allValues = projections.flatMap(p => [p.confidence_lower, p.cost_per_sqm, p.confidence_upper]);
  const minV = Math.max(0, Math.min(...allValues) * 0.85);
  const maxV = Math.max(...allValues) * 1.08;
  const range = maxV - minV || 1;

  // Map value to y pixel
  const toY = (v: number) => PAD_T + CHART_H - ((v - minV) / range) * CHART_H;

  // Map index to x pixel (equal spacing)
  const toX = (i: number) =>
    PAD_L + (i / Math.max(projections.length - 1, 1)) * CHART_W;

  // Build path strings
  const pts = projections.map((p, i) => ({
    x:     toX(i),
    y:     toY(p.cost_per_sqm),
    yLo:   toY(p.confidence_lower),
    yHi:   toY(p.confidence_upper),
    label: p.horizon_label,
    cost:  p.cost_per_sqm,
    lower: p.confidence_lower,
    upper: p.confidence_upper,
    unc:   p.uncertainty_pct,
    proj:  p.is_projection,
  }));

  const linePath  = pts.map((p, i) => `${i === 0 ? 'M' : 'L'} ${p.x.toFixed(1)} ${p.y.toFixed(1)}`).join(' ');
  const areaTop   = pts.map((p, i) => `${i === 0 ? 'M' : 'L'} ${p.x.toFixed(1)} ${p.yHi.toFixed(1)}`).join(' ');
  const areaBot   = [...pts].reverse().map((p, i) => `${i === 0 ? 'L' : 'L'} ${p.x.toFixed(1)} ${p.yLo.toFixed(1)}`).join(' ');
  const areaPath  = `${areaTop} ${areaBot} Z`;

  // Y-axis grid labels (4 steps)
  const gridSteps = 4;
  const gridVals  = Array.from({ length: gridSteps + 1 }, (_, i) =>
    minV + (i / gridSteps) * range
  );

  const currentCost = projections[0]?.cost_per_sqm ?? 0;
  const lastCost    = projections[projections.length - 1]?.cost_per_sqm ?? 0;
  const change5yr   = currentCost > 0 ? ((lastCost / currentCost - 1) * 100).toFixed(1) : '0';

  return (
    <div>
      {/* Chart title */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginBottom: 8 }}>
        <div>
          <p style={{
            fontFamily: 'var(--font-ui)', fontSize: 11, fontWeight: 600,
            color: COLOURS.textMuted, margin: 0, letterSpacing: '0.05em', textTransform: 'uppercase',
          }}>
            Cost Projection (NGN/sqm)
          </p>
          <p style={{ fontFamily: 'var(--font-ui)', fontSize: 10, color: COLOURS.textDim, margin: '2px 0 0' }}>
            Compound inflation at {annualInflationRate.toFixed(1)}% p.a. · CI widens with horizon
          </p>
        </div>
        <span style={{
          fontFamily:   'var(--font-ui)', fontSize: 12, fontWeight: 600,
          color:        parseFloat(change5yr) > 0 ? COLOURS.red : COLOURS.green,
          background:   parseFloat(change5yr) > 0 ? COLOURS.redLight : COLOURS.greenLight,
          padding:      '3px 8px', borderRadius: 6,
        }}>
          5yr: {parseFloat(change5yr) > 0 ? '+' : ''}{change5yr}%
        </span>
      </div>

      {/* SVG Chart */}
      <svg
        viewBox={`0 0 ${W} ${H}`}
        style={{ width: '100%', height: H, display: 'block', overflow: 'visible' }}
      >
        {/* Grid lines */}
        {gridVals.map((v, i) => {
          const y = toY(v);
          return (
            <g key={i}>
              <line
                x1={PAD_L} x2={W - PAD_R}
                y1={y} y2={y}
                stroke={COLOURS.border} strokeWidth={0.6}
              />
              <text
                x={PAD_L - 6} y={y + 4}
                textAnchor="end" fontSize={9}
                fill={COLOURS.textDim}
              >
                {formatNGN(v).replace('NGN ', '')}
              </text>
            </g>
          );
        })}

        {/* Confidence band (shaded area) */}
        <path
          d={areaPath}
          fill={COLOURS.accentBg}
          stroke="none"
        />

        {/* Dashed line separating current from projections */}
        {pts.length > 1 && (
          <line
            x1={pts[0].x + (pts[1].x - pts[0].x) / 2}
            x2={pts[0].x + (pts[1].x - pts[0].x) / 2}
            y1={PAD_T}
            y2={H - PAD_B}
            stroke={COLOURS.border2}
            strokeWidth={1}
            strokeDasharray="4 3"
          />
        )}

        {/* Main cost line */}
        <path
          d={linePath}
          fill="none"
          stroke={COLOURS.accent}
          strokeWidth={2.5}
          strokeLinejoin="round"
        />

        {/* Data points */}
        {pts.map((p, i) => (
          <g key={i}>
            {/* Point circle */}
            <circle
              cx={p.x} cy={p.y}
              r={p.proj ? 4 : 5}
              fill={p.proj ? COLOURS.accent : COLOURS.textPrimary}
              stroke={COLOURS.surface}
              strokeWidth={2}
            />

            {/* X-axis label */}
            <text
              x={p.x} y={H - PAD_B + 16}
              textAnchor="middle"
              fontSize={9}
              fill={p.proj ? COLOURS.textMuted : COLOURS.textPrimary}
              fontWeight={p.proj ? 400 : 600}
            >
              {p.label.replace('Short-term ', '<1yr').replace('Medium-term ', '<3yrs').replace('Long-term ', '<5yrs')}
            </text>

            {/* Cost label above point (alternate above/below to avoid overlap) */}
            <text
              x={p.x}
              y={p.y - 9}
              textAnchor="middle"
              fontSize={8.5}
              fill={COLOURS.accent}
              fontWeight={600}
            >
              {formatNGN(p.cost).replace('NGN ', '')}
            </text>

            {/* Uncertainty % for projection points */}
            {p.proj && (
              <text
                x={p.x} y={H - PAD_B + 27}
                textAnchor="middle"
                fontSize={8}
                fill={COLOURS.textDim}
              >
                ±{p.unc.toFixed(0)}%
              </text>
            )}
          </g>
        ))}

        {/* "NOW" label */}
        <text
          x={pts[0]?.x ?? 0} y={H - PAD_B + 38}
          textAnchor="middle"
          fontSize={8}
          fill={COLOURS.textDim}
          fontStyle="italic"
        >
          now
        </text>
      </svg>

      {/* Legend */}
      <div style={{ display: 'flex', gap: 16, marginTop: 6, justifyContent: 'center' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 5 }}>
          <div style={{ width: 20, height: 2.5, background: COLOURS.accent, borderRadius: 2 }} />
          <span style={{ fontFamily: 'var(--font-ui)', fontSize: 10, color: COLOURS.textDim }}>
            Point estimate
          </span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 5 }}>
          <div style={{ width: 14, height: 10, background: COLOURS.accentBg, borderRadius: 3 }} />
          <span style={{ fontFamily: 'var(--font-ui)', fontSize: 10, color: COLOURS.textDim }}>
            90% confidence band
          </span>
        </div>
      </div>

      {/* Disclaimer */}
      <p style={{
        fontFamily:   'var(--font-ui)',
        fontSize:     10,
        color:        COLOURS.textDim,
        margin:       '8px 0 0',
        lineHeight:   1.4,
        borderTop:    `1px solid ${COLOURS.border}`,
        paddingTop:   6,
      }}>
        ⚠ Projections are indicative cost scenarios based on compound inflation methodology (VAR + LightGBM).
        Confidence bands widen with horizon. Not a financial forecast. Verify with a qualified QS before committing to a budget.
        DATA SOURCE: {projections[0]?.is_projection === false ? 'AMBER' : 'RED'} — synthetic proxy until real NIQS data is configured.
      </p>
    </div>
  );
}
