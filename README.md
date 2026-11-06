# FXPilot AI — Cross-Border Currency Conversion Intelligence Platform

**FXPilot AI** is an institutional-grade fintech dashboard and intelligence copilot engineered for cross-border merchants, international SaaS businesses, and exporters. It delivers real-time visibility into interbank zero-margin exchange rates, audits payment provider conversion quotes (e.g., PayPal), detects embedded retail spread markups, and provides actionable tactical execution recommendations.

---

## 🌟 Key Capabilities & Features

### 1. Overview Dashboard (`/`)
- **Executive KPIs**: Real-time tracking of *Total Transaction Volume* ($128,450), *Average FX Markup* (1.42%), *Potential Savings* (₹24,850), and *Transactions Audited* (248).
- **Interactive Exchange Rate Trajectory**: High-fidelity Recharts area chart tracking historical USD/INR (and other pairs) across `1D`, `1W`, `1M`, `3M`, and `1Y` timeframes with live tooltips.
- **Real-Time Spread Comparison**: Side-by-side audit of Mid-Market Interbank reference rates versus PayPal simulated settlement quotes with absolute cost calculation.
- **Recent International Transactions**: Ledger with status indicators (*Optimized*, *Standard*, *High Markup*, *Pending Review*). Clicking any row opens an audit drawer.
- **AI Tactical Signal Panel**: Instant cross-border advice on timing, weekend spread widening risks, and corridor routing.

### 2. FX Converter & Spread Auditor (`/converter`)
- **Live Currency Conversion**: Convert between `USD`, `INR`, `EUR`, `GBP`, `JPY`, `AUD`, `CAD`, and `SGD`.
- **Bidirectional Currency Swapper**: Instant toggle between base and counter currencies.
- **Batch Presets**: Quick-select presets ($1,000, $5,000, $10,000, $25,000, $50,000).
- **Waterfall Spread Breakdown**: Deconstructs gross fair value, provider discount deduction, and net credited settlement.
- **Competitive Provider Benchmark Matrix**: Compares PayPal quotes directly against Mid-Market baseline, Wise multi-currency, and traditional wire transfers.

### 3. FX Analytics & Fee Decomposition (`/analytics`)
- **Historical Spread Corridor Chart**: Visualizes the markup gap between interbank zero-margin rates and provider quotes over time.
- **Monthly FX Markup Trend**: 6-month historical tracking of standard retail markups versus FXPilot-optimized batch conversions.
- **Cross-Border Fee Anatomy**: Dissects conversion margin (3.25%), international jurisdiction surcharge (1.50%), and network interchange (0.30%).
- **Interactive Annual Savings Calculator**: Dynamic volume slider estimating annual retained capital across volumes from $25,000 to $2,000,000+.

### 4. AI Intelligence Agent (`/agent`)
- **Simulated Financial Copilot**: Conversational AI assistant analyzing cross-border transaction scenarios.
- **Suggested Tactical Prompts**:
  1. *"Analyse my $5,000 USD to INR conversion."*
  2. *"Compare the current reference and provider rates."*
  3. *"Explain how much markup I am paying."*
  4. *"Should I convert now or wait?"*
- **Live Tactical Analysis Panel**: Dynamic card displaying active corridor reference rate, quoted rate, markup %, and AI strategic signals (*HOLD / WAIT*, *CONVERT NOW*, *OPTIMIZE ROUTE*).

### 5. Transactions Audit Ledger (`/transactions`)
- **Comprehensive Ledger**: Search by transaction ID, merchant name, or reference code.
- **Multi-Factor Filtering**: Filter by currency pair and audit status.
- **Export to CSV**: Client-side ledger export for accounting and audits.
- **Full Audit Drawer**: In-depth inspection drawer showing exchange rates, spread differences, metadata, and raw JSON payload.

### 6. Settings & Integration Hub (`/settings`)
- **Persistent Theme Switcher**: Toggle between Dark Mode (Default) and Light Mode.
- **Alert Thresholds**: Customizable slider for spread markup notifications.
- **FastAPI Integration Center**: Pre-wired endpoint configuration (`/quotes/calculate`, `/rates/history`, `/transactions`, `/agent/chat`).

---

## 🎨 Design System & Theme Engine

The application implements a custom dual-theme design system adhering to strict fintech aesthetics:

