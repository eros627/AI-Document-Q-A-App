import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from services.embeddings import extract_text, chunk_text, embed_and_store

router = APIRouter()


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    contents = await file.read()   # read raw bytes from the upload
    doc_id = str(uuid.uuid4())     # unique ID for this document

    text = extract_text(contents)

    if not text.strip():
        raise HTTPException(status_code=422, detail="Could not extract text from PDF.")

    chunks = chunk_text(text)
    embed_and_store(doc_id, chunks)

    return {
        "doc_id": doc_id,
        "filename": file.filename,
        "chunks_stored": len(chunks)
    }
