FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Train the model at build time so startup is instant
RUN python -m backend.model && chmod +x start.sh

EXPOSE 8000 5000

CMD ["./start.sh"]
