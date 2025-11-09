from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()

# Initialize Gemini model
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# Inject custom CSS for modern UI
st.markdown("""
    <style>
    /* 🌙 Background & general text */
    .stApp {
        background-color: #42b883;
        color: black;
        font-family: 'Poppins', sans-serif;
    }

    /* 🧠 Header styling */
    h1, h2, h3 {
        color: black;
        text-align: center;
        font-weight: 700;
        margin-bottom: 20px;
        font-size: 24px;
    }

    /* Custom h5 styling */
    h5 {
        color: #000000 !important;
        font-size: 24px !important;
        font-weight: 700 !important;
        text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.3);
        margin-bottom: 5px !important;
    }

    /* 🎯 Label text for Streamlit widgets */
    div.stTextInput label,
    div.stTextArea label {
        color: #000000 !important;
        font-size: 40px !important;
        font-weight: 700 !important;
        text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.3);
        margin-bottom: 5px !important;
    }

    /* Remove space between label and text area */
    div.stTextArea {
        margin-top: 0px !important;
    }

    div.stTextArea > label {
        margin-bottom: 5px !important;
    }

    /* 🔹 Text input / Text area styling */
    div.stTextInput>div>div>input,
    div.stTextArea>div>div>textarea {
        background-color: #000000 !important;
        border: 2px solid #ffffff !important;
        border-radius: 10px !important;
        color: #ffffff !important;
        font-size: 18px !important;
        margin-top: 0px !important;
    }
    div.stTextInput>div>div>input::placeholder,
    div.stTextArea>div>div>textarea::placeholder {
        color: rgba(255, 255, 255, 0.5) !important;
    }

    
    /* 🟢 Button styling */
    .stButton>button {
        background-color: black;
        color: white;
        font-size: 18px;
        font-weight: bold;
        border: none;
        border-radius: 10px;
        padding: 0.75em 2em;
        transition: all 0.3s ease;
        text-align:center;
        margin-left: 250px;
        width:160px;
        margin-bottom:10px;
    }

    .stButton>button:active {
        background-color: black !important;
        transform: scale(0.9);
        cursor: pointer;
    }

    
    .stButton>button:hover {
        background-color: black !important;
        cursor: pointer;
    }
    /* Smooth transitions */
    * {
        transition: all 0.3s ease-in-out;
    }
    </style>
""", unsafe_allow_html=True)

# App title
st.markdown("<h1>Text Decryption Tool</h1>", unsafe_allow_html=True)

# Custom label
st.markdown("<h5 style='margin-bottom: 0px;'> Enter the text </h5>", unsafe_allow_html=True)

# Text area input
decrypt_text = st.text_area("",height=60, placeholder="Enter your text here...", label_visibility="collapsed")

# Create prompt
chatTemplate = ChatPromptTemplate.from_messages([
    ("system", "You are an expert who can encrypt and decrypt keys and has vast knowledge about it."),
    (
        "human",
        "Decrypt and explain the key '{decrypt_text}' in very simple English. "
        "The explanation should be not too long and not too short."
    ),
])

# Button functionality
if st.button("Submit"):
    if decrypt_text.strip() == "":
        st.warning("Please enter some text to decrypt!")
    else:
        with st.spinner("Generating explanation..."):
            chain = chatTemplate | model
            result = chain.invoke({
                "decrypt_text": decrypt_text
            })
        st.markdown(f"<p style='font-size: 30px; font-weight: 900; color: black; text-align:center'><strong>Given Input to decrypt = </strong> {decrypt_text}</p>", unsafe_allow_html=True)
        st.markdown(f"**Decryption Explanation:** {result.content if hasattr(result, 'content') else str(result)}")