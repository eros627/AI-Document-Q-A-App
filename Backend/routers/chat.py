import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import anthropic
from services.retrieval import retrieve_relevant_chunks

router = APIRouter()
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


class ChatRequest(BaseModel):
    question: str
    doc_id: str


def build_prompt(question: str, chunks: list[str]) -> str:
    context = "\n\n".join(chunks)
    return f"""You are a helpful assistant. Answer the user's question using only the context below.
If the answer is not in the context, say "I couldn't find that in the document."

Context:
{context}

Question:
{question}"""


def stream_claude(prompt: str):
    with client.messages.stream(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        for text in stream.text_stream:
            yield text


@router.post("/ask")
async def ask_question(request: ChatRequest):
    try:
        chunks = retrieve_relevant_chunks(request.question, request.doc_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Document not found.")

    prompt = build_prompt(request.question, chunks)

    return StreamingResponse(
        stream_claude(prompt),
        media_type="text/plain"
    )
