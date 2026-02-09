import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk
from langchain_google_genai import ChatGoogleGenerativeAI

# =====================
# Load ENV
# =====================
load_dotenv()
AZURE_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_REGION = os.getenv("AZURE_SPEECH_REGION")

# =====================
# Azure Speech Config
# =====================
speech_config = speechsdk.SpeechConfig(
    subscription=AZURE_KEY,
    region=AZURE_REGION
)

# Default voice
speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"
speech_config.speech_recognition_language = "en-US"

audio_input = speechsdk.audio.AudioConfig(use_default_microphone=True)
audio_output = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

recognizer = speechsdk.SpeechRecognizer(
    speech_config=speech_config,
    audio_config=audio_input
)

synthesizer = speechsdk.SpeechSynthesizer(
    speech_config=speech_config,
    audio_config=audio_output
)

# =====================
# LLM
# =====================
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# =====================
# Helpers
# =====================
def speak(text: str):
    synthesizer.speak_text(text)

# =====================
# Voice Assistant Loop
# =====================
print("Voice Assistant Started. Say 'exit' to quit.")

conversation = []

while True:
    print("\nListening...")
    result = recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        user_text = result.text.strip()
        print("You:", user_text)

        if "exit" in user_text.lower():
            print("Exiting...")
            break

        # Language detection (Urdu vs English)
        if any('\u0600' <= c <= '\u06FF' for c in user_text):
            speech_config.speech_recognition_language = "ur-PK"
            speech_config.speech_synthesis_voice_name = "ur-PK-UzmaNeural"
        else:
            speech_config.speech_recognition_language = "en-US"
            speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"

        # Context (last 6 turns)
        conversation.append(f"User: {user_text}")
        context = "\n".join(conversation[-6:])

        try:
            ai_reply = model.invoke(context)   # 🔴 returns AIMessage
            ai_text = ai_reply.content         # ✅ FIX
        except Exception as e:
            print("Model Error:", e)
            ai_text = "Sorry, I could not process that."

        print("Assistant:", ai_text)
        speak(ai_text)

        conversation.append(f"Assistant: {ai_text}")

    elif result.reason == speechsdk.ResultReason.Canceled:
        details = speechsdk.CancellationDetails(result)
        print("STT Cancelled:", details.reason, details.error_details)
