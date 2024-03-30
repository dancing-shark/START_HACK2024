from core.text_analysis import Call
from core.voice_input import VoiceInput
from core.voice_to_text import VoiceToText
from core.text_to_voice import TextToVoice
from core.voice_output import VoiceOutput
import logging
from core.voice_output_elevenLabs import TextToVoice as TTT

from langchain_groq import ChatGroq
from langchain_community.embeddings.cohere import CohereEmbeddings

import os
from dotenv import load_dotenv
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
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)
cohere_api_key = os.getenv('COHERE_API_KEY') 
groq_api_key = os.getenv('GROQ_API_KEY') 
path = os.getenv('CHROMA_DB_PATH') 
store = {}

chat = ChatGroq(temperature=0, groq_api_key=groq_api_key, model_name="mixtral-8x7b-32768")
embeddings_model_x = CohereEmbeddings(cohere_api_key=cohere_api_key,model="embed-multilingual-v3.0")

# New Call arived
call = Call(1, chat, embeddings_model=embeddings_model_x, path_db=path)
mic = VoiceInput()
vtt = VoiceToText()
ttv = TextToVoice()
box = VoiceOutput()
ttt = TTT(use_elevenlabs_api=False)

logger.info("Starting the call loop.")
while True:
    # 1. voice_input
    logger.info("voice_input")
    res = mic.record_audio()

    # 2. voice_to_text
    logger.info("voice_to_text")
    res = vtt.transcribe(res)
    logger.warning(f"Transscribed: {res}")

    # 3. text_analysis
    logger.info("text_analysis")
    res = call.process_with_retrieval(res, "en")
    # res = call.process(res)
    logger.warning(f"Answer: {res}")

    # 4. text_to_voice
    # logger.info("text_to_voice")
    # # ttv.generate(res)
    # ttt.generate(res)

    # 5. voice_output
    # logger.info("voice_output")
    # box.play("canton_call_bot/resources/voice_outputs/synthesized_speech.wav")
