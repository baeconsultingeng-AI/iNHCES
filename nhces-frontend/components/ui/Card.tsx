import { GS } from '@/lib/styles';
import type { CSSProperties, ReactNode } from 'react';

interface CardProps {
  children:  ReactNode;
  compact?:  boolean;
  hover?:    boolean;
  style?:    CSSProperties;
  className?: string;
}

export default function Card({ children, compact, hover, style, className }: CardProps) {
  return (
    <div
      className={`${hover ? 'hover-lift' : ''} ${className ?? ''}`}
      style={{ ...(compact ? GS.cardCompact : GS.card), ...style }}
    >
      {children}
    </div>
  );
}
