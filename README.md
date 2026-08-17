# AI Research Copilot

An AI-powered research assistant that lets users upload research papers, build document-specific knowledge bases, and ask questions using Retrieval-Augmented Generation (RAG) with optional web search.

**Live Demo:** [Railway-hosted deployment](#)

---

## Overview

AI Research Copilot is a FastAPI-based research assistant that makes working with research papers easier. Users can:

- Create a user session
- Upload research papers as PDFs
- Maintain multiple documents
- Select an active document for context
- Ask questions about the selected paper
- Perform web searches when external information is required
- Combine information from uploaded documents and the web
- Generate contextual answers using an LLM

The application combines **RAG**, **LangGraph**, **LangChain**, **FAISS**, **Hugging Face embeddings**, **web search**, and **Groq-powered LLM inference** into a single workflow.

---

## How It Works

The application follows a document-aware RAG pipeline, orchestrated by a LangGraph router that directs each query to the RAG pipeline, web search, or a hybrid of both before passing context to the LLM for a final answer.

**Query flow:**
```
User → FastAPI API → LangGraph Router → [RAG | Web Search | Hybrid] → Groq LLM → Answer
```

**Document ingestion flow (on PDF upload):**
```
PDF → Text Extraction → Chunking → Hugging Face Embeddings
    → FAISS Vector Store → Similarity Retrieval → Relevant Context
    → LLM → Answer
```

This lets the model answer questions using the actual contents of the uploaded paper instead of relying only on its pretrained knowledge.

---

## Key Features

**Document-Aware RAG**
Each uploaded document is processed into its own vector representation. The selected document becomes the active knowledge source for subsequent questions.

**Web Search**
Routes questions toward web search when information outside the uploaded document is required.

**Hybrid Retrieval**
The LangGraph workflow can combine retrieved PDF context, web search results, and LLM reasoning — answering questions that need both paper-specific and external knowledge.

**User-Aware Storage**
Documents and user state are organized per user:
```
data/
└── users/
    └── <username>/
        ├── documents/
        │   ├── paper1.pdf
        │   └── paper2.pdf
        └── profile.json
```

**Active Document Selection**
Users can upload multiple PDFs and explicitly choose which one is used as the active knowledge source.

---

## Tech Stack

| Category | Technology |
|---|---|
| Backend | FastAPI |
| LLM | Groq |
| Agent Orchestration | LangGraph |
| LLM Framework | LangChain |
| Embeddings | Hugging Face |
| Vector Database | FAISS |
| Web Search | DuckDuckGo |
| Database / Storage | Supabase |
| Containerization | Docker |
| Deployment | Railway |
| Language | Python 3.11 |

---

## Project Structure

```
AI_Research_Copilot/
├── agents/
│   └── rag_agent.py
├── api/
│   ├── auth.py
│   ├── chat.py
│   └── upload.py
├── data/
│   └── pdfs/
├── graph/
│   ├── graph.py
│   ├── nodes.py
│   ├── router.py
│   └── state.py
├── rag/
│   ├── chain.py
│   ├── embeddings.py
│   ├── loader.py
│   ├── retriever.py
│   ├── splitter.py
│   └── vectordb.py
├── supabase/
│   └── migrations/
├── tools/
│   └── search.py
├── utils/
│   ├── supabase_client.py
│   └── user_state.py
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── config.py
├── main.py
└── requirements.txt
```

---

## Local Setup

**1. Clone the repository**
```bash
git clone <repository-url>
cd AI_Research_Copilot
```

**2. Create a virtual environment**
```bash
python -m venv .venv
```
Activate it (Windows):
```bash
.venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure environment variables**

Create a `.env` file:
```
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=your_model_name
```
Add any additional Supabase configuration required by the application.

**5. Run the application**
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```
Then open: `http://127.0.0.1:8000`

---

## Running with Docker

Build the image:
```bash
docker build -t ai-research-copilot .
```

Run the container:
```bash
docker run -p 8000:8000 --env-file .env ai-research-copilot
```

The application will be available locally on port `8000`.

**Docker flow:** `Dockerfile → Docker Image → Container → FastAPI + Uvicorn → Application`

---

## Deployment

The application deploys via a Docker-based workflow on Railway:

```
GitHub Repository → Railway → Docker Build → Docker Image → Running Container → FastAPI Application
```

Railway builds the application from the repository's `Dockerfile` and runs the resulting container. Environment secrets such as API keys should be configured through the deployment platform rather than committed to the repository.

---

## Security Notes

This project is primarily a learning and portfolio project and should **not** be considered production-grade in its current form. Before exposing it to real users, the following should be improved:

- Replace simplified authentication with proper authentication
- Hash passwords
- Add authorization checks
- Validate uploaded files and limit upload size
- Add API rate limiting
- Protect sensitive endpoints
- Move persistent files to proper object storage
- Use production-grade user/session management
- Add monitoring and logging

Never commit `.env` files or API keys to GitHub.

---

## Storage Considerations

The application currently uses local filesystem storage for uploaded documents and vector data. This works well for learning, demos, small-scale testing, and portfolio purposes — but ephemeral cloud containers can lose local files when underlying storage is recreated.

For a production system, uploaded documents should live in persistent object storage, and vector indexes should be stored in a persistent or managed vector database.

---

## Current Limitations

- Authentication is simplified
- Local filesystem storage limits horizontal scalability
- FAISS indexes are tied to local storage
- Large PDFs can increase memory usage
- Embedding/index creation can be computationally expensive
- No sophisticated authorization system
- No production-grade observability yet

These are deliberate trade-offs made to keep the project simple and understandable.

---

## Future Improvements

- [ ] OAuth / JWT authentication
- [ ] Persistent object storage for PDFs
- [ ] Managed vector database
- [ ] Streaming LLM responses
- [ ] Citation-aware answers
- [ ] Multi-document retrieval
- [ ] Conversation history
- [ ] Research-paper metadata extraction
- [ ] Automatic paper summarization
- [ ] Background document processing
- [ ] Rate limiting
- [ ] Production monitoring
- [ ] Automated testing and CI/CD

---

## What I Learned From This Project

This project was built to explore how modern AI applications are assembled end-to-end. Key concepts explored:

Retrieval-Augmented Generation (RAG) · Vector embeddings · Semantic search · FAISS · LangChain · LangGraph · Agentic routing · LLM inference · FastAPI · Docker · Environment-based configuration · Cloud deployment · Persistent storage considerations

The main goal wasn't simply to call an LLM API, but to understand the architecture required to build and deploy a document-aware AI application.

---

## License

This project is intended for educational and portfolio purposes.
