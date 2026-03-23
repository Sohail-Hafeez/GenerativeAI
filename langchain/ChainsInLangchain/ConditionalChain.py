from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain.schema.runnable import RunnableBranch, RunnableLambda
from pydantic import BaseModel, Field
from typing import Literal

load_dotenv()

# Model
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# Parsers
parser = StrOutputParser()

class Feedback(BaseModel):
    sentiment: Literal['positive', 'negative'] = Field(description='Sentiment of the feedback')

parser2 = PydanticOutputParser(pydantic_object=Feedback)

# Prompt 1: Sentiment classification
prompt1 = PromptTemplate(
    template='Classify the sentiment of the following feedback text into positive or negative \n {feedback} \n {format_instruction}',
    input_variables=['feedback'],
    partial_variables={'format_instruction': parser2.get_format_instructions()}
)

classifierChain = prompt1 | model | parser2  # Output will be a Pydantic object

# Prompts for responses
prompt_positive = PromptTemplate(
    template='Write an appropriate response to this positive feedback: \n {feedback}',
    input_variables=['feedback']
)

prompt_negative = PromptTemplate(
    template='Write an appropriate response to this negative feedback: \n {feedback}',
    input_variables=['feedback']
)

# Branch based on sentiment
branch_chain = RunnableBranch(
    (lambda x: x.sentiment == 'positive', prompt_positive | model | parser),
    (lambda x: x.sentiment == 'negative', prompt_negative | model | parser),
    RunnableLambda(lambda x: "Could not determine sentiment")
)

# Full chain
chain = classifierChain | branch_chain

# Test
result = chain.invoke({'feedback': 'This is a beautiful phone'})
print(result)

# Optional: visualize
chain.get_graph().print_ascii()
