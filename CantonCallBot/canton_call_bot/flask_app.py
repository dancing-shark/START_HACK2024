import base64
import os
from dotenv import load_dotenv

import numpy as np
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import wave
from flask_cors import CORS
import speech_recognition as sr
import soundfile as sf
import torchaudio
from langchain_community.embeddings.cohere import CohereEmbeddings
from langchain_groq import ChatGroq
from torchaudio.transforms import Resample

import core.voice_to_text as voice_to_text
from pydub import AudioSegment

from core.text_analysis import Call
from core.text_to_voice import TextToVoice
from core.voice_input import VoiceInput
from core.voice_output_elevenLabs import TextToVoice as TTT

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, debug=True, cors_allowed_origins='*')
vtt = voice_to_text.VoiceToText()

counter = 0
counter_whole = 0

transcript_result = []


@app.route('/')
def index():
    return "Test"


@app.route('/operation')
def operation():
    return "Test"

@socketio.on('voice_input_whole')
def handle_message(audio_data):
    print('received message')

    filename = save_audio_chunk_whole(audio_data)
    res = transcribe_audio()
    res = call.process_with_retrieval(res)
    print(res)
    ttt.generate(res)
    #test
    #send_wav_file("resources/test_files/Die Stadt Zürich lie.wav")
    # real
    send_wav_file("resources/voice_outputs/synthesized_speech.wav")


def load_audio_file(file_path):
    global counter_whole
    waveform, sample_rate = torchaudio.load(file_path)

    resampled_waveform = Resample(48000, 16000)(waveform)

    target_path = f"resources/voice_inputs/whole_rec/received_audio_whole_{counter_whole}_16.wav"
    torchaudio.save(target_path, resampled_waveform, 16000)

    recognizer = sr.Recognizer()
    with sr.AudioFile(target_path) as source:
        audio_data = recognizer.record(source)
    return audio_data.get_wav_data()


def transform_audio(file_path):
    global counter_whole
    waveform, sample_rate = torchaudio.load(file_path)

    resampled_waveform = Resample(48000, 16000)(waveform)

    target_path = f"resources/voice_inputs/whole_rec/received_audio_whole_{counter_whole}_16.wav"
    print(f"transform: {target_path}")
    torchaudio.save(target_path, resampled_waveform, 16000)


def transcribe_audio() -> str:
    global counter_whole
    transform_audio(f"resources/voice_inputs/whole_rec/received_audio_whole_{counter_whole}.wav")
    target_path = f"resources/voice_inputs/whole_rec/received_audio_whole_{counter_whole}_16.wav"
    print(f"transcribe: {target_path}")
    waveform, sample_rate = torchaudio.load(target_path)
    mid = waveform.squeeze(0)

    # audio_array = np.frombuffer(res, dtype=np.int32)
    res = vtt.transcribe(mid)
    print(f"Transcribed: {res}")
    return res


def save_audio_chunk_whole(data):
    print("Audiodatei empfangen")
    global counter_whole
    global transcript_result
    filename = f"resources/voice_inputs/whole_rec/received_audio_whole_{counter_whole}.wav"

    with wave.open(filename, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(4)
        wav_file.setframerate(48000.0)
        wav_file.writeframes(data)
    print(f"Audiodatei gespeichert: {filename}")

    # counter_whole = counter_whole + 1
    return filename




def send_wav_file(file_path):
    print("Send wav file")
    with open(file_path, "rb") as wav_file:
        wav_data = wav_file.read()
        encoded_data = base64.b64encode(wav_data).decode('utf-8')
        socketio.emit('voice_output_whole', {'data': encoded_data})


if __name__ == '__main__':
    dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    load_dotenv(dotenv_path=dotenv_path)
    cohere_api_key = os.getenv('COHERE_API_KEY') 
    groq_api_key = os.getenv('GROQ_API_KEY') 
    path = os.getenv('CHROMA_DB_PATH') 
    chat = ChatGroq(temperature=0, groq_api_key=groq_api_key, model_name="mixtral-8x7b-32768")
    embeddings_model_x = CohereEmbeddings(model="embed-multilingual-v3.0")

    call = Call(1, chat, embeddings_model=embeddings_model_x, path_db=path)
    mic = VoiceInput()
    vtt = voice_to_text.VoiceToText()
    # ttv = TextToVoice()
    ttt = TTT(use_elevenlabs_api=False)

    socketio.run(app, host="0.0.0.0", port=8000, debug=True, allow_unsafe_werkzeug=True)