| Token | Dark Theme (Default) | Light Theme |
| :--- | :--- | :--- |
| **Main Background** | `#050707` | `#F5F8F7` |
| **Sidebar Surface** | `#090D0D` | `#FFFFFF` |
| **Card Surface** | `#101717` | `#FFFFFF` |
| **Elevated Surface** | `#151F1E` | `#EDF3F1` |
| **Primary Teal** | `#19C3B1` | `#119E91` |
| **Soft Teal** | `#83DED2` | `#DDF5F0` |
| **Positive Green** | `#36C98F` | `#168B61` |
| **Negative Red** | `#F16B70` | `#D94D57` |
| **Main Text** | `#F2F5F4` | `#172321` |
| **Secondary Text** | `#899795` | `#71817D` |
| **Borders** | `#202C2A` | `#E2EAE7` |

Themes are persisted in `localStorage` under `fxpilot_theme` and apply uniformly to typography, charts, modals, sidebars, and forms without flickering.

---

## 🚀 Quickstart & Installation (Windows PowerShell)

Follow these exact steps to run the application locally on Windows:

### Step 1: Open Windows PowerShell
Navigate to the extracted project directory:
```powershell
cd c:\Users\tiyas\Downloads\paypalapp
```

### Step 2: Install Dependencies
```powershell
npm.cmd install
```
*(Or `npm install` if PowerShell execution policy is configured)*

### Step 3: Run the Development Server
```powershell
npm.cmd run dev
```

### Step 4: Open in Your Browser
Once started, open your browser and navigate to:
```
http://localhost:5173
```

### Step 5: Build for Production
To build the optimized static production bundle:
```powershell
npm.cmd run build
```

---

## 📂 Project Architecture

```
paypalapp/
├── index.html                   # HTML entry point with theme flash prevention
├── package.json                 # Dependencies and build scripts
├── postcss.config.js            # PostCSS configuration
├── tailwind.config.js           # Custom fintech color palette & shadows
├── tsconfig.json                # TypeScript compiler configuration
├── vite.config.ts               # Vite bundler configuration with @ alias
└── src/
    ├── App.tsx                  # Top-level routes and context providers
    ├── main.tsx                 # React DOM mount point
    ├── index.css                # Tailwind base and CSS variables for themes
    ├── types/
    │   └── index.ts             # Strict TypeScript models & interfaces
    ├── data/
    │   └── mockData.ts          # Realistic rates, corridors, 30+ transactions & AI logic
    ├── services/
    │   └── fxService.ts         # Unified service layer with FastAPI hooks
    ├── utils/
    │   └── formatters.ts        # Currency, date, percentage & CSV download helpers
    ├── context/
    │   ├── ThemeContext.tsx     # Reusable theme context with localStorage sync
    │   └── ToastContext.tsx     # Toast notification dispatcher
    ├── components/
    │   ├── common/
    │   │   ├── CurrencySelector.tsx
    │   │   ├── DemoBanner.tsx
    │   │   ├── SearchModal.tsx
    │   │   ├── StatusBadge.tsx
    │   │   └── ThemeToggle.tsx
    │   ├── layout/
    │   │   ├── DashboardLayout.tsx
    │   │   ├── Sidebar.tsx
    │   │   └── Topbar.tsx
    │   ├── dashboard/
    │   │   ├── AIInsight.tsx
    │   │   ├── ExchangeRateChart.tsx
    │   │   ├── FXComparison.tsx
    │   │   ├── RecentTransactions.tsx
    │   │   └── StatCard.tsx
    │   └── transactions/
    │       └── TransactionDetailDrawer.tsx
    └── pages/
        ├── Overview.tsx         # Executive dashboard
        ├── Converter.tsx        # FX converter & benchmark matrix
        ├── Analytics.tsx        # Historical volatility & fee breakdown
        ├── Agent.tsx            # Conversational intelligence copilot
        ├── Transactions.tsx     # Filterable transaction ledger
        └── Settings.tsx         # Appearance, preferences & backend setup
```

---

## 🔌 Connecting to Python FastAPI Backend

When ready to connect to your live Python FastAPI backend:
1. Create a `.env` file from `.env.example`:
   ```bash
   VITE_FASTAPI_BASE_URL=http://localhost:8000/api/v1
   ```
2. In `src/services/fxService.ts`, set `API_CONFIG.useMock = false`.
3. The frontend expects the following endpoints:
   - `POST /api/v1/quotes/calculate`: Body `{ from_currency, to_currency, amount }`
   - `GET /api/v1/rates/history?pair=USD/INR&period=1M`
   - `GET /api/v1/transactions`
   - `POST /api/v1/agent/chat`: Body `{ query }`

---

## ⚖️ Disclaimer
All exchange rates, PayPal conversion quotes, and AI agent insights rendered in this demo version are generated from realistic simulation models for hackathon presentation and testing purposes.
