import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Create model (gemini-1.5-flash is free and fast)
model = genai.GenerativeModel("gemini-2.5-flash")

# Load image
img = Image.open("a.png")

# Generate a short caption
response = model.generate_content(
    ["Generate a short and engaging caption for this image.", img]
)

# Print the caption text
print(response.text)
