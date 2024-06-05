FROM python:3.9-slim as builder
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000 6333
ENV NAME .env

# Install Supervisor
RUN apt-get update && apt-get install -y supervisor

# Copy the Supervisor configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD ["supervisord.conf"]
