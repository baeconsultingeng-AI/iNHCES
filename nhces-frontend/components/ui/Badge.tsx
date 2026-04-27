import { GS, COLOURS } from '@/lib/styles';
import type { CSSProperties } from 'react';

type BadgeVariant = 'default' | 'success' | 'warning' | 'danger' | 'accent';

const VARIANT_STYLES: Record<BadgeVariant, CSSProperties> = {
  default: { background: COLOURS.surfaceAlt,  color: COLOURS.textMuted },
  success: { background: COLOURS.greenLight,  color: COLOURS.green },
  warning: { background: COLOURS.amberLight,  color: COLOURS.amber },
  danger:  { background: COLOURS.redLight,    color: COLOURS.red },
  accent:  { background: COLOURS.accentBg,    color: COLOURS.accent },
};

interface BadgeProps {
  children: React.ReactNode;
  variant?: BadgeVariant;
  style?:   CSSProperties;
}

export default function Badge({ children, variant = 'default', style }: BadgeProps) {
  return (
    <span style={{ ...GS.tag, ...VARIANT_STYLES[variant], ...style }}>
      {children}
    </span>
  );
}
