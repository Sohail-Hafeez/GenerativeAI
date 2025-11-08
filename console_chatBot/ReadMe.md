# Console based Chatbot

This project implements a **console-based chatbot** powered by **Google Gemini** (via LangChain).  
It includes two variants:
1. `chatBot_withMemory.py` — maintains conversation history for contextual replies.  
2. `chatBot_withoutMemory.py` — stateless chatbot that handles one prompt at a time.



## Setup
1. Open your VS code or any IDE and setup a folder 
2. Now create a Virtual Enviroment by opening new terminal and typing `python -m venv venv`
3. Now activate your venv by entering  `venv\Scripts\activate`
4. Run `pip install -r requirements.txt`
5. Go to Google AI studio and Create a API key
6. copy that and paste in .env file
7. run `chatBot_withMemory.py` and this `chatBot_withoutMemory.py`


# chatBot_withoutMemory

![WhatsApp Image 2025-11-08 at 12 09 59_02ce2de7](https://github.com/user-attachments/assets/02ba34e4-b415-438c-9ae9-9c784142c183)

# chatBot_withMemory

![WhatsApp Image 2025-11-08 at 12 22 03_83318c35](https://github.com/user-attachments/assets/2368ab43-6c33-4360-84b9-0fe20e1f155a)

# Messages

Now lets talk about what are masseges that are used in message.py file
There are 3 types of messages
1. System Message  (Assigning a role to our model or simply telling it its duty)
2. Humman Message  (The prompt that user enter)
3. AI Message  (The response of AI)

# Why do we need Messages?
Now in the above `chatBot_withMemory.py` we made a chat memory by simply appending each user and Ai message into chatHistory. Now the problem is that we cannot distinguish between the messages that either it is from user or AI
Hence the concept of messages sorts this out really Well

![WhatsApp Image 2025-11-08 at 13 28 47_94e67ebc](https://github.com/user-attachments/assets/7a787b7f-1e55-49d2-a488-f889a3edcb62)

# Chat Prompt Template 
Up till now we have only discussed about static prompts what if we have dynammic prompts
A dynamic prompt is a prompt whose content changes automatically at runtime based on user input variables or context rather than being fixed in advance.
They make your AI apps:
1. Reusable : same template can adapt to different queries.
2. Contextual : inject real time info, chat history, user role, or environment data.
3. Personalized : tailor output per user or session.

![WhatsApp Image 2025-11-08 at 14 09 16_3ed9aaee](https://github.com/user-attachments/assets/f81cd75b-b653-4b69-8eb7-af3837c947cf)

# Message Place Holders

To understand the concept of a message placeholder, consider the following example:
Imagine you are a student at a university. After graduating, instead of directly contacting the administration office or visiting the campus, you communicate with an AI support chatbot provided by the university.
For instance, you ask, “What about my security refund?” and the chatbot replies, “Your security deposit will be transferred to your account within 5 to 10 working days.”
A few days later, you return and ask again, “What’s the status of my refund?” Even though time has passed, the chatbot should still remember your previous conversation to respond appropriately.
To enable this continuity of conversation — where the chatbot recalls previous messages and maintains context — we use message placeholders. These placeholders store and represent the ongoing chat history between the user and the AI, allowing the chatbot to deliver context-aware responses.

![WhatsApp Image 2025-11-08 at 14 08 24_f05e937f](https://github.com/user-attachments/assets/d0b08916-a11b-4d07-ad87-821c24b456a8)




