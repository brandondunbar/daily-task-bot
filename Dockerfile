# syntax=docker/dockerfile:1.7
FROM python:3.12-slim AS base

# System deps (add OS packages your bot needs)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates \
  && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 10001 appuser

# Set workdir
WORKDIR /app

# Install Python deps (cache layer)
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy code
COPY src ./src
COPY entrypoint.sh ./
COPY config.yaml ./
COPY secrets/service_account.json ./
COPY templates/leetcode_template.j2 ./templates/
COPY templates/math_template.j2 ./templates/
RUN chmod +x entrypoint.sh

# Environment
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=America/New_York

# Switch to non-root
USER appuser

# Healthcheck (tweak to your app’s quick check)
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
  CMD python -c "import sys; sys.exit(0)"

# Default command; override with `docker run ...`
ENTRYPOINT ["./entrypoint.sh"]
CMD ["python", "-m", "src"]
