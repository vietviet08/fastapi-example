# Ultra-optimized FastAPI backend
FROM python:3.11-alpine AS builder

# Install build dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-dev \
    python3-dev \
    libffi-dev \
    openssl-dev

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements-prod.txt .

# Install dependencies to local user directory
RUN pip install --no-cache-dir --user -r requirements-prod.txt

# Remove unnecessary files to reduce size
RUN find /root/.local \( -type d -a -name test -o -name tests \) -exec rm -rf '{}' + || true && \
    find /root/.local \( -type f -a -name '*.pyc' -o -name '*.pyo' \) -delete && \
    find /root/.local -name "*.dist-info" -exec rm -rf {} + || true

# Production stage
FROM python:3.11-alpine AS production

# Install only essential runtime dependencies
RUN apk add --no-cache libpq && \
    rm -rf /var/cache/apk/*

# Create non-root user
RUN addgroup -g 1001 -S appgroup && \
    adduser -S appuser -u 1001 -G appgroup

# Set working directory
WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /root/.local /home/appuser/.local

# Copy only necessary application files
COPY --chown=appuser:appgroup main.py .
COPY --chown=appuser:appgroup app/ ./app/
COPY --chown=appuser:appgroup alembic.ini .
COPY --chown=appuser:appgroup alembic/ ./alembic/

# Switch to non-root user
USER appuser

# Set environment variables for optimization
ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Run the application
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
