FROM python:3.10-slim

WORKDIR /app

COPY ./generator /app

COPY ./generator/requirements.txt /app/requirements.txt
COPY .env /app/.env

RUN pip install --no-cache-dir -r /app/requirements.txt

CMD ["python", "main.py"]