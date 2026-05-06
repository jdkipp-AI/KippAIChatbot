import os
import time
import csv
from datetime import datetime
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate

# --- UPDATED IMPORTS FOR LANGCHAIN 1.0+ ---
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain

# --- CONFIGURATION ---
DB_PATH = "./chroma_db"
LOG_FILE = "chatbot_performance.csv"
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

# --- LOGGING FUNCTION ---
def log_performance(query, response, duration):
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Query", "Response", "Duration_Seconds"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), query, response, round(duration, 2)])

# --- PERSISTENCE LOGIC ---
if os.path.exists(DB_PATH):
    print("--- Loading existing Vector Store ---")
    vectorstore = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
else:
    print("--- Folder not found. Indexing PDFs for the first time... ---")
    loader = DirectoryLoader('./docs', glob="./*.pdf", loader_cls=PyPDFLoader)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    vectorstore = Chroma.from_documents(
        documents=splits, 
        embedding=embeddings, 
        persist_directory=DB_PATH
    )

# --- LLM & PROMPT SETUP ---
llm = ChatOllama(model="llama3.2", temperature=0)

system_prompt = (
    "You are a literal assistant. Answer the question using ONLY the provided context. "
    "If the answer is not in the context, say 'I do not know'. "
    "\n\n"
    "Context: {context}"
)

prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", "{input}")])

# Setup Retrieval Chain
retriever = vectorstore.as_retriever(search_kwargs={"k": 10})
document_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, document_chain)

# --- CHAT LOOP ---
print("\n--- Chatbot Ready (Type 'exit' to quit) ---")
while True:
    query = input("\nAsk: ")
    if query.lower() == 'exit': 
        break
    
    # Performance timing
    start_time = time.time()
    
    # Run the AI
    response = rag_chain.invoke({"input": query})
    answer = response["answer"]
    
    # Calculate duration and log
    duration = time.time() - start_time
    log_performance(query, answer, duration)
    
    print(f"\nAI Response ({round(duration, 2)}s):", answer)