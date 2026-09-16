# Adding tests, Docker and CI to Foliowise

Everything in this drop was written against the code as it stands on `main` and
was run before being handed over. The backend suite passes against a real
PostgreSQL 16 instance and the frontend suite passes under Vitest.

## What is in the drop

| Path | What it is |
|---|---|
| `backend/tests/conftest.py` | Fixtures: schema creation, table truncation between tests, TestClient, register/login helpers |
| `backend/tests/test_auth.py` | 16 tests over password hashing, registration, login and JWT validation |
| `backend/tests/test_holdings.py` | 11 tests over holdings CRUD, tenant isolation and the free tier limit |
| `backend/tests/test_health.py` | 4 tests over `/`, `/health`, the OpenAPI schema and CORS preflight |
| `backend/pytest.ini` | pytest configuration |
| `backend/requirements-dev.txt` | Test-only dependencies, kept out of the production image |
| `backend/Dockerfile` | Production image for the API |
| `backend/.dockerignore` | Keeps the venv, tests and `.env` out of the build context |
| `docker-compose.yml` | Postgres plus the API for local development |
| `scripts/create-test-db.sh` | Creates `foliowise_test` when the Postgres volume is first initialised |
| `.github/workflows/ci.yml` | Three jobs: backend tests, Docker build and smoke test, frontend tests and build |
| `frontend/src/app/services/toast.spec.ts` | 9 tests over the notification queue |
| `frontend/src/app/services/auth.spec.ts` | 10 tests over token storage, login, logout and headers |
| `frontend/src/app/services/api.spec.ts` | 7 tests over request URLs, payloads and auth headers |

## Files that were deleted, and why

`npm test` did not run before this change. The Angular CLI scaffold specs
imported class names that no longer exist, for example `Api` from
`services/api.ts` where the exported class is `ApiService`, so the build failed
at type check. Every one of them asserted only `expect(service).toBeTruthy()`.

Deleted:

```
src/app/app.spec.ts
src/app/services/api.spec.ts          (replaced with real tests)
src/app/services/auth.spec.ts         (replaced with real tests)
src/app/components/dashboard/dashboard.spec.ts
src/app/components/holdings/holdings.spec.ts
src/app/components/login/login.spec.ts
src/app/components/navbar/navbar.spec.ts
src/app/components/register/register.spec.ts
src/app/components/sentiment/sentiment.spec.ts
```

## Running it

Backend, with Docker:

```bash
docker compose up -d db
cd backend
pip install -r requirements-dev.txt
DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:5432/foliowise_test \
SECRET_KEY=test-secret \
pytest
```

Backend, with a local Postgres instead of Docker: create a database whose name
contains `test` and point `DATABASE_URL` at it. The suite refuses to run
otherwise, because it truncates every table between tests.

Frontend:

```bash
cd frontend
npm ci
npm test
npm run build
```

Docker image:

```bash
docker build -t foliowise-api backend/
docker run --rm -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@host:5432/db \
  -e SECRET_KEY=something \
  foliowise-api
curl http://localhost:8000/health
```

## Expected results

```
backend    31 passed
frontend   26 passed  (3 files)
```

## One thing still to verify yourself

The Docker image could not be built in the environment these files were written
in, because Docker Hub was unreachable from it. The Dockerfile is standard and
the CI job builds it, but **build it locally once before relying on it**:

```bash
docker build -t foliowise-api backend/
```

## Two notes on the build

`npm run build` inlines Google Fonts at build time, so the production build
needs network access to `fonts.googleapis.com`. GitHub Actions has it. If that
ever becomes a problem, setting `optimization.fonts.inline` to `false` in the
production configuration in `angular.json` makes the build offline-safe at the
cost of an extra request at page load.

`passlib` prints a trapped `error reading bcrypt version` warning on startup
with bcrypt 4.x. It is cosmetic, hashing works correctly, and
`requirements.txt` already pins `bcrypt<5.0.0`.
