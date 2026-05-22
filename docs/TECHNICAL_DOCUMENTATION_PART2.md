# Foliowise Technical Documentation - Part 2

## 14. Complete API Examples

### 14.1 Authentication Flow Examples

#### Register New User

```bash
curl -X POST "https://api.foliowise.app/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "investor@example.com",
    "password": "SecurePass123!"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1NTBlODQwMC1lMjliLTQxZDQtYTcxNi00NDY2NTU0NDAwMDAiLCJleHAiOjE3MTI2Nzg0MDB9.abc123...",
  "token_type": "bearer"
}
```

#### Login Existing User

```bash
curl -X POST "https://api.foliowise.app/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=investor@example.com&password=SecurePass123!"
```

#### Get Current User

```bash
curl -X GET "https://api.foliowise.app/auth/me" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
```

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "investor@example.com",
  "is_active": true,
  "subscription_tier": "free",
  "subscription_status": "active",
  "referral_code": "INV-X7K9M2",
  "referral_count": 3,
  "created_at": "2026-01-15T10:30:00Z"
}
```

---

### 14.2 Holdings Management Examples

#### Create Holding

```bash
curl -X POST "https://api.foliowise.app/holdings/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "NVDA",
    "quantity": 25,
    "avg_cost_basis": 875.50
  }'
```

**Response:**
```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "ticker": "NVDA",
  "quantity": 25,
  "avg_cost_basis": 875.50,
  "realized_gains": 0.0,
  "created_at": "2026-04-09T14:30:00Z",
  "updated_at": null
}
```

#### List All Holdings

```bash
curl -X GET "https://api.foliowise.app/holdings/" \
  -H "Authorization: Bearer $TOKEN"
```

**Response:**
```json
[
  {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "ticker": "NVDA",
    "quantity": 25,
    "avg_cost_basis": 875.50,
    "realized_gains": 0.0,
    "created_at": "2026-04-09T14:30:00Z"
  },
  {
    "id": "b2c3d4e5-f6a7-8901-bcde-f23456789012",
    "ticker": "AAPL",
    "quantity": 50,
    "avg_cost_basis": 168.25,
    "realized_gains": 450.00,
    "created_at": "2026-03-01T09:00:00Z"
  }
]
```

#### Update Holding

```bash
curl -X PUT "https://api.foliowise.app/holdings/a1b2c3d4-e5f6-7890-abcd-ef1234567890" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "quantity": 30,
    "avg_cost_basis": 865.00
  }'
```

#### Import Holdings from CSV

```bash
curl -X POST "https://api.foliowise.app/holdings/import" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@holdings.csv"
```

**CSV Format:**
```csv
ticker,quantity,avg_cost_basis
AAPL,50,168.25
GOOGL,20,142.50
MSFT,35,415.00
AMZN,15,178.75
```

**Response:**
```json
{
  "imported": 4,
  "updated": 0,
  "skipped": 0,
  "errors": []
}
```

---

### 14.3 Portfolio Analytics Examples

#### Get Portfolio Summary

```bash
curl -X GET "https://api.foliowise.app/portfolio/summary" \
  -H "Authorization: Bearer $TOKEN"
```

**Response:**
```json
{
  "total_value": 87542.50,
  "total_cost": 75000.00,
  "total_profit_loss": 12542.50,
  "total_profit_loss_percent": 16.72,
  "day_change": 1234.50,
  "day_change_percent": 1.43,
  "holdings_count": 5,
  "holdings": [
    {
      "id": "...",
      "ticker": "NVDA",
      "name": "NVIDIA Corporation",
      "quantity": 25,
      "avg_cost_basis": 875.50,
      "current_price": 1125.00,
      "current_value": 28125.00,
      "total_cost": 21887.50,
      "profit_loss": 6237.50,
      "profit_loss_percent": 28.50,
      "day_change": 45.00,
      "day_change_percent": 4.17
    },
    {
      "id": "...",
      "ticker": "AAPL",
      "name": "Apple Inc.",
      "quantity": 50,
      "avg_cost_basis": 168.25,
      "current_price": 192.50,
      "current_value": 9625.00,
      "total_cost": 8412.50,
      "profit_loss": 1212.50,
      "profit_loss_percent": 14.41,
      "day_change": -2.30,
      "day_change_percent": -1.18
    }
  ]
}
```

#### Get Portfolio Performance

```bash
curl -X GET "https://api.foliowise.app/portfolio/performance?period=3mo" \
  -H "Authorization: Bearer $TOKEN"
