import os
import io
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
chroma_client = chromadb.PersistentClient(path="./chroma_db")


def extract_text(file_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(file_bytes))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def embed_and_store(doc_id: str, user_id: str, chunks: list[str]):
    collection = chroma_client.get_or_create_collection(name="documents")
    embeddings = embedding_model.encode(chunks).tolist()

    collection.upsert(
        ids=[f"{doc_id}_chunk_{i}" for i in range(len(chunks))],
        embeddings=embeddings,
        documents=chunks,
        metadatas=[{"doc_id": doc_id, "user_id": user_id} for _ in chunks]
    )
