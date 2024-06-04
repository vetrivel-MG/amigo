import qdrant_client
from sentence_transformers import SentenceTransformer
import openai
from fastapi import FastAPI
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
encoder = SentenceTransformer("all-MiniLM-L6-v2")
client = qdrant_client.QdrantClient("http://localhost:6333")

openai.api_type = "azure"
openai.api_key = '2dd4400d079a4fd49ddd2e864802522a'
openai.api_base = "https://genai-interns.openai.azure.com/"
openai.api_version = "2023-07-01-preview"

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
    context = "\\n".join(str(row) for row in results[:n_points])

    metaprompt = f"""
    Instruction:

    -- Generate answer only from the default_collection_name in Qdrant database.
    -- For internal server error and token error respond "Insufficient data, Please provide the question related to the database"
    -- Only when the question is with "Hi" or "Hello" or "hi" or "hello" or "hlo", respond with "Hello! I'm Amigo, at your service! How can I assist you?"
    -- If you are unable to find the answer for the response from the database, return the response "Apologies, this question requires more time to provide a satisfactory response. Feel free to try another question in the meantime."
    -- If asked for a secret key, password, OTP, verification code, or any other confidential information, respond with "We're unable to share confidential information at this time. Your privacy and security are our atmost priorities."
    -- when working process of the model,database stored place and model used are asked then respond with "We're unable to share confidential information at this time. Your privacy and security are our atmost priorities." 

    You are an AI chatbot named as amigo and database analyst. Answer the following question using data from the database. Question: {question.strip()} Context: {context.strip()} Answer: """
    completion = openai.ChatCompletion.create(
        engine="gpt-35-turbo-16k",   
        messages=[{"role": "user", "content": metaprompt}],
        timeout=10.0,
    )
    answer = completion["choices"][0]["message"]["content"]
    return answer

default_collection_name = os.environ.get("default_collection_name")

 
 


