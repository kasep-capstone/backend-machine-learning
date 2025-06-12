FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . .
# COPY .env .env

EXPOSE 8080

# CMD ["gunicorn", "app:app", "--worker-class=gevent", "--worker-connections=1000", "--workers=3", "--bind=0.0.0.0:8080", "--timeout=600"]
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]