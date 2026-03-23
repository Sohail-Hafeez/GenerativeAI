from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnableParallel

load_dotenv()

# Model 1: Google Gemini
model1 = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# Model 2: HuggingFace model
model2 = ChatHuggingFace(
    llm = HuggingFaceEndpoint(
        repo_id="meta-llama/Llama-3.1-8B-Instruct",  
        task="text-generation"
    )
)

# prompt number 1 
prompt1 = PromptTemplate(
    template='Generate short and simple notes from the following text \n {text}',
    input_variables=['text']
)

# prompt number 2
prompt2 = PromptTemplate(
    template='Generate 5 short question answers from the following text \n {text}',
    input_variables=['text']
)

prompt3 = PromptTemplate(
    template='Merge the provided notes and quiz into a single document \n notes -> {notes} and quiz -> {quiz}',
    input_variables=['notes', 'quiz']
)

parser = StrOutputParser()

parallelChain = RunnableParallel({
    'notes' : prompt1 | model1 | parser,
    'quiz' : prompt2 | model2 | parser
})

mergeChain = prompt3 | model1 | parser

chain = parallelChain | mergeChain

text = """
Neural Networks are powerful computational models inspired by the structure and functioning of the human brain. 
They consist of interconnected layers of artificial neurons, where each neuron receives input, applies a 
mathematical transformation, and passes the output to the next layer. This layered structure enables neural networks 
to learn complex patterns, relationships, and representations from data.

A basic neural network includes three main components: an input layer, one or more hidden layers, and an output layer. 
Each connection between neurons carries a weight that gets adjusted during training through algorithms such as 
backpropagation and gradient descent. These adjustments help the model minimize error and improve prediction accuracy.

Neural networks excel in various fields such as image recognition, speech processing, natural language understanding, 
predictive analytics, and autonomous systems. Modern deep neural networks, with many hidden layers, have dramatically 
advanced the capabilities of artificial intelligence by enabling machines to perform tasks once thought impossible.

Overall, neural networks are foundational to deep learning and play a crucial role in building intelligent systems 
capable of learning, adapting, and making decisions from large amounts of data.
"""


result = chain.invoke({'text': text})

print(result)

chain.get_graph().print_ascii()