FROM python:3.9-slim as builder

WORKDIR /app
RUN pip install --no-cache-dir --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt
COPY . /app

EXPOSE 8000 6333
ENV NAME .env

FROM qdrant/qdrant:latest as qdrant
ENV QDRANT_HOST=qdrant_host
ENV QDRANT_PORT=6333

CMD ["python", "database_updation/automatic_updation.py", "&&", "python", "endpoint/output.py"]
