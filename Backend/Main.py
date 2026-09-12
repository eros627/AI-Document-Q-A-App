from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import documents

app = FastAPI(title="AI Doc Q&A")

# Codespaces frontend URL is dynamic, so we allow all origins for now.
# We'll lock this down to the specific Codespaces URL in a later phase.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents.router, prefix="/documents", tags=["documents"])


@app.get("/")
def root():
    return {"status": "running"}
