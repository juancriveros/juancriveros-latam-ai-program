# Minimal RAG Project – Ingest, API & CLI

This repository contains a simple example of **retrieval‑augmented generation (RAG)**.  It shows how to load your own documents into a vector store, query them through an API, and generate grounded answers with a language model.  The project is kept intentionally small so you can experiment and extend it as you learn.

## Components

- **`ingest_docs.py`** – A script that accepts a path to a single file or a directory and adds all supported documents to a local ChromaDB collection called `docs`.  It supports plain text, Markdown, Word (`.docx`), PDF, and Excel (`.xls`, `.xlsx`) files.
- **`rag_api.py`** – A FastAPI application exposing a `POST /ask` endpoint.  When you send it a question and the number of results to retrieve (`k_index`), it fetches the most relevant chunks from the vector store, builds a prompt, and calls a language model (via an Ollama server) to generate an answer.
- **`cli_app.py`** – A command‑line client for the API.  It takes a query and a retrieval index, makes the request to `/ask`, and prints the API’s response.

## Requirements

- Python 3.10 or higher.
- Install the dependencies:

  ```bash
  pip install fastapi uvicorn chromadb requests pandas python-docx

- For PDF support, make sure pdftotext (Poppler) is installed and on your system PATH. For Excel support, you may need openpyxl.

- Optionally, run an Ollama server at http://localhost:11434 with a model like llama3. Without Ollama, the API will not be able to generate answers.

## Quick Start

Follow these steps to ingest documents and start asking questions:

1. Add your documents to the vector store:

python ingest_docs.py path/to/your/file_or_directory


This command will read every supported file in the given path (recursively if it’s a directory) and store its content in the docs collection under ./chroma_db.

2. Run the API server:

uvicorn rag_api:app --host 0.0.0.0 --port 8000 --reload


The server will load the existing docs collection and listen for requests at http://localhost:8000/ask.

3.Ask questions via the CLI:

python cli_app.py --query "What is this project about?" --k_index 2


Adjust --k_index to change how many documents are retrieved (defaults to 2). The CLI will print the response returned by the API. You can also query the API directly with curl:

curl -X POST http://localhost:8000/ask \
     -H "Content-Type: application/json" \
     -d '{"query": "What is this project about?", "k_index": 2}'
