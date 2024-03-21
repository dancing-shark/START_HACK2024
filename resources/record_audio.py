import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

def record_audio(duration, sample_rate=16000):
    """
    Record audio from the microphone.

    Parameters:
    - duration: Length of the recording in seconds.
    - sample_rate: Sampling rate of the audio recording.

    Returns:
    - A NumPy array with the recorded audio.
    """
    print("Recording...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
    sd.wait()  # Wait until recording is finished
    print("Recording stopped.")
    return recording.flatten()
