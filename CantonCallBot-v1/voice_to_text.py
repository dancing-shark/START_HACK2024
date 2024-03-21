from transformers import Wav2Vec2ForCTC, AutoProcessor
import torch
from CantonCallBot.resources.record_audio import record_audio




class VoiceToText:
    def __init__(self):
        model_id = "facebook/mms-1b-all"
        self.processor = AutoProcessor.from_pretrained(model_id)
        self.model = Wav2Vec2ForCTC.from_pretrained(model_id)


    def transscribe(self, recording, sample_rate=16000):
        # Preprocess the recording
        input_values = self.processor(recording, sampling_rate=sample_rate, return_tensors="pt").input_values

        # Perform the prediction
        with torch.no_grad():
            logits = self.model(input_values).logits

        # Decode the predicted ids to the transcription
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = self.processor.batch_decode(predicted_ids)[0]

        return transcription