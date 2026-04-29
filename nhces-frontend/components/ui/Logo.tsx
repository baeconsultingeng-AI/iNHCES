/**
 * iNHCES Logo Component
 *
 * Renders the iNHCES icon mark (house + "i" dot + ascending bars) with
 * an optional wordmark. The icon mark is an inline SVG — no external files
 * required, works at any size.
 *
 * Design rationale:
 *   • The golden circle at the roof peak = the "i" in iNHCES (AI intelligence)
 *   • The house silhouette = national housing domain
 *   • Three ascending bars inside the house = cost estimation / ML projections
 *   • Colour: COLOURS.accent (#8b6400 warm gold) — matches Warm Ivory palette
 *
 * Usage:
 *   <Logo />                          // icon + wordmark, default 28px icon
 *   <Logo size={40} textSize={22} />  // larger variant (e.g. landing page)
 *   <Logo showText={false} size={20}/>// icon only (e.g. mobile / favicon)
 */

import { COLOURS, FONTS } from '@/lib/styles';

interface LogoProps {
  /** Width & height of the icon mark in px. Default: 28 */
  size?: number;
  /** Whether to show the "iNHCES" wordmark text. Default: true */
  showText?: boolean;
  /** Font size of the wordmark in px. Default: 19 */
  textSize?: number;
}

export default function Logo({ size = 28, showText = true, textSize = 19 }: LogoProps) {
  const c = COLOURS.accent; // #8b6400

  return (
    <span style={{ display: 'inline-flex', alignItems: 'center', gap: Math.round(size * 0.28) }}>
      {/* Icon mark — inline SVG, no external dependency */}
      <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 40 40"
        width={size}
        height={size}
        fill="none"
        aria-hidden="true"
        style={{ flexShrink: 0 }}
      >
        {/* "i" dot — intelligence / AI dot above roof peak */}
        <circle cx="20" cy="5" r="2.5" fill={c} />

        {/* Roof — two lines from base corners meeting at peak (20, 11) */}
        <path
          d="M6 20L20 11L34 20"
          stroke={c}
          strokeWidth="1.8"
          strokeLinecap="round"
          strokeLinejoin="round"
        />

        {/* House body — semi-transparent fill with solid border */}
        <rect
          x="6" y="20" width="28" height="17" rx="1"
          fill={c} fillOpacity="0.08"
          stroke={c} strokeWidth="1.8"
        />

        {/* Ascending bars — cost estimation / ML projections over time */}
        {/* All bars share the same bottom (y=37 = rect bottom) */}
        <rect x="9"  y="29" width="5" height="8"  rx="0.5" fill={c} fillOpacity="0.40" />
        <rect x="17" y="26" width="5" height="11" rx="0.5" fill={c} fillOpacity="0.68" />
        <rect x="25" y="23" width="5" height="14" rx="0.5" fill={c} />
      </svg>

      {/* Wordmark */}
      {showText && (
        <span
          style={{
            fontFamily:    FONTS.display,
            fontSize:      textSize,
            fontWeight:    700,
            color:         c,
            letterSpacing: '-0.01em',
            lineHeight:    1,
            userSelect:    'none',
          }}
        >
          iNHCES
        </span>
      )}
    </span>
  );
}
