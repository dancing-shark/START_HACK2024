from text_analysis import Call
from voice_input import VoiceInput
from voice_to_text import VoiceToText
from text_to_voice import TextToVoice
from voice_output import VoiceOutput
import logging

from langchain_groq import ChatGroq
from langchain_community.embeddings.cohere import CohereEmbeddings

import os

import logging
import colorlog

# Create a logger
logger = colorlog.getLogger()
logger.setLevel(logging.DEBUG)

# Create a colored log format
log_format = (
    '%(log_color)s%(asctime)s - %(levelname)s - %(message)s'
)

# Create a color formatter
formatter = colorlog.ColoredFormatter(
    log_format,
    datefmt='%Y-%m-%d %H:%M:%S',
    reset=True,
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    },
    secondary_log_colors={},
    style='%'
)

# Create a StreamHandler with colored formatter
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Add the colored handler to the logger
logger.addHandler(console_handler)




logger.info("Setting up the environment variables.")
os.environ['COHERE_API_KEY'] = "zE6fWh7WodD48szFXjx2rX8RPEpAIqNamhjFOBL9"

chat = ChatGroq(temperature=0, groq_api_key="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", model_name="mixtral-8x7b-32768")
embeddings_model = CohereEmbeddings(model="embed-multilingual-v3.0")
path = "/chroma_db_full3"


# New Call arived
call = Call(1, chat, embeddings_model, path)
mic = VoiceInput()
vtt = VoiceToText()
ttv = TextToVoice()
box = VoiceOutput()

logger.info( "Starting the call loop.")
while True:
    # 1. voice_input
    logger.info("voice_input")
    res = mic.record_audio()


    # 2. voice_to_text
    logger.info("voice_to_text")
    res = vtt.transscribe(res)
    logger.warning(f"Transscribed: {res}")

    # 3. text_analysis
    logger.info("text_analysis")
    res = call.process(res, "de")
    logger.warning(f"Answer: {res}")


    # 4. text_to_voice
    logger.info("text_to_voice")
    ttv.generate(res)

    # 5. voice_output
    logger.info("voice_output")
    box.play()
