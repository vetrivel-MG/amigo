# Build stage
FROM python:3.9-alpine as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.9-alpine
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.9/site-packages ./site-packages
COPY --from=builder /usr/local/bin/python ./site-packages/bin/python
COPY . .
COPY .env .
RUN echo "import os; os.environ.update(dict(line.split('=') for line in open('.env') if not line.startswith('#') and '=' in line)); import subprocess; subprocess.run(['python', 'automatic_updation.py']); subprocess.run(['python', 'output.py'])" > run_scripts.py
CMD ["python", "run_scripts.py"]
