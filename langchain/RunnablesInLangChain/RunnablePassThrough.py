from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain.schema.runnable import RunnableSequence , RunnableParallel , RunnablePassthrough

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

parser = StrOutputParser()

prompt1 = PromptTemplate(
    template= "Write only one joke on {topic}",
    input_variables= ['topic']
)

prompt2 = PromptTemplate(
    template= "Explain the joke in the  {text}",
    input_variables= ['text']
)

genratingJoke = prompt1 | model | parser

parallelChain = RunnableParallel({
    'joke' : RunnablePassthrough(),
    'Expalanation' : prompt2 | model | parser
})

result =  genratingJoke | parallelChain

FinalResult = result.invoke({"topic" : "Software Enginnering"})

print(FinalResult)