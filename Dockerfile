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

# Expose the port for the Python application
EXPOSE 8000

# Start Qudrant and the Python application
CMD ["sh", "-c", "qudrant &>/dev/null & uvicorn updation_endpoint:app --host 0.0.0.0 --port 8000 --reload"]