```

**Response:**
```json
{
  "period": "3mo",
  "data": [
    {"date": "2026-01-09", "value": 72500.00},
    {"date": "2026-01-10", "value": 73125.00},
    {"date": "2026-01-11", "value": 72890.00},
    // ... 90 days of data
    {"date": "2026-04-09", "value": 87542.50}
  ],
  "total_cost": 75000.00,
  "start_value": 72500.00,
  "end_value": 87542.50,
  "total_return": 12542.50,
  "total_return_percent": 16.72,
  "period_return": 15042.50,
  "period_return_percent": 20.75
}
```

#### Get Gains Summary

```bash
curl -X GET "https://api.foliowise.app/portfolio/gains" \
  -H "Authorization: Bearer $TOKEN"
```

**Response:**
```json
{
  "unrealized_gains": 12092.50,
  "unrealized_gains_percent": 16.12,
  "realized_gains": 3450.00,
  "total_gains": 15542.50,
  "holdings": [
    {
      "ticker": "NVDA",
      "name": "NVIDIA Corporation",
      "unrealized": 6237.50,
      "realized": 0.00,
      "cost_basis": 21887.50,
      "current_value": 28125.00
    },
    {
      "ticker": "AAPL",
      "name": "Apple Inc.",
      "unrealized": 1212.50,
      "realized": 450.00,
      "cost_basis": 8412.50,
      "current_value": 9625.00
    }
  ]
}
```

---

### 14.4 Market Data Examples

#### Get Stock Quote

```bash
curl -X GET "https://api.foliowise.app/market/quote/TSLA"
```

**Response:**
```json
{
  "ticker": "TSLA",
  "name": "Tesla, Inc.",
  "current_price": 245.80,
  "previous_close": 242.50,
  "day_change": 3.30,
  "day_change_percent": 1.36,
  "day_high": 248.90,
  "day_low": 241.20,
  "volume": 45678234,
  "market_cap": 782500000000,
  "fifty_two_week_high": 299.29,
  "fifty_two_week_low": 138.80
}
```

#### Get Historical Data

```bash
curl -X GET "https://api.foliowise.app/market/history/TSLA?period=1mo"
```

**Response:**
```json
[
  {
    "date": "2026-03-09",
    "open": 235.50,
    "high": 238.90,
    "low": 233.20,
    "close": 237.80,
    "volume": 42345678
  },
  // ... 30 days of OHLCV data
]
```

#### Search Stocks

```bash
curl -X GET "https://api.foliowise.app/market/search?q=tesla&limit=5"
```

**Response:**
```json
{
  "results": [
    {"symbol": "TSLA", "name": "Tesla, Inc.", "exchange": "NASDAQ", "type": "Equity"},
    {"symbol": "TSLL", "name": "Direxion Daily TSLA Bull 2X", "exchange": "NYSE", "type": "ETF"},
    {"symbol": "TSLS", "name": "Direxion Daily TSLA Bear 1X", "exchange": "NYSE", "type": "ETF"}
  ]
}
```

#### Get Price Prediction

```bash
curl -X GET "https://api.foliowise.app/market/predict/AAPL?days=14"
```

**Response:**
```json
{
  "ticker": "AAPL",
  "current_price": 192.50,
  "predictions": [
    {"date": "2026-04-10", "predicted_price": 193.20, "upper_bound": 195.50, "lower_bound": 190.90},
    {"date": "2026-04-11", "predicted_price": 193.85, "upper_bound": 196.80, "lower_bound": 190.90},
    {"date": "2026-04-12", "predicted_price": 194.10, "upper_bound": 197.50, "lower_bound": 190.70},
    // ... 14 days
    {"date": "2026-04-23", "predicted_price": 198.45, "upper_bound": 206.20, "lower_bound": 190.70}
  ],
  "summary": {
    "days_ahead": 14,
    "final_predicted_price": 198.45,
    "predicted_change": 5.95,
    "predicted_change_percent": 3.09,
    "confidence_score": 78.5,
    "volatility": 15.2,
    "rsi": 52.8,
    "trend_direction": "bullish"
  },
  "disclaimer": "Predictions are for educational purposes only. Past performance does not guarantee future results. Always do your own research before making investment decisions."
}
```

---

### 14.5 Trading Arena Examples

#### List Competitions

```bash
curl -X GET "https://api.foliowise.app/competitions/?status=active" \
  -H "Authorization: Bearer $TOKEN"
