from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

prompt = PromptTemplate(
    template = "Wriet five lines on beauty of {city}",
    input_variables= ['city']
)

parser = StrOutputParser()

chain = prompt | model | parser

result = chain.invoke({'city':'Rawalpindi'})

print(result)