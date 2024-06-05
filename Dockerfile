FROM python:3.9-slim as builder
 
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip
RUN pip install --no-cache-dir torch==1.12.0
RUN pip install --no-cache-dir pymongo
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir qdrant-client
 
# Copy Qdrant configuration (if needed)
# COPY qdrant_config.yaml /app/qdrant_config.yaml
 
EXPOSE 8000 6333
ENV NAME .env
 
# # Runtime stage
# FROM python:3.9-slim
# WORKDIR /app
# COPY --from=builder /usr/local/lib/python3.9/site-packages ./site-packages
# COPY --from=builder /usr/local/bin/python ./site-packages/bin/python
# COPY . .
# COPY .env .
# Qdrant stage
FROM qdrant/qdrant:latest as qdrant
# Set environment variables for Qdrant (if needed)
ENV QDRANT_HOST=qdrant_host
ENV QDRANT_PORT=6333
 
CMD ["python", "database_updation/automatic_updation.py", "&&", "python", "endpoint/output.py"]
