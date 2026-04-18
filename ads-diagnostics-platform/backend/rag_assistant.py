from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from backend.rag import retrieve_relevant

# Load LLM
model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def ask_rag(question):

    # Retrieve context
    context_docs = retrieve_relevant(question)

    context = "\n".join(context_docs)

    prompt = f"""
You are an expert Google Ads troubleshooting assistant.

Context:
{context}

User Question:
{question}

Provide the most likely cause and a solution.

Answer:
"""

    inputs = tokenizer(prompt, return_tensors="pt")

    outputs = model.generate(
        **inputs,
        max_new_tokens=150,
        temperature=0.7,
        do_sample=True
    )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    if "Answer:" in response:
        response = response.split("Answer:")[-1].strip()

    return response