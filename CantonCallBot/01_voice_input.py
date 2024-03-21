import speech_recognition as sr

def record() -> any:
    r = sr.Recognizer()
    with sr.Microphone() as source:
       print("Say something!")
       audio = r.listen(source)
    return audio



from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import wave
from flask_cors import CORS
from 02_speech_to_text import transcribe
import eventlet

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app,debug=True,cors_allowed_origins='*')

counter = 0

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
        wav_file.setframerate(48000.0)
        wav_file.writeframes(audio_data)

    recording = wave.open(filename, "rb")
    print(f"Audio chunk saved to {filename}")
    counter = counter + 1
    transcript_result = transcribe(recording.readframes(recording.getnframes()), 48000)
    print(f"Transcription result: {transcript_result}")
    transcript_result.append(transcript_result)

@socketio.on('voice_input')
def handle_message(audio_data):
    print('received message')

    save_audio_chunk(audio_data)


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=8000, debug= True, allow_unsafe_werkzeug=True)
