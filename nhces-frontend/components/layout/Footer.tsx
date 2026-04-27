import { COLOURS } from '@/lib/styles';

export default function Footer() {
  return (
    <footer style={{
      background:  COLOURS.surface,
      borderTop:   `1px solid ${COLOURS.border}`,
      padding:     '24px',
      textAlign:   'center',
    }}>
      <p style={{
        fontFamily: 'var(--font-ui)',
        fontSize:   13,
        color:      COLOURS.textDim,
        margin:     0,
        lineHeight: 1.6,
      }}>
        iNHCES — Intelligent National Housing Cost Estimating System
        {' · '}
        TETFund National Research Fund 2025
        {' · '}
        Department of Quantity Surveying, ABU Zaria
        <br />
        AI-assisted research tool. All estimates are indicative only.
        Verify independently before use in procurement or publications.
      </p>
    </footer>
  );
}
