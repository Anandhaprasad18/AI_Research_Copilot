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

## Deploying to Fly.io (quick)

1. Install `flyctl` and create an app: `flyctl launch --name your-app-name`.
2. Set required secrets in your Fly app:

```bash
flyctl secrets set GROQ_API_KEY=your_groq_api_key_here
flyctl secrets set OTHER_SECRET=secret_value
```

3. Update `fly.toml`'s `app` value with your Fly app name.
4. Push from GitHub; the included GitHub Actions workflow (`.github/workflows/deploy-fly.yml`) will run on pushes to `main` and deploy automatically. Ensure you add `FLY_API_TOKEN` and `GROQ_API_KEY` to your repository secrets.

Notes:
- The app saves FAISS indexes and uploaded PDFs under `data/` — mount a persistent volume on Fly (use `flyctl volumes create`) or expect rebuilds on instance restarts.
- For multi-instance horizontal scaling, consider using a hosted vector DB (Weaviate/Chroma/Pinecone) and external object storage for uploads.

## Production deployment (recommended checklist)

Follow this checklist to prepare the app for production-level deployment:

- **Pin Python/runtime**: choose and document a Python version (3.11 recommended) and pin dependencies in `requirements.txt` or a constraints file.
- **Secrets management**: use cloud secret storage (Fly secrets, GitHub secrets, AWS Secrets Manager). Do NOT commit `.env`.
- **Persistent storage**: mount a persistent volume for `data/` so uploaded PDFs and FAISS indexes survive restarts.
- **Vector DB strategy**: either persist FAISS indexes to disk (current approach) or migrate to a hosted vector DB (Weaviate, Pinecone, Chroma Cloud) for multi-instance scaling.
- **HTTPS & domain**: configure TLS via the platform (Fly, Render, etc.) or front a CDN/load balancer.
- **Authentication**: replace the fixed `admin` password with real auth (OAuth, Auth0, or API key gating) when exposing publicly.
- **Resource sizing**: embeddings and FAISS builds can be memory/CPU intensive; provision sufficient CPU/RAM or use background jobs to build indexes.
- **Monitoring & logging**: send logs to a centralized service (Papertrail, Logflare, Datadog) and enable platform health checks (use `/health`).
- **Backups**: schedule periodic backups of `data/` (PDFs + vectordb) to object storage (S3-compatible) and export backups off-host.

## Environment variables

Set these in your production environment (via secrets or platform env settings):

- `GROQ_API_KEY` — API key for Groq (or set to empty to use the DummyLLM).
- `GROQ_MODEL` — model name (optional).
- `PORT` — port to bind the HTTP server (platform usually sets this).

Add any other provider-specific secrets (e.g., S3 credentials) as needed.

## Persistent FAISS / Storage

This repo now persists FAISS indexes under `data/vectordb/<username>/<document>/` and user uploads under `data/users/`. For production you should:

- Mount `./data` as a persistent volume in the cloud (Fly volumes, Render persistent disks, or an attached EBS volume on AWS).
- Alternatively, migrate to a hosted vector DB and store uploads in object storage (S3) so app instances can be stateless.

Quick Fly.io volume example:

```bash
flyctl volumes create ai-data --size 3 --region ord
# update fly.toml or attach the volume when configuring the app
```

## CI/CD recommendations

- The repo includes `.github/workflows/deploy-fly.yml` to deploy to Fly.io. Add `FLY_API_TOKEN` and `GROQ_API_KEY` as GitHub repository secrets.
- For Render or Railway, use their GitHub integration and set env/secret variables in the service dashboard.
- For AWS: build and push a Docker image to ECR and deploy via ECS/Fargate or EKS. Use EFS or S3 for persistent storage.

Example GitHub Actions flow (concept):

1. Checkout code
2. Build Docker image (or use platform remote build)
3. Authenticate to platform (Fly/Render/ECR)
4. Deploy and set environment secrets

## Scaling & performance

- For low-latency inference, keep the app single-instance only if using persisted local FAISS. To scale horizontally, use a centralized vector DB and shared object storage so multiple instances can serve traffic.
- Offload heavy index-building to a background worker or queue (Celery/RQ). Build indexes on upload asynchronously and notify users when ready.
- Consider model size and embedding cost: use smaller embedding models or batch embeddings to reduce cost.

## Security hardening

- Replace fixed password auth with OAuth2, JWT, or API-key based auth. Protect the upload endpoints and admin routes.
- Rate-limit endpoints to prevent abuse.
- Sanitize and validate uploaded PDFs; prevent zip-bombs and large uploads.

## Monitoring & operations

- Use platform health checks pointing to `/health`.
- Export metrics (Prometheus) and integrate with alerts for CPU/memory, error rates, and queue backlogs.
- Periodically re-index or prune vectordb to remove stale data and control storage costs.

## Example production deploy flows (short)

- Fly.io: good free tier for small apps and supports persistent volumes. Use the provided `fly.toml` and GitHub Action.
- Render: easy Docker deploys and persistent disks; use their web UI to connect GitHub and set secrets.
- Railway: quick deployments but persistent volumes are limited on free tier.
- AWS (ECR + ECS/Fargate): production-grade, supports EFS for persistent volumes; more setup but highly configurable.
- GCP Cloud Run: fully managed serverless containers; needs external object storage (GCS) and hosted vector DB for multi-instance support.

## Operational checklist before public launch

1. Verify secrets are only in platform secret storage.
2. Confirm `data/` is persisted and backed up.
3. Replace the fixed `admin` password or disable direct public signups.
4. Run a load test for expected concurrent users and observe memory/CPU under load.
5. Configure TLS and domain.
6. Set up monitoring and alerting.

---

If you'd like, I can: (A) add a sample `docker-compose.prod.yml` and `systemd` unit file, (B) add a background worker skeleton for async indexing, or (C) create a Render/Railway/GCP deploy workflow. Tell me which and I'll implement it.
