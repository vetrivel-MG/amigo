FROM python:3.10-slim as builder
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
ENV NAME .env
ENV MONGO_URI=mongodb://localhost:27017
ENV QDRANT_HOST=localhost
ENV QDRANT_PORT=6333
# Run the command to start the application using Uvicorn
CMD ["uvicorn", "updation_endpoint:app", "--host", "0.0.0.0", "--port", "8000"]
