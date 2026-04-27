'use client';
import { GS } from '@/lib/styles';
import type { InputHTMLAttributes, TextareaHTMLAttributes } from 'react';

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?:   string;
  error?:   string;
}

interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?:    string;
  error?:    string;
  options:   { value: string; label: string }[];
}

interface TextareaProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  error?: string;
}

function FieldWrapper({ label, error, children }: {
  label?: string; error?: string; children: React.ReactNode;
}) {
  return (
    <div style={{ marginBottom: 16 }}>
      {label && <label style={GS.label}>{label}</label>}
      {children}
      {error && (
        <p style={{ ...GS.metaText, color: '#c0392b', marginTop: 4 }}>{error}</p>
      )}
    </div>
  );
}

export function Input({ label, error, style, ...props }: InputProps) {
  return (
    <FieldWrapper label={label} error={error}>
      <input style={{ ...GS.input, ...(error ? { borderColor: '#c0392b' } : {}), ...style }} {...props} />
    </FieldWrapper>
  );
}

export function Select({ label, error, options, style, ...props }: SelectProps) {
  return (
    <FieldWrapper label={label} error={error}>
      <select style={{ ...GS.select, ...(error ? { borderColor: '#c0392b' } : {}), ...style }} {...props}>
        {options.map(o => (
          <option key={o.value} value={o.value}>{o.label}</option>
        ))}
      </select>
    </FieldWrapper>
  );
}

export function Textarea({ label, error, style, ...props }: TextareaProps) {
  return (
    <FieldWrapper label={label} error={error}>
      <textarea style={{ ...GS.textarea, ...(error ? { borderColor: '#c0392b' } : {}), ...style }} {...props} />
    </FieldWrapper>
  );
}
