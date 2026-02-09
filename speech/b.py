import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

# Load .env
load_dotenv()

# Read from environment
speech_key = os.environ.get("AZURE_SPEECH_KEY")
region = os.environ.get("AZURE_SPEECH_REGION")

# Initialize speech config
speech_config = speechsdk.SpeechConfig(
    subscription=speech_key,
    region=region
)

# Choose voice
speech_config.speech_synthesis_voice_name = "ur-PK-AsadNeural"

# Output file
audio_config = speechsdk.audio.AudioOutputConfig(filename="outputt2.wav")

# Create synthesizer
synthesizer = speechsdk.SpeechSynthesizer(
    speech_config=speech_config,
    audio_config=audio_config
)

# Text to speak
text = "hello tum kon ho"

# Synthesize speech
result = synthesizer.speak_text(text)

if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print("Speech synthesized successfully")
else:
    print("Error:", result.reason)
