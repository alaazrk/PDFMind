# PDFMind — Assistant IA pour vos documents PDF

PDFMind est une application web qui permet d'importer des documents PDF et d'interagir avec eux grâce à l'IA : poser des questions (RAG), générer un résumé automatique, et créer un quiz pour réviser leur contenu.

![Statut](https://img.shields.io/badge/statut-en%20d%C3%A9veloppement-orange)

## Sommaire

- [Fonctionnalités](#fonctionnalités)
- [Stack technique](#stack-technique)
- [Architecture](#architecture)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Variables d'environnement](#variables-denvironnement)
- [Lancer le projet](#lancer-le-projet)
- [Structure du projet](#structure-du-projet)
- [Limitations connues](#limitations-connues)
- [Pistes d'amélioration](#pistes-damélioration)

## Fonctionnalités

- **Import de PDF** avec indexation automatique (extraction, découpage, embeddings)
- **Chat RAG** — pose des questions sur un document précis, réponses sourcées et fondées uniquement sur son contenu
- **Résumé automatique** — génère une synthèse structurée (vue d'ensemble + points clés) d'un document déjà importé
- **Génération de quiz** — crée automatiquement des questions (QCM, vrai/faux, réponse courte) à partir du contenu d'un PDF, avec correction et score
- **Historique des conversations** — questions et réponses passées consultables, persistées localement
- **Connexion Google** (en cours d'intégration)
- Interface sombre, épurée, en React + Tailwind

## Stack technique

**Backend**
- [FastAPI](https://fastapi.tiangolo.com/) — API REST
- [LangChain](https://www.langchain.com/) — orchestration RAG
- [ChromaDB](https://www.trychroma.com/) — base vectorielle
- [HuggingFace Embeddings](https://huggingface.co/sentence-transformers) — génération des embeddings
- [Groq](https://groq.com/) (modèle Qwen3) — génération de texte
- [PyPDFLoader](https://python.langchain.com/) — extraction du texte des PDF

**Frontend**
- [React](https://react.dev/) + [Vite](https://vitejs.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [react-markdown](https://github.com/remarkjs/react-markdown) + [KaTeX](https://katex.org/) — rendu markdown et formules mathématiques
- [lucide-react](https://lucide.dev/) — icônes
- [@react-oauth/google](https://github.com/MomenSherif/react-oauth) — connexion Google

## Architecture

Utilisateur
      │
      ▼
Frontend (React + Vite)
      │
      │ REST API
      ▼
Backend (FastAPI)
      ├── Uploads/PDF
      ├── ChromaDB
      └── Groq (Qwen3)
      │
      ▼
Réponse au Frontend
## Prérequis

- Python 3.11+
- Node.js 18+
- Une clé API [Groq](https://console.groq.com/) (gratuite)
- (Optionnel) Un Client ID Google OAuth pour la connexion — voir [Google Cloud Console](https://console.cloud.google.com/apis/credentials)

## Installation

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
```

## Variables d'environnement

### `backend/.env`

```env
GROQ_API_KEY=votre_clé_groq
GROQ_MODEL=qwen/qwen3-32b
GOOGLE_CLIENT_ID=votre_client_id.apps.googleusercontent.com
```

### `frontend/.env`

```env
VITE_GOOGLE_CLIENT_ID=votre_client_id.apps.googleusercontent.com
```

## Lancer le projet

Deux terminaux séparés sont nécessaires.

**Terminal 1 — Backend**
```bash
cd backend
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

**Terminal 2 — Frontend**
```bash
cd frontend
npm run dev
```

L'application est accessible sur **http://localhost:5173**.

## Structure du projet

```
RAG-chatbot/
├── backend/
│   ├── app/
│   │   ├── api/              # Routes FastAPI
│   │   │   ├── upload.py
│   │   │   ├── chat.py
│   │   │   ├── documents.py
│   │   │   ├── delete_document.py
│   │   │   ├── resume.py
│   │   │   ├── quiz.py
│   │   │   ├── auth.py
│   │   │   └── health.py
│   │   ├── rag/               # Logique métier RAG
│   │   │   ├── chat.py
│   │   │   ├── summarize.py
│   │   │   ├── quiz.py
│   │   │   ├── vector_store.py
│   │   │   ├── embeddings.py
│   │   │   ├── pdf_loader.py
│   │   │   ├── text_splitter.py
│   │   │   └── llm_utils.py
│   │   ├── config.py
│   │   └── main.py
│   ├── uploads/                # PDF importés (créé automatiquement)
│   └── chroma_db/              # Base vectorielle (créée automatiquement)
│
└── frontend/
    └── src/
        ├── components/
        │   ├── Sidebar.jsx
        │   ├── ChatView.jsx
        │   ├── ResumeView.jsx
        │   ├── QuizView.jsx
        │   └── MarkdownText.jsx
        ├── services/
        │   ├── api.js
        │   └── auth.js
        ├── config.js
        ├── App.jsx
        ├── main.jsx
        └── index.css
```

## Limitations connues

- **Tier gratuit Groq** : limité à 6000 tokens/minute. Le résumé et la génération de quiz sur de longs documents peuvent donc prendre du temps (traitement séquentiel par blocs pour respecter cette limite).
- **Un seul utilisateur** : les documents sont partagés globalement, pas de séparation par compte (même avec la connexion Google branchée, il n'y a pas encore de stockage par utilisateur).
- **Base vectorielle locale** : ChromaDB est stocké en local (`chroma_db/`), non adapté à un déploiement multi-instance.

## Pistes d'amélioration

- Isoler les documents par utilisateur (nécessite une base de données)
- Passer à un tier Groq payant ou un LLM local (Ollama) pour lever la limite de débit
- Ajouter du streaming des réponses (SSE) pour un affichage progressif
- Déploiement (Docker, hébergement du frontend/backend)

---

Projet réalisé dans le cadre d'un travail personnel / académique.
