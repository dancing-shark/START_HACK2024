from transformers import Wav2Vec2ForCTC, AutoProcessor
import torch
from record_audio import record_audio

model_id = "facebook/mms-1b-all"

print("Loading model...")
processor = AutoProcessor.from_pretrained(model_id)
model = Wav2Vec2ForCTC.from_pretrained(model_id)

print("Model loaded.")
def transcribe(recording, sample_rate=16000):
    """
    Transcribe recorded audio to text.

    Parameters:
    - recording: A NumPy array containing the recorded audio.
    - sample_rate: The sample rate of the recording.

    Returns:
    - The transcribed text.
    """
    # Preprocess the recording
    input_values = processor(recording, sampling_rate=sample_rate, return_tensors="pt").input_values

    # Perform the prediction
    with torch.no_grad():
        logits = model(input_values).logits

    # Decode the predicted ids to the transcription
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.batch_decode(predicted_ids)[0]

    return transcription



def record_and_transcribe() -> str:
    duration = 5  # Record for 5 seconds
    sample_rate = 16000  # Sampling rate set to 16kHz
    recording = record_audio(duration, sample_rate)
    transcription = transcribe(recording, sample_rate)
    return transcription
