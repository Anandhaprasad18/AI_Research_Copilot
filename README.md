# AI Research Copilot

A FastAPI-based PDF research assistant with user-aware document selection, personal profiles, and RAG-powered answers.

## What this project does

- Provides a web UI for user login and PDF upload
- Stores per-user documents in `data/users/<username>/documents`
- Keeps each user's active document and personalization in `data/users/<username>/profile.json`
- Uses LangGraph + LangChain + Groq to route questions to:
  - RAG-only responses from PDF content
  - Web search responses
  - Hybrid responses combining PDF context and web search

## Key features

- Login with any username and the fixed password `admin`
- Upload PDF files via the sidebar
- Choose which uploaded document should be active for the current session
- Preserve the active document per user across requests
- Send the selected document into the chat/RAG pipeline for consistent context

## Project structure

```
main.py              # FastAPI app + frontend HTML/JS
config.py            # Environment/config loader and shared Groq LLM
api/
  auth.py            # Login endpoint and user authentication
  chat.py            # Chat endpoint that passes active_document to the graph
  upload.py          # Upload/document list and active-document management
data/
  users/             # User-specific storage for profiles and PDFs
    <username>/      # Created per login/user
      documents/     # Uploaded PDFs for that user
      profile.json   # Active document, personalization, login defaults
graph/
  graph.py           # LangGraph graph builder and compiled graph
  nodes.py           # rag / search / both / writter runtime nodes
  router.py          # simple route decision logic
  state.py           # shared state model for LangGraph
rag/
  chain.py           # cached RAG chain builder per user/document
  embeddings.py      # embedding model loader (HuggingFace)
  retriever.py       # retriever builder using FAISS
  splitter.py        # PDF chunking/splitting logic
  vectordb.py        # per-user/document FAISS store cache and reset logic
tools/
  search.py          # DuckDuckGo web search tool
requirements.txt     # Python dependencies
README.md            # This documentation
```

## Setup

1. Install dependencies:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Set the Groq API key in a `.env` file at the repo root:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

3. Make sure the project files are available and the working directory is `AI_Research_Copilot`.

## Run the app

```bash
py -3.12 -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Then open `http://127.0.0.1:8000` in your browser.

## How to use

1. Enter a username and password `admin` on the left panel.
2. Upload one or more PDFs using the drag-and-drop area or file selector.
3. Choose the active document via the document radio buttons.
4. Ask questions in the chat input. The app will use the selected PDF as the active knowledge source.

## User storage

- `data/users/<username>/profile.json`
  - `username`
  - `password` (fixed to `admin`)
  - `personalization`
  - `active_document`
- `data/users/<username>/documents/`
  - Stored PDF files for that user

## Important endpoints

- `POST /login` — login and initialize user profile
- `GET /documents?username=<username>` — list uploaded documents and active document
- `POST /upload` — upload a PDF for a user and set it active
- `POST /set-active-document` — switch the active document for the user
- `POST /chat` — ask a question, sending `active_document` to the backend

## Notes

- The application uses a fixed login password `admin` for simplicity.
- Uploaded documents are kept per username, so different users can manage separate knowledge bases.
- Active document selection is preserved across chat requests and used by the RAG pipeline.
- If the server is restarted, uploaded files and user profiles remain in `data/users`.

## Troubleshooting

- If the web UI cannot reach the server, verify `uvicorn` is running and the browser is loading `http://127.0.0.1:8000`.
- If chat requests are returning errors, confirm the active document exists for the current user.
- If the app cannot create user storage, ensure the process has write permissions for `data/users`.
