import torch
import scipy
import numpy as np

from transformers import VitsTokenizer, VitsModel, set_seed




class TextToVoice:
    def __init__(self):
        self.tokenizer = VitsTokenizer.from_pretrained("facebook/mms-tts-deu")
        self.model = VitsModel.from_pretrained("facebook/mms-tts-deu")

    def generate(self, text: str):
        inputs = self.tokenizer(text=text, return_tensors="pt")

        set_seed(555)  # make deterministic

        with torch.no_grad():
            outputs = self.model(**inputs)

        waveform = outputs.waveform[0]
        waveform_np = waveform.cpu().numpy()
        waveform_int16 = np.int16(waveform_np * np.iinfo(np.int16).max)
        scipy.io.wavfile.write("synthesized_speech.wav", rate=self.model.config.sampling_rate, data=waveform_int16)



# text_to_voice = TextToVoice(use_elevenlabs_api=True)
# text_to_voice.generate("Your text here")