```

**Response:**
```json
[
  {
    "id": "comp-uuid-001",
    "name": "Weekly Challenge - Week 15",
    "description": "Compete with other traders to achieve the highest returns this week.",
    "type": "weekly",
    "status": "active",
    "starting_balance": 100000.0,
    "max_participants": null,
    "entry_fee": 0.0,
    "prize_description": "Top 3 get featured on the leaderboard + exclusive badges",
    "start_date": "2026-04-07T00:00:00Z",
    "end_date": "2026-04-14T00:00:00Z",
    "participant_count": 127,
    "user_joined": true,
    "user_rank": 15
  }
]
```

#### Join Competition

```bash
curl -X POST "https://api.foliowise.app/competitions/comp-uuid-001/join" \
  -H "Authorization: Bearer $TOKEN"
```

**Response:**
```json
{
  "id": "portfolio-uuid-001",
  "competition_id": "comp-uuid-001",
  "cash_balance": 100000.0,
  "total_value": 100000.0,
  "total_return": 0.0,
  "total_return_percent": 0.0,
  "current_rank": 128,
  "trades_count": 0,
  "winning_trades": 0,
  "losing_trades": 0,
  "holdings": []
}
```

#### Execute Virtual Trade

```bash
curl -X POST "https://api.foliowise.app/competitions/comp-uuid-001/trade" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "META",
    "type": "BUY",
    "quantity": 50
  }'
```

**Response:**
```json
{
  "trade": {
    "id": "trade-uuid-001",
    "ticker": "META",
    "type": "BUY",
    "quantity": 50,
    "price": 485.25,
    "total_value": 24262.50,
    "realized_pl": null,
    "executed_at": "2026-04-09T15:30:00Z"
  },
  "portfolio": {
    "id": "portfolio-uuid-001",
    "competition_id": "comp-uuid-001",
    "cash_balance": 75737.50,
    "total_value": 100000.00,
    "total_return": 0.0,
    "total_return_percent": 0.0,
    "current_rank": 98,
    "trades_count": 1,
    "winning_trades": 0,
    "losing_trades": 0,
    "holdings": [
      {
        "id": "holding-uuid-001",
        "ticker": "META",
        "quantity": 50,
        "avg_cost": 485.25,
        "current_price": 485.25,
        "current_value": 24262.50,
        "profit_loss": 0.0,
        "profit_loss_percent": 0.0
      }
    ]
  }
}
```

#### Sell Position

```bash
curl -X POST "https://api.foliowise.app/competitions/comp-uuid-001/trade" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "META",
    "type": "SELL",
    "quantity": 25
  }'
```

**Response:**
```json
{
  "trade": {
    "id": "trade-uuid-002",
    "ticker": "META",
    "type": "SELL",
    "quantity": 25,
    "price": 492.50,
    "total_value": 12312.50,
    "realized_pl": 181.25,
    "executed_at": "2026-04-09T16:45:00Z"
  },
  "portfolio": {
    "id": "portfolio-uuid-001",
    "cash_balance": 88050.00,
    "total_value": 100181.25,
    "total_return": 181.25,
    "total_return_percent": 0.18,
    "current_rank": 72,
    "trades_count": 2,
    "winning_trades": 1,
    "losing_trades": 0,
    "holdings": [
      {
        "ticker": "META",
        "quantity": 25,
        "avg_cost": 485.25,
        "current_price": 492.50,
        "current_value": 12312.50,
        "profit_loss": 181.25,
        "profit_loss_percent": 1.49
      }
    ]
  }
}
```

#### Get Leaderboard

```bash
curl -X GET "https://api.foliowise.app/competitions/comp-uuid-001/leaderboard?limit=10" \
  -H "Authorization: Bearer $TOKEN"
