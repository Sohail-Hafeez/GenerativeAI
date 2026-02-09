import os
import shutil
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain.text_splitter import RecursiveCharacterTextSplitter

load_dotenv

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

# Using API to fetch the transcript

from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

def fetchTranscript(video_id):
    """
    Fetch transcript in Urdu, Hindi, or English (in priority order).
    """

    # Priority: Urdu → Hindi → English
    lang_priority = ["ur", "hi", "en"]

    try:
        # Try to fetch transcript in any of these languages
        transcript_list = YouTubeTranscriptApi.get_transcript(
            video_id,
            languages=lang_priority
        )

        # Convert chunks → plain text
        transcript = " ".join(chunk["text"] for chunk in transcript_list)

        print("\n--- Transcript Found ---\n")
        print(transcript)
        return transcript

    except NoTranscriptFound:
        print("❌ No transcript available in Urdu, Hindi, or English.")
        return None

    except TranscriptsDisabled:
        print("❌ Captions are disabled for this video.")
        return None

    except Exception as e:
        print(f"⚠ Error: {e}")
        return None
    

url = "J5_-l7WIO_w&list"
transcript = fetchTranscript(url)


#  Text splitting 
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.create_documents([transcript])

#  Retrieval
retriever = vector_store.as_retriever(search_type = "similarity", search_kwargs={"k" : 4})



