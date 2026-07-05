from fastapi import APIRouter
from app.rag.quiz import generate_quiz

router = APIRouter(
    prefix="/quiz",
    tags=["Quiz"]
)

@router.post("/{filename}")
def quiz(filename: str):

    print("====== QUIZ API ======")
    print(filename)

    result = generate_quiz(filename)

    print("quiz terminé")

    return result