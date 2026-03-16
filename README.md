# Workshop-sih

# SecureGov AI: Intelligent Organizational Assistant

SecureGov AI is a high-performance, secure Retrieval-Augmented Generation (RAG) chatbot designed for public sector organizations. It allows employees to query complex HR and IT manuals in real-time while maintaining strict security through 2FA and professional content filtering.

## 🎯 Aim

The goal of this project is to bridge the gap between long organizational manuals and employee needs. By using Deep Learning, we turn 10+ page PDFs into an interactive conversation that is:

* **Secure:** Protected by a 2-Factor Authentication gateway.
* **Accurate:** Grounded 100% in official documentation (no hallucinations).
* **Fast:** Sub-3 second response times for 5+ concurrent users.
* **Professional:** Equipped with real-time profanity and language moderation.

## 🛠️ Technical Stack

* **Language:** Python 3.13
* **Framework:** Streamlit (UI) & LangChain (Orchestration)
* **AI Model:** Google Gemini 1.5 Flash
* **Vector Database:** FAISS (Facebook AI Similarity Search)
* **Preprocessing:** PyPDF & RecursiveCharacterTextSplitter

## 📋 System Design & Code Logic

The system uses a **RAG (Retrieval-Augmented Generation)** architecture:

1. **Authentication:** A random 6-digit OTP is generated for identity verification.
2. **Ingestion:** Documents are split into 1000-character chunks to preserve semantic context.
3. **Indexing:** Chunks are converted into vector embeddings using Google Generative AI.
4. **Retrieval:** When a user asks a question, FAISS performs a similarity search to find the most relevant text.
5. **Generation:** The Gemini model synthesizes a professional response based strictly on the retrieved data.

## 🚀 Getting Started

### 1. Prerequisites

Ensure you have Python 3.10+ installed. Install the required libraries:

```bash
pip install streamlit langchain-google-genai langchain-community faiss-cpu pypdf better-profanity langchain

```

### 2. API Setup

Get a free API key from [Google AI Studio](https://aistudio.google.com/) and add it to the `main.py` file:

```python
GEMINI_KEY = "YOUR_API_KEY_HERE"

```

### 3. Running the App

```bash
streamlit run main.py

```

## 📜 Source Code

The core logic is contained in `main.py`. It handles the 2FA login, document chunking, vector storage, and the retrieval-chain execution.

## ✅ Conclusion

SecureGov AI demonstrates that Generative AI can be deployed safely in government sectors. By combining a 2FA gateway with a document-focused AI architecture, the project provides a scalable, accurate, and low-latency solution that meets all modern organizational standards.

---
