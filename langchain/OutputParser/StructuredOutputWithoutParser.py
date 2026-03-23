from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StructuredOutputParser , ResponseSchema
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

schema = [
    ResponseSchema(name='fact1', description='fact 1 about the topic'),
    ResponseSchema(name='fact2', description='fact 2 about the topic'),
    ResponseSchema(name='fact3', description='fact 3 about the topic'),
]

parser = StructuredOutputParser.from_response_schemas(schema)

template = PromptTemplate(
    template="Give me three facts about the {topic}.\n{format_instruction}",
    input_variables=["topic"],
    partial_variables={"format_instruction": parser.get_format_instructions()}
)

prompt = template.invoke({"topic": "Black Hole"})
result = model.invoke(prompt)

finalResult = parser.parse(result.content)

print(finalResult)
