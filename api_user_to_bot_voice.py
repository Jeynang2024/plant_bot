import logging
import os
import wave
import requests
import pyaudio
import speech_recognition as sr
from fastapi import FastAPI, UploadFile, File
from groq import Groq
from fastapi.responses import JSONResponse

# Initialize FastAPI
app = FastAPI()

# API Keys
GROQ_API_KEY="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"
stt_model = "whisper-large-v3"
FAISS_API_URL = "http://127.0.0.1:8000/query/"

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def transcribe_with_groq(audio_filepath):
    """Transcribe audio using Groq Whisper API."""
    client = Groq(api_key=GROQ_API_KEY)
    with open(audio_filepath, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model=stt_model,
            file=audio_file,
            language="en"
        )
    return transcription.text

@app.post("/transcribe-and-query/")
async def transcribe_and_query(audio_file: UploadFile = File(...)):
    """Accepts an audio file, transcribes it, queries FAISS, and returns the response."""
    try:
        # Save uploaded file
        temp_audio_path = f"temp_{audio_file.filename}"
        with open(temp_audio_path, "wb") as buffer:
            buffer.write(await audio_file.read())

        # Transcribe audio
        transcribed_text = transcribe_with_groq(temp_audio_path)
        logging.info(f"Transcription: {transcribed_text}")
        os.remove(temp_audio_path)  # Clean up

        # Query FAISS
        response = requests.get(f"{FAISS_API_URL}?question={transcribed_text}")
        faiss_response = response.json()

        return JSONResponse(content={
            "transcription": transcribed_text,
            "faiss_response": faiss_response
        })
    except Exception as e:
        logging.error(f"Error: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/")
def home():
    return {"message": "Speech to FAISS Query API is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
