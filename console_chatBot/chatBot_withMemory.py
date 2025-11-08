from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model = "gemini-2.5-flash")

chatHistory = []
while True:
    userInput = input("YOU : " )
    chatHistory.append(userInput)
    if userInput == "exit" or userInput == "Exit":
        print("AI : Bye Bye If you need any assistance in future feel free to ask me....  ")
        break
    else:
        result = model.invoke(chatHistory)
        chatHistory.append(result)
        print("AI : " , result.content)
        