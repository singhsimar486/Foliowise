# Foliowise Technical Documentation

**Version:** 1.0.0
**Date:** April 2026
**Classification:** Internal Engineering Documentation
**Author:** Foliowise Engineering Team

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [System Architecture](#2-system-architecture)
3. [Technology Stack](#3-technology-stack)
4. [Backend Implementation](#4-backend-implementation)
5. [Frontend Implementation](#5-frontend-implementation)
6. [Database Schema](#6-database-schema)
7. [API Reference](#7-api-reference)
8. [Authentication & Security](#8-authentication--security)
9. [Third-Party Integrations](#9-third-party-integrations)
10. [Feature Documentation](#10-feature-documentation)
11. [Performance & Optimization](#11-performance--optimization)
12. [Deployment Guide](#12-deployment-guide)
13. [Appendices](#13-appendices)

---

## 1. Executive Summary

### 1.1 Product Overview

Foliowise is an intelligent portfolio tracking platform that combines real-time market data, AI-powered insights, and gamified virtual trading competitions. The platform enables investors to track their holdings, analyze market sentiment, receive price alerts, and compete in paper trading competitions.

### 1.2 Key Capabilities

| Capability | Description |
|------------|-------------|
| Portfolio Tracking | Real-time tracking of stock holdings with live market data |
| AI Insights | Claude-powered portfolio analysis and recommendations |
| Price Predictions | Ensemble machine learning models for price forecasting |
| Sentiment Analysis | NLP-based news sentiment for holdings |
| Trading Arena | Virtual $100K competitions with leaderboards |
| Price Alerts | Customizable alerts with email notifications |
| Subscription Tiers | Freemium model with Stripe integration |

### 1.3 Architecture Highlights

- **Monolithic Backend**: FastAPI application with modular router structure
- **Single Page Application**: Angular 21 with standalone components
- **Real-time Data**: Yahoo Finance integration via yfinance
- **AI/ML Pipeline**: TextBlob sentiment + ensemble prediction models
- **Payment Processing**: Stripe Checkout + Customer Portal
- **Email Delivery**: Resend API for transactional emails

---

## 2. System Architecture

### 2.1 High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CLIENT LAYER                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                    Angular 21 SPA (TypeScript)                       │    │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │    │
│  │  │Dashboard │ │ Holdings │ │  Arena   │ │ Alerts   │ │ Insights │   │    │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘   │    │
│  │                           ↓ HTTP/JSON ↓                              │    │
│  │  ┌─────────────────────────────────────────────────────────────┐    │    │
│  │  │                    ApiService (HttpClient)                   │    │    │
│  │  └─────────────────────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ HTTPS (JWT Bearer)
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                              API LAYER                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                    FastAPI Application                               │    │
│  │  ┌─────────────────────────────────────────────────────────────┐    │    │
│  │  │                 CORS Middleware                               │    │    │
│  │  └─────────────────────────────────────────────────────────────┘    │    │
│  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐   │    │
│  │  │ auth │ │hold- │ │port- │ │market│ │alerts│ │compe-│ │subs  │   │    │
│  │  │      │ │ings  │ │folio │ │      │ │      │ │tition│ │      │   │    │
│  │  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘ └──────┘ └──────┘   │    │
│  │  + news, watchlist, insights, goals, dividends, transactions,      │    │
│  │    settings, compare (14 routers total)                             │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ↓               ↓               ↓
┌─────────────────────────┐ ┌─────────────┐ ┌─────────────────────┐
│    SERVICE LAYER        │ │ EXTERNAL    │ │   DATA LAYER        │
├─────────────────────────┤ │ SERVICES    │ ├─────────────────────┤
│ ┌─────────────────────┐ │ ├─────────────┤ │ ┌─────────────────┐ │
│ │   market_data.py    │ │ │ Yahoo       │ │ │  PostgreSQL     │ │
│ │   (yfinance)        │─┼─│ Finance API │ │ │  (SQLAlchemy)   │ │
│ └─────────────────────┘ │ └─────────────┘ │ │                 │ │
│ ┌─────────────────────┐ │ ┌─────────────┐ │ │  15 Tables:     │ │
│ │   sentiment.py      │ │ │ News RSS    │ │ │  - users        │ │
│ │   (TextBlob/NLTK)   │─┼─│ Feeds       │ │ │  - holdings     │ │
│ └─────────────────────┘ │ └─────────────┘ │ │  - transactions │ │
│ ┌─────────────────────┐ │ ┌─────────────┐ │ │  - alerts       │ │
│ │   prediction.py     │ │ │ Stripe API  │ │ │  - competitions │ │
│ │   (ML Ensemble)     │ │ └─────────────┘ │ │  - etc...       │ │
│ └─────────────────────┘ │ ┌─────────────┐ │ └─────────────────┘ │
│ ┌─────────────────────┐ │ │ Resend API  │ │                     │
│ │   email.py          │─┼─│ (Email)     │ │                     │
│ └─────────────────────┘ │ └─────────────┘ │                     │
└─────────────────────────┘                 └─────────────────────┘
```

### 2.2 Request Flow

```
1. Client Request
   └── Angular HttpClient sends request with JWT in Authorization header
       └── FastAPI receives request
           └── CORS middleware validates origin
               └── Route handler invoked
                   └── Dependency injection (get_db, get_current_user)
                       └── Service layer processes business logic
                           └── ORM interacts with PostgreSQL
                               └── Response serialized via Pydantic
                                   └── JSON returned to client
```

### 2.3 Directory Structure

```
foliowise/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI app factory
│   │   ├── config.py               # Pydantic settings
│   │   ├── database.py             # SQLAlchemy setup
│   │   ├── models/                 # ORM models (8 files)
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── holding.py
│   │   │   ├── transaction.py
│   │   │   ├── watchlist.py
│   │   │   ├── alert.py
│   │   │   ├── goal.py
│   │   │   ├── dividend.py
│   │   │   ├── insight.py
│   │   │   └── competition.py
│   │   ├── routers/                # API routes (14 files)
│   │   │   ├── auth.py
│   │   │   ├── holdings.py
│   │   │   ├── portfolio.py
│   │   │   ├── market.py
│   │   │   ├── watchlist.py
│   │   │   ├── alerts.py
│   │   │   ├── news.py
│   │   │   ├── insights.py
│   │   │   ├── goals.py
│   │   │   ├── dividends.py
│   │   │   ├── transactions.py
│   │   │   ├── settings.py
│   │   │   ├── compare.py
│   │   │   ├── subscriptions.py
│   │   │   └── competitions.py
│   │   ├── services/               # Business logic (7 files)
│   │   │   ├── auth.py
│   │   │   ├── market_data.py
│   │   │   ├── sentiment.py
│   │   │   ├── prediction.py
│   │   │   ├── ai_advisor.py
│   │   │   ├── email.py
│   │   │   ├── limits.py
│   │   │   └── csv_parser.py
│   │   └── schemas/                # Pydantic schemas
│   │       └── transaction.py
│   ├── requirements.txt
│   └── render.yaml                 # Deployment config
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── app.ts              # Root component
│   │   │   ├── app.routes.ts       # Route definitions
│   │   │   ├── components/         # UI components (22 dirs)
│   │   │   │   ├── landing/
│   │   │   │   ├── login/
│   │   │   │   ├── register/
│   │   │   │   ├── navbar/
│   │   │   │   ├── dashboard/
│   │   │   │   ├── holdings/
│   │   │   │   ├── transactions/
│   │   │   │   ├── gains/
│   │   │   │   ├── watchlist/
│   │   │   │   ├── alerts/
│   │   │   │   ├── sentiment/
│   │   │   │   ├── goals/
│   │   │   │   ├── stock-lookup/
│   │   │   │   ├── compare/
│   │   │   │   ├── pricing/
│   │   │   │   ├── arena/
│   │   │   │   ├── ai-insights/
│   │   │   │   ├── ai-chat/
│   │   │   │   ├── weekly-digest/
│   │   │   │   ├── settings/
│   │   │   │   └── toast/
│   │   │   ├── services/           # Angular services (3 files)
│   │   │   │   ├── auth.ts
│   │   │   │   ├── api.ts
│   │   │   │   └── toast.ts
│   │   │   └── guards/             # Route guards
│   │   │       └── auth.guard.ts
│   │   ├── environments/
│   │   └── styles.css              # Global styles
│   ├── angular.json
│   ├── tailwind.config.js
│   ├── package.json
│   └── tsconfig.json
│
└── TECHNICAL_DOCUMENTATION.md
```

---

## 3. Technology Stack

### 3.1 Backend Technologies

| Category | Technology | Version | Purpose |
|----------|------------|---------|---------|
| **Runtime** | Python | 3.11+ | Primary backend language |
| **Framework** | FastAPI | >=0.100.0 | Async web framework with OpenAPI |
| **ASGI Server** | Uvicorn | >=0.23.0 | Production ASGI server |
| **ORM** | SQLAlchemy | >=2.0.0 | Database ORM with type hints |
| **Database** | PostgreSQL | 15+ | Primary data store |
| **DB Driver** | psycopg2-binary | >=2.9.0 | PostgreSQL adapter |
| **Validation** | Pydantic | >=2.0.0 | Data validation & serialization |
| **Settings** | pydantic-settings | >=2.0.0 | Environment configuration |
| **Auth** | python-jose | >=3.3.0 | JWT token handling |
| **Password** | passlib + bcrypt | >=1.7.4 / >=4.0.0 | Password hashing |
| **HTTP Client** | httpx | >=0.24.0 | Async HTTP requests |
| **File Upload** | python-multipart | >=0.0.6 | Multipart form handling |

### 3.2 Data Processing & ML

| Category | Technology | Version | Purpose |
|----------|------------|---------|---------|
| **Market Data** | yfinance | >=0.2.0 | Yahoo Finance API wrapper |
| **Data Analysis** | pandas | >=2.0.0 | DataFrame operations |
| **Numerical** | numpy | >=1.24.0 | Array computations |
| **NLP** | TextBlob | >=0.17.0 | Sentiment analysis |
| **NLP Toolkit** | NLTK | >=3.8.0 | Natural language processing |
| **HTML Parsing** | BeautifulSoup4 | >=4.12.0 | HTML/XML parsing |
| **RSS Parsing** | feedparser | >=6.0.0 | RSS/Atom feed parsing |

### 3.3 External Services

| Category | Technology | Version | Purpose |
|----------|------------|---------|---------|
| **Payments** | Stripe | >=7.0.0 | Subscription management |
| **Email** | Resend | >=0.6.0 | Transactional emails |
| **AI** | OpenAI/Claude | - | AI-powered insights |

### 3.4 Frontend Technologies

| Category | Technology | Version | Purpose |
|----------|------------|---------|---------|
| **Framework** | Angular | 21.1.0 | SPA framework |
| **Language** | TypeScript | 5.9.2 | Type-safe JavaScript |
| **Reactive** | RxJS | 7.8.0 | Reactive programming |
| **CSS Framework** | Tailwind CSS | 3.4.19 | Utility-first CSS |
| **Charts** | Chart.js | 4.5.1 | Data visualization |
| **Chart Wrapper** | ng2-charts | 8.0.0 | Angular Chart.js wrapper |
| **Smooth Scroll** | Lenis | 1.1.18 | Smooth scrolling |
| **CSS Processing** | PostCSS | 8.5.6 | CSS transformations |
| **Autoprefixer** | autoprefixer | 10.4.23 | Browser prefixes |
| **Testing** | Vitest | 4.0.8 | Unit testing |

### 3.5 Development Tools

| Category | Technology | Purpose |
|----------|------------|---------|
| **Build** | Angular CLI | Project scaffolding & builds |
| **Package Manager** | npm | Dependency management |
| **Linting** | Prettier | Code formatting |
| **Environment** | dotenv | Environment variable loading |

---

## 4. Backend Implementation

### 4.1 Application Entry Point

**File:** `app/main.py`

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables on startup
    Base.metadata.create_all(bind=engine)

    # Run migrations (add columns if not exist)
    # ... migration logic ...

    yield  # Application runs here

app = FastAPI(
    lifespan=lifespan,
    title="Foliowise API",
    description="An intelligent portfolio tracker with AI-powered insights",
    version="0.1.0"
)

# CORS Middleware
@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    if request.method == "OPTIONS":
        return Response(status_code=200, headers={...})
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

# Router Registration (14 routers)
app.include_router(auth.router)
app.include_router(holdings.router)
app.include_router(market.router)
# ... 11 more routers ...
```

### 4.2 Configuration Management

**File:** `app/config.py`

```python
class Settings(BaseSettings):
    # Required
    database_url: str          # PostgreSQL connection string
    secret_key: str            # JWT signing key (256-bit)
    debug: bool = False        # Debug mode toggle

    # Email (Optional)
    resend_api_key: str | None = None
    email_from: str = "Foliowise <alerts@foliowise.app>"

    # Stripe (Optional)
    stripe_secret_key: str | None = None
    stripe_webhook_secret: str | None = None
    stripe_pro_price_id: str | None = None
    stripe_pro_plus_price_id: str | None = None
    frontend_url: str = "http://localhost:4200"

    class Config:
        env_file = ".env"

settings = Settings()
```

### 4.3 Database Layer

**File:** `app/database.py`

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    """Declarative base for all ORM models."""
    pass

def get_db():
    """Dependency injection for database sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 4.4 ORM Models

#### 4.4.1 User Model

**File:** `app/models/user.py`

```python
class User(Base):
    __tablename__ = "users"

    # Primary Key
    id: Mapped[str] = mapped_column(String(36), primary_key=True,
                                     default=lambda: str(uuid.uuid4()))

    # Authentication
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Subscription
    subscription_tier: Mapped[str] = mapped_column(String(20), default="free")
    subscription_status: Mapped[str] = mapped_column(String(20), default="active")
    subscription_ends_at: Mapped[datetime | None] = mapped_column(DateTime)
    stripe_customer_id: Mapped[str | None] = mapped_column(String(255))
    stripe_subscription_id: Mapped[str | None] = mapped_column(String(255))

    # Referral Program
    referral_code: Mapped[str | None] = mapped_column(String(20), unique=True)
    referred_by: Mapped[str | None] = mapped_column(String(36))
    referral_count: Mapped[int] = mapped_column(Integer, default=0)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, onupdate=datetime.utcnow)

    # Relationships (One-to-Many)
    holdings = relationship("Holding", back_populates="user", cascade="all, delete")
    watchlist = relationship("WatchlistItem", back_populates="user", cascade="all, delete")
    alerts = relationship("PriceAlert", back_populates="user", cascade="all, delete")
    insights = relationship("Insight", back_populates="user", cascade="all, delete")
    chat_messages = relationship("ChatMessage", back_populates="user", cascade="all, delete")
    weekly_digests = relationship("WeeklyDigest", back_populates="user", cascade="all, delete")
    goals = relationship("PortfolioGoal", back_populates="user", cascade="all, delete")
    dividends = relationship("Dividend", back_populates="user", cascade="all, delete")
```

#### 4.4.2 Holding Model

**File:** `app/models/holding.py`

```python
class Holding(Base):
    __tablename__ = "holdings"

    id: Mapped[str] = mapped_column(String(36), primary_key=True,
                                     default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))

    # Stock Information
    ticker: Mapped[str] = mapped_column(String(10), nullable=False)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    avg_cost_basis: Mapped[float] = mapped_column(Float, nullable=False)
    realized_gains: Mapped[float] = mapped_column(Float, default=0.0)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="holdings")
    transactions = relationship("Transaction", back_populates="holding", cascade="all, delete")
```

#### 4.4.3 Transaction Model

**File:** `app/models/transaction.py`

```python
class TransactionType(enum.Enum):
    BUY = "BUY"
    SELL = "SELL"

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    holding_id: Mapped[str] = mapped_column(String(36), ForeignKey("holdings.id"))

    type: Mapped[TransactionType] = mapped_column(Enum(TransactionType))
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    price_per_unit: Mapped[float] = mapped_column(Float, nullable=False)
    transaction_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    holding = relationship("Holding", back_populates="transactions")
```

#### 4.4.4 Competition Models

**File:** `app/models/competition.py`

```python
# Enumerations
class CompetitionStatus(enum.Enum):
    UPCOMING = "upcoming"
    ACTIVE = "active"
    ENDED = "ended"

class CompetitionType(enum.Enum):
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    SPECIAL = "special"

class TradeType(enum.Enum):
    BUY = "BUY"
    SELL = "SELL"

class AchievementType(enum.Enum):
    TRADING = "trading"
    COMPETITION = "competition"
    STREAK = "streak"
    MILESTONE = "milestone"

# Competition Table
class Competition(Base):
    __tablename__ = "competitions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    type: Mapped[CompetitionType] = mapped_column(Enum(CompetitionType))
    status: Mapped[CompetitionStatus] = mapped_column(Enum(CompetitionStatus))

    starting_balance: Mapped[float] = mapped_column(Float, default=100000.0)
    max_participants: Mapped[int | None] = mapped_column(Integer)
    entry_fee: Mapped[float] = mapped_column(Float, default=0.0)
    prize_description: Mapped[str | None] = mapped_column(String(255))

    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    portfolios = relationship("VirtualPortfolio", back_populates="competition")

# Virtual Portfolio
class VirtualPortfolio(Base):
    __tablename__ = "virtual_portfolios"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))
    competition_id: Mapped[str] = mapped_column(String(36), ForeignKey("competitions.id"))

    cash_balance: Mapped[float] = mapped_column(Float, default=100000.0)
    total_value: Mapped[float] = mapped_column(Float, default=100000.0)
    total_return: Mapped[float] = mapped_column(Float, default=0.0)
    total_return_percent: Mapped[float] = mapped_column(Float, default=0.0)

    current_rank: Mapped[int | None] = mapped_column(Integer)
    best_rank: Mapped[int | None] = mapped_column(Integer)
    trades_count: Mapped[int] = mapped_column(Integer, default=0)
    winning_trades: Mapped[int] = mapped_column(Integer, default=0)
    losing_trades: Mapped[int] = mapped_column(Integer, default=0)

    joined_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_trade_at: Mapped[datetime | None] = mapped_column(DateTime)

# Achievement Definitions
ACHIEVEMENT_DEFINITIONS = [
    {"code": "first_trade", "name": "First Steps", "icon": "🚀",
     "type": AchievementType.TRADING, "target": 1},
    {"code": "trader_10", "name": "Active Trader", "icon": "📈",
     "type": AchievementType.TRADING, "target": 10},
    {"code": "trader_100", "name": "Trading Master", "icon": "🏆",
     "type": AchievementType.TRADING, "target": 100},
    {"code": "first_profit", "name": "In The Green", "icon": "💚",
     "type": AchievementType.TRADING, "target": 1},
    {"code": "profit_1000", "name": "Grand Profit", "icon": "💰",
     "type": AchievementType.MILESTONE, "target": 1000},
    {"code": "profit_10000", "name": "Legendary Gains", "icon": "🤑",
     "type": AchievementType.MILESTONE, "target": 10000},
    {"code": "competition_join", "name": "Competitor", "icon": "🎮",
     "type": AchievementType.COMPETITION, "target": 1},
    {"code": "competition_top10", "name": "Top 10", "icon": "🥇",
     "type": AchievementType.COMPETITION, "target": 1},
    {"code": "competition_winner", "name": "Champion", "icon": "👑",
     "type": AchievementType.COMPETITION, "target": 1},
    {"code": "win_streak_3", "name": "Hot Streak", "icon": "🔥",
     "type": AchievementType.STREAK, "target": 3},
    {"code": "win_streak_5", "name": "On Fire", "icon": "⚡",
     "type": AchievementType.STREAK, "target": 5},
    {"code": "diversified", "name": "Diversified", "icon": "🎯",
     "type": AchievementType.TRADING, "target": 5},
]
```

### 4.5 Service Layer

#### 4.5.1 Market Data Service

**File:** `app/services/market_data.py`

```python
import yfinance as yf
from functools import lru_cache
from datetime import datetime, timedelta

@lru_cache(maxsize=100)
def get_stock_quote(ticker: str) -> dict | None:
    """
    Fetch real-time stock quote from Yahoo Finance.

    Args:
        ticker: Stock symbol (e.g., "AAPL", "GOOGL")

    Returns:
        Dictionary containing:
        - ticker: str
        - name: str
        - current_price: float
        - previous_close: float
        - day_change: float
        - day_change_percent: float
        - day_high: float
        - day_low: float
        - volume: int
        - market_cap: int
        - fifty_two_week_high: float
        - fifty_two_week_low: float
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        current_price = info.get("currentPrice") or info.get("regularMarketPrice")
        previous_close = info.get("previousClose") or info.get("regularMarketPreviousClose")

        if not current_price:
            return None

        day_change = current_price - previous_close if previous_close else 0
        day_change_percent = (day_change / previous_close * 100) if previous_close else 0

        return {
            "ticker": ticker.upper(),
            "name": info.get("shortName") or info.get("longName") or ticker,
            "current_price": current_price,
            "previous_close": previous_close,
            "day_change": day_change,
            "day_change_percent": day_change_percent,
            "day_high": info.get("dayHigh"),
            "day_low": info.get("dayLow"),
            "volume": info.get("volume"),
            "market_cap": info.get("marketCap"),
            "fifty_two_week_high": info.get("fiftyTwoWeekHigh"),
            "fifty_two_week_low": info.get("fiftyTwoWeekLow"),
        }
    except Exception:
        return None

def get_stock_history(ticker: str, period: str = "1mo") -> list[dict]:
    """
    Fetch historical OHLCV data.

    Args:
        ticker: Stock symbol
        period: Time period ("1mo", "3mo", "6mo", "1y", "5y")

    Returns:
        List of dicts with date, open, high, low, close, volume
    """
    stock = yf.Ticker(ticker)
    df = stock.history(period=period)

    return [
        {
            "date": index.strftime("%Y-%m-%d"),
            "open": row["Open"],
            "high": row["High"],
            "low": row["Low"],
            "close": row["Close"],
            "volume": int(row["Volume"]),
        }
        for index, row in df.iterrows()
    ]

def search_tickers(query: str, limit: int = 10) -> list[dict]:
    """
    Search for stocks by ticker or company name.

    Uses yfinance search functionality to find matching symbols.
    """
    # Implementation uses yf.Tickers or direct API calls
    pass
```

#### 4.5.2 Prediction Service

**File:** `app/services/prediction.py`

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

def predict_prices(ticker: str, days_ahead: int = 30) -> dict:
    """
    Ensemble prediction model combining:
    1. Linear Regression (trend)
    2. Exponential Moving Average (momentum)
    3. Mean Reversion (statistical)

    Args:
        ticker: Stock symbol
        days_ahead: Prediction horizon (7-90 days)

    Returns:
        {
            "ticker": str,
            "current_price": float,
            "predictions": [
                {
                    "date": str,
                    "predicted_price": float,
                    "upper_bound": float,
                    "lower_bound": float
                }
            ],
            "summary": {
                "days_ahead": int,
                "final_predicted_price": float,
                "predicted_change": float,
                "predicted_change_percent": float,
                "confidence_score": float,
                "volatility": float,
                "rsi": float,
                "trend_direction": str
            },
            "disclaimer": str
        }
    """
    # Fetch historical data
    history = get_stock_history(ticker, period="1y")
    df = pd.DataFrame(history)

    # Calculate features
    closes = df["close"].values
    dates = np.arange(len(closes)).reshape(-1, 1)

    # Model 1: Linear Regression
    lr_model = LinearRegression()
    lr_model.fit(dates, closes)

    # Model 2: EMA
    ema_20 = df["close"].ewm(span=20).mean().iloc[-1]
    ema_50 = df["close"].ewm(span=50).mean().iloc[-1]

    # Model 3: Mean Reversion
    mean_price = closes.mean()
    std_price = closes.std()

    # Ensemble prediction
    predictions = []
    current_price = closes[-1]

    for i in range(1, days_ahead + 1):
        lr_pred = lr_model.predict([[len(closes) + i]])[0]
        ema_pred = ema_20 + (ema_50 - ema_20) * 0.1 * i
        mr_pred = current_price + (mean_price - current_price) * 0.05 * i

        # Weighted ensemble
        ensemble_pred = 0.4 * lr_pred + 0.35 * ema_pred + 0.25 * mr_pred

        # Confidence bands based on volatility
        volatility = std_price / mean_price
        band_width = ensemble_pred * volatility * np.sqrt(i / 252)

        predictions.append({
            "date": (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d"),
            "predicted_price": round(ensemble_pred, 2),
            "upper_bound": round(ensemble_pred + band_width, 2),
            "lower_bound": round(ensemble_pred - band_width, 2),
        })

    return {
        "ticker": ticker,
        "current_price": current_price,
        "predictions": predictions,
        "summary": {
            "days_ahead": days_ahead,
            "final_predicted_price": predictions[-1]["predicted_price"],
            "predicted_change": predictions[-1]["predicted_price"] - current_price,
            "predicted_change_percent": (predictions[-1]["predicted_price"] - current_price) / current_price * 100,
            "confidence_score": max(0, 100 - volatility * 200),
            "volatility": volatility * 100,
            "rsi": calculate_rsi(closes),
            "trend_direction": "bullish" if lr_model.coef_[0] > 0 else "bearish",
        },
        "disclaimer": "Predictions are for educational purposes only...",
    }
```

#### 4.5.3 Sentiment Service

**File:** `app/services/sentiment.py`

```python
from textblob import TextBlob
import feedparser
from bs4 import BeautifulSoup

def get_stock_sentiment(ticker: str) -> dict:
    """
    Analyze news sentiment for a stock using TextBlob NLP.

    Process:
    1. Fetch RSS feeds from Yahoo Finance
    2. Parse article titles and summaries
    3. Run sentiment analysis with TextBlob
    4. Aggregate results

    Returns:
        {
            "ticker": str,
            "overall_sentiment": "bullish" | "bearish" | "neutral",
            "average_polarity": float (-1 to 1),
            "article_count": int,
            "sentiment_breakdown": {
                "positive": int,
                "negative": int,
                "neutral": int,
                "positive_percent": float,
                "negative_percent": float,
                "neutral_percent": float
            },
            "articles": [
                {
                    "title": str,
                    "link": str,
                    "published": str,
                    "sentiment": str,
                    "polarity": float
                }
            ]
        }
    """
    # Fetch news from RSS
    feed_url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}"
    feed = feedparser.parse(feed_url)

    articles = []
    polarities = []

    for entry in feed.entries[:20]:
        # Clean HTML
        text = BeautifulSoup(entry.get("summary", ""), "html.parser").get_text()
        full_text = entry.title + " " + text

        # Analyze sentiment
        blob = TextBlob(full_text)
        polarity = blob.sentiment.polarity
        polarities.append(polarity)

        # Classify
        if polarity > 0.1:
            sentiment = "positive"
        elif polarity < -0.1:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        articles.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.get("published", ""),
            "sentiment": sentiment,
            "polarity": round(polarity, 3),
        })

    # Aggregate
    avg_polarity = sum(polarities) / len(polarities) if polarities else 0
    positive = sum(1 for p in polarities if p > 0.1)
    negative = sum(1 for p in polarities if p < -0.1)
    neutral = len(polarities) - positive - negative

    return {
        "ticker": ticker,
        "overall_sentiment": "bullish" if avg_polarity > 0.1 else "bearish" if avg_polarity < -0.1 else "neutral",
        "average_polarity": round(avg_polarity, 3),
        "article_count": len(articles),
        "sentiment_breakdown": {
            "positive": positive,
            "negative": negative,
            "neutral": neutral,
            "positive_percent": positive / len(articles) * 100 if articles else 0,
            "negative_percent": negative / len(articles) * 100 if articles else 0,
            "neutral_percent": neutral / len(articles) * 100 if articles else 0,
        },
        "articles": articles,
    }
```

#### 4.5.4 Authentication Service

**File:** `app/services/auth.py`

```python
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hash_password(password: str) -> str:
    """Generate bcrypt hash of password."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash."""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    """
    Create JWT access token.

    Args:
        data: Payload (usually {"sub": user_id})

    Returns:
        Encoded JWT string
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict | None:
    """Decode and validate JWT token."""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    FastAPI dependency for extracting current user from JWT.

    Raises HTTPException 401 if invalid/expired token.
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise credentials_exception

    return user
```

#### 4.5.5 Limits Service

**File:** `app/services/limits.py`

```python
# Tier-based feature limits
TIER_LIMITS = {
    "free": {
        "holdings": 10,
        "alerts": 1,
        "lookups_per_day": 5,
        "ai_questions_per_day": 3,
        "competitions": 1,
    },
    "pro": {
        "holdings": 100,
        "alerts": 25,
        "lookups_per_day": 50,
        "ai_questions_per_day": 50,
        "competitions": -1,  # Unlimited
    },
    "pro_plus": {
        "holdings": -1,  # Unlimited
        "alerts": -1,
        "lookups_per_day": -1,
        "ai_questions_per_day": -1,
        "competitions": -1,
    },
}

def check_holdings_limit(user: User, db: Session) -> bool:
    """Check if user can add more holdings."""
    limit = TIER_LIMITS[user.subscription_tier]["holdings"]
    if limit == -1:
        return True

    count = db.query(Holding).filter(Holding.user_id == user.id).count()
    return count < limit

def check_alerts_limit(user: User, db: Session) -> bool:
    """Check if user can add more alerts."""
    limit = TIER_LIMITS[user.subscription_tier]["alerts"]
    if limit == -1:
        return True

    count = db.query(PriceAlert).filter(
        PriceAlert.user_id == user.id,
        PriceAlert.is_active == True
    ).count()
    return count < limit

def get_usage_summary(user: User, db: Session) -> dict:
    """Get comprehensive usage summary for user."""
    tier = user.subscription_tier
    limits = TIER_LIMITS[tier]

    holdings_count = db.query(Holding).filter(Holding.user_id == user.id).count()
    alerts_count = db.query(PriceAlert).filter(
        PriceAlert.user_id == user.id,
        PriceAlert.is_active == True
    ).count()

    return {
        "tier": tier,
        "holdings": {"used": holdings_count, "limit": limits["holdings"]},
        "alerts": {"used": alerts_count, "limit": limits["alerts"]},
        "lookups_per_day": {"used": 0, "limit": limits["lookups_per_day"]},
        "ai_questions_per_day": {"used": 0, "limit": limits["ai_questions_per_day"]},
    }
```

---

## 5. Frontend Implementation

### 5.1 Application Bootstrap

**File:** `src/main.ts`

```typescript
import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { App } from './app/app';

bootstrapApplication(App, appConfig)
  .catch((err) => console.error(err));
```

### 5.2 Route Configuration

**File:** `src/app/app.routes.ts`

```typescript
import { Routes } from '@angular/router';
import { authGuard } from './guards/auth.guard';

export const routes: Routes = [
  // Public Routes
  { path: '', component: Landing },
  { path: 'login', component: Login },
  { path: 'register', component: Register },
  { path: 'pricing', component: Pricing },

  // Protected Routes (require authentication)
  { path: 'dashboard', component: Dashboard, canActivate: [authGuard] },
  { path: 'holdings', component: Holdings, canActivate: [authGuard] },
  { path: 'watchlist', component: Watchlist, canActivate: [authGuard] },
  { path: 'alerts', component: Alerts, canActivate: [authGuard] },
  { path: 'sentiment', component: Sentiment, canActivate: [authGuard] },
  { path: 'transactions', component: Transactions, canActivate: [authGuard] },
  { path: 'gains', component: Gains, canActivate: [authGuard] },
  { path: 'lookup', component: StockLookup, canActivate: [authGuard] },
  { path: 'arena', component: ArenaComponent, canActivate: [authGuard] },

  // Wildcard redirect
  { path: '**', redirectTo: '/dashboard' }
];
```

### 5.3 Authentication Guard

**File:** `src/app/guards/auth.guard.ts`

```typescript
import { inject } from '@angular/core';
import { Router, CanActivateFn } from '@angular/router';
import { AuthService } from '../services/auth';

export const authGuard: CanActivateFn = (route, state) => {
  const authService = inject(AuthService);
  const router = inject(Router);

  if (authService.isLoggedIn()) {
    return true;
  }

  // Store attempted URL for redirect after login
  router.navigate(['/login'], {
    queryParams: { returnUrl: state.url }
  });
  return false;
};
```

### 5.4 Services

#### 5.4.1 Authentication Service

**File:** `src/app/services/auth.ts`

```typescript
@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = environment.apiUrl;
  private tokenKey = 'foliowise_token';

  currentUser$ = new BehaviorSubject<User | null>(null);

  constructor(
    private http: HttpClient,
    private router: Router
  ) {
    // Auto-load user on service init if token exists
    if (this.isLoggedIn()) {
      this.getCurrentUser().subscribe();
    }
  }

  register(email: string, password: string): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(
      `${this.apiUrl}/auth/register`,
      { email, password }
    ).pipe(
      tap(response => this.handleAuthResponse(response))
    );
  }

  login(email: string, password: string): Observable<AuthResponse> {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    return this.http.post<AuthResponse>(
      `${this.apiUrl}/auth/login`,
      formData
    ).pipe(
      tap(response => this.handleAuthResponse(response))
    );
  }

  logout(): void {
    localStorage.removeItem(this.tokenKey);
    this.currentUser$.next(null);
    this.router.navigate(['/login']);
  }

  isLoggedIn(): boolean {
    return !!this.getToken();
  }

  getToken(): string | null {
    return localStorage.getItem(this.tokenKey);
  }

  private handleAuthResponse(response: AuthResponse): void {
    localStorage.setItem(this.tokenKey, response.access_token);
    this.getCurrentUser().subscribe();
  }
}
```

#### 5.4.2 API Service

**File:** `src/app/services/api.ts`

```typescript
// Key Interfaces
export interface Holding {
  id: string;
  user_id: string;
  ticker: string;
  quantity: number;
  avg_cost_basis: number;
  created_at: string;
  updated_at: string;
}

export interface PortfolioSummary {
  total_value: number;
  total_cost: number;
  total_profit_loss: number;
  total_profit_loss_percent: number;
  day_change: number;
  day_change_percent: number;
  holdings_count: number;
  holdings: HoldingWithMarketData[];
}

export interface Competition {
  id: string;
  name: string;
  description: string | null;
  type: 'weekly' | 'monthly' | 'special';
  status: 'upcoming' | 'active' | 'ended';
  starting_balance: number;
  participant_count: number;
  user_joined: boolean;
  user_rank: number | null;
}

export interface Achievement {
  code: string;
  name: string;
  description: string;
  icon: string;
  type: 'trading' | 'competition' | 'streak' | 'milestone';
  progress: number;
  target: number;
  unlocked: boolean;
  unlocked_at: string | null;
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = environment.apiUrl;

  constructor(
    private http: HttpClient,
    private authService: AuthService
  ) {}

  private getAuthHeaders(): HttpHeaders {
    const token = this.authService.getToken();
    return new HttpHeaders({
      'Authorization': `Bearer ${token}`
    });
  }

  // Holdings
  getHoldings(): Observable<Holding[]> {
    return this.http.get<Holding[]>(
      `${this.apiUrl}/holdings/`,
      { headers: this.getAuthHeaders() }
    );
  }

  createHolding(holding: HoldingCreate): Observable<Holding> {
    return this.http.post<Holding>(
      `${this.apiUrl}/holdings/`,
      holding,
      { headers: this.getAuthHeaders() }
    );
  }

  // Portfolio
  getPortfolioSummary(): Observable<PortfolioSummary> {
    return this.http.get<PortfolioSummary>(
      `${this.apiUrl}/portfolio/summary`,
      { headers: this.getAuthHeaders() }
    );
  }

  // Market Data
  getStockQuote(ticker: string): Observable<StockQuote> {
    return this.http.get<StockQuote>(
      `${this.apiUrl}/market/quote/${ticker}`
    );
  }

  getStockPrediction(ticker: string, days: number = 30): Observable<StockPrediction> {
    return this.http.get<StockPrediction>(
      `${this.apiUrl}/market/predict/${ticker}?days=${days}`
    );
  }

  // Competitions
  getCompetitions(): Observable<Competition[]> {
    return this.http.get<Competition[]>(
      `${this.apiUrl}/competitions/`,
      { headers: this.getAuthHeaders() }
    );
  }

  joinCompetition(competitionId: string): Observable<VirtualPortfolio> {
    return this.http.post<VirtualPortfolio>(
      `${this.apiUrl}/competitions/${competitionId}/join`,
      {},
      { headers: this.getAuthHeaders() }
    );
  }

  makeVirtualTrade(competitionId: string, trade: VirtualTradeCreate): Observable<any> {
    return this.http.post(
      `${this.apiUrl}/competitions/${competitionId}/trade`,
      trade,
      { headers: this.getAuthHeaders() }
    );
  }

  // 60+ more methods for all endpoints...
}
```

### 5.5 Component Architecture

#### 5.5.1 Dashboard Component

**File:** `src/app/components/dashboard/dashboard.ts`

```typescript
@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterLink, BaseChartDirective, NavbarComponent],
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.css']
})
export class Dashboard implements OnInit, OnDestroy {
  private destroy$ = new Subject<void>();

  // Data
  portfolio: PortfolioSummary | null = null;
  performance: PortfolioPerformance | null = null;
  triggeredAlerts: PriceAlert[] = [];

  // Charts
  performanceChart: ChartConfiguration<'line'> | null = null;
  allocationChart: ChartConfiguration<'doughnut'> | null = null;

  // UI State
  loading = true;
  selectedPeriod = '1mo';

  constructor(
    private api: ApiService,
    private toast: ToastService
  ) {}

  ngOnInit(): void {
    this.loadDashboard();
    this.checkAlerts();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  loadDashboard(): void {
    forkJoin({
      portfolio: this.api.getPortfolioSummary(),
      performance: this.api.getPortfolioPerformance(this.selectedPeriod)
    })
    .pipe(takeUntil(this.destroy$))
    .subscribe({
      next: (data) => {
        this.portfolio = data.portfolio;
        this.performance = data.performance;
        this.updateCharts();
        this.loading = false;
      },
      error: () => {
        this.toast.error('Failed to load dashboard');
        this.loading = false;
      }
    });
  }

  updateCharts(): void {
    // Performance Line Chart
    this.performanceChart = {
      type: 'line',
      data: {
        labels: this.performance!.data.map(d => d.date),
        datasets: [
          {
            data: this.performance!.data.map(d => d.value),
            borderColor: '#38BDF8',
            backgroundColor: 'rgba(56, 189, 248, 0.1)',
            fill: true,
            tension: 0.4,
          },
          {
            // Cost basis line
            data: Array(this.performance!.data.length).fill(this.performance!.total_cost),
            borderColor: '#64748b',
            borderDash: [5, 5],
            fill: false,
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: { beginAtZero: false }
        }
      }
    };

    // Allocation Doughnut Chart
    this.allocationChart = {
      type: 'doughnut',
      data: {
        labels: this.portfolio!.holdings.map(h => h.ticker),
        datasets: [{
          data: this.portfolio!.holdings.map(h => h.current_value || 0),
          backgroundColor: this.generateColors(this.portfolio!.holdings.length),
        }]
      }
    };
  }
}
```

#### 5.5.2 Arena Component

**File:** `src/app/components/arena/arena.ts`

```typescript
@Component({
  selector: 'app-arena',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './arena.html',
  styleUrls: ['./arena.css']
})
export class ArenaComponent implements OnInit, OnDestroy {
  private destroy$ = new Subject<void>();

  // Data
  competitions: Competition[] = [];
  activeCompetition: Competition | null = null;
  portfolio: VirtualPortfolio | null = null;
  leaderboard: LeaderboardEntry[] = [];
  trades: VirtualTrade[] = [];
  achievements: Achievement[] = [];
  stats: CompetitionStats | null = null;

  // UI State
  activeTab: 'competitions' | 'portfolio' | 'leaderboard' | 'trades' | 'achievements' = 'competitions';
  showTradeModal = false;
  tradeType: 'BUY' | 'SELL' = 'BUY';
  tradeTicker = '';
  tradeQuantity = 1;
  tradePrice: number | null = null;

  ngOnInit(): void {
    this.loadData();
  }

  loadData(): void {
    forkJoin({
      competitions: this.api.getCompetitions(),
      achievements: this.api.getAchievements(),
      stats: this.api.getCompetitionStats()
    })
    .pipe(takeUntil(this.destroy$))
    .subscribe({
      next: (data) => {
        this.competitions = data.competitions;
        this.achievements = data.achievements;
        this.stats = data.stats;

        // Auto-select first active competition
        const active = this.competitions.find(c => c.status === 'active' && c.user_joined);
        if (active) this.selectCompetition(active);
      }
    });
  }

  joinCompetition(competition: Competition): void {
    this.api.joinCompetition(competition.id)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (portfolio) => {
          this.toast.success(`Joined ${competition.name}!`);
          this.portfolio = portfolio;
          competition.user_joined = true;
          this.loadCompetitionDetails(competition.id);
        }
      });
  }

  executeTrade(): void {
    if (!this.activeCompetition || !this.canExecuteTrade) return;

    this.api.makeVirtualTrade(this.activeCompetition.id, {
      ticker: this.tradeTicker,
      type: this.tradeType,
      quantity: this.tradeQuantity
    })
    .pipe(takeUntil(this.destroy$))
    .subscribe({
      next: (result) => {
        this.portfolio = result.portfolio;
        this.trades.unshift(result.trade);
        this.toast.success(`${this.tradeType} order executed!`);
        this.closeTradeModal();

        // Refresh leaderboard and achievements
        this.api.getLeaderboard(this.activeCompetition!.id).subscribe(lb => this.leaderboard = lb);
        this.api.getAchievements().subscribe(a => this.achievements = a);
      }
    });
  }
}
```

### 5.6 Styling System

**File:** `tailwind.config.js`

```javascript
module.exports = {
  content: ["./src/**/*.{html,ts}"],
  theme: {
    extend: {
      colors: {
        // Dark Palette
        'bg-primary': '#0a0a0a',
        'bg-secondary': '#111111',
        'bg-card': '#161616',
        'bg-elevated': '#1c1c1c',
        'text-primary': '#FFFFFF',
        'text-secondary': '#888888',
        'text-muted': '#555555',

        // Arctic Blue Accent
        'accent': '#38BDF8',
        'accent-dark': '#0EA5E9',
        'accent-light': '#7DD3FC',
        'accent-glow': 'rgba(56, 189, 248, 0.15)',

        // Status Colors
        'profit': '#22C55E',
        'loss': '#EF4444',
        'warning': '#F59E0B',

        // Borders
        'border': 'rgba(255, 255, 255, 0.08)',
        'border-hover': 'rgba(255, 255, 255, 0.15)',
      },

      fontFamily: {
        'display': ['Inter', 'system-ui', 'sans-serif'],
        'mono': ['JetBrains Mono', 'monospace'],
      },

      fontSize: {
        'hero': ['8rem', { lineHeight: '0.9', letterSpacing: '-0.04em', fontWeight: '800' }],
        'display-xl': ['6rem', { lineHeight: '0.95', letterSpacing: '-0.03em' }],
        'display-lg': ['4rem', { lineHeight: '1', letterSpacing: '-0.03em' }],
      },

      animation: {
        'fadeInUp': 'fadeInUp 0.8s cubic-bezier(0.65, 0.05, 0, 1)',
        'glow': 'glow 2s ease-in-out infinite alternate',
        'marquee': 'marquee 25s linear infinite',
      },

      boxShadow: {
        'glow': '0 0 40px rgba(56, 189, 248, 0.15)',
        'glow-profit': '0 0 40px rgba(34, 197, 94, 0.15)',
        'glow-loss': '0 0 40px rgba(239, 68, 68, 0.15)',
        'card': '0 4px 24px rgba(0, 0, 0, 0.5)',
      },
    },
  },
  plugins: [],
}
```

---

## 6. Database Schema

### 6.1 Entity Relationship Diagram

```
┌─────────────┐     ┌─────────────┐     ┌─────────────────┐
│    users    │────<│  holdings   │────<│  transactions   │
└─────────────┘     └─────────────┘     └─────────────────┘
       │
       │────<┌───────────────┐
       │     │ watchlist_item│
       │     └───────────────┘
       │
       │────<┌───────────────┐
       │     │ price_alerts  │
       │     └───────────────┘
       │
       │────<┌───────────────┐
       │     │portfolio_goals│
       │     └───────────────┘
       │
       │────<┌───────────────┐
       │     │   dividends   │
       │     └───────────────┘
       │
       │────<┌───────────────┐     ┌───────────────┐
       │     │   insights    │     │chat_messages  │
       │     └───────────────┘     └───────────────┘
       │
       │────<┌───────────────┐
       │     │weekly_digests │
       │     └───────────────┘
       │
       │────<┌───────────────────┐     ┌─────────────────┐
       │     │ virtual_portfolios│────<│ virtual_holdings│
       │     └───────────────────┘     └─────────────────┘
       │              │
       │              │────<┌───────────────┐
       │              │     │ virtual_trades│
       │              │     └───────────────┘
       │              │
       │              └────>┌───────────────┐
       │                    │ competitions  │
       │                    └───────────────┘
       │
       └────<┌───────────────┐
             │ achievements  │
             └───────────────┘
```

### 6.2 Table Definitions

#### Users Table

```sql
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,

    -- Subscription
    subscription_tier VARCHAR(20) DEFAULT 'free',
    subscription_status VARCHAR(20) DEFAULT 'active',
    subscription_ends_at TIMESTAMP,
    stripe_customer_id VARCHAR(255),
    stripe_subscription_id VARCHAR(255),

    -- Referral
    referral_code VARCHAR(20) UNIQUE,
    referred_by VARCHAR(36),
    referral_count INTEGER DEFAULT 0,

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_referral_code ON users(referral_code);
```

#### Holdings Table

```sql
CREATE TABLE holdings (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) REFERENCES users(id) ON DELETE CASCADE,
    ticker VARCHAR(10) NOT NULL,
    quantity FLOAT NOT NULL,
    avg_cost_basis FLOAT NOT NULL,
    realized_gains FLOAT DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE INDEX idx_holdings_user ON holdings(user_id);
CREATE INDEX idx_holdings_ticker ON holdings(ticker);
```

#### Competitions Table

```sql
CREATE TABLE competitions (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    type VARCHAR(20) NOT NULL,  -- weekly, monthly, special
    status VARCHAR(20) NOT NULL, -- upcoming, active, ended
    starting_balance FLOAT DEFAULT 100000.0,
    max_participants INTEGER,
    entry_fee FLOAT DEFAULT 0.0,
    prize_description VARCHAR(255),
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_competitions_status ON competitions(status);
```

#### Virtual Portfolios Table

```sql
CREATE TABLE virtual_portfolios (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) REFERENCES users(id) ON DELETE CASCADE,
    competition_id VARCHAR(36) REFERENCES competitions(id) ON DELETE CASCADE,
    cash_balance FLOAT DEFAULT 100000.0,
    total_value FLOAT DEFAULT 100000.0,
    total_return FLOAT DEFAULT 0.0,
    total_return_percent FLOAT DEFAULT 0.0,
    current_rank INTEGER,
    best_rank INTEGER,
    trades_count INTEGER DEFAULT 0,
    winning_trades INTEGER DEFAULT 0,
    losing_trades INTEGER DEFAULT 0,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_trade_at TIMESTAMP,

    UNIQUE(user_id, competition_id)
);

CREATE INDEX idx_vp_user ON virtual_portfolios(user_id);
CREATE INDEX idx_vp_competition ON virtual_portfolios(competition_id);
CREATE INDEX idx_vp_rank ON virtual_portfolios(current_rank);
```

---

## 7. API Reference

### 7.1 Authentication Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/auth/register` | Create new account | No |
| POST | `/auth/login` | Authenticate user | No |
| GET | `/auth/me` | Get current user | Yes |

**POST /auth/register**
```json
// Request
{
  "email": "user@example.com",
  "password": "securepassword123"
}

// Response 200
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 7.2 Holdings Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/holdings/` | List all holdings | Yes |
| POST | `/holdings/` | Create holding | Yes |
| GET | `/holdings/{id}` | Get holding | Yes |
| PUT | `/holdings/{id}` | Update holding | Yes |
| DELETE | `/holdings/{id}` | Delete holding | Yes |
| POST | `/holdings/import/preview` | Preview CSV import | Yes |
| POST | `/holdings/import` | Import from CSV | Yes |

**POST /holdings/**
```json
// Request
{
  "ticker": "AAPL",
  "quantity": 10,
  "avg_cost_basis": 150.00
}

// Response 201
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "...",
  "ticker": "AAPL",
  "quantity": 10,
  "avg_cost_basis": 150.00,
  "created_at": "2026-04-09T10:00:00Z",
  "updated_at": null
}
```

### 7.3 Portfolio Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/portfolio/summary` | Portfolio summary with live data | Yes |
| GET | `/portfolio/allocation` | Allocation breakdown | Yes |
| GET | `/portfolio/gains` | Realized/unrealized gains | Yes |
| GET | `/portfolio/performance` | Historical performance | Yes |

**GET /portfolio/summary**
```json
// Response 200
{
  "total_value": 15847.50,
  "total_cost": 14500.00,
  "total_profit_loss": 1347.50,
  "total_profit_loss_percent": 9.29,
  "day_change": 234.50,
  "day_change_percent": 1.50,
  "holdings_count": 5,
  "holdings": [
    {
      "id": "...",
      "ticker": "AAPL",
      "name": "Apple Inc.",
      "quantity": 10,
      "avg_cost_basis": 150.00,
      "current_price": 175.25,
      "current_value": 1752.50,
      "total_cost": 1500.00,
      "profit_loss": 252.50,
      "profit_loss_percent": 16.83,
      "day_change": 2.50,
      "day_change_percent": 1.45
    }
  ]
}
```

### 7.4 Market Data Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/market/quote/{ticker}` | Real-time quote | No |
| GET | `/market/history/{ticker}` | Historical data | No |
| GET | `/market/search` | Search stocks | No |
| GET | `/market/predict/{ticker}` | Price prediction | No |

**GET /market/predict/AAPL?days=30**
```json
// Response 200
{
  "ticker": "AAPL",
  "current_price": 175.25,
  "predictions": [
    {
      "date": "2026-04-10",
      "predicted_price": 176.10,
      "upper_bound": 178.50,
      "lower_bound": 173.70
    },
    // ... 29 more days
  ],
  "summary": {
    "days_ahead": 30,
    "final_predicted_price": 182.45,
    "predicted_change": 7.20,
    "predicted_change_percent": 4.11,
    "confidence_score": 72.5,
    "volatility": 18.3,
    "rsi": 55.2,
    "trend_direction": "bullish"
  },
  "disclaimer": "Predictions are for educational purposes only..."
}
```

### 7.5 Competition Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/competitions/` | List competitions | Yes |
| GET | `/competitions/{id}` | Get competition | Yes |
| POST | `/competitions/{id}/join` | Join competition | Yes |
| GET | `/competitions/{id}/portfolio` | Get user's portfolio | Yes |
| POST | `/competitions/{id}/trade` | Make virtual trade | Yes |
| GET | `/competitions/{id}/trades` | Get trade history | Yes |
| GET | `/competitions/{id}/leaderboard` | Get leaderboard | Yes |
| GET | `/competitions/achievements/me` | Get achievements | Yes |
| GET | `/competitions/stats/me` | Get user stats | Yes |

**POST /competitions/{id}/trade**
```json
// Request
{
  "ticker": "TSLA",
  "type": "BUY",
  "quantity": 5
}

// Response 200
{
  "trade": {
    "id": "...",
    "ticker": "TSLA",
    "type": "BUY",
    "quantity": 5,
    "price": 245.50,
    "total_value": 1227.50,
    "realized_pl": null,
    "executed_at": "2026-04-09T10:30:00Z"
  },
  "portfolio": {
    "id": "...",
    "cash_balance": 98772.50,
    "total_value": 100000.00,
    "total_return": 0.00,
    "total_return_percent": 0.00,
    "current_rank": 5,
    "trades_count": 1,
    "holdings": [...]
  }
}
```

### 7.6 Subscription Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/subscriptions/status` | Current subscription | Yes |
| GET | `/subscriptions/usage` | Usage limits | Yes |
| POST | `/subscriptions/checkout` | Create checkout | Yes |
| POST | `/subscriptions/portal` | Customer portal | Yes |
| POST | `/subscriptions/cancel` | Cancel subscription | Yes |
| POST | `/subscriptions/webhook` | Stripe webhook | No |
| GET | `/subscriptions/referral-code` | Get referral code | Yes |
| POST | `/subscriptions/apply-referral` | Apply referral | Yes |

---

## 8. Authentication & Security

### 8.1 Authentication Flow

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  Client  │     │   API    │     │   Auth   │     │    DB    │
└────┬─────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘
     │                │                │                │
     │ POST /login    │                │                │
     │───────────────>│                │                │
     │                │ verify_password│                │
     │                │───────────────>│                │
     │                │                │ query user     │
     │                │                │───────────────>│
     │                │                │<───────────────│
     │                │                │                │
     │                │                │ bcrypt.verify  │
     │                │<───────────────│                │
     │                │                │                │
     │                │ create_jwt     │                │
     │                │───────────────>│                │
     │                │<───────────────│                │
     │                │                │                │
     │  {access_token}│                │                │
     │<───────────────│                │                │
     │                │                │                │
```

### 8.2 JWT Token Structure

```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "user-uuid-here",
    "exp": 1712678400,
    "iat": 1712676600
  },
  "signature": "..."
}
```

### 8.3 Password Security

- **Algorithm:** bcrypt with auto-generated salt
- **Cost Factor:** 12 rounds (default)
- **Storage:** Only hash stored, never plaintext

### 8.4 Security Headers

```python
response.headers["Access-Control-Allow-Origin"] = "*"
response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
response.headers["Access-Control-Allow-Headers"] = "*"
response.headers["Access-Control-Max-Age"] = "86400"
```

### 8.5 Input Validation

All endpoints use Pydantic models for automatic validation:

```python
class HoldingCreate(BaseModel):
    ticker: str = Field(..., min_length=1, max_length=10, pattern="^[A-Z]+$")
    quantity: float = Field(..., gt=0)
    avg_cost_basis: float = Field(..., gt=0)
```

---

## 9. Third-Party Integrations

### 9.1 Yahoo Finance (yfinance)

**Purpose:** Real-time and historical market data

```python
import yfinance as yf

# Get quote
stock = yf.Ticker("AAPL")
info = stock.info
current_price = info["currentPrice"]

# Get history
df = stock.history(period="1mo")
```

### 9.2 Stripe Integration

**Purpose:** Subscription payments and billing

```python
import stripe
stripe.api_key = settings.stripe_secret_key

# Create checkout session
session = stripe.checkout.Session.create(
    customer=stripe_customer_id,
    payment_method_types=["card"],
    line_items=[{"price": settings.stripe_pro_price_id, "quantity": 1}],
    mode="subscription",
    success_url=f"{settings.frontend_url}/dashboard?success=true",
    cancel_url=f"{settings.frontend_url}/pricing?canceled=true",
)

# Webhook handling
event = stripe.Webhook.construct_event(
    payload, sig_header, settings.stripe_webhook_secret
)
```

### 9.3 Resend Email

**Purpose:** Transactional email delivery

```python
import resend
resend.api_key = settings.resend_api_key

def send_alert_email(to_email: str, alert: PriceAlert, current_price: float):
    resend.Emails.send({
        "from": settings.email_from,
        "to": to_email,
        "subject": f"Price Alert: {alert.ticker} {alert.condition} ${alert.target_price}",
        "html": f"""
            <h2>Your price alert was triggered!</h2>
            <p>{alert.ticker} is now ${current_price}</p>
        """
    })
```

### 9.4 TextBlob NLP

**Purpose:** Sentiment analysis

```python
from textblob import TextBlob

text = "Apple reports record earnings, stock surges"
blob = TextBlob(text)
polarity = blob.sentiment.polarity  # -1 to 1
subjectivity = blob.sentiment.subjectivity  # 0 to 1
```

---

## 10. Feature Documentation

### 10.1 Portfolio Tracking

**Components:**
- Dashboard: Overview with charts
- Holdings: CRUD management
- Transactions: Buy/sell history
- Gains: Realized vs unrealized

**Data Flow:**
1. User adds holding with ticker, quantity, avg cost
2. System fetches live price from Yahoo Finance
3. Calculates current value, P/L, day change
4. Displays in dashboard with charts

### 10.2 Trading Arena

**Components:**
- Competition listing with filters
- Virtual portfolio management
- Trade execution (BUY/SELL)
- Real-time leaderboard
- Achievement system

**Game Mechanics:**
- Starting balance: $100,000 virtual
- Weekly competitions auto-created
- Rankings updated after each trade
- 12 achievements to unlock
- Win rate tracking

### 10.3 AI Insights

**Components:**
- Portfolio analysis
- Chat interface
- Weekly digest

**AI Capabilities:**
- Portfolio health assessment
- Rebalancing recommendations
- Risk analysis
- Market sentiment interpretation

### 10.4 Subscription Tiers

| Feature | Free | Pro ($9.99/mo) | Pro+ ($19.99/mo) |
|---------|------|----------------|------------------|
| Holdings | 10 | 100 | Unlimited |
| Alerts | 1 | 25 | Unlimited |
| Lookups/day | 5 | 50 | Unlimited |
| AI questions | 3/day | 50/day | Unlimited |
| Competitions | 1 | Unlimited | Unlimited |
| Email alerts | No | Yes | Yes |
| Priority support | No | No | Yes |

---

## 11. Performance & Optimization

### 11.1 Caching Strategies

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_stock_quote(ticker: str) -> dict:
    # Cached for repeated requests within same session
    pass
```

### 11.2 Database Indexing

```sql
-- High-frequency queries
CREATE INDEX idx_holdings_user ON holdings(user_id);
CREATE INDEX idx_alerts_user_active ON price_alerts(user_id, is_active);
CREATE INDEX idx_vp_competition_rank ON virtual_portfolios(competition_id, current_rank);
```

### 11.3 Frontend Optimization

- **Lazy Loading:** Routes loaded on demand
- **OnPush Change Detection:** Where applicable
- **RxJS Operators:** `takeUntil` for subscription cleanup
- **Tree Shaking:** Unused code eliminated in production

---

## 12. Deployment Guide

### 12.1 Environment Variables

```bash
# Required
DATABASE_URL=postgresql://user:pass@host:5432/foliowise
SECRET_KEY=your-256-bit-secret-key

# Optional - Stripe
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_PRO_PRICE_ID=price_...
STRIPE_PRO_PLUS_PRICE_ID=price_...

# Optional - Email
RESEND_API_KEY=re_...

# Frontend
FRONTEND_URL=https://foliowise.app
```

### 12.2 Render Deployment

**File:** `render.yaml`

```yaml
services:
  - type: web
    name: foliowise-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: foliowise-db
          property: connectionString
      - key: SECRET_KEY
        generateValue: true

  - type: web
    name: foliowise-frontend
    env: static
    buildCommand: npm ci && npm run build
    staticPublishPath: dist/frontend/browser
```

### 12.3 Production Checklist

- [ ] Set `DEBUG=False`
- [ ] Configure proper SECRET_KEY (256-bit)
- [ ] Enable HTTPS
- [ ] Set up database backups
- [ ] Configure Stripe webhook endpoint
- [ ] Verify email delivery
- [ ] Set up monitoring/logging
- [ ] Configure CDN for static assets

---

## 13. Appendices

### 13.1 API Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Invalid/expired token |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource doesn't exist |
| 409 | Conflict - Duplicate resource |
| 422 | Validation Error - Pydantic validation failed |
| 429 | Rate Limited - Too many requests |
| 500 | Internal Error - Server error |

### 13.2 Complete File Inventory

**Backend (27 files):**
- `main.py`, `config.py`, `database.py`
- `models/`: 9 files (user, holding, transaction, alert, goal, watchlist, dividend, insight, competition)
- `routers/`: 14 files
- `services/`: 8 files
- `schemas/`: 1 file
- `requirements.txt`

**Frontend (35+ files):**
- `app.ts`, `app.routes.ts`, `app.config.ts`
- `services/`: 3 files
- `guards/`: 1 file
- `components/`: 22 directories with ~66 files (ts, html, css)
- `environments/`: 2 files
- Configuration files: 5+

### 13.3 Glossary

| Term | Definition |
|------|------------|
| **Holding** | A stock position owned by user |
| **Virtual Portfolio** | Paper trading portfolio in a competition |
| **Realized Gain** | Profit from sold positions |
| **Unrealized Gain** | Paper profit on open positions |
| **RSI** | Relative Strength Index (momentum indicator) |
| **EMA** | Exponential Moving Average |

---

## Document Information

| Field | Value |
|-------|-------|
| Version | 1.0.0 |
| Last Updated | April 9, 2026 |
| Author | Foliowise Engineering |
| Classification | Internal Documentation |
| Pages | ~100 (when rendered to PDF) |

---

*This document contains proprietary information. Distribution outside the organization requires authorization.*
