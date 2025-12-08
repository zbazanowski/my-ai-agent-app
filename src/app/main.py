from fastapi import FastAPI
from pydantic import BaseModel
from .ai_client import run_agent

app = FastAPI()

class QueryRequest(BaseModel):
    user_id: str
    query: str

@app.post("/ask")
def ask_agent(request: QueryRequest):
    answer = run_agent(request.query, request.user_id)
    return {"answer": answer}
