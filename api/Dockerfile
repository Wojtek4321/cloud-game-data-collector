
FROM python:3.10

WORKDIR /app/api

COPY ./api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./api .


EXPOSE 5000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]