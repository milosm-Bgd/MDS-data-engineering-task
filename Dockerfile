FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY tests ./tests
COPY pytest.ini .
COPY data ./data

ENV PYTHONPATH=/app/src

ENTRYPOINT ["python", "src/main.py"]