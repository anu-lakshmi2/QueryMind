from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from nlp.parser import natural_language_query

app = FastAPI(title="QueryMind API")

# Allow frontend (running on a different port) to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message": "QueryMind API is running"}

@app.post("/query")
def query(request: QueryRequest):
    result = natural_language_query(request.text)
    return result