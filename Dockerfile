# Dockerfile (place at repo root)
### Stage 1: build / install deps
FROM python:3.11-slim AS builder

# avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive
# create app directory
WORKDIR /app

# system deps (if you add packages that need build tools, add them here)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# copy only requirements first for layer caching
COPY src/requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

### Stage 2: runtime
FROM python:3.11-slim

WORKDIR /app

# create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# copy app source
COPY src /app/src

# expose port used by Flask
EXPOSE 5000

# change ownership and switch user
RUN chown -R appuser:appuser /app
USER appuser

# instruct Docker how to run the app; run as module so imports work
CMD ["python", "-m", "src.app"]
