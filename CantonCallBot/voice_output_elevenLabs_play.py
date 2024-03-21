import requests
import numpy as np
import sounddevice as sd
import soundfile as sf
from io import BytesIO
from transformers import VitsTokenizer, VitsModel, set_seed

class TextToVoice:
    def __init__(self, use_elevenlabs_api=False):
        self.use_elevenlabs_api = use_elevenlabs_api
        if not use_elevenlabs_api:
            self.tokenizer = VitsTokenizer.from_pretrained("facebook/mms-tts-deu")
            self.model = VitsModel.from_pretrained("facebook/mms-tts-deu")

    def generate(self, text: str):
        if self.use_elevenlabs_api:
            self._generate_with_elevenlabs_and_play(text)
        else:
            self._generate_with_vits_and_play(text)

    def _generate_with_vits_and_play(self, text: str):
        inputs = self.tokenizer(text=text, return_tensors="pt")
        set_seed(555)  # make deterministic

        with torch.no_grad():
            outputs = self.model(**inputs)

        waveform = outputs.waveform[0].cpu().numpy()
        sd.play(waveform, samplerate=self.model.config.sampling_rate)
        sd.wait()

    def _generate_with_elevenlabs_and_play(self, text: str):
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
            "xi-api-key": "d2357064a6d2188c2b1341ad36f17e71",
            "Content-Type": "application/json"
        }

        response = requests.request("POST", url, json=payload, headers=headers)
        if response.status_code == 200:
            audio_data, samplerate = sf.read(BytesIO(response.content))
            sd.play(audio_data, samplerate)
            sd.wait()
        else:
            print("Failed to synthesize speech with ElevenLabs API:", response.text)
