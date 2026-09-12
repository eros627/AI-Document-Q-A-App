import os
import io
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb

# Load the model once at startup — it downloads on first run (~90MB), then caches
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# PersistentClient saves ChromaDB to disk so data survives server restarts
chroma_client = chromadb.PersistentClient(path="./chroma_db")


def extract_text(file_bytes: bytes) -> str:
    """Pull all text out of a PDF's pages."""
    reader = PdfReader(io.BytesIO(file_bytes))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """
    Split text into overlapping chunks by word count.
    Overlap ensures context isn't lost at chunk boundaries.
    """
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap  # slide forward, but back up by overlap
    return chunks


def embed_and_store(doc_id: str, chunks: list[str]):
    """
    Embed each chunk locally using sentence-transformers,
    then store in ChromaDB.
    """
    collection = chroma_client.get_or_create_collection(name="documents")

    # encode() runs the model locally — no API call
    # returns a numpy array of shape (num_chunks, 384)
    embeddings = embedding_model.encode(chunks).tolist()  # ChromaDB needs plain lists

    # upsert = insert if new, update if ID already exists (safe for re-uploads)
    collection.upsert(
        ids=[f"{doc_id}_chunk_{i}" for i in range(len(chunks))],
        embeddings=embeddings,
        documents=chunks,                                    # raw text of each chunk
        metadatas=[{"doc_id": doc_id} for _ in chunks]      # lets us filter by doc later
    )
