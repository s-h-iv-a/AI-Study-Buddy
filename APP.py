import streamlit as st
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import requests
import os

st.set_page_config(page_title="AI Study Buddy", page_icon="📚", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Source+Serif+4:ital,wght@0,300;0,400;1,300&display=swap');
:root { --bg:#0f0e0c; --surface:#1a1814; --surface2:#231f1a; --accent:#c9a84c; --accent2:#8b6914; --text:#e8e0d0; --muted:#7a7060; --border:#2e2922; }
html,body,[data-testid="stAppViewContainer"] { background-color:var(--bg)!important; color:var(--text)!important; font-family:'Source Serif 4',Georgia,serif!important; }
[data-testid="stSidebar"] { background-color:var(--surface)!important; border-right:1px solid var(--border)!important; }
.main-header { text-align:center; padding:2.5rem 0 1.5rem; border-bottom:1px solid var(--border); margin-bottom:2rem; }
.main-header h1 { font-family:'Playfair Display',serif!important; font-size:3rem!important; color:var(--accent)!important; margin:0; }
.main-header p { color:var(--muted); font-style:italic; font-size:1.05rem; margin-top:0.5rem; }
.chat-message { padding:1rem 1.5rem; border-radius:4px; margin:0.8rem 0; font-size:1rem; line-height:1.7; }
.user-message { background:var(--surface2); border-left:3px solid var(--accent); }
.bot-message { background:var(--surface); border-left:3px solid var(--muted); }
.stTextInput>div>div>input { background-color:var(--surface2)!important; border:1px solid var(--border)!important; color:var(--text)!important; border-radius:4px!important; }
.stButton>button { background-color:var(--accent2)!important; color:var(--bg)!important; border:none!important; font-family:'Playfair Display',serif!important; font-weight:700!important; border-radius:2px!important; }
.stButton>button:hover { background-color:var(--accent)!important; }
.sidebar-label { font-family:'Playfair Display',serif; color:var(--accent); font-size:0.85rem; letter-spacing:0.12em; text-transform:uppercase; margin-bottom:0.5rem; }
.status-box { background:var(--surface2); border:1px solid var(--border); border-radius:4px; padding:0.8rem 1rem; font-size:0.9rem; color:var(--muted); font-style:italic; }
.status-ready { border-color:var(--accent2); color:var(--accent); }
#MainMenu,footer,header { visibility:hidden; }
</style>
""", unsafe_allow_html=True)


# ── FUNCTIONS ──────────────────────────────────

def extract_text_from_pdfs(pdf_files):
    text = ""
    for pdf in pdf_files:
        reader = PdfReader(pdf)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text


def create_vector_store(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_text(text)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return FAISS.from_texts(chunks, embeddings)


def ask_groq(context, question, api_key):
    """Call Groq API - free, fast, and reliable."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful study assistant. Answer questions based only on the provided context. Be clear and concise."
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}"
            }
        ],
        "max_tokens": 512,
        "temperature": 0.5
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=30
    )

    if response.status_code != 200:
        return f"Error {response.status_code}: {response.text}"

    return response.json()["choices"][0]["message"]["content"]


def get_relevant_context(question, vector_store):
    docs = vector_store.similarity_search(question, k=3)
    return "\n\n".join([doc.page_content for doc in docs])


# ── SESSION STATE ───────────────────────────────
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "pdf_processed" not in st.session_state:
    st.session_state.pdf_processed = False


# ── SIDEBAR ─────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-label">Your Documents</div>', unsafe_allow_html=True)
    uploaded_files = st.file_uploader("Upload PDFs", type=["pdf"], accept_multiple_files=True, label_visibility="collapsed")

    st.markdown("---")
    st.markdown('<div class="sidebar-label">Groq API Key (Free)</div>', unsafe_allow_html=True)
    st.markdown("<small style='color:#7a7060'>Get free key at <b>console.groq.com</b></small>", unsafe_allow_html=True)
    api_key = st.text_input("Groq Key", type="password", placeholder="gsk_...", label_visibility="collapsed")
    if api_key:
        st.session_state["api_key"] = api_key

    st.markdown("---")
    if uploaded_files:
        if st.button("Process Documents", use_container_width=True):
            with st.spinner("Reading documents..."):
                raw_text = extract_text_from_pdfs(uploaded_files)
            with st.spinner("Building knowledge base..."):
                st.session_state.vector_store = create_vector_store(raw_text)
                st.session_state.pdf_processed = True
                st.session_state.chat_history = []
            st.success(f"Done! {len(uploaded_files)} file(s) ready.")

    st.markdown("---")
    if st.session_state.pdf_processed:
        st.markdown('<div class="status-box status-ready">Documents loaded and ready</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-box">No documents loaded yet</div>', unsafe_allow_html=True)

    st.markdown("---")
    if st.button("Clear Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()


# ── MAIN ────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>AI Study Buddy</h1>
    <p>Upload your notes or textbooks and ask anything.</p>
</div>
""", unsafe_allow_html=True)

if st.session_state.chat_history:
    for msg in st.session_state.chat_history:
        css = "user-message" if msg["role"] == "user" else "bot-message"
        icon = "You" if msg["role"] == "user" else "Study Buddy"
        st.markdown(f'<div class="chat-message {css}"><strong>{icon}:</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)
else:
    if not st.session_state.pdf_processed:
        st.markdown("""
        <div style='text-align:center;padding:4rem 2rem;color:#4a4030'>
            <div style='font-size:3rem'>📄</div>
            <div style='font-family:Playfair Display,serif;font-size:1.3rem;color:#7a7060;margin-top:1rem'>
                Upload a PDF on the left to begin
            </div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("<div style='text-align:center;padding:3rem;color:#7a7060;font-style:italic'>Ask your first question below</div>", unsafe_allow_html=True)

if st.session_state.pdf_processed:
    col1, col2 = st.columns([5, 1])
    with col1:
        question = st.text_input("Question", placeholder="What is the main concept in this document?", label_visibility="collapsed")
    with col2:
        ask_btn = st.button("Ask", use_container_width=True)

    if ask_btn and question:
        api_key = st.session_state.get("api_key", "")
        if not api_key:
            st.warning("Please enter your Groq API key in the sidebar.")
        else:
            st.session_state.chat_history.append({"role": "user", "content": question})
            with st.spinner("Thinking..."):
                context = get_relevant_context(question, st.session_state.vector_store)
                answer = ask_groq(context, question, api_key)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            st.rerun()
