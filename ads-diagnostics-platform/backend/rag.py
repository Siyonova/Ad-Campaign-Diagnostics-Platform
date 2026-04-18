from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pandas as pd
from backend.analyzer import analyze_campaigns

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# ---- Load campaign issues ----
issues = analyze_campaigns()

issue_docs = [
    f"Campaign {i['campaign_id']} issue: {i['issue']} explanation: {i['explanation']}"
    for i in issues
]

# ---- Load support tickets ----
tickets = pd.read_csv("support_tickets.csv")

ticket_docs = [
    f"Support ticket: {row.ticket_text}. Diagnosed issue: {row.diagnosed_issue}"
    for _, row in tickets.iterrows()
]

# ---- Combine documents ----
documents = issue_docs + ticket_docs

# ---- Create embeddings ----
embeddings = model.encode(documents)

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))


def retrieve_relevant(query, k=5):

    query_embedding = model.encode([query])

    distances, indices = index.search(np.array(query_embedding), k)

    results = [documents[i] for i in indices[0]]

    # remove duplicates
    results = list(dict.fromkeys(results))

    return results