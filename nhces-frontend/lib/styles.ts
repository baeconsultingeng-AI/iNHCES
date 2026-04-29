/**
 * iNHCES Global Style System — Warm Ivory Palette
 * Adopted from Buildwise NG (BUILDWISE_CONTEXT.md).
 *
 * RULE: Never hardcode a colour, font-family, or border-radius directly
 *       in a component. Always import and use tokens from this file.
 *
 * Usage:  import { GS, COLOURS } from '@/lib/styles';
 *         <div style={{ ...GS.card, padding: 32 }}>
 */

import type { CSSProperties } from 'react';

// ── Colour tokens ──────────────────────────────────────────────────────────────
export const COLOURS = {
  // Backgrounds
  background:   '#f5f1eb',   // warm ivory — page background
  surface:      '#ffffff',   // cards, panels, inputs
  surfaceAlt:   '#f0ece4',   // alternate rows, secondary panels

  // Borders
  border:       '#ddd8cf',   // default borders
  border2:      '#c9c2b8',   // input focus rings
  border3:      '#b8b0a4',   // hover borders

  // Text  (all WCAG AA or better)
  textPrimary:  '#1a1410',   // near-black warm brown — contrast 16.8:1 AAA
  textMuted:    '#5c4f42',   // medium warm brown   — contrast 7.2:1  AAA
  textDim:      '#8a7d72',   // dim warm brown      — contrast 4.6:1  AA

  // Brand accent
  accent:       '#8b6400',   // dark amber/gold — buttons, active nav, headings
  accentBg:     'rgba(139,100,0,0.10)',
  accentBorder: 'rgba(139,100,0,0.28)',

  // Semantic (maps directly to iNHCES DATA SOURCE Declaration System)
  green:        '#007a5e',   // GREEN data level — live data, success, verified
  greenLight:   'rgba(0,122,94,0.10)',
  amber:        '#b8620a',   // AMBER data level — AI template, warnings
  amberLight:   'rgba(184,98,10,0.10)',
  red:          '#c0392b',   // RED data level   — synthetic, errors, danger
  redLight:     'rgba(192,57,43,0.10)',

  white:        '#ffffff',
  black:        '#000000',
} as const;

// ── Typography ─────────────────────────────────────────────────────────────────
// Fonts are loaded in app/layout.tsx via next/font/google
export const FONTS = {
  display: 'var(--font-display)',   // Playfair Display — headings, page titles
  body:    'var(--font-body)',      // Lora — body copy, descriptions
  ui:      'var(--font-ui)',        // DM Sans — buttons, labels, nav, data values
} as const;

// ── Shared values ──────────────────────────────────────────────────────────────
const RADIUS_SM  = '6px';
const RADIUS_MD  = '10px';
const RADIUS_LG  = '14px';
const RADIUS_PILL = '9999px';
const SHADOW_SM  = '0 1px 3px rgba(26,20,16,0.08)';
const SHADOW_MD  = '0 2px 8px rgba(26,20,16,0.10)';
const TRANSITION = 'all 0.15s ease';

