# AI-Study-Buddy
upload a pdf, ask anything from it.


📚 AI Study Buddy

Upload any PDF (textbook, notes, research paper) and chat with it like a personal tutor.


🚀 How It Works
PDF Upload → Extract Text → Split into Chunks → Create Embeddings 
→ Store in FAISS → User Asks Question → Find Relevant Chunks → AI Answers
This is called RAG (Retrieval-Augmented Generation) — one of the hottest AI techniques right now.

🛠️ Setup (Step by Step)
Step 1 — Install Python
Make sure you have Python 3.9+ installed.
Download from: https://www.python.org/downloads/
Step 2 — Create a Virtual Environment
bash# Open terminal in this folder and run:
python -m venv venv

# Activate it:
# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate


Step 3 — Install Dependencies
bashpip install -r requirements.txt
⚠️ This may take 5–10 minutes (downloading AI models). That's normal!


Step 4 — Get a Free HuggingFace Token

Go to https://huggingface.co and create a free account
Go to Settings → Access Tokens → New Token
Copy the token (starts with hf_...)

Step 5 — Run the App
bashstreamlit run app.py
Your browser will open automatically at http://localhost:8501

💡 How to Use It

Paste your HuggingFace token in the sidebar
Upload one or more PDF files
Click "Process Documents" and wait ~30 seconds
Start asking questions!

Example Questions to Try:

"Summarize the main points of this document"
"What does the author say about X?"
"Explain the concept of Y in simple terms"
"What are the key differences between A and B?"


📁 Project Structure
ai_study_buddy/
│
├── app.py              ← Main Streamlit application
├── requirements.txt    ← All Python packages needed
└── README.md           ← This file

🧠 Tech Stack
ToolPurposeStreamlitWeb UI (no HTML/CSS needed)LangChainConnects all AI componentsPyPDF2Reads PDF filesFAISSVector database (stores text as numbers)HuggingFaceFree AI models for embeddings & answerssentence-transformersConverts text to vectors

🚢 Deploy It Online (Free)
Option 1: Streamlit Cloud (Easiest)

Push code to GitHub
Go to https://streamlit.io/cloud
Connect your repo → Deploy!
Add your HF token in Secrets settings

Option 2: Hugging Face Spaces

Create a Space at huggingface.co/spaces
Choose Streamlit as framework
Upload your files


🎯 What You'll Learn Building This

✅ How RAG (Retrieval-Augmented Generation) works
✅ How to use LangChain to build AI pipelines
✅ How vector databases store and search text
✅ How to build and deploy a real AI web app
✅ How to use free HuggingFace models


🔧 Upgrade Ideas (Make it More Impressive)

 Support for .docx and .txt files
 Add a "Quiz Me" button that auto-generates questions
 Show which page/section the answer came from
 Add a summary button for quick overviews
 Support multiple languages
 Add a voice input feature


❓ Common Issues
"Module not found" error
→ Make sure your virtual environment is activated and you ran pip install -r requirements.txt
App is slow on first run
→ Normal! It's downloading AI models (~500MB) the first time.
Bad/irrelevant answers
→ Try uploading a cleaner PDF (not scanned images). Also try rephrasing your question.

Built with ❤️ using Python, LangChain, and Streamlit
