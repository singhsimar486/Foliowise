import os
from fastapi import FastAPI, Request
from starlette.responses import Response
from contextlib import asynccontextmanager

from app.routers import auth, holdings, market, portfolio, news, watchlist, alerts, insights, goals, dividends, settings, compare, transactions, subscriptions, competitions, recurring, allocation
from app.database import engine, Base
from app import models  # Import all models to register them


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create all database tables on startup
    # Wrapped in try/except so the app can start even without a database
    # (useful for health checks in CI/CD pipelines)
    try:
        Base.metadata.create_all(bind=engine)

        # Add realized_gains column if it doesn't exist (migration)
        from sqlalchemy import text, inspect
        inspector = inspect(engine)
        columns = [col['name'] for col in inspector.get_columns('holdings')]
        if 'realized_gains' not in columns:
            with engine.connect() as conn:
                conn.execute(text('ALTER TABLE holdings ADD COLUMN realized_gains FLOAT DEFAULT 0.0'))
                conn.commit()

        # Add subscription columns to users table (migration)
        user_columns = [col['name'] for col in inspector.get_columns('users')]
        migrations = []
        if 'subscription_tier' not in user_columns:
            migrations.append("ALTER TABLE users ADD COLUMN subscription_tier VARCHAR(20) DEFAULT 'free'")
        if 'stripe_customer_id' not in user_columns:
            migrations.append("ALTER TABLE users ADD COLUMN stripe_customer_id VARCHAR(255)")
        if 'stripe_subscription_id' not in user_columns:
            migrations.append("ALTER TABLE users ADD COLUMN stripe_subscription_id VARCHAR(255)")
        if 'subscription_status' not in user_columns:
            migrations.append("ALTER TABLE users ADD COLUMN subscription_status VARCHAR(20) DEFAULT 'active'")
        if 'subscription_ends_at' not in user_columns:
            migrations.append("ALTER TABLE users ADD COLUMN subscription_ends_at TIMESTAMP")
        if 'referral_code' not in user_columns:
            migrations.append("ALTER TABLE users ADD COLUMN referral_code VARCHAR(20) UNIQUE")
        if 'referred_by' not in user_columns:
            migrations.append("ALTER TABLE users ADD COLUMN referred_by VARCHAR(36)")
        if 'referral_count' not in user_columns:
            migrations.append("ALTER TABLE users ADD COLUMN referral_count INTEGER DEFAULT 0")

        if migrations:
            with engine.connect() as conn:
                for migration in migrations:
                    try:
                        conn.execute(text(migration))
                    except Exception:
                        pass  # Column might already exist
                conn.commit()
    except Exception as e:
        import logging
        logging.warning(f"Database not available on startup: {e}")

    yield


app = FastAPI(
    lifespan=lifespan,
    title="Foliowise API",
    description="An intelligent portfolio tracker with AI-powered insights",
    version="0.1.0"
)


@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    # Handle preflight OPTIONS request
    if request.method == "OPTIONS":
        response = Response(status_code=200)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
        response.headers["Access-Control-Allow-Headers"] = "*"
        response.headers["Access-Control-Max-Age"] = "86400"
        return response

    try:
        response = await call_next(request)
    except Exception as e:
        response = Response(content=str(e), status_code=500)

    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Max-Age"] = "86400"
    return response


app.include_router(auth.router)
app.include_router(holdings.router)
app.include_router(market.router)
app.include_router(portfolio.router)
app.include_router(news.router)
app.include_router(watchlist.router)
app.include_router(alerts.router)
app.include_router(insights.router)
app.include_router(goals.router)
app.include_router(dividends.router)
app.include_router(settings.router)
app.include_router(compare.router)
app.include_router(transactions.router)
app.include_router(subscriptions.router)
app.include_router(competitions.router)
app.include_router(recurring.router)
app.include_router(allocation.router)


@app.get("/")
def root():
    return {"message": "Welcome to Foliowise API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
