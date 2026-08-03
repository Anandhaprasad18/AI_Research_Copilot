# AI Research Copilot

A small research assistant built with **LangGraph** + **LangChain** + **Groq**.
Each question is routed to one of three paths:

| Route    | Triggered by                                                       | What it does                                  |
|----------|----------------------------------------------------------------------|------------------------------------------------|
| `rag`    | `policy`, `pdf`, `document`, `manual`, `report` in the question      | Answers from your indexed PDFs only            |
| `both`   | `latest`, `recent`, `new`, `current`, `today`, `now` in the question  | Combines PDF context **and** a live web search |
| `search` | anything else                                                        | Plain web search                                |

A final "writer" node merges whatever context it has into one complete answer.

## Project structure

```
app.py                 # Streamlit UI (entry point)
config.py               # Loads .env, builds the shared Groq `llm`
graph/
  state.py              # LangGraph State schema
  router.py              # Keyword-based router
  nodes.py                # rag / search / both / writter nodes
  graph.py                 # Wires nodes into a compiled LangGraph
rag/
  loader.py               # Loads PDFs from data/pdfs
  splitter.py              # Chunks documents
  embeddings.py             # HuggingFace sentence-transformer embeddings
  vectordb.py               # FAISS vector store (cached, rebuildable)
  retriever.py               # Retriever built on top of the vector store
  chain.py                    # RAG chain: retrieve -> prompt -> llm -> parse
tools/
  search.py                # DuckDuckGo web search tool
agents/
  rag_agent.py             # Optional: rag_chain wrapped as a LangChain @tool
data/pdfs/                # Drop PDFs here (or upload via the UI)
```

## Setup

1. **Create a virtual environment and install dependencies:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Set your Groq API key** in `.env` (already present in this project):
   ```
   GROQ_API_KEY=gsk_your_key_here
   ```
   Get a free key at https://console.groq.com/keys.

   > ⚠️ The `.env` shipped in this project already contains a key. Since it
   > was sitting in a downloadable zip, treat it as exposed and **rotate it**
   > in the Groq console before relying on this project.

3. **Add PDFs** to `data/pdfs/` (or upload them from the app's sidebar).

## Run

```bash
streamlit run app.py
```

Open the local URL Streamlit prints (usually http://localhost:8501), upload
PDFs from the sidebar, click **Rebuild knowledge base**, and start asking
questions.

## Notes

- The Groq model defaults to `openai/gpt-oss-120b` (Groq deprecated
  `llama-3.3-70b-versatile` in June 2026). Override with the `GROQ_MODEL`
  env var if you want a different model.
- Web search uses DuckDuckGo (`duckduckgo-search`), so no extra API key is
  needed beyond `GROQ_API_KEY`.
- The vector index is rebuilt in-memory on demand (via the sidebar button),
  not persisted to disk — restarting the app re-indexes from `data/pdfs/`.
