# Base hardened Python runtime
FROM python:3.12-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5001

WORKDIR /app

# Install security updates and dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create non-root application user for container runtime security
RUN groupadd -r appgroup && useradd -r -g appgroup -s /sbin/nologin appuser

# Copy application source code
COPY app/ ./app/

# Set ownership to non-root user
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

EXPOSE 5001

CMD ["python", "app/app.py"]
