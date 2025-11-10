import argparse
import sys
import requests


RAG_API_HOST = 'http://localhost:8000'

def send_question(question: str, index: int) -> dict:
    
    url = RAG_API_HOST.rstrip('/') + '/ask'
    payload = {
        'query': question,
        'k_index': index,
    }
    response = requests.post(url, json=payload, timeout=30)
    response.raise_for_status()
    try:
        return response.json()
    except ValueError:
        # If response is not JSON, return text
        return {'response': response.text}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query a FAQ assistant using RAG")
    parser.add_argument('--query', help='Query to the FAQ according to the documentation provided on ingest.py')
    parser.add_argument('--k_index', help='Index to search', default=2, type=int)

    args = parser.parse_args()

    response = send_question(args.query, args.k_index)
    print(f"Answer: {response}")