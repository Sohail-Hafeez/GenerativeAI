from langchain_core.prompts import ChatPromptTemplate

chatTemplate = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful {domain} expert."),
        ("human", "Explain in simple terms, what is {topic}?")
    ]
)

prompt = chatTemplate.invoke({
    "domain": "cricket",
    "topic": "How many overs are in a one-day match?"
})

print(prompt)
