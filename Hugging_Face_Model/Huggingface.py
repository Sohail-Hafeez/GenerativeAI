from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
import os

load_dotenv()

print("Loaded token:", os.getenv("HUGGINGFACEHUB_API_TOKEN"))

mistralai = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.2",   # ✅ chat-capable model
    task="text-generation",
    streaming=True,
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
)


model = ChatHuggingFace(llm=mistralai)
for data in model.stream("What is AI"):
    print(data.content , end="" , flush=True)

