from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Chat Prompt Template
chatTemplate = ChatPromptTemplate.from_messages(
    [
        ('system', 'You are a helpful student support agent.'),
        MessagesPlaceholder(variable_name='chatHistory'),
        ('human', '{query}')
    ]
)

# Load and parse the chat history file
chatHistory = []
try:
    with open('chatHistory.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith("HumanMessage"):
                # Extract content inside quotes
                content = line.split('content =', 1)[1].strip().strip('")(').replace('")', '').replace('("', '').replace('"', '')
                chatHistory.append(HumanMessage(content=content))
            elif line.startswith("AIMessage"):
                content = line.split('content =', 1)[1].strip().strip('")(').replace('")', '').replace('("', '').replace('"', '')
                chatHistory.append(AIMessage(content=content))
except FileNotFoundError:
    open('chatHistory.txt', 'w').close()

print("Loaded chat history:")
for msg in chatHistory:
    print(f"{msg.type.capitalize()}: {msg.content}")

# Build the prompt
prompt = chatTemplate.invoke({
    'chatHistory': chatHistory,
    'query': 'Where is my money?'
})

print("\nFinal Prompt:")
print(prompt)
