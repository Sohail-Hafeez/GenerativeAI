from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnableParallel


load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

prompt1 = PromptTemplate(
    template = "Wriet a detailed paragraph describing the importance of {topic}",
    input_variables= ['topic']
)


prompt2 = PromptTemplate(
    template = "Summerize the given {text} in easy wording with in 5-6 points",
    input_variables= ['text']
)


parser = StrOutputParser()

chain = prompt1 | model | parser | prompt2 | model | parser

result = chain.invoke({"topic":"Logistic Regression"})

print(result)

chain.get_graph().print_ascii()