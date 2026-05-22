<div align="center">

# Foliowise

### Intelligent Portfolio Tracking with AI-Powered Insights

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![Angular](https://img.shields.io/badge/angular-21-red.svg)](https://angular.io)
[![FastAPI](https://img.shields.io/badge/fastapi-0.100+-green.svg)](https://fastapi.tiangolo.com)

[Features](#features) • [Demo](#demo) • [Tech Stack](#tech-stack) • [Installation](#installation) • [API Reference](#api-reference) • [Documentation](#documentation)

</div>

---

## Personal Contribution 

Foliowise was built using AI-assisted development (Claude). I designed the
product, defined the architecture, and directed implementation through detailed
prompting and iteration. All feature decisions, debugging, deployment, and
integration work were hands-on. The codebase reflects my understanding of
full-stack development with FastAPI, Angular, and PostgreSQL.

---

## Overview

Foliowise is a comprehensive investment portfolio tracker that combines real-time market data, AI-powered insights, sentiment analysis, and gamified virtual trading competitions. Built for modern investors who want more than just tracking—they want intelligence.

<div align="center">

**Track. Analyze. Compete. Grow.**

</div>

---

## Features

### Core Portfolio Management
- **Real-Time Tracking** — Live stock prices from Yahoo Finance with automatic updates
- **Holdings Management** — Add, edit, delete holdings with transaction history
- **Performance Analytics** — Track total value, P/L, daily changes, and historical performance
- **Allocation Visualization** — Interactive pie charts showing portfolio distribution
- **CSV Import/Export** — Bulk import holdings, export data for tax reporting

### AI & Analytics
- **AI-Powered Insights** — Claude-powered portfolio analysis and recommendations
- **Price Predictions** — Ensemble ML models (Linear Regression, EMA, Mean Reversion) with confidence bands
- **Sentiment Analysis** — NLP-based news sentiment for individual stocks and portfolio-wide
- **Weekly Digest** — AI-generated portfolio health reports with actionable recommendations

### Trading Arena 🏆
- **Virtual Competitions** — Compete with $100K paper money portfolios
- **Weekly Challenges** — Auto-generated weekly trading competitions
- **Real-Time Leaderboards** — Track your ranking against other traders
- **Achievement System** — 12 unlockable badges (First Trade, Champion, Hot Streak, etc.)
- **Win Rate Tracking** — Monitor your trading performance over time

### Alerts & Notifications
- **Price Alerts** — Set ABOVE/BELOW price targets with instant notifications
- **Email Notifications** — Get alerted when price targets are hit (via Resend)
- **Triggered Alert History** — Review past alerts and market movements

### Additional Features
- **Stock Lookup** — Search and view any stock without adding to holdings
- **Stock Comparison** — Compare 2-5 stocks side-by-side with charts
- **Watchlist** — Track stocks you're interested in
- **Dividend Tracking** — Log dividend payments with summary analytics
- **Portfolio Goals** — Set and track investment milestones
- **Transaction History** — Full buy/sell history with realized gains calculation

### Monetization
- **Subscription Tiers** — Free, Pro ($9.99/mo), Pro+ ($19.99/mo)
- **Stripe Integration** — Secure payment processing with customer portal
- **Referral Program** — Earn rewards for inviting friends
- **Usage Limits** — Tiered access to features based on subscription

---

## Demo

### Dashboard
Real-time portfolio overview with performance charts, allocation breakdown, and key metrics.

### Trading Arena
Virtual trading competitions with leaderboards, achievements, and paper trading.

### AI Insights
Get intelligent recommendations and chat with AI about your portfolio.

---

## Tech Stack

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.11+ | Runtime |
| FastAPI | 0.100+ | Web framework |
| PostgreSQL | 15+ | Database |
| SQLAlchemy | 2.0+ | ORM |
| Pydantic | 2.0+ | Validation |
| yfinance | 0.2+ | Market data |
| TextBlob | 0.17+ | Sentiment analysis |
| Stripe | 7.0+ | Payments |
| Resend | 0.6+ | Email delivery |

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| Angular | 21 | SPA framework |
| TypeScript | 5.9 | Language |
| Tailwind CSS | 3.4 | Styling |
| Chart.js | 4.5 | Data visualization |
| RxJS | 7.8 | Reactive programming |

### Infrastructure
- **Hosting:** Render
- **Database:** PostgreSQL (Render managed)
- **CDN:** Render static hosting

---

## Installation

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- npm 10+

### Backend Setup

```bash
# Clone repository
git clone https://github.com/singhsimar486/Foliowise.git
cd Foliowise/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cat > .env << EOF
DATABASE_URL=postgresql://username@localhost:5432/foliowise
SECRET_KEY=$(openssl rand -hex 32)
DEBUG=True

# Optional: Stripe (for subscriptions)
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_PRO_PRICE_ID=price_...
STRIPE_PRO_PLUS_PRICE_ID=price_...

# Optional: Resend (for email alerts)
RESEND_API_KEY=re_...

FRONTEND_URL=http://localhost:4200
EOF

# Create database
createdb foliowise

# Run server
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Configure environment
echo 'export const environment = { apiUrl: "http://localhost:8000" };' > src/environments/environment.ts

# Run development server
npm start
```

### Access
- **API Docs:** http://localhost:8000/docs
- **Frontend:** http://localhost:4200

---

## API Reference

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Create account |
| POST | `/auth/login` | Get JWT token |
| GET | `/auth/me` | Current user |

### Holdings
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/holdings/` | List holdings |
| POST | `/holdings/` | Create holding |
| PUT | `/holdings/{id}` | Update holding |
| DELETE | `/holdings/{id}` | Delete holding |
| POST | `/holdings/import` | Import CSV |

### Portfolio
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/portfolio/summary` | Portfolio with live data |
| GET | `/portfolio/allocation` | Allocation breakdown |
| GET | `/portfolio/gains` | Realized/unrealized gains |
| GET | `/portfolio/performance` | Historical performance |

### Market Data
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/market/quote/{ticker}` | Real-time quote |
| GET | `/market/history/{ticker}` | Historical OHLCV |
| GET | `/market/search` | Search stocks |
| GET | `/market/predict/{ticker}` | Price prediction |

### Competitions
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/competitions/` | List competitions |
| POST | `/competitions/{id}/join` | Join competition |
| POST | `/competitions/{id}/trade` | Make virtual trade |
| GET | `/competitions/{id}/leaderboard` | Get leaderboard |
| GET | `/competitions/achievements/me` | User achievements |

### Additional Endpoints
- **Alerts:** `/alerts/` — Price alert management
- **Watchlist:** `/watchlist/` — Stock watchlist
- **Insights:** `/insights/` — AI analysis and chat
- **Dividends:** `/dividends/` — Dividend tracking
- **Goals:** `/goals/` — Portfolio goals
- **Transactions:** `/transactions/` — Transaction history
- **Subscriptions:** `/subscriptions/` — Stripe integration
- **Settings:** `/settings/` — Account management

**Full API documentation:** See [TECHNICAL_DOCUMENTATION.md](./TECHNICAL_DOCUMENTATION.md)

---

## Documentation

| Document | Description |
|----------|-------------|
| [TECHNICAL_DOCUMENTATION.md](./TECHNICAL_DOCUMENTATION.md) | Complete technical reference (80+ pages) |
| [TECHNICAL_DOCUMENTATION_PART2.md](./TECHNICAL_DOCUMENTATION_PART2.md) | API examples & troubleshooting |
| [README_DOCUMENTATION.md](./README_DOCUMENTATION.md) | Documentation index |

### Generate PDF
```bash
chmod +x convert_to_pdf.sh
./convert_to_pdf.sh
```

---

## Project Structure

```
foliowise/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── config.py            # Environment settings
│   │   ├── database.py          # SQLAlchemy setup
│   │   ├── models/              # ORM models (9 files)
│   │   ├── routers/             # API routes (14 files)
│   │   └── services/            # Business logic (8 files)
│   └── requirements.txt
│
├── frontend/
│   ├── src/app/
│   │   ├── components/          # Angular components (22)
│   │   ├── services/            # API & auth services
│   │   └── guards/              # Route guards
│   ├── tailwind.config.js
│   └── package.json
│
├── TECHNICAL_DOCUMENTATION.md
└── README.md
```

---

## Subscription Tiers

| Feature | Free | Pro | Pro+ |
|---------|------|-----|------|
| Holdings | 10 | 100 | Unlimited |
| Price Alerts | 1 | 25 | Unlimited |
| Stock Lookups/day | 5 | 50 | Unlimited |
| AI Questions/day | 3 | 50 | Unlimited |
| Competitions | 1 | Unlimited | Unlimited |
| Email Alerts | No | Yes | Yes |
| Priority Support | No | No | Yes |
| **Price** | $0 | $9.99/mo | $19.99/mo |

---

## Roadmap

- [x] Portfolio tracking with real-time data
- [x] AI-powered insights and chat
- [x] Price predictions with ML
- [x] News sentiment analysis
- [x] Trading Arena competitions
- [x] Achievement system
- [x] Subscription tiers with Stripe
- [x] Email notifications
- [x] Comprehensive documentation
- [ ] Mobile app (React Native)
- [ ] Social features (follow traders)
- [ ] Options tracking
- [ ] Cryptocurrency support
- [ ] Tax report generation

---

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Author

**Simar Singh**

- GitHub: [@singhsimar486](https://github.com/singhsimar486)

---

<div align="center">

**Built with passion for investors who want more.**

[Report Bug](https://github.com/singhsimar486/Foliowise/issues) • [Request Feature](https://github.com/singhsimar486/Foliowise/issues)

</div>
