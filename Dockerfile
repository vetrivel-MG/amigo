# Use the official Python image as the base image
FROM python:3.9-slim
 
# Set the working directory in the container
WORKDIR /app
 
# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
 
# Copy the entire project directory to the container
COPY . .
 
# Copy the .env file to the container
COPY .env .
 
# Create a script to run both files
RUN echo "import os; os.environ.update(dict(line.split('=') for line in open('.env') if not line.startswith('#') and '=' in line)); import subprocess; subprocess.run(['python', 'automatic_updation.py']); subprocess.run(['python', 'output.py'])" > run_scripts.py
 
# Set the command to run the script when the container starts
CMD ["python", "run_scripts.py"]