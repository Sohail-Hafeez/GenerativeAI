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

   
    /* 🔽 Select boxes */
    div[data-baseweb="select"] > div {
        background-color: #121212 !important;
        color: white !important;
        border-radius: 8px;
        border: 2px solid white !important;
        font-size: 18px !important;
    }

    /* 🎯 Label text fix for Streamlit widgets */
    div.stSelectbox label, 
    div.stRadio label, 
    div.stTextInput label, 
    div.stNumberInput label,
    .stSelectbox > div:first-child > p {
        color: black !important;
        font-size: 28px !important;
        font-weight: bold !important;
    }

    /* 🟢 Button styling */
    .stButton>button {
        background-color: #121212;
        color: white;
        font-size: 18px;
        font-weight: bold;
        border: none;
        border-radius: 10px;
        padding: 0.75em 2em;
        transition: all 0.3s ease;
        margin-top: 1.5em;
    }

    .stButton>button:hover {
        background-color: #444444;
        transform: scale(1.03);
        cursor: pointer;
    }

    /* Smooth transitions */
    * {
        transition: all 0.3s ease-in-out;
    }
    </style>
""", unsafe_allow_html=True)

# App title
st.markdown("<h1>Research Paper Explainer</h1>", unsafe_allow_html=True)

# UI components
paper_input = st.selectbox(
    "Select Research Paper Name",
    [
        "Attention Is All You Need",
        "BERT: Pre-training of Deep Bidirectional Transformers",
        "GPT-3: Language Models are Few-Shot Learners",
        "Diffusion Models Beat GANs on Image Synthesis"
    ]
)

style_input = st.selectbox(
    "Select Explanation Style",
    ["Beginner-Friendly", "Technical", "Code-Oriented", "Mathematical"]
)

length_input = st.selectbox(
    "Select Explanation Length",
    ["Short (1-2 paragraphs)", "Medium (3-5 paragraphs)", "Long (detailed explanation)"]
)

# Create prompt
chatTemplate = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research assistant who explains research papers."),
    (
        "human",
        "Explain the research paper titled '{paper_input}' in a {style_input} style. "
        "The explanation should be {length_input}. Make it clear, accurate, and engaging."
    ),
])

# Button functionality
if st.button("Summarize"):
    with st.spinner("Generating explanation..."):
        chain = chatTemplate | model
        result = chain.invoke({
            "paper_input": paper_input,
            "style_input": style_input,
            "length_input": length_input
        })

        # Display result
        st.markdown(f"### Explanation for: *{paper_input}*")
        st.markdown(result.content if hasattr(result, "content") else str(result))
