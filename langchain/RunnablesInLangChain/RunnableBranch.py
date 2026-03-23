from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain.schema.runnable import RunnableSequence , RunnableBranch , RunnablePassthrough

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

parser = StrOutputParser()

prompt1 = PromptTemplate(
    template= "Write a long story on {topic}",
    input_variables= ['topic']
)

prompt2 = PromptTemplate(
    template= "Explain the story in the  {text} in 10 lines",
    input_variables= ['text']
)


StoryGenration = prompt1 | model | parser

branchChain = RunnableBranch(
    (lambda x : len(x.split())>300 , prompt2 | model | parser),
    RunnablePassthrough()
)

finalChain =  StoryGenration | branchChain
 
result = finalChain.invoke({"topic" : "Alexender the great"})

print(result)