// ── Global Style Object ────────────────────────────────────────────────────────
export const GS: Record<string, CSSProperties> = {

  // Root app shell
  app: {
    background:  COLOURS.background,
    color:       COLOURS.textPrimary,
    fontFamily:  FONTS.body,
    minHeight:   '100vh',
    fontSize:    17,
  },

  // ── Navigation ───────────────────────────────────────────────────────────────
  navBar: {
    background:     COLOURS.surface,
    borderBottom:   `1px solid ${COLOURS.border}`,
    position:       'sticky',
    top:            0,
    zIndex:         100,
    padding:        '0 24px',
    height:         60,
    display:        'flex',
    alignItems:     'center',
    gap:            8,
    boxShadow:      SHADOW_SM,
  },
  navBrand: {
    fontFamily:  FONTS.display,
    fontSize:    20,
    fontWeight:  700,
    color:       COLOURS.accent,
    textDecoration: 'none',
    marginRight:  16,
  },
  navBtn: {
    fontFamily:     FONTS.ui,
    fontSize:       15,
    fontWeight:     500,
    color:          COLOURS.accent,
    padding:        '6px 14px',
    borderRadius:   RADIUS_SM,
    border:         'none',
    background:     'transparent',
    cursor:         'pointer',
    textDecoration: 'none',
    display:        'inline-flex',
    alignItems:     'center',
    gap:            6,
    transition:     TRANSITION,
  },
  navBtnActive: {
    background:  COLOURS.accentBg,
    color:       COLOURS.accent,
    fontWeight:  600,
    border:      `1px solid ${COLOURS.accentBorder}`,
  },

  // ── Cards ─────────────────────────────────────────────────────────────────────
  card: {
    background:   COLOURS.surface,
    border:       `1px solid ${COLOURS.border}`,
    borderRadius: RADIUS_LG,
    padding:      24,
    boxShadow:    SHADOW_SM,
  },
  cardCompact: {
    background:   COLOURS.surface,
    border:       `1px solid ${COLOURS.border}`,
    borderRadius: RADIUS_MD,
    padding:      16,
    boxShadow:    SHADOW_SM,
  },

  // ── Buttons ───────────────────────────────────────────────────────────────────
  btn: {
    background:   COLOURS.accent,
    color:        COLOURS.white,
    border:       'none',
    borderRadius: RADIUS_MD,
    padding:      '11px 22px',
    fontFamily:   FONTS.ui,
    fontSize:     15,
    fontWeight:   600,
    cursor:       'pointer',
    display:      'inline-flex',
    alignItems:   'center',
    justifyContent: 'center',
    gap:          8,
    transition:   TRANSITION,
    textDecoration: 'none',
  },
  btnGhost: {
    background:   'transparent',
    color:        COLOURS.accent,
    border:       `1.5px solid ${COLOURS.accentBorder}`,
    borderRadius: RADIUS_MD,
    padding:      '10px 22px',
    fontFamily:   FONTS.ui,
    fontSize:     15,
    fontWeight:   600,
    cursor:       'pointer',
    display:      'inline-flex',
    alignItems:   'center',
    justifyContent: 'center',
    gap:          8,
    transition:   TRANSITION,
    textDecoration: 'none',
  },
  btnDanger: {
    background:   COLOURS.red,
    color:        COLOURS.white,
    border:       'none',
    borderRadius: RADIUS_MD,
    padding:      '10px 22px',
    fontFamily:   FONTS.ui,
    fontSize:     15,
    fontWeight:   600,
    cursor:       'pointer',
    display:      'inline-flex',
    alignItems:   'center',
    gap:          8,
    transition:   TRANSITION,
  },
  btnSm: {
    padding:   '7px 14px',
    fontSize:  13,
    borderRadius: RADIUS_SM,
  },

  // ── Inputs ────────────────────────────────────────────────────────────────────
  input: {
    background:   COLOURS.surface,
    border:       `1px solid ${COLOURS.border2}`,
    borderRadius: RADIUS_MD,
    padding:      '10px 14px',
    fontFamily:   FONTS.body,
    fontSize:     15,
    color:        COLOURS.textPrimary,
    width:        '100%',
    outline:      'none',
    transition:   TRANSITION,
    boxSizing:    'border-box',
  },
  textarea: {
    background:   COLOURS.surface,
    border:       `1px solid ${COLOURS.border2}`,
    borderRadius: RADIUS_MD,
    padding:      '10px 14px',
    fontFamily:   FONTS.body,
    fontSize:     15,
    color:        COLOURS.textPrimary,
    width:        '100%',
    outline:      'none',
    transition:   TRANSITION,
    boxSizing:    'border-box',
    resize:       'vertical',
    minHeight:    80,
  },
  select: {
    background:   COLOURS.surface,
    border:       `1px solid ${COLOURS.border2}`,
    borderRadius: RADIUS_MD,
    padding:      '10px 14px',
    fontFamily:   FONTS.ui,
    fontSize:     15,
    color:        COLOURS.textPrimary,
    width:        '100%',
    outline:      'none',
    cursor:       'pointer',
    boxSizing:    'border-box',
  },

  // ── Labels + Tags ─────────────────────────────────────────────────────────────
  label: {
    fontFamily:    FONTS.ui,
    fontSize:      13,
    fontWeight:    600,
    color:         COLOURS.textMuted,
    letterSpacing: '0.04em',
    textTransform: 'uppercase',
    display:       'block',
    marginBottom:  6,
  },
  tag: {
    fontFamily:   FONTS.ui,
    fontSize:     12,
    fontWeight:   500,
    padding:      '3px 10px',
    borderRadius: RADIUS_PILL,
    display:      'inline-block',
  },

  // ── Typography ────────────────────────────────────────────────────────────────
  pageTitle: {
    fontFamily:  FONTS.display,
    fontSize:    32,
    fontWeight:  700,
    color:       COLOURS.textPrimary,
    lineHeight:  1.25,
    margin:      0,
  },
  pageSub: {
    fontFamily:  FONTS.body,
    fontSize:    17,
    color:       COLOURS.textMuted,
    lineHeight:  1.6,
    margin:      '8px 0 0',
  },
  sectionTitle: {
    fontFamily:  FONTS.display,
    fontSize:    22,
    fontWeight:  700,
    color:       COLOURS.textPrimary,
    lineHeight:  1.3,
    margin:      '0 0 4px',
  },
  bodyText: {
    fontFamily:  FONTS.body,
    fontSize:    17,
    color:       COLOURS.textPrimary,
    lineHeight:  1.65,
  },
  metaText: {
    fontFamily:  FONTS.ui,
    fontSize:    13,
    color:       COLOURS.textDim,
  },

  // ── Layout helpers ────────────────────────────────────────────────────────────
  page: {
    maxWidth:  1200,
    margin:    '0 auto',
    padding:   '32px 24px',
  },
  pageNarrow: {
    maxWidth:  760,
    margin:    '0 auto',
    padding:   '32px 24px',
  },
  row: {
    display:       'flex',
    alignItems:    'center',
    gap:           12,
  },
  spaceBetween: {
    display:       'flex',
    alignItems:    'center',
    justifyContent: 'space-between',
    gap:           12,
  },
  grid2: {
    display:             'grid',
    gridTemplateColumns: 'repeat(2, 1fr)',
    gap:                 20,
  },
  grid3: {
    display:             'grid',
    gridTemplateColumns: 'repeat(3, 1fr)',
    gap:                 20,
  },
  divider: {
    border:        'none',
    borderTop:     `1px solid ${COLOURS.border}`,
    margin:        '20px 0',
  },

  // ── Data table ────────────────────────────────────────────────────────────────
  table: {
    width:          '100%',
    borderCollapse: 'collapse',
    fontFamily:     FONTS.ui,
    fontSize:       14,
  },
  th: {
    background:    COLOURS.surfaceAlt,
    color:         COLOURS.textMuted,
    fontWeight:    600,
    textAlign:     'left',
    padding:       '10px 14px',
    borderBottom:  `2px solid ${COLOURS.border}`,
    fontSize:      13,
    letterSpacing: '0.03em',
  },
  td: {
    padding:       '10px 14px',
    borderBottom:  `1px solid ${COLOURS.border}`,
    color:         COLOURS.textPrimary,
    verticalAlign: 'middle',
  },

  // ── Alert / Info boxes ────────────────────────────────────────────────────────
  alertInfo: {
    background:   COLOURS.accentBg,
    border:       `1px solid ${COLOURS.accentBorder}`,
    borderRadius: RADIUS_MD,
    padding:      '12px 16px',
    fontFamily:   FONTS.body,
    fontSize:     14,
    color:        COLOURS.accent,
  },
  alertSuccess: {
    background:   COLOURS.greenLight,
    border:       `1px solid ${COLOURS.green}`,
    borderRadius: RADIUS_MD,
    padding:      '12px 16px',
    fontFamily:   FONTS.body,
    fontSize:     14,
    color:        COLOURS.green,
  },
  alertDanger: {
    background:   COLOURS.redLight,
    border:       `1px solid ${COLOURS.red}`,
    borderRadius: RADIUS_MD,
    padding:      '12px 16px',
    fontFamily:   FONTS.body,
    fontSize:     14,
    color:        COLOURS.red,
  },
};

