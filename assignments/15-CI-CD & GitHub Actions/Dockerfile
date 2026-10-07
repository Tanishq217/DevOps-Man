# Base image with official slim Python runtime
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install runtime dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code and tests
COPY app/ ./app/
COPY tests/ ./tests/

# Default container entrypoint
ENTRYPOINT ["python", "app/calculator.py"]
