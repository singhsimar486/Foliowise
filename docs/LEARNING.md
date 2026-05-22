# Foliowise Learning Journal

This document tracks what I learned while building Foliowise from scratch.

---

## Day 1: Project Setup

### What We Did
1. Created project folder structure
2. Initialized Git repository
3. Set up Python virtual environment
4. Installed core dependencies (FastAPI, SQLAlchemy, etc.)
5. Created requirements.txt to lock dependencies

### Concepts Learned

**Git**
- Git is a version control system that tracks changes locally
- GitHub hosts repositories online for sharing and backup
- `git init` creates a new repository

**Virtual Environments**
- Isolate project dependencies from global Python
- Created with `python3 -m venv venv`
- Activated with `source venv/bin/activate`
- `(venv)` in terminal prompt confirms it's active

**Dependencies Installed**
| Package | Purpose |
|---------|---------|
| fastapi | Web framework for building APIs |
| uvicorn | Server to run the FastAPI app |
| sqlalchemy | ORM for database interactions |
| psycopg2-binary | PostgreSQL driver for Python |
| python-dotenv | Load environment variables from .env files |

**Key Terminal Commands**
- `cd` - change directory
- `mkdir` - make directory
- `ls` - list files
- `pwd` - print working directory
- `source` - run a script in current session
- `which python` - show path to active Python
- `pip freeze > requirements.txt` - save dependencies to file

### What's Next
- Create first FastAPI endpoint
- Run the development server
- Set up project file structure

---

## Day 1 (Continued): Database & Authentication Setup

### What We Did
1. Installed PostgreSQL using Homebrew
2. Created the foliowise database
3. Created database models (User, Holding, Transaction)
4. Generated real tables from Python models
5. Started building authentication system

### Concepts Learned

**Database Models vs Schemas**
| Models | Schemas |
|--------|---------|
| Define database tables | Define API request/response format |
| SQLAlchemy | Pydantic |
| How data is stored | How data is transferred |

**Relationships in SQLAlchemy**
- `ForeignKey` creates the actual database link (like storing a phone number)
- `relationship()` creates Python convenience access (like having the contact saved)
- `back_populates` connects both sides so they stay in sync

**Password Security**
- Never store plain passwords
- Use bcrypt to hash passwords (slow on purpose to prevent brute-force)
- Same password produces different hashes each time (salting)

**JWT Authentication Flow**
1. User sends email + password
2. Server verifies credentials
3. Server creates signed JWT token with expiration
4. User sends token with every future request
5. Server verifies token to identify user

**Key Terminal Commands Learned**
- `brew install` — Install packages via Homebrew
- `createdb` — Create a PostgreSQL database
- `psql` — Connect to PostgreSQL
- `\dt` — List tables in database
- `\d tablename` — Show table structure
- `\q` — Exit psql

### Dependencies Added
| Package | Purpose |
|---------|---------|
| python-jose | Create and verify JWT tokens |
| passlib | Secure password hashing with bcrypt |
| email-validator | Validate email format in schemas |

### What's Next
- Create auth router (register/login endpoints)
- Test authentication flow
- Build holdings endpoints

---

## Tech Stack Decision: Angular Frontend

### Why Angular
- Industry demand for Angular skills
- Enterprise-grade frontend framework
- Strong TypeScript integration
- Component-based architecture similar to React

### What We'll Learn
- TypeScript fundamentals
- Angular components and modules
- Services and dependency injection
- RxJS and Observables
- Angular Material for UI components
- Connecting Angular to our FastAPI backend

### Updated Tech Stack
| Layer | Technology |
|-------|------------|
| Backend | Python, FastAPI, SQLAlchemy |
| Database | PostgreSQL |
| Frontend | Angular, TypeScript, Angular Material |
| AI/ML | FinBERT (sentiment), Claude API (insights) |

---

## Day 1 (Continued): Market Data & Portfolio Features

### What We Did
1. Installed yfinance for real-time market data
2. Created market data service with three functions
3. Built market data API endpoints
4. Created portfolio summary endpoint
5. Created portfolio allocation endpoint

### Concepts Learned

**Third-Party API Integration**
- yfinance library pulls data from Yahoo Finance
- No API key needed (free, but rate-limited)
- Wrapped in try/except for error handling
- Returns None for invalid tickers (graceful failure)

**Data Transformation**
- Raw market data → cleaned, structured response
- Combined database data (holdings) with live data (prices)
- Calculated derived values (profit/loss, percentages)

**Portfolio Calculations**
```
current_value = quantity × current_price
total_cost = quantity × avg_cost_basis
profit_loss = current_value - total_cost
profit_loss_percent = (profit_loss / total_cost) × 100
day_change = quantity × price_change_today
```

**Public vs Protected Endpoints**
| Endpoint | Auth Required | Why |
|----------|---------------|-----|
| /market/quote/{ticker} | No | Public data, not user-specific |
| /portfolio/summary | Yes | User's personal holdings |

**Batch Operations for Efficiency**
- Instead of fetching one stock at a time
- Collect all tickers, fetch in batch
- Reduces API calls and improves speed

### New Files Created
```
app/services/market_data.py — Market data fetching logic
app/routers/market.py — Public market data endpoints
app/routers/portfolio.py — Portfolio analytics endpoints
app/schemas/market.py — Market data schemas
```

### Dependencies Added
| Package | Purpose |
|---------|---------|
| yfinance | Fetch real-time stock data from Yahoo Finance |

### API Endpoints Built
| Endpoint | Method | Purpose |
|----------|--------|---------|
| /market/quote/{ticker} | GET | Real-time stock quote |
| /market/history/{ticker} | GET | Historical prices for charts |
| /portfolio/summary | GET | Complete portfolio with live values |
| /portfolio/allocation | GET | Percentage breakdown for pie chart |

### Key Takeaways
1. Always handle external API failures gracefully
2. Combine data sources (database + external API) for rich responses
3. Calculate derived values on the backend, not frontend
4. Public data doesn't need authentication

### What's Next
- News aggregation with sentiment analysis
- AI-powered portfolio insights using Claude
- Angular frontend with charts and visualizations