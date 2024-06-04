 
from fastapi import APIRouter
from function.function import rag 
from function.function import default_collection_name
 

router = APIRouter()

@router.get("/ask")
def ask_question(question: str):
    response = rag(question, default_collection_name)
    return { "query": question,
            "data_source": "MongoDb",
            "answer": response,}
   