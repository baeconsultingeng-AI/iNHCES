# iNHCES Frontend

**Intelligent National Housing Cost Estimating System — Next.js Frontend**  
TETFund NRF 2025 | Department of Quantity Surveying, ABU Zaria

---

## Overview

The iNHCES frontend is a Next.js 14 (App Router) application that provides a professional interface for Nigerian housing construction cost estimation. It connects to the FastAPI backend for ML predictions and displays results with SHAP explainability charts, temporal cost projections, and macroeconomic data dashboards.

**Design system**: Warm Ivory palette — Playfair Display (headings) + Lora (body) + DM Sans (UI).

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | Next.js 14.2 (App Router, TypeScript) |
| Auth | Supabase Auth (`@supabase/ssr`) |
| Styling | Tailwind CSS (Warm Ivory design system) |
| Charts | SVG (inline — no chart library dependency) |
| Deployment | Vercel |

---

## Project Structure

```
nhces-frontend/
├── app/
│   ├── layout.tsx          # Root layout (Google Fonts, Navbar, Footer)
│   ├── page.tsx            # Landing page (hero, stats, steps, CTA)
│   ├── estimate/
│   │   └── page.tsx        # Cost estimate form + results + SHAP + projections
│   ├── dashboard/
│   │   └── page.tsx        # Macro snapshot, model status, pipeline health
│   ├── projects/
│   │   └── page.tsx        # Project list (CRUD)
│   ├── reports/
│   │   └── page.tsx        # Generated PDF report list + download
│   ├── macro/
│   │   └── page.tsx        # Macroeconomic data explorer + chart
│   ├── login/
│   │   └── page.tsx        # Supabase Auth login form
│   └── register/
│       └── page.tsx        # Supabase Auth registration form
├── components/
│   ├── layout/
│   │   ├── Navbar.tsx      # Responsive nav with auth state
│   │   └── Footer.tsx      # Footer with research attribution
│   ├── ui/
│   │   ├── Button.tsx      # Warm Ivory button variants
│   │   ├── Card.tsx        # Card container
│   │   ├── Input.tsx       # Labelled input with error state
│   │   ├── Badge.tsx       # Status badge
│   │   ├── DataSourceBadge.tsx  # GREEN / AMBER / RED data quality badge
│   │   └── LoadingSpinner.tsx
│   ├── estimate/
│   │   ├── EstimateResult.tsx   # Cost breakdown summary card
│   │   ├── ShapChart.tsx        # SHAP horizontal bar chart (SVG)
│   │   └── TemporalChart.tsx    # 4-horizon projection chart (SVG + widening CI)
│   └── dashboard/
│       ├── MacroSnapshot.tsx    # 7-variable macro data cards
│       ├── ModelStatus.tsx      # Champion model version + MAPE
│       ├── PipelineHealth.tsx   # Airflow DAG status badges
│       └── RecentPredictions.tsx
├── lib/
│   ├── api.ts              # Typed fetch client for the FastAPI backend
│   ├── auth.ts             # Supabase auth helpers
│   ├── styles.ts           # Design system constants (Warm Ivory palette)
│   └── formatters.ts       # NGN currency, number, date formatters
├── .env.local.example      # Environment variable template
├── next.config.js
├── package.json
├── tsconfig.json
└── vercel.json             # Vercel deployment config with API proxy
```

---

## Quick Start

### Prerequisites

- Node.js 18.17+
- npm 9+ or pnpm 8+
- A running iNHCES backend (see [nhces-backend/README.md](../nhces-backend/README.md))
- A Supabase project (same one used by the backend)

### 1. Install dependencies

```bash
cd nhces-frontend
npm install
```

### 2. Configure environment variables

```bash
cp .env.local.example .env.local
# Edit .env.local and fill in your values
```

Required variables:

| Variable | Description |
|----------|-------------|
| `NEXT_PUBLIC_SUPABASE_URL` | Your Supabase project URL |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase anon (public) key |
| `NEXT_PUBLIC_API_URL` | FastAPI backend URL (default: `http://localhost:8000`) |

### 3. Run the development server

```bash
npm run dev
# Open http://localhost:3000
```

### 4. Build for production

```bash
npm run build
npm run start
```

---

## Pages

| Route | Description | Auth Required |
|-------|-------------|--------------|
| `/` | Landing page — hero, feature overview, data quality guide | No |
| `/estimate` | Cost estimation form + ML results + SHAP + projections | No |
| `/dashboard` | Macro data snapshot, model status, pipeline health | No |
| `/macro` | Macroeconomic data explorer with historical chart | No |
| `/projects` | Project management (CRUD) | Yes |
| `/reports` | Generated PDF reports with download links | No (empty if unauthed) |
| `/login` | Supabase Auth login | No |
| `/register` | Supabase Auth registration | No |

---

## Data Flow

```
User fills /estimate form
  → POST /estimate (FastAPI backend)
    → LightGBM champion model
    → SHAP TreeExplainer
    → Temporal projection engine (25% p.a. inflation)
  ← EstimateResponse (cost_per_sqm, projections[4], shap_top_features)
  → EstimateResult card + ShapChart + TemporalChart rendered
```

---

## API Client (`lib/api.ts`)

All backend calls are made through the typed client. Example:

```typescript
import { postEstimate, getMacroSnapshot } from '@/lib/api';

// Cost estimate
const result = await postEstimate({
  building_type:     'Residential',
  construction_type: 'New Build',
  floor_area_sqm:    120,
  num_floors:        1,
  location_state:    'Kaduna',
  location_zone:     'North West',
});

// Macro snapshot
const macro = await getMacroSnapshot();
```

In production, API calls are proxied through Vercel rewrites (`/api/*` → Railway backend) to avoid CORS issues.

---

## Auth

Authentication uses Supabase GoTrue (email + password). The JWT token is stored in the Supabase session and forwarded as a `Bearer` header on all authenticated requests via `lib/auth.ts`.

User roles (set in `app_metadata` by an admin):
- `qsprofessional` — default for registered users
- `researcher` — access to `/pipeline` and research-level data
- `admin` — full access

---

## Design System

Warm Ivory palette defined in `lib/styles.ts`:

| Token | Value | Usage |
|-------|-------|-------|
| `ivory` | `#FAF8F3` | Page background |
| `charcoal` | `#2C2C2C` | Body text |
| `navy` | `#0F2850` | Headings, accents |
| `gold` | `#B48C1E` | Borders, highlights |
| `sage` | `#5A7A5E` | GREEN data badge |
| `amber` | `#B87A00` | AMBER data badge |
| `rust` | `#A03020` | RED data badge |

Typography: **Playfair Display** (headings) · **Lora** (body) · **DM Sans** (UI elements)

---

## Deployment (Vercel)

The `vercel.json` configures:
1. `npm run build` as the build command
2. API rewrites: `/api/*` → `https://nhces-api.up.railway.app/*`

```bash
# Deploy via Vercel CLI
npx vercel --prod

# Or push to GitHub — Vercel auto-deploys from main branch
```

Set these environment variables in the Vercel dashboard:
- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- `NEXT_PUBLIC_API_URL` → `https://nhces-api.up.railway.app`

---

## Research Context

This frontend is part of the iNHCES research system developed under TETFund NRF 2025 Grant, Department of Quantity Surveying, Ahmadu Bello University (ABU) Zaria.

**Principal Investigator**: Department of Quantity Surveying, ABU Zaria  
**Grant**: TETFund National Research Fund (NRF) 2025
