from fastapi import FastAPI
from backend.rag_assistant import ask_rag
from backend.analyzer import analyze_campaigns

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Ad Campaign Diagnostics API running"}

@app.get("/diagnostics")
def get_diagnostics():
    results = analyze_campaigns()
    return {"issues_detected": len(results), "issues": results[:50]}

@app.get("/ask-rag")
def ask_rag_endpoint(question: str):

    answer = ask_rag(question)

    return {"answer": answer}