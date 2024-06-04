# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from endpoint.output import router as generate_output_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(generate_output_router, prefix="/api")