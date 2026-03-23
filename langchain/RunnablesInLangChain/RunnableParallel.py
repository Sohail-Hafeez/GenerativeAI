from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain.schema.runnable import RunnableSequence , RunnableParallel

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

parser = StrOutputParser()

prompt1 = PromptTemplate(
    template= "Write a facebook post on {topic}",
    input_variables= ['topic']
)


prompt2 = PromptTemplate(
    template= "Write a Linkdyn post on {topic}",
    input_variables= ['topic']
)

parallelChains = RunnableParallel({
    'facebook' : prompt1 | model | parser,
    'linkdyn' : prompt2 | model | parser    
})

result = parallelChains.invoke({"topic" : "AI"})

print(result["linkdyn"])