```

**Response:**
```json
[
  {
    "rank": 1,
    "user_id": "user-001",
    "username": "TradingPro",
    "total_value": 128450.00,
    "total_return": 28450.00,
    "total_return_percent": 28.45,
    "trades_count": 47,
    "is_current_user": false
  },
  {
    "rank": 2,
    "user_id": "user-002",
    "username": "MarketMaster",
    "total_value": 122180.00,
    "total_return": 22180.00,
    "total_return_percent": 22.18,
    "trades_count": 38,
    "is_current_user": false
  },
  // ... top 10
]
```

#### Get Achievements

```bash
curl -X GET "https://api.foliowise.app/competitions/achievements/me" \
  -H "Authorization: Bearer $TOKEN"
```

**Response:**
```json
[
  {
    "code": "first_trade",
    "name": "First Steps",
    "description": "Make your first virtual trade",
    "icon": "🚀",
    "type": "trading",
    "progress": 1,
    "target": 1,
    "unlocked": true,
    "unlocked_at": "2026-04-09T15:30:00Z"
  },
  {
    "code": "first_profit",
    "name": "In The Green",
    "description": "Close your first profitable trade",
    "icon": "💚",
    "type": "trading",
    "progress": 1,
    "target": 1,
    "unlocked": true,
    "unlocked_at": "2026-04-09T16:45:00Z"
  },
  {
    "code": "trader_10",
    "name": "Active Trader",
    "description": "Complete 10 trades",
    "icon": "📈",
    "type": "trading",
    "progress": 2,
    "target": 10,
    "unlocked": false,
    "unlocked_at": null
  },
  // ... all 12 achievements
]
```

---

### 14.6 Price Alerts Examples

#### Create Alert

```bash
curl -X POST "https://api.foliowise.app/alerts/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "GOOGL",
    "condition": "ABOVE",
    "target_price": 155.00
  }'
```

**Response:**
```json
{
  "id": "alert-uuid-001",
  "ticker": "GOOGL",
  "condition": "ABOVE",
  "target_price": 155.00,
  "is_active": true,
  "is_triggered": false,
  "triggered_at": null,
  "triggered_price": null,
  "created_at": "2026-04-09T10:00:00Z",
  "current_price": 148.75,
  "stock_name": "Alphabet Inc."
}
```

#### Check Alerts

```bash
curl -X GET "https://api.foliowise.app/alerts/check" \
  -H "Authorization: Bearer $TOKEN"
```

**Response:**
```json
{
  "triggered_alerts": [
    {
      "id": "alert-uuid-002",
      "ticker": "MSFT",
      "condition": "BELOW",
      "target_price": 420.00,
      "is_triggered": true,
      "triggered_at": "2026-04-09T14:30:00Z",
      "triggered_price": 418.50,
      "current_price": 418.50,
      "stock_name": "Microsoft Corporation"
    }
  ],
  "total_checked": 3
}
```

---

### 14.7 Subscription Examples

#### Get Subscription Status

```bash
curl -X GET "https://api.foliowise.app/subscriptions/status" \
  -H "Authorization: Bearer $TOKEN"
```

**Response:**
```json
{
  "tier": "pro",
  "status": "active",
  "ends_at": "2026-05-09T00:00:00Z",
  "stripe_customer_id": "cus_abc123...",
  "referral_code": "INV-X7K9M2",
  "referral_count": 3
}
```

#### Create Checkout Session

```bash
curl -X POST "https://api.foliowise.app/subscriptions/checkout?plan=pro" \
  -H "Authorization: Bearer $TOKEN"
```

**Response:**
```json
{
  "checkout_url": "https://checkout.stripe.com/c/pay/cs_live_...",
  "session_id": "cs_live_abc123..."
}
```

#### Get Usage

```bash
curl -X GET "https://api.foliowise.app/subscriptions/usage" \
  -H "Authorization: Bearer $TOKEN"
