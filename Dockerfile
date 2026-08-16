# Build stage
FROM python:3.11-slim as builder

WORKDIR /tmp

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    HF_HUB_DISABLE_TELEMETRY=1 \
    TRANSFORMERS_CACHE=/dev/null \
    HF_HOME=/dev/null \
    SENTENCE_TRANSFORMERS_HOME=/dev/null

COPY requirements.txt ./

# Install build dependencies, install Python packages, clean up aggressively
RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
    && pip install --user --no-cache-dir -r python-multipart \
    && pip install --user --no-cache-dir -r requirements.txt \
    && apt-get remove -y build-essential \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && find /root/.local -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true \
    && find /root/.local -name "*.pyc" -delete

# Runtime stage
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PORT=8000 \
    HF_HUB_DISABLE_TELEMETRY=1

# Copy only installed packages (no build tools)
COPY --from=builder /root/.local /root/.local

ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
