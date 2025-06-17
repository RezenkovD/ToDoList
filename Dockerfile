FROM python:3.12

RUN apt-get update && apt-get install -y build-essential libpq-dev && pip install httpx

WORKDIR /app

COPY requirements.txt .
COPY requirements-dev.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt && pip install -r requirements-dev.txt

COPY . .

ENV PYTHONPATH=/app/src

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