```

**Response:**
```json
{
  "tier": "free",
  "holdings": {"used": 7, "limit": 10},
  "alerts": {"used": 1, "limit": 1},
  "lookups_per_day": {"used": 3, "limit": 5},
  "ai_questions_per_day": {"used": 1, "limit": 3}
}
```

---

## 15. Troubleshooting Guide

### 15.1 Common Errors

#### 401 Unauthorized

**Symptom:** API returns 401 error

**Causes:**
1. JWT token expired (30 min lifetime)
2. Invalid token format
3. Token not included in request

**Solutions:**
```bash
# Check if token is expired
# Decode JWT at jwt.io and check "exp" claim

# Re-authenticate
curl -X POST "https://api.foliowise.app/auth/login" \
  -d "username=email&password=pass"
```

#### 422 Validation Error

**Symptom:** API returns validation error

**Example Response:**
```json
{
  "detail": [
    {
      "loc": ["body", "quantity"],
      "msg": "ensure this value is greater than 0",
      "type": "value_error.number.not_gt"
    }
  ]
}
```

**Solution:** Check request body matches schema requirements

#### 500 Internal Server Error

**Symptom:** API returns 500 error

**Common Causes:**
1. Database connection issue
2. External API failure (Yahoo Finance)
3. Missing environment variables

**Debug Steps:**
```bash
# Check backend logs
tail -f /var/log/foliowise/app.log

# Verify database connection
psql $DATABASE_URL -c "SELECT 1"

# Test Yahoo Finance
python -c "import yfinance; print(yfinance.Ticker('AAPL').info)"
```

### 15.2 Performance Issues

#### Slow Portfolio Summary

**Cause:** Multiple Yahoo Finance API calls

**Solution:**
- Implement caching (already using `@lru_cache`)
- Batch quote requests
- Use background refresh

#### High Memory Usage

**Cause:** Large dataframes in memory

**Solution:**
```python
# Use generators instead of loading all data
def get_history_chunked(ticker, period):
    for chunk in pd.read_sql_query(..., chunksize=1000):
        yield chunk
```

### 15.3 Frontend Issues

#### CORS Errors

**Symptom:** Browser console shows CORS error

**Solution:** Verify backend CORS middleware is configured:
```python
@app.middleware("http")
async def add_cors_headers(request, call_next):
    response.headers["Access-Control-Allow-Origin"] = "*"
    # ...
```

#### Chart Not Rendering

**Cause:** Data format mismatch

**Debug:**
```typescript
console.log('Chart data:', this.performanceChart);
// Verify data structure matches Chart.js requirements
```

### 15.4 Database Issues

#### Migration Failures

**Symptom:** Column doesn't exist

**Solution:**
```sql
-- Manually add missing column
ALTER TABLE holdings ADD COLUMN IF NOT EXISTS realized_gains FLOAT DEFAULT 0.0;
```

#### Connection Pool Exhaustion

**Symptom:** "Too many connections"

**Solution:**
```python
# Ensure sessions are closed
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # Critical!
```

---

## 16. Testing Documentation

### 16.1 Backend Testing

#### Unit Tests

```python
# tests/test_auth.py
import pytest
from app.services.auth import hash_password, verify_password

def test_password_hashing():
    password = "SecurePass123!"
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrong", hashed)

def test_jwt_creation():
    from app.services.auth import create_access_token, decode_access_token

    token = create_access_token({"sub": "user-123"})
    payload = decode_access_token(token)

    assert payload["sub"] == "user-123"
```

#### Integration Tests

```python
# tests/test_api.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_register_user():
    response = client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "TestPass123!"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
```

#### Running Tests

```bash
# Backend
cd backend
pytest tests/ -v --cov=app --cov-report=html

# View coverage report
open htmlcov/index.html
```

### 16.2 Frontend Testing

#### Component Tests

```typescript
// arena.spec.ts
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ArenaComponent } from './arena';
import { ApiService } from '../../services/api';

