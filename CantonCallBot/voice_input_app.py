import base64

import numpy as np
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import wave
from flask_cors import CORS
import speech_recognition as sr
import soundfile as sf
import torchaudio
from torchaudio.transforms import Resample

import CantonCallBot.voice_to_text as voice_to_text
from pydub import AudioSegment

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app,debug=True,cors_allowed_origins='*')
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
def save_audio_chunk(audio_data):
    global counter
    global transcript_result
    filename = f"resources/voice_inputs/received_audio_{counter}.wav"
    print("Saving audio chunk")
    """
    Saves the received audio chunk to a WAV file. If the file doesn't exist, it creates it with proper headers.
    """
    with wave.open(filename, "wb") as wav_file:
        # These parameters should match the client's audio settings
        wav_file.setnchannels(1)
        wav_file.setsampwidth(4)
        wav_file.setframerate(16000.0)
        wav_file.writeframes(audio_data)

    print(f"Audio chunk saved to {filename}")
    wav_file.close()


    with wave.open(filename, 'rb') as wav_file:
        frames = wav_file.readframes(wav_file.getnframes())
        # Umwandlung in ein NumPy-Array
        # Stellen Sie sicher, dass der dtype und die Anzahl der Kanäle mit den WAV-Dateieinstellungen übereinstimmen
        audio_array = np.frombuffer(frames, dtype=np.int32).flatten()

    with wave.open(filename, "rb") as wav_file_r:
        wav_file_r.rewind()
    transcript_result = voice_to_text.transscribe(audio_array)

    print(f"Transcription result: {transcript_result}")
    transcript_result.append(transcript_result)
    counter = counter + 1



@socketio.on('voice_input')
def handle_message(audio_data):
    print('received message')

    save_audio_chunk(audio_data)

@socketio.on('voice_input_whole')
def handle_message(audio_data):
    print('received message')

    save_audio_chunk_whole(audio_data)

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


def transcribe_audio():
    global counter_whole
    transform_audio(f"resources/voice_inputs/whole_rec/received_audio_whole_{counter_whole}.wav")
    target_path = f"resources/voice_inputs/whole_rec/received_audio_whole_{counter_whole}_16.wav"
    print(f"transcribe: {target_path}")
    waveform, sample_rate = torchaudio.load(target_path)
    mid = waveform.squeeze(0)

    #audio_array = np.frombuffer(res, dtype=np.int32)
    res = vtt.transscribe(mid)
    print(f"Transscribed: {res}")


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
    transcribe_audio()

    counter_whole = counter_whole + 1

    send_wav_file("resources/voice_inputs/Die Stadt Zürich lie.wav")


def send_wav_file(file_path):
    with open(file_path, "rb") as wav_file:
        wav_data = wav_file.read()
        encoded_data = base64.b64encode(wav_data).decode('utf-8')
        socketio.emit('voice_output_whole', {'data': encoded_data})






if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=8000, debug= True, allow_unsafe_werkzeug=True)
