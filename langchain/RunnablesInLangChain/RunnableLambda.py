from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain.schema.runnable import RunnableSequence , RunnableParallel , RunnablePassthrough , RunnableLambda

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

parser = StrOutputParser()

def wordCount(text):
    return len(text.split())

prompt1 = PromptTemplate(
    template= "Write only one joke on {topic}",
    input_variables= ['topic']
)

genratingJoke = prompt1 | model | parser

parallelChain = RunnableParallel({
    'joke' : RunnablePassthrough(),
    'words' : RunnableLambda(wordCount)
})

result =  genratingJoke | parallelChain

FinalResult = result.invoke({"topic" : "Software Enginnering"})

print(FinalResult)