describe('ArenaComponent', () => {
  let component: ArenaComponent;
  let fixture: ComponentFixture<ArenaComponent>;
  let apiService: jasmine.SpyObj<ApiService>;

  beforeEach(async () => {
    const spy = jasmine.createSpyObj('ApiService', ['getCompetitions']);

    await TestBed.configureTestingModule({
      imports: [ArenaComponent],
      providers: [{ provide: ApiService, useValue: spy }]
    }).compileComponents();

    apiService = TestBed.inject(ApiService) as jasmine.SpyObj<ApiService>;
    fixture = TestBed.createComponent(ArenaComponent);
    component = fixture.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should load competitions on init', () => {
    apiService.getCompetitions.and.returnValue(of([]));
    fixture.detectChanges();
    expect(apiService.getCompetitions).toHaveBeenCalled();
  });
});
```

#### E2E Tests

```typescript
// e2e/arena.e2e.ts
describe('Trading Arena', () => {
  beforeEach(() => {
    cy.login('test@example.com', 'password');
    cy.visit('/arena');
  });

  it('should display competitions', () => {
    cy.get('.competition-card').should('have.length.greaterThan', 0);
  });

  it('should join competition', () => {
    cy.get('.join-btn').first().click();
    cy.get('.toast-success').should('contain', 'Joined');
  });

  it('should execute trade', () => {
    cy.get('.trade-btn.buy').click();
    cy.get('input[name="ticker"]').type('AAPL');
    cy.get('input[name="quantity"]').type('10');
    cy.get('.execute-btn').click();
    cy.get('.toast-success').should('contain', 'executed');
  });
});
```

---

## 17. Monitoring & Observability

### 17.1 Logging Configuration

```python
# app/logging_config.py
import logging
import sys

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('app.log')
        ]
    )

    # Reduce noise from libraries
    logging.getLogger('yfinance').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
```

### 17.2 Key Metrics to Monitor

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| Response Time P99 | 99th percentile latency | > 2s |
| Error Rate | 5xx errors / total requests | > 1% |
| Active Users | Concurrent authenticated users | > 1000 |
| DB Connections | Active PostgreSQL connections | > 80% pool |
| Memory Usage | Application memory | > 90% |
| Yahoo Finance Calls | External API calls/minute | > 100/min |

### 17.3 Health Checks

```python
@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/health/detailed")
def detailed_health(db: Session = Depends(get_db)):
    checks = {
        "database": check_db(db),
        "yahoo_finance": check_yfinance(),
        "stripe": check_stripe(),
    }

    all_healthy = all(c["healthy"] for c in checks.values())

    return {
        "status": "healthy" if all_healthy else "degraded",
        "checks": checks,
        "timestamp": datetime.utcnow().isoformat()
    }
```

---

## 18. Security Checklist

### 18.1 Pre-Production Checklist

- [ ] **Authentication**
  - [ ] JWT secret is 256-bit cryptographically random
  - [ ] Passwords hashed with bcrypt (cost >= 12)
  - [ ] Token expiration set appropriately (30 min)
  - [ ] Refresh token mechanism implemented

- [ ] **API Security**
  - [ ] HTTPS enforced in production
  - [ ] CORS configured properly (not `*` in prod)
  - [ ] Rate limiting enabled
  - [ ] Input validation on all endpoints
  - [ ] SQL injection protection (ORM parameterized queries)

- [ ] **Data Protection**
  - [ ] Database encrypted at rest
  - [ ] Sensitive data not logged
  - [ ] PII handled according to privacy policy
  - [ ] Database backups encrypted

- [ ] **Third-Party**
  - [ ] Stripe webhook signatures verified
  - [ ] API keys stored as environment variables
  - [ ] Dependencies scanned for vulnerabilities

### 18.2 Security Headers

```python
# Recommended headers for production
@app.middleware("http")
async def security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000"
    return response
```

---

## 19. Changelog

### Version 1.0.0 (April 2026)

**Features:**
- Portfolio tracking with real-time market data
- Holdings, transactions, dividends management
- Price alerts with email notifications
- AI-powered portfolio insights and chat
- Weekly digest generation
- Stock watchlist and comparison
- Virtual trading competitions with achievements
- Subscription tiers (Free, Pro, Pro+)
- Referral program
- CSV import/export
- Stock price predictions

**Technical:**
- FastAPI backend with 14 routers
- Angular 21 frontend with 22 components
- PostgreSQL database with 15 tables
- Stripe integration for payments
- Resend integration for emails
- Yahoo Finance for market data
- TextBlob for sentiment analysis

---

*End of Technical Documentation Part 2*
