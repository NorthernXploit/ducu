# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Use Gunicorn in production (listens on PORT from env)
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --worker-class sync app:app