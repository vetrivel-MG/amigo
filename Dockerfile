# Use the official Python image as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the Python requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python application code
COPY . .

# Install Qudrant
RUN apt-get update && \
    apt-get install -y curl && \
    curl -L https://github.com/qdrant/qdrant/releases/download/v0.8.12/qdrant-v0.8.12-linux-amd64.tar.gz -o qdrant.tar.gz && \
    tar -xzf qdrant.tar.gz && \
    mv qdrant /usr/local/bin/

# Expose the port for the Python application
EXPOSE 8000

# Set environment variables for Qudrant
ENV QDRANT_HOST=localhost \
    QDRANT_PORT=6333

# Start Qudrant and the Python application
CMD ["sh", "-c", "qudrant &>/dev/null & uvicorn updation_endpoint:app --host 0.0.0.0 --port 8000 --reload"]
