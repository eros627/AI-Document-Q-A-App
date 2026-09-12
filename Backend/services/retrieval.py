import os
from sentence_transformers import SentenceTransformer
import chromadb

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
chroma_client = chromadb.PersistentClient(path="./chroma_db")


def retrieve_relevant_chunks(question: str, doc_id: str, n_results: int = 5) -> list[str]:
    collection = chroma_client.get_collection(name="documents")

    question_embedding = embedding_model.encode([question]).tolist()

    results = collection.query(
        query_embeddings=question_embedding,
        n_results=n_results,
        where={"doc_id": doc_id}
    )

    return results["documents"][0]
