/**
 * DataSourceBadge — iNHCES mandatory UI component.
 *
 * Must appear on every page that displays ML predictions, macro data,
 * or any content derived from the iNHCES data pipeline.
 *
 * Operationalises the DATA SOURCE Declaration System at the UI level:
 *   GREEN = Live Data
 *   AMBER = AI Template (validate before publication)
 *   RED   = Synthetic Data (MUST replace before publication)
 */

import { DATA_SOURCE_CONFIG, type DataSourceLevel } from '@/lib/styles';

export type { DataSourceLevel };
import type { CSSProperties } from 'react';

interface DataSourceBadgeProps {
  level:     DataSourceLevel;
  compact?:  boolean;    // pill only, no description
  style?:    CSSProperties;
}

export default function DataSourceBadge({ level, compact, style }: DataSourceBadgeProps) {
  const cfg = DATA_SOURCE_CONFIG[level];

  if (compact) {
    return (
      <span style={{
        background:   cfg.bg,
        color:        cfg.text,
        fontFamily:   'var(--font-ui)',
        fontSize:     11,
        fontWeight:   700,
        padding:      '2px 8px',
        borderRadius: 9999,
        letterSpacing:'0.04em',
        ...style,
      }}>
        {cfg.label}
      </span>
    );
  }

  return (
    <div style={{
      background:   cfg.bg,
      color:        cfg.text,
      fontFamily:   'var(--font-ui)',
      fontSize:     13,
      fontWeight:   500,
      padding:      '8px 14px',
      borderRadius: 8,
      display:      'flex',
      alignItems:   'center',
      gap:          10,
      ...style,
    }}>
      <span style={{ fontWeight: 700, letterSpacing: '0.05em' }}>{cfg.label}</span>
      <span style={{ opacity: 0.9 }}>{cfg.description}</span>
    </div>
  );
}
