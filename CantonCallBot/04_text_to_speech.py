import torch
import scipy
import numpy as np

from transformers import VitsTokenizer, VitsModel, set_seed

tokenizer = VitsTokenizer.from_pretrained("facebook/mms-tts-eng")
model = VitsModel.from_pretrained("facebook/mms-tts-eng")


def generate_speech_output(text: str):
    inputs = tokenizer(text=text, return_tensors="pt")

    set_seed(555)  # make deterministic

    with torch.no_grad():
        outputs = model(**inputs)

    waveform = outputs.waveform[0]
    waveform_np = waveform.cpu().numpy()
    waveform_int16 = np.int16(waveform_np * np.iinfo(np.int16).max)
    scipy.io.wavfile.write("synthesized_speech.wav", rate=model.config.sampling_rate, data=waveform_int16)

