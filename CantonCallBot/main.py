from text_analysis import Call
from voice_input import VoiceInput
from voice_to_text import VoiceToText
from text_to_voice import TextToVoice
from voice_output import VoiceOutput

from langchain_groq import ChatGroq
from langchain_community.embeddings.cohere import CohereEmbeddings



chat = ChatGroq(temperature=0, groq_api_key="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",model_name="mixtral-8x7b-32768")
embeddings_model = None#CohereEmbeddings(model="embed-multilingual-v3.0")
path = None #"path"

# New Call arived
call = Call(1, chat, embeddings_model, path)
mic = VoiceInput()
vtt = VoiceToText()
ttv = TextToVoice()
box = VoiceOutput()


while True:
    # 1. voice_input
    res = mic.record_audio()

    # 2. voice_to_text
    res = vtt.transscribe(res)

    # 3. text_analysis
    res = call.process(res, "de")

    # 4. text_to_voice
    ttv.generate(res)

    # 5. voice_output
    box.play()
