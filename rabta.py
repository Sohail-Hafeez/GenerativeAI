from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from gtts import gTTS
from playsound import playsound
import os
import random

# Load .env (must contain GOOGLE_API_KEY)
load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

chatHistory = []
while True:
    userInput = input("YOU : ")
    chatHistory.append(userInput)
    
    if userInput.lower() == "exit":
        print("AI : Bye Bye If you need any assistance in future feel free to ask me....")
        
        farewell = "farewell.mp3"
        tts = gTTS("Bye Bye If you need any assistance in future feel free to ask me.", lang="en")
        tts.save(farewell)
        playsound(farewell)
        os.remove(farewell)
        break

    # Generate AI text
    result = model.invoke(chatHistory)
    ai_text = result.content
    chatHistory.append(ai_text)

    # Convert to audio
    filename = f"reply_{random.randint(1000,9999)}.mp3"

    try:
        tts = gTTS(ai_text, lang="en")
        tts.save(filename)
        print("AI : (Audio Reply Playing)")
        playsound(filename)
        os.remove(filename)

    except Exception as e:
        print("AI (Error Fallback):", ai_text)
