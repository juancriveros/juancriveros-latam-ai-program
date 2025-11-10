import argparse
import chromadb
from chromadb import config
from chromadb.utils import embedding_functions
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
import docx
import subprocess
import pandas as pd
import os
import uuid


CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "docs"


def read_txt_md(path: str) -> str:
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()


def read_docx(path: str) -> str:
    doc = docx.Document(path)
    return "\n".join(paragraph.text for paragraph in doc.paragraphs)


def read_pdf(path: str) -> str:
    result = subprocess.run(
            ['pdftotext', '-layout', path, '-'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
    return result.stdout.decode('utf-8', errors='ignore')


def read_excel(path: str) -> str:
    xls = pd.ExcelFile(path)
    texts = []
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name, dtype=str)
        df = df.fillna('').astype(str)
        sheet_text = df.to_csv(sep='\t', index=False)
        texts.append(f"-- {sheet_name} --\n{sheet_text}")
    return "\n".join(texts)

def load_file(path: str) -> tuple[str, str]:
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File not found: {path}")
    ext = os.path.splitext(path)[1].lower()
    if ext in {'.txt', '.md'}:
        content = read_txt_md(path)
    elif ext == '.docx':
        content = read_docx(path)
    elif ext == '.pdf':
        content = read_pdf(path)
    elif ext in {'.xls', '.xlsx'}:
        content = read_excel(path)
    else:
        raise ValueError(
            f"Unsupported file type: {ext}. Supported types are .txt, .md, .docx, .pdf, .xls, .xlsx"
        )
    return content, ext

def ingest_document(path: str) -> None:
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    embedding_function = DefaultEmbeddingFunction()
    collection = client.get_or_create_collection(name=COLLECTION_NAME, embedding_function=embedding_function)

    if os.path.isdir(path):
        for root, _, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    content, ext = load_file(file_path)
                except Exception as e:
                    print(f"Skipping {file_path}: {e}")
                    continue
                doc_id = f"{os.path.basename(file_path)}-{uuid.uuid4()}"
                metadata = {'source_path': file_path, 'file_type': ext}
                collection.add(
                    ids=[doc_id], 
                    documents=[content], 
                    metadatas=[metadata]
                )
    else:
        content, ext = load_file(path)
        doc_id = f"{os.path.basename(path)}-{uuid.uuid4()}"
        metadata = {'source_path': path, 'file_type': ext}
        collection.add(
            ids=[doc_id], 
            documents=[content], 
            metadatas=[metadata]
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest a document(s) into a ChromaDB collection")
    parser.add_argument('file_path', help='Path to the document file or to a folder. Extensions supported: txt, md, docx, pdf and xlsx')

    args = parser.parse_args()

    print(args)

    try:
        ingest_document(args.file_path)
    except Exception as e:
        print(f"Error ingesting document: {e}")


if __name__ == '__main__':
    main()