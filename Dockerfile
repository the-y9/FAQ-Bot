# --- Stage 1: Build dependencies ---
FROM python:3.10-slim AS builder

WORKDIR /app

# Install system packages required for building scientific libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libatlas-base-dev \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy only the requirements file
COPY requirements.txt .

# Create a virtual environment and install dependencies there
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# --- Stage 2: Runtime image ---
FROM python:3.10-slim

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app

# Install only runtime libraries needed (not compilers)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libatlas-base-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy only necessary app files
COPY app/ ./app/
COPY fastapi_wrapper.py .  # Adjust depending on your entry file
COPY static/ ./static/     # If you have static files

# Expose the FastAPI port
EXPOSE 5000

# Command to run the FastAPI app with Gunicorn and Uvicorn workers
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "fastapi_wrapper:app", "--host", "0.0.0.0", "--port", "5000"]
