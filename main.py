# main.py
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from api.auth import router as auth_router
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
app.include_router(auth_router)
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
<title>AI Research Copilot | Pro</title>
<!-- Include Marked.js for Markdown parsing -->
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<style>
  :root {
    --bg-dark: #0a0a0a;
    --bg-panel: #171717;
    --border: #262626;
    --text-main: #ededed;
    --text-muted: #a3a3a3;
    --accent: #ffffff;
    --accent-glow: rgba(255, 255, 255, 0.1);
    --user-msg: #262626;
    --radius: 12px;
    --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  }
  
  * { box-sizing: border-box; }
  
  body {
    margin: 0;
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-dark);
    color: var(--text-main);
    height: 100vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  /* Header */
  header {
    padding: 16px 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid var(--border);
    background: var(--bg-dark);
    z-index: 10;
    flex-shrink: 0;
    gap: 16px;
  }
  header .brand {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 1.1rem;
    font-weight: 600;
    letter-spacing: -0.02em;
  }
  header .brand span.logo {
    width: 28px; height: 28px;
    background: var(--text-main);
    color: var(--bg-dark);
    border-radius: 6px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.9rem;
  }
  header .status {
    font-size: 0.8rem;
    color: var(--text-muted);
    display: flex; align-items: center; gap: 8px;
    font-weight: 500;
  }
  header .dot {
    width: 8px; height: 8px; border-radius: 50%;
    background: #10b981;
    box-shadow: 0 0 10px rgba(16, 185, 129, 0.4);
  }

  /* Layout */
  main {
    flex: 1;
    display: grid;
    grid-template-columns: 300px 1fr;
    height: calc(100vh - 65px);
    overflow: hidden;
  }
  @media (max-width: 900px) {
    main { grid-template-columns: 1fr; }
    .sidebar { display: none; }
  }

  .auth-card, .document-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 12px;
    margin-bottom: 12px;
  }
  .auth-card input, .document-card select, .document-card .document-radios {
    width: 100%;
    margin-top: 8px;
    padding: 8px 10px;
    border-radius: 8px;
    border: 1px solid var(--border);
    background: var(--bg-dark);
    color: var(--text-main);
  }
  .document-card .document-radios {
    padding: 12px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    max-height: 180px;
    overflow-y: auto;
    border-radius: 12px;
  }
  .document-card .document-radios label {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 0.9rem;
    color: var(--text-main);
    cursor: pointer;
  }
  .document-card .document-radios input {
    accent-color: #10b981;
  }
  .auth-card button, .document-card button {
    margin-top: 8px;
    width: 100%;
    padding: 8px 10px;
    border-radius: 8px;
    border: none;
    cursor: pointer;
    background: var(--text-main);
    color: var(--bg-dark);
    font-weight: 600;
  }

  /* Sidebar / Upload */
  .sidebar {
    background: var(--bg-panel);
    border-right: 1px solid var(--border);
    padding: 24px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    height: 100%;
  }
  .sidebar h2 {
    font-size: 0.75rem;
    margin: 0 0 16px;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 600;
  }
  .dropzone {
    border: 1px dashed #404040;
    border-radius: var(--radius);
    padding: 32px 16px;
    text-align: center;
    color: var(--text-muted);
    cursor: pointer;
    transition: all 0.2s ease;
    font-size: 0.85rem;
    background: rgba(255,255,255,0.02);
    flex-shrink: 0;
  }
  .dropzone:hover, .dropzone.drag {
    border-color: var(--text-main);
    background: var(--accent-glow);
    color: var(--text-main);
  }
  #fileInput { display: none; }
  .file-list {
    margin-top: 20px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    flex: 1;
    overflow-y: auto;
  }
  .file-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: var(--bg-dark);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 10px 12px;
    font-size: 0.8rem;
    flex-shrink: 0;
  }
  .file-item .name { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 140px; }
  .file-item .badge { font-size: 0.65rem; padding: 3px 8px; border-radius: 4px; font-weight: 600; text-transform: uppercase; }
  .badge.ok { background: rgba(16, 185, 129, 0.1); color: #10b981; }
  .badge.pending { background: rgba(163, 163, 163, 0.1); color: var(--text-muted); }
  .badge.error { background: rgba(239, 68, 68, 0.1); color: #ef4444; }

  /* Chat Area - FIXED HEIGHT BREAKOUT */
  .chat-area {
    display: flex;
    flex-direction: column;
    position: relative;
    height: 100%;
    overflow: hidden;
  }
  .chat-window {
    flex: 1;
    overflow-y: auto;
    padding: 40px 24px;
    display: flex;
    flex-direction: column;
    gap: 32px;
    scroll-behavior: smooth;
  }
  .msg-container {
    max-width: 800px;
    margin: 0 auto;
    width: 100%;
    display: flex;
    flex-direction: column;
  }
  
  /* User Message */
  .msg-container.user {
    align-items: flex-end;
  }
  .msg-container.user .content {
    background: var(--user-msg);
    color: var(--text-main);
    padding: 14px 20px;
    border-radius: 20px;
    font-size: 0.95rem;
    line-height: 1.5;
    max-width: 75%;
    white-space: pre-wrap;
  }

  /* Bot Message & Markdown Styles */
  .msg-container.bot {
    align-items: flex-start;
  }
  .msg-container.bot .content {
    width: 100%;
    font-size: 0.95rem;
    line-height: 1.7;
    color: #d4d4d4;
  }
  
  /* Rich Markdown Formatting */
  .markdown-body h1, .markdown-body h2, .markdown-body h3 { color: var(--text-main); margin-top: 1.5em; margin-bottom: 0.5em; font-weight: 600; }
  .markdown-body h1 { font-size: 1.5rem; }
  .markdown-body h2 { font-size: 1.25rem; border-bottom: 1px solid var(--border); padding-bottom: 8px; }
  .markdown-body p { margin-bottom: 1em; }
  .markdown-body ul, .markdown-body ol { margin-bottom: 1em; padding-left: 24px; }
  .markdown-body li { margin-bottom: 0.25em; }
  .markdown-body pre {
    background: #000000;
    border: 1px solid var(--border);
    padding: 16px;
    border-radius: 8px;
    overflow-x: auto;
    margin: 1em 0;
  }
  .markdown-body code {
    font-family: var(--font-mono);
    font-size: 0.85em;
    background: rgba(255,255,255,0.1);
    padding: 3px 6px;
    border-radius: 4px;
  }
  .markdown-body pre code { background: transparent; padding: 0; }
  .markdown-body blockquote {
    border-left: 4px solid #404040;
    margin: 0;
    padding-left: 16px;
    color: var(--text-muted);
  }
  .markdown-body strong { color: var(--text-main); }

  /* Structured Tools (RAG / Web Search) */
  .tools-wrapper {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-bottom: 16px;
    width: 100%;
  }
  details.tool-call {
    background: rgba(255,255,255,0.02);
    border: 1px solid var(--border);
    border-radius: 8px;
    overflow: hidden;
  }
  details.tool-call summary {
    padding: 10px 16px;
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--text-muted);
    cursor: pointer;
    list-style: none;
    display: flex;
    align-items: center;
    gap: 8px;
    user-select: none;
  }
  details.tool-call summary::-webkit-details-marker { display: none; }
  details.tool-call summary:hover { background: rgba(255,255,255,0.04); color: var(--text-main); }
  details.tool-call[open] summary { border-bottom: 1px solid var(--border); }
  details.tool-call .tool-content {
    padding: 16px;
    font-size: 0.85rem;
    color: #a3a3a3;
    max-height: 250px;
    overflow-y: auto;
    background: #000;
  }

  /* Input Area - SECURED DOWN AT BOTTOM */
  .input-wrapper {
    padding: 0 24px 32px;
    background: linear-gradient(0deg, var(--bg-dark) 85%, transparent);
    flex-shrink: 0;
  }
  .input-box {
    max-width: 800px;
    margin: 0 auto;
    position: relative;
    display: flex;
    background: var(--bg-panel);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 8px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    transition: border-color 0.2s;
  }
  .input-box:focus-within { border-color: #525252; }
  .input-box input {
    flex: 1;
    background: transparent;
    border: none;
    color: var(--text-main);
    padding: 12px 16px;
    font-size: 1rem;
    outline: none;
    font-family: inherit;
  }
  .input-box input::placeholder { color: #525252; }
  .input-box button {
    background: var(--text-main);
    color: var(--bg-dark);
    border: none;
    width: 40px;
    height: 40px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: transform 0.2s, opacity 0.2s;
  }
  .input-box button:hover:not(:disabled) { transform: scale(1.05); }
  .input-box button:disabled { opacity: 0.3; cursor: not-allowed; }
  .input-box button svg { width: 20px; height: 20px; fill: currentColor; }

  /* Scrollbars styling */
  ::-webkit-scrollbar { width: 6px; height: 6px; }
  ::-webkit-scrollbar-track { background: transparent; }
  ::-webkit-scrollbar-thumb { background: #404040; border-radius: 10px; }
  ::-webkit-scrollbar-thumb:hover { background: #525252; }
</style>
</head>
<body>

<header>
  <div class="brand"><span class="logo">✦</span> AI Research Copilot</div>
  <div class="status" id="statusBadge"><span class="dot"></span> System Online</div>
</header>

<main>
  <!-- Sidebar -->
  <aside class="sidebar">
    <div class="auth-card">
      <h2>Access</h2>
      <input id="usernameInput" placeholder="Your name" />
      <input id="passwordInput" type="password" placeholder="Password (admin)" />
      <button id="loginBtn">Enter workspace</button>
      <div id="loginMessage" style="margin-top:8px;color:#a3a3a3;font-size:0.8rem;"></div>
    </div>
    <div class="document-card">
      <h2>Active document</h2>
      <div id="documentRadioGroup" class="document-radios"></div>
      <button id="switchDocumentBtn">Use selected document</button>
    </div>
    <h2>Knowledge Base</h2>
    <div class="dropzone" id="dropzone">
      <div style="margin-bottom: 8px;">📄</div>
      Drag & drop PDF here<br/>or click to upload
      <input type="file" id="fileInput" accept="application/pdf" multiple />
    </div>
    <div class="file-list" id="fileList"></div>
  </aside>

  <!-- Chat Area -->
  <section class="chat-area">
    <div class="chat-window" id="chatWindow">
      <!-- Initial Greeting -->
      <div class="msg-container bot">
        <div class="content markdown-body">
          <h3>Welcome to Copilot.</h3>
          <p>I am ready to assist. Upload context documents to the Knowledge Base, or ask me directly to search the web for the latest information.</p>
        </div>
      </div>
    </div>

    <!-- Input Box Area -->
    <div class="input-wrapper">
      <div class="input-box">
        <input type="text" id="questionInput" placeholder="Message Copilot..." autocomplete="off" />
        <button id="sendBtn" disabled>
          <svg viewBox="0 0 24 24"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"></path></svg>
        </button>
      </div>
    </div>
  </section>
</main>

<script>
// Configure marked.js to handle markdown formatting cleanly
marked.setOptions({ breaks: true, gfm: true });

const dropzone      = document.getElementById('dropzone');
const fileInput     = document.getElementById('fileInput');
const fileList      = document.getElementById('fileList');
const chatWindow    = document.getElementById('chatWindow');
const questionInput = document.getElementById('questionInput');
const sendBtn       = document.getElementById('sendBtn');
const usernameInput = document.getElementById('usernameInput');
const passwordInput = document.getElementById('passwordInput');
const loginBtn      = document.getElementById('loginBtn');
const loginMessage  = document.getElementById('loginMessage');
const statusBadge   = document.getElementById('statusBadge');
const documentRadioGroup = document.getElementById('documentRadioGroup');
const switchDocumentBtn = document.getElementById('switchDocumentBtn');
let currentUser = '';
let currentDocuments = [];

// Toggle the send button state based on the input string length
questionInput.addEventListener('input', () => {
  sendBtn.disabled = questionInput.value.trim().length === 0;
});

// ---------- Login / session handling ----------
async function loginUser() {
  const username = usernameInput.value.trim();
  const password = passwordInput.value;
  if (!username || !password) {
    loginMessage.textContent = 'Enter your name and the admin password to continue.';
    return;
  }

  try {
    const res = await fetch('/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    const data = await res.json();
    if (!res.ok) {
      loginMessage.textContent = data.detail || 'Login failed.';
      return;
    }

    currentUser = data.username;
    statusBadge.innerHTML = '<span class="dot"></span> Logged in as ' + currentUser;
    loginMessage.textContent = 'Workspace ready. Upload documents and start chatting.';
    await loadDocuments();
    addUserMessage(`Welcome ${currentUser}! I will personalize answers for you.`);
  } catch (err) {
    console.error('Login fetch failed', err);
    loginMessage.textContent = 'Could not reach the login service: ' + (err.message || err);
  }
}

async function loadDocuments() {
  if (!currentUser) return;
  try {
    const res = await fetch(`/documents?username=${encodeURIComponent(currentUser)}`);
    const data = await res.json();
    currentDocuments = data.documents || [];
    documentRadioGroup.innerHTML = '';
    if (currentDocuments.length === 0) {
      documentRadioGroup.innerHTML = '<div style="color:#a3a3a3;font-size:0.85rem;">No documents uploaded yet.</div>';
      fileList.innerHTML = '';
      return;
    }

    const activeDoc = data.active_document || currentDocuments[0];
    documentRadioGroup.innerHTML = currentDocuments
      .map((doc, index) => `
        <label>
          <input type="radio" name="document" value="${doc}" ${doc === activeDoc ? 'checked' : ''} />
          ${doc}
        </label>
      `)
      .join('');

    fileList.innerHTML = currentDocuments
      .map(doc => `<div class='file-item'><span class='name'>${doc}</span><span class='badge ok'>${doc === activeDoc ? 'Active' : 'Saved'}</span></div>`)
      .join('');
  } catch (err) {
    console.error(err);
  }
}

function getSelectedDocument() {
  const radio = documentRadioGroup.querySelector('input[name="document"]:checked');
  return radio ? radio.value : (currentDocuments[0] || '');
}

async function switchDocument() {
  if (!currentUser) {
    loginMessage.textContent = 'Log in first to choose a document.';
    return;
  }
  const documentName = getSelectedDocument();
  if (!documentName) return;
  try {
    const res = await fetch('/set-active-document', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: currentUser, document_name: documentName })
    });
    const data = await res.json();
    if (res.ok) {
      loginMessage.textContent = `Using ${data.active_document} for this session.`;
      await loadDocuments();
    }
  } catch (err) {
    loginMessage.textContent = 'Could not switch document.';
  }
}

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
    alert(`${file.name} is not a valid PDF.`);
    return;
  }

  const row = document.createElement('div');
  row.className = 'file-item';
  row.innerHTML = `<span class="name" title="${file.name}">${file.name}</span><span class="badge pending">Syncing</span>`;
  fileList.prepend(row);

  const formData = new FormData();
  formData.append('file', file);
  formData.append('username', currentUser || usernameInput.value.trim() || 'guest');

  try {
    const res = await fetch('/upload', { method: 'POST', body: formData });
    const data = await res.json().catch(() => ({}));
    if (res.ok) {
      row.querySelector('.badge').textContent = 'Indexed';
      row.querySelector('.badge').className = 'badge ok';
      if (data.active_document) {
        loginMessage.textContent = `Saved ${file.name} and switched to ${data.active_document}.`;
      }
      await loadDocuments();
    } else {
      row.querySelector('.badge').textContent = 'Error';
      row.querySelector('.badge').className = 'badge error';
    }
  } catch (err) {
    row.querySelector('.badge').textContent = 'Failed';
    row.querySelector('.badge').className = 'badge error';
  }
}

// ---------- Chat handling ----------

function scrollToBottom() {
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

// Add user message to display
function addUserMessage(text) {
  const container = document.createElement('div');
  container.className = 'msg-container user';
  
  const content = document.createElement('div');
  content.className = 'content';
  content.textContent = text;
  
  container.appendChild(content);
  chatWindow.appendChild(container);
  scrollToBottom();
}

// Add bot typing indicator block
function addTypingIndicator() {
  const container = document.createElement('div');
  container.className = 'msg-container bot typing-indicator';
  
  const content = document.createElement('div');
  content.className = 'content';
  content.style.color = 'var(--text-muted)';
  content.innerHTML = '<i>Processing request...</i>';
  
  container.appendChild(content);
  chatWindow.appendChild(container);
  scrollToBottom();
  return container;
}

// Render dynamic bot structural components (Tools + Main Response)
function addBotAnswer(data) {
  const container = document.createElement('div');
  container.className = 'msg-container bot';

  // 1. Tool logs parsing (RAG / Web Search)
  if (data.rag_answer || data.web_result) {
    const toolsWrapper = document.createElement('div');
    toolsWrapper.className = 'tools-wrapper';

    if (data.rag_answer) {
      const ragDetails = document.createElement('details');
      ragDetails.className = 'tool-call';
      ragDetails.innerHTML = `
        <summary>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg>
          Analyzed Knowledge Base
        </summary>
        <div class="tool-content markdown-body">${marked.parse(data.rag_answer)}</div>
      `;
      toolsWrapper.appendChild(ragDetails);
    }
    
    if (data.web_result) {
      const webDetails = document.createElement('details');
      webDetails.className = 'tool-call';
      webDetails.innerHTML = `
        <summary>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>
          Web Search Results
        </summary>
        <div class="tool-content markdown-body">${marked.parse(data.web_result)}</div>
      `;
      toolsWrapper.appendChild(webDetails);
    }
    container.appendChild(toolsWrapper);
  }

  // 2. Main Markdown processing
  const content = document.createElement('div');
  content.className = 'content markdown-body';
  content.innerHTML = marked.parse(data.answer || "No structural response payload parsed.");
  
  container.appendChild(content);
  chatWindow.appendChild(container);
  scrollToBottom();
}

async function sendQuestion() {
  const question = questionInput.value.trim();
  if (!question) return;

  addUserMessage(question);
  questionInput.value = '';
  sendBtn.disabled = true;

  const typingNode = addTypingIndicator();

  try {
    const res = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        question,
        username: currentUser || usernameInput.value.trim() || 'guest',
        active_document: getSelectedDocument(),
      }),
    });
    
    const data = await res.json();
    typingNode.remove();

    if (res.ok) {
      addBotAnswer(data);
    } else {
      addBotAnswer({ answer: "**Error:** The upstream backend rejected the request parameters." });
    }
  } catch (err) {
    typingNode.remove();
    addBotAnswer({ answer: "**Connection Interrupted:** Host interface cannot communicate with server routes." });
  } finally {
    sendBtn.disabled = questionInput.value.trim().length === 0;
  }
}

loginBtn.addEventListener('click', loginUser);
passwordInput.addEventListener('keydown', (e) => { if (e.key === 'Enter') loginUser(); });
switchDocumentBtn.addEventListener('click', switchDocument);
sendBtn.addEventListener('click', sendQuestion);
questionInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') sendQuestion();
});
</script>

</body>
</html>
"""