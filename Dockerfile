# Use an official Python runtime as a parent image
FROM python:3.10-slim as builder

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variables
ENV NAME .env
ENV MONGO_URI=mongodb://mongodb:27017
ENV QDRANT_HOST=qdrant
ENV QDRANT_PORT=6333

# Run the command to start the application using Uvicorn
CMD ["uvicorn", "updation_endpoint:app", "--host", "0.0.0.0", "--port", "8000"]
