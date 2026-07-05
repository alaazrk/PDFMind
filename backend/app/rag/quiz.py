import json
import random
import time

from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq

from app.config import GROQ_API_KEY, GROQ_MODEL
from app.rag.vector_store import vector_store


llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name=GROQ_MODEL,
    temperature=0.3,
)


PROMPT = """
Tu es un professeur universitaire.

Lis attentivement le contexte.

Crée EXACTEMENT 3 questions.

Les questions doivent porter sur des parties différentes du texte.

Utilise plusieurs types :

- mcq
- true_false
- short

Pour les QCM :

- exactement 4 propositions

- une seule correcte

- mélange l'ordre des réponses

Les questions doivent être progressives :

1 facile

1 moyenne

1 difficile

Les réponses doivent être précises.

Ajoute toujours une explication pédagogique.

Retourne uniquement du JSON.

{
    "questions":[
        {
            "type":"mcq",
            "question":"",
            "choices":[
                "",
                "",
                "",
                ""
            ],
            "answer":"",
            "explanation":""
        }
    ]
}

Contexte :

{context}
"""





def ask_llm(context):

    response = llm.invoke([
        HumanMessage(
            content=PROMPT.format(context=context)
        )
    ])

    content = response.content.strip()

    if content.startswith("```json"):
        content = content.replace("```json", "")
        content = content.replace("```", "")

    return json.loads(content)


def generate_quiz(filename):

    chunks = vector_store.get_representative_chunks(
    filename,
    k=40
)
   

    if not chunks:

        return {
            "title": "Quiz",
            "questions": []
        }

    questions = []

    # --------- paramètres ---------

    CHUNK_PER_REQUEST = 10

    MAX_CONTEXT = 12000

    SLEEP_TIME = 0.7

    # ------------------------------

    for i in range(0, len(chunks), CHUNK_PER_REQUEST):

        batch = chunks[i:i + CHUNK_PER_REQUEST]

        context = ""

        for chunk in batch:

            if len(context) + len(chunk) > MAX_CONTEXT:
                break

            context += chunk + "\n\n"

        if not context:
            continue

        try:

            result = ask_llm(context)

            questions.extend(
                result.get("questions", [])
            )

        except Exception as e:

            print(e)

        time.sleep(SLEEP_TIME)

    # Supprimer les doublons

    unique = []

    seen = set()

    for q in questions:

        key = q["question"].lower()

        if key not in seen:

            seen.add(key)

            unique.append(q)

    random.shuffle(unique)

    return {

        "title": f"Quiz - {filename}",

        "questions": unique[:10]

    }