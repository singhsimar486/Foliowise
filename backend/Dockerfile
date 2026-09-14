# Foliowise API
#
# python:3.11-slim is used rather than the full image to keep the layer small,
# and rather than alpine because psycopg2 and numpy ship manylinux wheels for
# glibc. On alpine both would be compiled from source at build time.
FROM python:3.11-slim

# Keeps the image smaller and the logs unbuffered so container logs appear in
# real time rather than being held in Python's stdout buffer.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# libpq5 is the runtime library psycopg2-binary links against. build-essential
# is not needed because every dependency here has a prebuilt wheel.
RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq5 curl \
    && rm -rf /var/lib/apt/lists/*

# Requirements are copied and installed before the application code so that
# editing a router does not invalidate the cached dependency layer.
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY app ./app

# Run as a non-root user. If the container is ever compromised, the process
# does not have root inside it.
RUN useradd --create-home --uid 1000 appuser \
    && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Hitting the same endpoint Render uses for its own health checks.
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD curl --fail http://localhost:8000/health || exit 1

# $PORT is honoured so the same image runs unchanged on a platform that assigns
# the port at runtime; it falls back to 8000 locally.
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
