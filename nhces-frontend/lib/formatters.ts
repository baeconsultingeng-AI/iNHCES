/**
 * iNHCES Formatting Utilities
 * Always use these — never format manually in components.
 */

/** Format a Naira amount with K / M / B suffix. */
export function formatNGN(value: number): string {
  if (value >= 1_000_000_000) return `NGN ${(value / 1_000_000_000).toFixed(2)}B`;
  if (value >= 1_000_000)     return `NGN ${(value / 1_000_000).toFixed(2)}M`;
  if (value >= 1_000)         return `NGN ${(value / 1_000).toFixed(0)}K`;
  return `NGN ${value.toLocaleString('en-NG', { maximumFractionDigits: 0 })}`;
}

/** Format NGN per sqm with comma-separated thousands. */
export function formatNGNPerSqm(value: number): string {
  return `NGN ${value.toLocaleString('en-NG', { maximumFractionDigits: 0 })} / sqm`;
}

/** Format a MAPE percentage. */
export function formatMAPE(value: number): string {
  return `${value.toFixed(2)}%`;
}

/** Format an ISO date string to "26 Apr 2026". */
export function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString('en-GB', {
    day: 'numeric', month: 'short', year: 'numeric',
  });
}

/** Format an ISO datetime to "26 Apr 2026, 10:00 WAT". */
export function formatDateTime(iso: string): string {
  return new Date(iso).toLocaleString('en-GB', {
    day: 'numeric', month: 'short', year: 'numeric',
    hour: '2-digit', minute: '2-digit',
  });
}

/** Format a floor area. */
export function formatSqm(value: number): string {
  return `${value.toLocaleString('en-NG')} sqm`;
}

/** Truncate a string to maxLen with ellipsis. */
export function truncate(str: string, maxLen: number): string {
  return str.length <= maxLen ? str : `${str.slice(0, maxLen)}...`;
}
