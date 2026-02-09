import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

# Load the .env file
load_dotenv()

# Read values from environment
speech_key = os.environ.get("AZURE_SPEECH_KEY")
region = os.environ.get("AZURE_SPEECH_REGION")

# Initialize Azure Speech config
speech_config = speechsdk.SpeechConfig(
    subscription=speech_key,
    region=region
)

speech_config.speech_recognition_language = "en-US"

# Microphone input
audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
recognizer = speechsdk.SpeechRecognizer(
    speech_config=speech_config,
    audio_config=audio_config
)

print("Speak now...")
result = recognizer.recognize_once()

if result.reason == speechsdk.ResultReason.RecognizedSpeech:
    print("Recognized:", result.text)
else:
    print("Error:", result.reason)