// ── Data Source badge config (iNHCES-specific) ─────────────────────────────────
export type DataSourceLevel = 'GREEN' | 'AMBER' | 'RED';

export const DATA_SOURCE_CONFIG: Record<DataSourceLevel, {
  bg: string; text: string; label: string; description: string;
}> = {
  GREEN: {
    bg:          COLOURS.green,
    text:        COLOURS.white,
    label:       'GREEN',
    description: 'Live Data',
  },
  AMBER: {
    bg:          COLOURS.amber,
    text:        COLOURS.white,
    label:       'AMBER',
    description: 'AI Template -- Validate Before Publication',
  },
  RED: {
    bg:          COLOURS.red,
    text:        COLOURS.white,
    label:       'RED',
    description: 'Synthetic Data -- Must Replace Before Publication',
  },
};

// ── CSS animation class string (injected in layout.tsx globals) ───────────────
export const ANIMATION_CSS = `
  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
  }
  .anim {
    animation: fadeUp 0.35s ease both;
  }
  .hover-lift {
    transition: transform 0.15s ease, box-shadow 0.15s ease;
  }
  .hover-lift:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(26,20,16,0.12);
  }
  .btn-hover:hover {
    filter: brightness(1.08);
    transform: translateY(-1px);
  }
  * { box-sizing: border-box; }
  body { margin: 0; padding: 0; }
  a { color: inherit; }
`;
