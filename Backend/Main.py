from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import documents, chat

app = FastAPI(title="AI Doc Q&A")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents.router, prefix="/documents", tags=["documents"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])

@app.get("/")
def root():
    return {"status": "running"}
