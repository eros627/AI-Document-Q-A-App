import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from auth import get_current_user, supabase
from services.embeddings import extract_text, chunk_text, embed_and_store

router = APIRouter()


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    user=Depends(get_current_user)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    contents = await file.read()
    doc_id = str(uuid.uuid4())

    text = extract_text(contents)
    if not text.strip():
        raise HTTPException(status_code=422, detail="Could not extract text from PDF.")

    chunks = chunk_text(text)
    embed_and_store(doc_id, user.id, chunks)

    supabase.table("documents").insert({
        "user_id": user.id,
        "doc_id": doc_id,
        "filename": file.filename,
    }).execute()

    return {
        "doc_id": doc_id,
        "filename": file.filename,
        "chunks_stored": len(chunks)
    }


@router.get("/list")
async def list_documents(user=Depends(get_current_user)):
    response = supabase.table("documents")\
        .select("*")\
        .eq("user_id", user.id)\
        .execute()

    return response.data
