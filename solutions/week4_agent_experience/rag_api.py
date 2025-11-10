from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import chromadb
import json
import requests


OLLAMA_ENDPOINT = "http://localhost:11434/api"
OLLAMA_CONFIG = {
    "model": "llama3",
    "stream": False,
}

CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "docs"

client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
collection = client.get_or_create_collection(name=COLLECTION_NAME)

class AskRequest(BaseModel):
    query: str
    k_index: int = 2


app = FastAPI(title="RAG API")

def get_prompt(user_query, context):
    print(user_query)
    print(context)
    prompt = f"""
    You are a helpful FAQ assistant. A user has asked the following question:
        '{user_query}'

    Here is some context that might be relevant:
    {context}

    Based on this context, please provide a clear and concise answer. If the context is not relevant, say so.
    """
    return prompt

def get_embedding(text):
    try:
        response = requests.post(
            f"{OLLAMA_ENDPOINT}/embeddings",
            json={"model": OLLAMA_CONFIG["model"], "prompt": text}
        )
        response.raise_for_status()
        return response.json()["embedding"]
    except requests.exceptions.RequestException as e:
        print(f"Error getting embedding: {e}")
        return None

def query_rag_agent(user_query, k):
    #query_embedding = get_embedding(user_query)
    #

    results = collection.query(
        query_texts=[user_query],
        n_results=k  # Retrieve the top 2 most relevant documents
    )

    prompt = get_prompt(user_query, results)

    print("----PROMPT BUILT-----")
    print(prompt)

    try:
        response = requests.post(
            f"{OLLAMA_ENDPOINT}/generate",
            json={"prompt": prompt, **OLLAMA_CONFIG}
        )
        response.raise_for_status()
        answer = json.loads(response.text)["response"]
    except requests.exceptions.RequestException as e:
        return f"Error communicating with the model: {e}"

    return answer

@app.post("/ask")
async def ask(request: AskRequest) -> dict[str, str]:
    query = request.query
    k = request.k_index

    print("----POST CALLED QUERY-----")
    print(query)

    print("----COLLECTION GOT-----")
    print(collection)
    print(collection.count())
    if collection.count() == 0:
        return {"query": request.query, "response": "Ingest documents before querying."} 

    answer = query_rag_agent(query, k)

    print("----ANSWER GOT-----")
    print(answer)

    return {"query": request.query, "response": answer}
