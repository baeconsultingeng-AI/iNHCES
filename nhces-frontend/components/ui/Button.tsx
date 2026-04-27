'use client';
import { GS } from '@/lib/styles';
import type { CSSProperties, ButtonHTMLAttributes, ReactNode } from 'react';

type Variant = 'primary' | 'ghost' | 'danger';
type Size    = 'sm' | 'md' | 'lg';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?:  Variant;
  size?:     Size;
  loading?:  boolean;
  children:  ReactNode;
  style?:    CSSProperties;
}

const VARIANT_STYLES: Record<Variant, CSSProperties> = {
  primary: GS.btn,
  ghost:   GS.btnGhost,
  danger:  GS.btnDanger,
};

const SIZE_EXTRA: Record<Size, CSSProperties> = {
  sm: { padding: '7px 14px', fontSize: 13 },
  md: {},
  lg: { padding: '13px 28px', fontSize: 16 },
};

export default function Button({
  variant  = 'primary',
  size     = 'md',
  loading  = false,
  children,
  style,
  disabled,
  ...props
}: ButtonProps) {
  return (
    <button
      className="btn-hover"
      disabled={disabled || loading}
      style={{
        ...VARIANT_STYLES[variant],
        ...SIZE_EXTRA[size],
        opacity: (disabled || loading) ? 0.6 : 1,
        cursor:  (disabled || loading) ? 'not-allowed' : 'pointer',
        ...style,
      }}
      {...props}
    >
      {loading ? (
        <>
          <span style={{
            display: 'inline-block', width: 14, height: 14,
            border: '2px solid currentColor', borderTopColor: 'transparent',
            borderRadius: '50%', animation: 'spin 0.7s linear infinite',
          }} />
          {children}
        </>
      ) : children}
    </button>
  );
}
