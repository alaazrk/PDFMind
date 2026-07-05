from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.upload import router as upload_router
from app.api.chat import router as chat_router
from app.api.documents import router as documents_router
from app.api.delete_document import router as delete_document_router
from app.api.health import router as health_router
from app.api.resume import router as resume_router
from app.api.quiz import router as quiz_router

app = FastAPI(title="AI RAG Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(chat_router)
app.include_router(documents_router)
app.include_router(delete_document_router)
app.include_router(health_router)
app.include_router(resume_router)
app.include_router(quiz_router)

# Expose le dossier des PDF uploadés pour permettre leur téléchargement
# depuis le frontend (bouton "Télécharger" dans l'en-tête du document).
app.mount("/files", StaticFiles(directory="uploads"), name="files")


@app.get("/")
def home():
    return {"message": "API Running"}