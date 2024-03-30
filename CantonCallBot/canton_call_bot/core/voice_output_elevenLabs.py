import requests
import scipy.io.wavfile
import numpy as np
from transformers import VitsTokenizer, VitsModel, set_seed
import torch
import os
class TextToVoice:
    voice_output_file_path: str = "canton_call_bot/resources/voice_outputs/synthesized_speech.wav"
    def __init__(self, use_elevenlabs_api=False):
        self.use_elevenlabs_api = use_elevenlabs_api
        if not use_elevenlabs_api:
            self.tokenizer = VitsTokenizer.from_pretrained("facebook/mms-tts-deu")
            self.model = VitsModel.from_pretrained("facebook/mms-tts-deu")

    def generate(self, text: str):
        if self.use_elevenlabs_api:
            self._generate_with_elevenlabs(text)
        else:
            self._generate_with_vits(text)

    def _generate_with_vits(self, text: str):
        inputs = self.tokenizer(text=text, return_tensors="pt")
        set_seed(555)  # make deterministic

        with torch.no_grad():
            outputs = self.model(**inputs)

        waveform = outputs.waveform[0]
        waveform_np = waveform.cpu().numpy()
        waveform_int16 = np.int16(waveform_np * np.iinfo(np.int16).max)
        print("Current Working Directory:", os.getcwd())
        scipy.io.wavfile.write(self.voice_output_file_path, rate=self.model.config.sampling_rate, data=waveform_int16)

    def _generate_with_elevenlabs(self, text: str):
        url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"
        payload = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "similarity_boost": 1,
                "stability": 1,
                "use_speaker_boost": True
            }
        }
        headers = {
            "xi-api-key": "71bebd1159d0398302e431ccfa1ae50a",
            "Content-Type": "application/json"
        }

        response = requests.request("POST", url, json=payload, headers=headers)
        if response.status_code == 200:
            # Assuming the API returns a WAV file directly, you'll need to adjust this
            # part if the API returns a link to the file or the file in a different format
            print("Current Working Directory:", os.getcwd())
            with open(self.voice_output_file_path, "wb") as f:
                f.write(response.content)
        else:
            print("Failed to synthesize speech with ElevenLabs API:", response.text)
