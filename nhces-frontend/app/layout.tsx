import type { Metadata } from 'next';
import { Playfair_Display, Lora, DM_Sans } from 'next/font/google';
import { ANIMATION_CSS, COLOURS } from '@/lib/styles';
import Navbar from '@/components/layout/Navbar';
import Footer from '@/components/layout/Footer';

// ── Google Fonts ───────────────────────────────────────────────────────────────
const playfair = Playfair_Display({
  subsets:  ['latin'],
  weight:   ['700', '900'],
  variable: '--font-display',
  display:  'swap',
});

const lora = Lora({
  subsets:  ['latin'],
  weight:   ['400', '500', '600', '700'],
  variable: '--font-body',
  display:  'swap',
});

const dmSans = DM_Sans({
  subsets:  ['latin'],
  weight:   ['400', '500', '600'],
  variable: '--font-ui',
  display:  'swap',
});

// ── Metadata ───────────────────────────────────────────────────────────────────
export const metadata: Metadata = {
  title:       'iNHCES — Intelligent National Housing Cost Estimating System',
  description: 'AI-powered housing construction cost estimation for Nigeria. ' +
               'TETFund NRF 2025 | Department of Quantity Surveying, ABU Zaria.',
  keywords:    ['housing cost', 'Nigeria', 'construction', 'AI', 'quantity surveying', 'iNHCES'],
};

// ── Root Layout ────────────────────────────────────────────────────────────────
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html
      lang="en"
      className={`${playfair.variable} ${lora.variable} ${dmSans.variable}`}
    >
      <head>
        <style dangerouslySetInnerHTML={{ __html: ANIMATION_CSS }} />
      </head>
      <body
        style={{
          margin:      0,
          padding:     0,
          background:  COLOURS.background,
          color:       COLOURS.textPrimary,
          fontFamily:  'var(--font-body)',
          fontSize:    17,
          lineHeight:  1.65,
        }}
      >
        <Navbar />
        <main style={{ minHeight: 'calc(100vh - 120px)' }}>
          {children}
        </main>
        <Footer />
      </body>
    </html>
  );
}
