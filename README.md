# 🤖 AI Learning Assistant

An AI-powered Learning Assistant that enables users to learn from **PDF documents, YouTube videos, and AI conversations** using **Retrieval-Augmented Generation (RAG)**. Built with **Python, Streamlit, Google Gemini, LangChain, HuggingFace Embeddings, and FAISS**, the application provides context-aware question answering, semantic search, and an interactive learning experience.

## ✨ Features

- 📄 **PDF Tutor**
  - Upload PDF documents
  - Context-aware question answering
  - Semantic search using FAISS
  - HuggingFace Embeddings
  - Automatic text chunking

- 🎥 **YouTube Tutor**
  - Learn directly from YouTube videos
  - Multi-language transcript support
  - Semantic search over video transcripts
  - Ask questions from video content

- 🌐 **General AI Chat**
  - Google Gemini powered chatbot
  - General-purpose AI assistant

- 🧠 **AI Study Tools (In Progress)**
  - AI Notes Generator
  - AI Summary Generator
  - Quiz Generator
  - Flashcards
  - Interview Questions
  - Topic-wise Notes
  - PDF/DOCX Export

- 📑 **Hybrid Document Processing (Planned)**
  - Digital PDF support
  - Scanned PDF support using Gemini Vision
  - Smart document detection

---

## 🏗 Architecture

```text
                    User
                      │
                      ▼
             AI Learning Assistant
                      │
      ┌───────────────┼────────────────┐
      │               │                │
      ▼               ▼                ▼
 PDF Tutor     YouTube Tutor     General Chat
      │               │
      ▼               ▼
Text Extraction   Transcript Retrieval
      │               │
      └───────────────┘
              ▼
        Text Chunking
              ▼
 HuggingFace Embeddings
              ▼
      FAISS Vector Store
              ▼
     Semantic Retrieval
              ▼
       Google Gemini
              ▼
      Context-Aware Answer
```

---

## 🛠 Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python
- **LLM:** Google Gemini 2.5 Flash
- **Framework:** LangChain
- **Embeddings:** HuggingFace (`all-MiniLM-L6-v2`)
- **Vector Database:** FAISS
- **PDF Processing:** PyMuPDF
- **YouTube Processing:** youtube-transcript-api
- **Environment:** Python, dotenv

---

## 📂 Project Structure

```text
AI-Learning-Assistant/
│
├── app.py
├── components/
│   ├── chat.py
│   ├── sidebar.py
│   ├── ui.py
│   └── pdf_processor.py
│
├── utils/
│   ├── llm.py
│   ├── chatbot.py
│   ├── rag_chain.py
│   ├── vector_store.py
│   ├── embeddings.py
│   ├── pdf_loader.py
│   ├── youtube/
│   └── content/
│
├── assets/
├── requirements.txt
└── README.md
```

---

## 🚀 Installation

```bash
git clone https://github.com/yourusername/AI-Learning-Assistant.git

cd AI-Learning-Assistant

python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file:

```env
GOOGLE_API_KEY=your_google_api_key
HF_TOKEN=your_huggingface_token
```

Run the application:

```bash
streamlit run app.py
```

---

## 📌 Current Features

- ✅ PDF-based Retrieval-Augmented Generation (RAG)
- ✅ YouTube Transcript RAG
- ✅ Google Gemini Integration
- ✅ FAISS Vector Database
- ✅ HuggingFace Embeddings
- ✅ Modular Project Architecture
- ✅ General AI Chat

---

## 🚧 Upcoming Features

- AI Notes Generation
- AI Summary Generation
- Flashcards
- Quiz Generator
- Interview Preparation
- PDF Export
- DOCX Export
- Gemini Vision for Scanned PDFs
- Authentication
- Chat History
- Multi-Document Knowledge Base
- Cloud Deployment

---

## 🎯 Learning Outcomes

This project demonstrates practical implementation of:

- Retrieval-Augmented Generation (RAG)
- Semantic Search
- Vector Databases
- Prompt Engineering
- LangChain
- Google Gemini API
- Modular AI Application Design
- Streamlit Development
- Production-inspired GenAI Architecture

---

## 👨‍💻 Author

**Anmol Singh**

B.Tech | AI/ML Enthusiast | Generative AI Developer

GitHub: https://github.com/yourusername

LinkedIn: https://linkedin.com/in/yourprofile

---

⭐ If you found this project helpful, consider giving it a star!
