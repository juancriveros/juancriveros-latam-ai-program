import requests
import json
import chromadb
import argparse
import time

# --- 1. Configuration ---
OLLAMA_ENDPOINT = "http://localhost:11434/api"
OLLAMA_CONFIG = {
    "model": "llama3",
    "stream": False,
}
CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "faq_collection"

# --- 2. Knowledge Base ---
# In a real-world scenario, this would come from a file, database, or API.
FAQ_DATA = [
    {"id": "faq1", "question": "What is the return policy?", "answer": "You can return any item within 30 days of purchase for a full refund."},
    {"id": "faq2", "question": "How do I track my order?", "answer": "Once your order has shipped, you will receive an email with a tracking number."},
    {"id": "faq3", "question": "Do you ship internationally?", "answer": "Yes, we ship to most countries worldwide. Shipping costs may vary."},
    {"id": "faq4", "question": "How can I contact customer support?", "answer": "You can reach our customer support team via email at support@example.com or by calling our toll-free number."},
    {"id": "faq5", "question": "What payment methods do you accept?", "answer": "We accept all major credit cards, PayPal, and Apple Pay."},
    {"id": "faq6", "question": "Can I change my shipping address?", "answer": "If your order has not yet shipped, you can contact customer support to update your shipping address."},
    {"id": "faq7", "question": "What are your business hours?", "answer": "Our customer support is available Monday to Friday, from 9 AM to 5 PM EST."},
    {"id": "faq8", "question": "Do you offer gift wrapping?", "answer": "Yes, we offer gift wrapping for an additional fee. You can select this option at checkout."},
    {"id": "faq9", "question": "How do I use a discount code?", "answer": "You can apply your discount code in the 'Promo Code' box at checkout."},
    {"id": "faq10", "question": "What if my item is damaged?", "answer": "If your item arrives damaged, please contact customer support immediately for a replacement or refund."}
]

# --- 3. ChromaDB Setup ---
client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
collection = client.get_or_create_collection(name=COLLECTION_NAME)

# --- 4. Helper Functions ---

def get_embedding(text):
    """
    Generates an embedding for the given text using the Ollama API.
    """
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

def index_knowledge_base():
    """
    Indexes the knowledge base into ChromaDB.
    """
    print("Indexing knowledge base...")
    for item in FAQ_DATA:
        # We are embedding the questions to find similar user queries.
        embedding = get_embedding(item["question"])
        if embedding:
            collection.add(
                ids=[item["id"]],
                embeddings=[embedding],
                documents=[item["answer"]],  # Store the answer as the document
                metadatas=[{"question": item["question"]}]
            )
    print("Indexing complete.")

def format_retrieved_context(results):
    """
    Envuelve los documentos recuperados en bloques de contexto claros.
    """
    if not results or not results.get("documents"):
        return "No relevant information found."

    docs = results["documents"][0]
    metas = results.get("metadatas", [[]])[0] if results.get("metadatas") else [{}]*len(docs)
    ids = results.get("ids", [[]])[0] if results.get("ids") else [f"doc{i+1}" for i in range(len(docs))]

    wrapped = []
    citations = []
    for i, (doc, meta, _id) in enumerate(zip(docs, metas, ids), start=1):
        question = meta.get("question", "")
        wrapped.append(
            f"\n---CONTEXT BLOCK {i}---"
            f"\n{doc}"
            f"\n---END CONTEXT BLOCK {i}---"
        )
        citations.append(f"- {_id}: \"{question}\"")
    return "\n".join(wrapped), citations

def query_rag_agent(user_query, k=2, no_context=False):
    """
    Queries the RAG agent with a user's question.
    """
    print(f"\n--- Querying for: '{user_query}' ---")
    
    # 1. Get embedding for the user query
    query_embedding = get_embedding(user_query)
    if not query_embedding:
        return "Sorry, I couldn't process your query."

    # 2. Query ChromaDB for relevant context
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k  # Retrieve the top 2 most relevant documents
    )
    
    retrieved_context = ""
    if not no_context:
        results = collection.query(query_embeddings=[query_embedding], n_results=k)
        retrieved_context, citations = format_retrieved_context(results)
        print("Retrieved context Juan:")
        print(retrieved_context)
    else:
        print("(No context mode enabled)")
    
    #retrieved_context = "\n".join(results['documents'][0]) if results['documents'] else "No relevant information found."
    
    #print(f"Retrieved context: {retrieved_context}")

    # 3. Construct the prompt for the LLM
    # prompt = f"""
    # You are a helpful FAQ assistant. A user has asked the following question:
    # '{user_query}'

    # Here is some context that might be relevant:
    # '{retrieved_context}'

    # Based on this context, please provide a clear and concise answer. If the context is not relevant, say so.
    # """

    if no_context:
        prompt = f"""
 You are a helpful FAQ assistant. A user has asked the following question:
    '{user_query}'
"""
    else:
        prompt = f"""
 You are a helpful FAQ assistant. A user has asked the following question:
    '{user_query}'

Here is some context that might be relevant:
{retrieved_context}

Based on this context, please provide a clear and concise answer. If the context is not relevant, say so.
"""

    # 4. Send the prompt to the LLM
    try:
        response = requests.post(
            f"{OLLAMA_ENDPOINT}/generate",
            json={"prompt": prompt, **OLLAMA_CONFIG}
        )
        response.raise_for_status()
        answer = json.loads(response.text)["response"]
    except requests.exceptions.RequestException as e:
        return f"Error communicating with the model: {e}"

    if not no_context and citations:
        answer += "\n\n[Citations]\n" + "\n".join(citations)

    return answer

# --- 5. Main Execution ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Week 1 Prompt Engineering Lab Runner")
    parser.add_argument("--k", default=2, help="Number of results kept.")
    parser.add_argument('--no-context', action='store_true', help='Allow generation without retrieval')
    args = parser.parse_args()

    print([args.k])
    # Check if the collection is empty before indexing
    if collection.count() == 0:
        index_knowledge_base()
    else:
        print("Knowledge base is already indexed.")

    # --- Test Queries ---
    test_queries = [
        "How can I return a product?",
        "What's the process for tracking my package?",
        "Do you ship to Canada?",
        "What are the support hours?",
        "Can I pay with Bitcoin?" # A question not in the knowledge base
    ]

    for query in test_queries:
        start_time = time.time() 
        answer = query_rag_agent(query, k=int(args.k), no_context=args.no_context)
        end_time = time.time()  # ⏱️ fin del cronómetro
        latency = end_time - start_time
        print(f"Answer: {answer}")
        print(f"Latency: {latency:.2f} seconds")
