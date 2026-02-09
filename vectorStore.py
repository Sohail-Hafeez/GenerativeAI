import os
from dotenv import load_dotenv

# Load .env containing GEMINI_API_KEY
load_dotenv()

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document



# === 1. CREATE STUDENT DOCUMENTS ===

doc1 = Document(
    page_content="Ali Raza is a dedicated software engineering student known for his strong problem-solving skills and consistent performance in programming courses. He actively participates in coding competitions and enjoys working on AI-based projects.",
    metadata={"department": "Software Engineering"}
)

doc2 = Document(
    page_content="Maria Khan is an electrical engineering student with a passion for embedded systems and robotics. She has worked on multiple hardware-related projects and is recognized for her practical approach to learning.",
    metadata={"department": "Electrical Engineering"}
)

doc3 = Document(
    page_content="Ahmed Bilal is a data science student who excels in statistics and machine learning. He frequently works on Kaggle datasets, builds predictive models, and contributes to open-source data science communities.",
    metadata={"department": "Data Science"}
)

doc4 = Document(
    page_content="Sara Malik is a cybersecurity student known for her interest in ethical hacking and network security. She has participated in several CTF competitions and regularly practices penetration testing techniques.",
    metadata={"department": "Cybersecurity"}
)

doc5 = Document(
    page_content="Usman Tariq is a computer science student with a strong command of algorithms and system design. He enjoys competitive programming and has represented his university in national-level programming contests.",
    metadata={"department": "Computer Science"}
)

docs = [doc1, doc2, doc3, doc4, doc5]



# === 2. GEMINI EMBEDDINGS ===
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004",        # Gemini embedding model
    google_api_key=os.getenv("GOOGLE_API_KEY")
)


# === 3. CHROMA VECTOR STORE ===
vector_store = Chroma(
    embedding_function=embeddings,
    persist_directory=r'C:\Users\Mushaf\Desktop\Lang Chain',
    collection_name='dataBase'
)

# Add documents
# vector_store.add_documents(docs)


# === 4. SEARCH ===
print("\n--- Similarity Search ---")
results = vector_store.similarity_search(
    query='Who is data Scientist',
    k=2
)
for r in results:
    print(r)


# === 5. SEARCH WITH SCORE ===
print("\n--- Similarity Search With Score ---")
results_score = vector_store.similarity_search_with_score(
    query='Who among these work in AI?',
    k=2
)
for r in results_score:
    print(r)



# === 7. UPDATE A DOCUMENT ===
updated_doc1 = Document(
    page_content="Sohail Hafeez is a software Engineering student from NUST and he is ambitious and intresting in AI",
    metadata={"team": "Royal Challengers Bangalore"}
)

id_to_update = "09a39dc6-3ba6-4ea7-927e-fdda591da5e4"   # Replace with real ID printed earlier
# vector_store.update_document(document_id=id_to_update, document=updated_doc1)
