import os
import shutil
from dotenv import load_dotenv

# Load .env containing GOOGLE_API_KEY
load_dotenv()

# DELETE OLD CHROMA DB ON EACH RUN (clean testing)
if os.path.exists("db"):
    shutil.rmtree("db")

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

# === 1. CREATE STUDENT DOCUMENTS ===
docs = [
    Document(page_content="Mr Muhammad Sohail Hafeez is a dedicated software engineering student known for his strong problem-solving skills and consistent performance in programming courses. He actively participates in coding competitions and enjoys working on AI-based projects.", metadata={"department": "Software Engineering"}),
    Document(page_content="Maria Khan is an electrical engineering student with a passion for embedded systems and robotics. She has worked on multiple hardware-related projects and is recognized for her practical approach to learning.", metadata={"department": "Electrical Engineering"}),
    Document(page_content="Ahmed Bilal is a data science student who excels in statistics and machine learning. He frequently works on Kaggle datasets, builds predictive models, and contributes to open-source data science communities.", metadata={"department": "Data Science"}),
    Document(page_content="Sara Malik is a cybersecurity student known for her interest in ethical hacking and network security. She has participated in several CTF competitions and regularly practices penetration testing techniques.", metadata={"department": "Cybersecurity"}),
    Document(page_content="Usman Tariq is a computer science student with a strong command of algorithms and system design. He enjoys competitive programming and has represented his university in national-level programming contests.", metadata={"department": "Computer Science"})
]

# === 2. EMBEDDINGS ===
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# === 3. CHROMA VECTOR STORE ===
vector_store = Chroma(
    embedding_function=embeddings,
    persist_directory="db",
    collection_name="dataBase"
)

# Function to add docs
def addDocs(docs):
    vector_store.add_documents(docs)

# === 4. RETRIEVER ===
retriever = vector_store.as_retriever(search_kwargs={"k": 2})

# Search Function
def Search(query):
    results = retriever.invoke(query)
    for i, doc in enumerate(results):
        print(f"\n------- Result {i+1} --------")
        print(doc.page_content)

# Add docs ONCE
addDocs(docs)

# Query
query = "who works in AI"
Search(query)
