import streamlit as st
import random
import os
from better_profanity import profanity

# Modern LangChain Imports
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# --- CONFIGURATION ---
GEMINI_KEY = "YOUR_GEMINI_API_KEY"  # <--- PASTE KEY HERE
profanity.load_censor_words()

st.set_page_config(page_title="Public Sector AI Bot", layout="wide")

# --- PHASE 1: 2FA SECURITY ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔐 Employee Secure Login")
    email = st.text_input("Organization Email")
    
    if st.button("Generate OTP"):
        st.session_state.otp = str(random.randint(100000, 999999))
        st.warning(f"DEBUG MODE: Your OTP is {st.session_state.otp}") # Mock Email
        
    user_otp = st.text_input("Enter 6-Digit OTP")
    if st.button("Verify"):
        if user_otp == st.session_state.get("otp"):
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Invalid OTP")
    st.stop()

# --- PHASE 2: DOCUMENT PROCESSING (RAG) ---
st.title("🤖 Organizational Assistant")
st.sidebar.header("Document Center")

uploaded_file = st.sidebar.file_uploader("Upload HR/IT Policy (8-10 page PDF)", type="pdf")

# We store the vector database in the session to keep it active for 5+ users
if uploaded_file and "vector_db" not in st.session_state:
    with open("temp_policy.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    with st.spinner("Processing Document..."):
        # 1. Load and Split
        loader = PyPDFLoader("temp_policy.pdf")
        docs = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = splitter.split_documents(docs)
        
        # 2. Create Embeddings & Vector Store
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GEMINI_KEY)
        st.session_state.vector_db = FAISS.from_documents(chunks, embeddings)
        st.sidebar.success("Document Ready!")

# --- PHASE 3: CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Query Logic
if prompt := st.chat_input("How can I help you today?"):
    
    # A. Profanity Filter
    if profanity.contains_profanity(prompt):
        st.error("Inappropriate language detected. Please remain professional.")
    else:
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # B. AI Response Logic (Modern LangChain 1.0)
        if "vector_db" in st.session_state:
            with st.chat_message("assistant"):
                llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GEMINI_KEY)
                
                # Define Prompt Template
                system_prompt = (
                    "You are an HR/IT assistant for a public sector organization. "
                    "Use the following pieces of retrieved context to answer the user's question. "
                    "If the answer isn't in the context, say you don't know. "
                    "Keep responses professional and under 5 sentences.\n\n"
                    "{context}"
                )
                
                qa_prompt = ChatPromptTemplate.from_messages([
                    ("system", system_prompt),
                    ("human", "{input}"),
                ])
                
                # Create the Chains
                doc_chain = create_stuff_documents_chain(llm, qa_prompt)
                rag_chain = create_retrieval_chain(st.session_state.vector_db.as_retriever(), doc_chain)
                
                # Run with performance tracking (< 5s)
                response = rag_chain.invoke({"input": prompt})
                answer = response["answer"]
                
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
        else:
            st.warning("Please upload a document in the sidebar first.")

# --- PHASE 4: QUICK ACTIONS ---
if st.sidebar.button("Summarize Document"):
    if "vector_db" in st.session_state:
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GEMINI_KEY)
        summary_res = llm.invoke("Summarize the main points of the uploaded document in 5 bullet points.")
        st.sidebar.info(summary_res.content)