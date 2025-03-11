import requests
#from api_secrets import API_KEY_ASSEMBLYAI
import sys
API_KEY_ASSEMBLYAI = "cb7b688c85b64d168a393d7bdd08d65c"
#uploading of file
from mic import *
import time
from connect import *
upload_endpoint = "https://api.assemblyai.com/v2/upload"
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"
headers = {'authorization':API_KEY_ASSEMBLYAI}

def upload(filename):
    def read_file(filename , chunk_size=5242880):
        with open(filename,'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data


    upload_response = requests.post(upload_endpoint,headers=headers,data=read_file(filename))
    

    audio_url = upload_response.json()['upload_url']
    return audio_url

#transcribe
def transcribe(audio_url):
    transcript_request = {"audio_url" : audio_url}
    transcript_response = requests.post(transcript_endpoint,json = transcript_request, headers=headers)
    
    job_id=transcript_response.json()['id']
    return job_id





#poll
def poll(transcript_id):
    polling_endpoint = transcript_endpoint + '/' + transcript_id
    polling_response=requests.get(polling_endpoint, headers =headers)
    return polling_response.json()

def get_transcription_result_url(audio_url):
    transcript_id = transcribe(audio_url)
    while(True):
        data = poll(transcript_id)
        
        if data['status'] == 'completed':
            return data,None
        elif data['status'] == 'error':
            return data, data['error']
        time.sleep(10)

#save transcription into text file

def save_transcript(audio_url):
    data , error = get_transcription_result_url(audio_url)   

    if data:
       
        print("\ntranscription:\n",data['text'])
        user_query=data['text']
        #print(user_query)
        response=qa_chain.invoke({'query': user_query})
        print("RESULT: ", response["result"])
    elif error :
        print("Error!!" , error)

if __name__ == "__main__":
    recorded_file = record_audio()  # Record and save as "output.wav"
    audio_url = upload(recorded_file)  # Upload recorded audio
    save_transcript(audio_url)
    