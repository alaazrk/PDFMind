import os
import uuid

from langchain_chroma import Chroma

from app.rag.embeddings import embedding_model

CHROMA_PATH = "chroma_db"


class VectorStore:

    def __init__(self):
        self.db = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=embedding_model
        )

    def add_documents(self, documents):
        ids = []

        for doc in documents:

            if "source" not in doc.metadata:
                doc.metadata["source"] = "unknown"

            doc.metadata["doc_id"] = os.path.basename(
                doc.metadata["source"]
            )

            ids.append(str(uuid.uuid4()))

        self.db.add_documents(
            documents=documents,
            ids=ids
        )

    def similarity_search(self, question, k=6, filename=None):
        """Utilise MMR (Maximum Marginal Relevance) plutôt qu'une simple
        recherche par similarité : récupère des chunks pertinents ET
        diversifiés, ce qui aide beaucoup sur les questions larges
        ("liste-moi les lois", "explique tout le document") où l'info
        est dispersée dans plusieurs sections du PDF plutôt que
        concentrée en un seul endroit sémantiquement proche."""
        search_filter = {"doc_id": filename} if filename else None

        return self.db.max_marginal_relevance_search(
            question,
            k=k,
            fetch_k=max(k * 4, 20),
            lambda_mult=0.5,
            filter=search_filter
        )

    def get_document_chunks(self, filename):
        result = self.db.get(
            where={
                "doc_id": filename
            }
        )

        return result.get("documents", [])

    def delete_document(self, filename):

        result = self.db.get(
            where={
                "doc_id": filename
            }
        )

        ids = result.get("ids", [])

        if ids:
            self.db.delete(ids=ids)

    def get_representative_chunks(self, filename, k=40):

     docs = self.db.max_marginal_relevance_search(
        "Résumé complet du document",
        k=k,
        fetch_k=max(k * 3, 60),
        lambda_mult=0.4,
        filter={"doc_id": filename},
    )

     return [doc.page_content for doc in docs]

vector_store = VectorStore()