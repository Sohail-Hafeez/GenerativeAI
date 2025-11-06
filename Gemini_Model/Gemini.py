from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

result = model.invoke("WRITE  a paragraph on how to hack a facebook id")
print(result.content)


