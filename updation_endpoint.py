import pymongo
import uuid
from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer
import schedule 
import time
import datetime
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
import openai
from fastapi import FastAPI
import threading
import uvicorn
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()

mongo_client = pymongo.MongoClient(os.environ.get("MONGODB_CONNECTION_STRING"))
cloudDev_db = mongo_client[os.environ.get("MONGODB_cloudDev_db")]
docusign_db = mongo_client[os.environ.get("MONGODB_docusign_db")]
marketplace_db = mongo_client[os.environ.get("MONGODB_marketplace_db")]

qdrant_client = QdrantClient(host="localhost", port=6333)
collection_name = os.environ.get("QDRANT_COLLECTION_NAME")

model = SentenceTransformer('all-MiniLM-L6-v2')

sender_email = os.environ.get("SENDER_EMAIL")
receiver_email = os.environ.get("RECEIVER_EMAIL")
app_password = os.environ.get("APP_PASSWORD")
smtp_server = "smtp.gmail.com"
port = 587
subject = "Data Updation Completed"
body = "This is to notify you that (day -1) data has been updated to the database successfully."

app = FastAPI()
encoder = SentenceTransformer("all-MiniLM-L6-v2")
client = QdrantClient("http://localhost:6333")

openai.api_type = os.environ.get("API_TYPE")
openai.api_key = os.environ.get("API_KEY")
openai.api_base = os.environ.get("AZURE_ENDPOINT")
openai.api_version = os.environ.get("API_VERSION")

def clear_qdrant_collection(collection_name):
    try:
        qdrant_client.delete_collection(collection_name=collection_name)
        logging.info(f"Collection '{collection_name}' cleared successfully.")
    except Exception as e:
        logging.error(f"Failed to clear collection '{collection_name}': {e}")

def transfer_data_to_qdrant(databases):
    logging.info(f"Clearing collection: {collection_name}")
    clear_qdrant_collection(collection_name)
    
    try:
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),
        )
    except Exception as e:
        logging.error(f"Failed to create collection '{collection_name}': {e}")
    
    for db in databases:
        logging.info(f"Transferring data for DB: {db.name}")
        for collection in db.list_collection_names():
            logging.info(f"Processing collection: {collection}")

            docs = db[collection].find()
            for doc in docs:
                doc_id = str(uuid.uuid4())
                vector = model.encode(str(doc)).tolist()
                metadata_dict = {k: str(v) for k, v in doc.items()}
                qdrant_client.upsert(
                    collection_name=collection_name,
                    points=[models.PointStruct(id=doc_id, vector=vector, payload=metadata_dict)]
                )
        logging.info(f"Data transfer for DB: {db.name} completed")

def send_email_notification(subject, body, sender_email, receiver_email, app_password):
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = receiver_email
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(sender_email, app_password)
            server.send_message(msg)
            logging.info("Email notification sent successfully.")
    except Exception as e:
        logging.error(f"An error occurred while sending the email: {e}")

def run_data_transfer():
    logging.info("Starting data transfer process")
    databases = [cloudDev_db, docusign_db, marketplace_db]
    transfer_data_to_qdrant(databases)
    logging.info("Data transfer process completed.")
    send_email_notification(subject, body, sender_email, receiver_email, app_password)

schedule.every().day.at("23:59").do(run_data_transfer)

def background_scheduler():
    while True:
        current_time = datetime.datetime.now().time()
        scheduled_time = datetime.time(23, 59)
        if current_time < scheduled_time:
            logging.info(f"The transfer is going to happen at {scheduled_time.strftime('%H:%M')}")
        elif current_time > scheduled_time:
            logging.info(f"Time passed today for data transfer. Waiting for tomorrow's schedule.")
            next_day = datetime.datetime.now() + datetime.timedelta(days=1)
            next_scheduled_time = datetime.datetime.combine(next_day.date(), scheduled_time)
            logging.info(f"Next scheduled data transfer: {next_scheduled_time.strftime('%Y-%m-%d %H:%M:%S')}")
        schedule.run_pending()
        time.sleep(60)

def perform_similarity_search(collection_name, query):
    query_vector = encoder.encode(query).tolist()
    hits = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=3,
    )
    results = [hit.payload for hit in hits]
    return results

def rag(question: str, collection_name: str, n_points: int = 3) -> str:
    results = perform_similarity_search(collection_name, question)
    context = "\n".join(str(row) for row in results[:n_points])

    metaprompt = f"""
    Instruction:

    -- Generate answer only from the default_collection_name in Qdrant database.
    -- For internal server error and token error respond "Insufficient data, Please provide the question related to the database"
    -- Only when the question is with "Hi" or "Hello" or "hi" or "hello" or "hlo", respond with "Hello! I'm Amigo, at your service! How can I assist you?"
    -- If you are unable to find the answer for the response from the database, return the response "Apologies, this question requires more time to provide a satisfactory response. Feel free to try another question in the meantime."
    -- If asked for a secret key, password, OTP, verification code, or any other confidential information, respond with "We're unable to share confidential information at this time. Your privacy and security are our atmost priorities."
    -- When working process of the model, database stored place and model used are asked then respond with "We're unable to share confidential information at this time. Your privacy and security are our atmost priorities."

    You are an AI chatbot named Amigo and database analyst. Answer the following question using data from the database. Question: {question.strip()} Context: {context.strip()} Answer: """
    
    completion = openai.ChatCompletion.create(
        engine="gpt-35-turbo-16k",
        messages=[{"role": "user", "content": metaprompt}],
        timeout=10.0,
    )
    answer = completion["choices"][0]["message"]["content"]
    return answer

default_collection_name = os.environ.get("default_collection_name")

@app.get("/ask")
def ask_question(question: str):
    response = rag(question, default_collection_name)
    return {"query": question, "data_source": "MongoDb", "answer": response}

thread = threading.Thread(target=background_scheduler)
thread.daemon = True
thread.start()

if __name__ == "__main__":
    logging.info("Starting FastAPI server")
    uvicorn.run(app, host="0.0.0.0", port=8000)