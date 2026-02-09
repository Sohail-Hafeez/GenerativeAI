from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI

# Define your structured output model
class Review(BaseModel):
    sentiment: str
    rating: int
    summary: str

# Initialize model
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key="YOUR_API_KEY")

# Get a structured output model
structured_model = model.with_structured_output(Review)

# Test
result = structured_model.invoke("The product is awesome and mind-blowing! Totally worth it.")

print(result)
