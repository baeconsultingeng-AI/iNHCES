import { COLOURS } from '@/lib/styles';
import type { CSSProperties } from 'react';

interface LoadingSpinnerProps {
  size?:  number;
  color?: string;
  style?: CSSProperties;
  label?: string;
}

export default function LoadingSpinner({
  size  = 32,
  color = COLOURS.accent,
  style,
  label = 'Loading...',
}: LoadingSpinnerProps) {
  return (
    <div style={{
      display:       'flex',
      flexDirection: 'column',
      alignItems:    'center',
      gap:           12,
      padding:       32,
      ...style,
    }}>
      <div style={{
        width:       size,
        height:      size,
        border:      `3px solid ${COLOURS.border}`,
        borderTop:   `3px solid ${color}`,
        borderRadius:'50%',
        animation:   'spin 0.7s linear infinite',
      }} />
      {label && (
        <p style={{
          fontFamily: 'var(--font-ui)',
          fontSize:   14,
          color:      COLOURS.textDim,
          margin:     0,
        }}>
          {label}
        </p>
      )}
      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
    </div>
  );
}
