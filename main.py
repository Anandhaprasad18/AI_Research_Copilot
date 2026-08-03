# main.py
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from api.chat import router as chat_router
from api.upload import router as upload_router

app = FastAPI(
    title="AI Research Copilot",
    description="AI Research Copilot using LangGraph + LangChain + Groq",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# Register APIs
# ----------------------------
app.include_router(upload_router)
app.include_router(chat_router)


# ----------------------------
# Health Check
# ----------------------------
@app.get("/health")
async def health():
    return {"status": "healthy"}


# ----------------------------
# Frontend (served at "/")
# ----------------------------
@app.get("/", response_class=HTMLResponse)
async def root():
    return HTML_PAGE


HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>AI Research Copilot</title>
<style>
  :root {
    --bg: #0b0f19;
    --panel: #131a2b;
    --panel-2: #1a2338;
    --border: #263151;
    --text: #e8ecf7;
    --muted: #8b95b3;
    --accent: #6c8dff;
    --accent-2: #9b6cff;
    --success: #3ddc97;
    --danger: #ff6b6b;
    --radius: 14px;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    background: radial-gradient(circle at 20% 0%, #16204a 0%, var(--bg) 55%);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }
  header {
    padding: 24px 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid var(--border);
    backdrop-filter: blur(6px);
  }
  header .brand {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 1.3rem;
    font-weight: 700;
  }
  header .brand span.logo {
    width: 36px; height: 36px;
    border-radius: 10px;
    background: linear-gradient(135deg, var(--accent), var(--accent-2));
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
  }
  header .status {
    font-size: 0.8rem;
    color: var(--muted);
    display: flex; align-items: center; gap: 6px;
  }
  header .dot {
    width: 8px; height: 8px; border-radius: 50%;
    background: var(--success);
    box-shadow: 0 0 8px var(--success);
  }

  main {
    flex: 1;
    display: grid;
    grid-template-columns: 320px 1fr;
    gap: 20px;
    padding: 24px 32px 32px;
    max-width: 1300px;
    margin: 0 auto;
    width: 100%;
  }
  @media (max-width: 900px) {
    main { grid-template-columns: 1fr; }
  }

  .panel {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 20px;
  }
  .panel h2 {
    font-size: 1rem;
    margin: 0 0 14px;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
  }

  /* Upload panel */
  .dropzone {
    border: 1.5px dashed var(--border);
    border-radius: 10px;
    padding: 24px 12px;
    text-align: center;
    color: var(--muted);
    cursor: pointer;
    transition: all 0.2s ease;
    font-size: 0.9rem;
  }
  .dropzone:hover, .dropzone.drag {
    border-color: var(--accent);
    background: rgba(108, 141, 255, 0.06);
    color: var(--text);
  }
  #fileInput { display: none; }

  .file-list {
    margin-top: 14px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    max-height: 220px;
    overflow-y: auto;
  }
  .file-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: var(--panel-2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 8px 10px;
    font-size: 0.82rem;
  }
  .file-item .name { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .file-item .badge {
    font-size: 0.7rem;
    padding: 2px 8px;
    border-radius: 20px;
    white-space: nowrap;
  }
  .badge.ok { background: rgba(61, 220, 151, 0.15); color: var(--success); }
  .badge.pending { background: rgba(139, 149, 179, 0.15); color: var(--muted); }
  .badge.error { background: rgba(255, 107, 107, 0.15); color: var(--danger); }

  .hint {
    margin-top: 14px;
    font-size: 0.78rem;
    color: var(--muted);
    line-height: 1.5;
  }

  /* Chat panel */
  .chat-panel {
    display: flex;
    flex-direction: column;
    height: 72vh;
  }
  .chat-window {
    flex: 1;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 14px;
    padding-right: 4px;
  }
  .msg {
    max-width: 78%;
    padding: 12px 16px;
    border-radius: 14px;
    line-height: 1.5;
    font-size: 0.94rem;
    white-space: pre-wrap;
  }
  .msg.user {
    align-self: flex-end;
    background: linear-gradient(135deg, var(--accent), var(--accent-2));
    color: white;
    border-bottom-right-radius: 4px;
  }
  .msg.bot {
    align-self: flex-start;
    background: var(--panel-2);
    border: 1px solid var(--border);
    border-bottom-left-radius: 4px;
  }
  .msg.bot.typing { color: var(--muted); font-style: italic; }

  details.sources {
    margin-top: 10px;
    font-size: 0.8rem;
    color: var(--muted);
  }
  details.sources summary { cursor: pointer; color: var(--accent); }
  details.sources .block { margin-top: 6px; padding: 8px; background: rgba(255,255,255,0.03); border-radius: 8px; }
  details.sources .block b { color: var(--text); }

  .input-row {
    margin-top: 16px;
    display: flex;
    gap: 10px;
  }
  .input-row input {
    flex: 1;
    background: var(--panel-2);
    border: 1px solid var(--border);
    color: var(--text);
    padding: 13px 16px;
    border-radius: 10px;
    font-size: 0.95rem;
    outline: none;
    transition: border-color 0.2s;
  }
  .input-row input:focus { border-color: var(--accent); }
  .input-row button {
    background: linear-gradient(135deg, var(--accent), var(--accent-2));
    border: none;
    color: white;
    padding: 0 22px;
    border-radius: 10px;
    font-weight: 600;
    cursor: pointer;
    transition: opacity 0.2s;
  }
  .input-row button:disabled { opacity: 0.5; cursor: not-allowed; }
  .input-row button:hover:not(:disabled) { opacity: 0.9; }

  ::-webkit-scrollbar { width: 6px; }
  ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
</style>
</head>
<body>

<header>
  <div class="brand"><span class="logo">🔎</span> AI Research Copilot</div>
  <div class="status"><span class="dot"></span> Backend connected</div>
</header>

<main>
  <section class="panel">
    <h2>Knowledge Base</h2>
    <div class="dropzone" id="dropzone">
      📄 Drag & drop a PDF here<br/>or click to browse
      <input type="file" id="fileInput" accept="application/pdf" multiple />
    </div>
    <div class="file-list" id="fileList"></div>
    <div class="hint">
      Uploaded PDFs are chunked, embedded, and indexed into FAISS automatically.
      Ask a question that mentions <b>“document / pdf / report / policy / manual”</b>
      to force a document-grounded answer, or <b>“latest / recent / current”</b>
      to combine your documents with a live web search.
    </div>
  </section>

  <section class="panel chat-panel">
    <h2>Chat</h2>
    <div class="chat-window" id="chatWindow">
      <div class="msg bot">👋 Hi! Upload a PDF, then ask me anything about it — or ask a general question and I'll search the web.</div>
    </div>
    <div class="input-row">
      <input type="text" id="questionInput" placeholder="Ask a research question..." />
      <button id="sendBtn">Send</button>
    </div>
  </section>
</main>

<script>
const dropzone   = document.getElementById('dropzone');
const fileInput  = document.getElementById('fileInput');
const fileList   = document.getElementById('fileList');
const chatWindow = document.getElementById('chatWindow');
const questionInput = document.getElementById('questionInput');
const sendBtn    = document.getElementById('sendBtn');

// ---------- Upload handling ----------
dropzone.addEventListener('click', () => fileInput.click());

['dragover', 'dragleave', 'drop'].forEach(evt => {
  dropzone.addEventListener(evt, (e) => {
    e.preventDefault();
    dropzone.classList.toggle('drag', evt === 'dragover');
  });
});
dropzone.addEventListener('drop', (e) => {
  handleFiles(e.dataTransfer.files);
});
fileInput.addEventListener('change', () => handleFiles(fileInput.files));

function handleFiles(files) {
  [...files].forEach(uploadFile);
}

async function uploadFile(file) {
  if (!file.name.toLowerCase().endsWith('.pdf')) {
    alert(`${file.name} is not a PDF.`);
    return;
  }

  const row = document.createElement('div');
  row.className = 'file-item';
  row.innerHTML = `<span class="name">${file.name}</span><span class="badge pending">indexing…</span>`;
  fileList.prepend(row);

  const formData = new FormData();
  formData.append('file', file);

  try {
    const res = await fetch('/upload', { method: 'POST', body: formData });
    const data = await res.json();
    if (res.ok) {
      row.querySelector('.badge').textContent = 'indexed';
      row.querySelector('.badge').className = 'badge ok';
    } else {
      row.querySelector('.badge').textContent = data.detail || 'error';
      row.querySelector('.badge').className = 'badge error';
    }
  } catch (err) {
    row.querySelector('.badge').textContent = 'failed';
    row.querySelector('.badge').className = 'badge error';
  }
}

// ---------- Chat handling ----------
function addMessage(text, sender) {
  const div = document.createElement('div');
  div.className = `msg ${sender}`;
  div.textContent = text;
  chatWindow.appendChild(div);
  chatWindow.scrollTop = chatWindow.scrollHeight;
  return div;
}

function addBotAnswer(data) {
  const wrapper = document.createElement('div');
  wrapper.className = 'msg bot';
  wrapper.textContent = data.answer;

  if (data.rag_answer || data.web_result) {
    const details = document.createElement('details');
    details.className = 'sources';
    const summary = document.createElement('summary');
    summary.textContent = 'Show reasoning details';
    details.appendChild(summary);

    if (data.rag_answer) {
      const block = document.createElement('div');
      block.className = 'block';
      block.innerHTML = `<b>📄 Document context:</b><br>${data.rag_answer}`;
      details.appendChild(block);
    }
    if (data.web_result) {
      const block = document.createElement('div');
      block.className = 'block';
      block.innerHTML = `<b>🌐 Web search:</b><br>${data.web_result}`;
      details.appendChild(block);
    }
    wrapper.appendChild(details);
  }

  chatWindow.appendChild(wrapper);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

async function sendQuestion() {
  const question = questionInput.value.trim();
  if (!question) return;

  addMessage(question, 'user');
  questionInput.value = '';
  sendBtn.disabled = true;

  const typing = addMessage('Thinking…', 'bot typing');

  try {
    const res = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question }),
    });
    const data = await res.json();
    typing.remove();

    if (res.ok) {
      addBotAnswer(data);
    } else {
      addMessage('⚠️ Something went wrong on the server.', 'bot');
    }
  } catch (err) {
    typing.remove();
    addMessage('⚠️ Could not reach the server.', 'bot');
  } finally {
    sendBtn.disabled = false;
  }
}

sendBtn.addEventListener('click', sendQuestion);
questionInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') sendQuestion();
});
</script>

</body>
</html>
"""