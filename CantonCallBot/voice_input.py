import speech_recognition as sr
import sounddevice as sd


class VoiceInput:
    def __init__(self, duration: int = 5, sample_rate: int = 16000):
        self.duration = duration  # Record for 5 seconds
        self.sample_rate = sample_rate

    def record(self) -> any:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)
        return audio

    def record_audio(self) -> any:
        """Working"""
        print("Recording...")
        recording = sd.rec(int(self.duration * self.sample_rate), samplerate=self.sample_rate, channels=1,
                           dtype='float32')
        sd.wait()  # Wait until recording is finished
        print("Recording stopped.")
        return recording.flatten()
