# Dockerfile for Token Scalper Bot
FROM python:3.11-slim

WORKDIR /app

COPY . /app

# Upgrade pip to latest version to avoid upgrade notices
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Default command: show CLI help
CMD ["python", "main.py"]
