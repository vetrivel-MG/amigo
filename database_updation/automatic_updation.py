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

load_dotenv()

mongo_client = pymongo.MongoClient(os.environ.get("MONGODB_CONNECTION_STRING"))

cloudDev_db = mongo_client[os.environ.get("MONGODB_cloudDev_db")]
docusign_db = mongo_client[os.environ.get("MONGODB_docusign_db")]
marketplace_db = mongo_client[os.environ.get("MONGODB_marketplace_db")]

qdrant_client = QdrantClient(host="localhost", port=6333)
collection_name = os.environ.get("QDRANT_COLLECTION_NAME")

qdrant_client.recreate_collection(
    collection_name=collection_name,
    vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE)
)

model = SentenceTransformer('all-MiniLM-L6-v2')

def transfer_data_to_qdrant(db):
    for collection in db.list_collection_names():
        docs = db[collection].find()
        for doc in docs:
            doc_id = str(uuid.uuid4())  
           
            vector = model.encode(str(doc)).tolist()
            metadata_dict = {k: str(v) for k, v in doc.items()}
            qdrant_client.upsert(
                collection_name=collection_name,
                points=[models.PointStruct(id=doc_id, vector=vector, payload=metadata_dict)]
            )

sender_email = os.environ.get("SENDER_EMAIL")
receiver_email = os.environ.get("RECEIVER_EMAIL")
app_password = os.environ.get("APP_PASSWORD")
smtp_server = "smtp.gmail.com"
port = 587 

subject = "Data Updation Completed"
body = "This is to notify you that (day -1) datas has been updated to the database successfully."

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
            print("Email notification sent successfully.")

    except Exception as e:
        print(f"An error occurred while sending the email: {e}")

def run_data_transfer():
    for db in [cloudDev_db, docusign_db, marketplace_db]:
        transfer_data_to_qdrant(db)
    print("Data transfer completed.")

    send_email_notification(subject, body, sender_email, receiver_email, app_password)

schedule.every().day.at("23:59").do(run_data_transfer)

while True:
    current_time = datetime.datetime.now().time()
    scheduled_time = datetime.time(23, 59)   

    if current_time < scheduled_time:
        print(f"The transfer is going to happen at {scheduled_time.strftime('%H:%M')}")
    elif current_time > scheduled_time:
        print(f"Time passed today for data transfer. Waiting for tomorrow's schedule.")
        next_day = datetime.datetime.now() + datetime.timedelta(days=1)
        next_scheduled_time = datetime.datetime.combine(next_day.date(), scheduled_time)
        print(f"Next scheduled data transfer: {next_scheduled_time.strftime('%Y-%m-%d %H:%M:%S')}")

    schedule.run_pending()
    time.sleep(60)
