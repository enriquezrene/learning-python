FROM python:3.11-slim
WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Use Gunicorn to bind to the PORT variable and point to run:app
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$PORT run:app"]