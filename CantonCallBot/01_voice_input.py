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
import eventlet

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app,debug=True,cors_allowed_origins='*')

counter = 0


@app.route('/')
def index():
    return "Test"


@app.route('/operation')
def operation():
    return "Test"
def save_audio_chunk(audio_data, filename=f"received_audio_{counter}.wav"):
    global counter
    """
    Saves the received audio chunk to a WAV file. If the file doesn't exist, it creates it with proper headers.
    """
    with wave.open(filename, "ab") as wav_file:
        # These parameters should match the client's audio settings
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(48000.0)
        wav_file.writeframes(audio_data)
    print(f"Audio chunk saved to {filename}")
    counter += 1

@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)
    emit('message', {'data': message})

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=8000, debug= True, allow_unsafe_werkzeug=True)
