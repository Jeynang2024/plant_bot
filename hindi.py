import pyaudio
import wave
import requests
import time
from mic import *
API_KEY_ASSEMBLYAI = "cb7b688c85b64d168a393d7bdd08d65c"

upload_endpoint = "https://api.assemblyai.com/v2/upload"
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"
headers = {'authorization': API_KEY_ASSEMBLYAI}

# Function to record audio


# Function to upload recorded audio
def upload(filename):
    def read_file(filename, chunk_size=5242880):
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data

    upload_response = requests.post(upload_endpoint, headers=headers, data=read_file(filename))
    return upload_response.json().get('upload_url')

# Function to transcribe and translate audio
def transcribe_and_translate(audio_url):
    transcript_request = {
        "audio_url": audio_url,
        "language_code": "hi",  # Hindi input
        "translate_to": ["en"]  # Translate to English
    }
    transcript_response = requests.post(transcript_endpoint, json=transcript_request, headers=headers)
    return transcript_response.json().get('id')

# Function to poll transcription status
def poll(transcript_id):
    polling_endpoint = transcript_endpoint + '/' + transcript_id
    polling_response = requests.get(polling_endpoint, headers=headers)
    return polling_response.json()

# Function to get translated transcription result
def get_transcription_result(audio_url):
    transcript_id = transcribe_and_translate(audio_url)
    while True:
        data = poll(transcript_id)
        if data['status'] == 'completed':
            return data.get('text')  # This will now be in English
        elif data['status'] == 'error':
            return None
        time.sleep(5)

# Print only the translated text
def print_transcript(audio_url):
    text = get_transcription_result(audio_url)
    if text:
        print(text)

# Main execution
if __name__ == "__main__":
    recorded_file = record_audio()  # Record and save as "output.wav"
    audio_url = upload(recorded_file)  # Upload recorded audio
    print_transcript(audio_url)  # Print translated English text
