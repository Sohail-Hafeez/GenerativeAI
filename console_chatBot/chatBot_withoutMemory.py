from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model = "gemini-2.5-flash")

while True:
    userInput = input("YOU : " )
    if userInput == "exit" or userInput == "Exit":
        print("AI : Bye Bye If you need any assistance in future feel free to ask me....  ")
        break
    else:
        result = model.invoke(userInput)
        print("AI : " , result.content)
        