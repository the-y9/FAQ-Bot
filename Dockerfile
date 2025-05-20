# Stage 1: Build dependencies
FROM python:3.10-slim AS builder

WORKDIR /app

# Install system dependencies for building libraries like matplotlib
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libatlas-base-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install dependencies into a virtual environment
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --prefix=/install -r requirements.txt

# Stage 2: Final image (runtime)
FROM python:3.10-slim

WORKDIR /app

# Copy installed Python dependencies from the builder stage
COPY --from=builder /install /usr/local

# Copy the FastAPI app and any necessary files (like frontend folder)
COPY . .

# Expose the port that FastAPI will run on
EXPOSE 5000

# Command to run the app using Gunicorn with Uvicorn workers
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "fastapi_wrapper:app", "--host", "0.0.0.0", "--port", "5000"]
