# Build stage
FROM python:3.9-slim as builder
WORKDIR /app
COPY . /app 
RUN pip install --upgrade pip
RUN pip install --no-cache-dir torch==1.12.0
RUN pip install --no-cache-dir pymongo
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080 6333

ENV NAME .env
# # Runtime stage
# FROM python:3.9-slim
# WORKDIR /app
# COPY --from=builder /usr/local/lib/python3.9/site-packages ./site-packages
# COPY --from=builder /usr/local/bin/python ./site-packages/bin/python
# COPY . .
# COPY .env .
CMD ["python", "database_updation/automatic_updation.py", "&&", "python", "endpoint/output.py"]
