# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import speech_recognition as sr
from CantonCallBot import speech_output, transcribe
import simpleaudio as sa


from openai import OpenAI
from groq import Groq

OPEN_AI_API_KEY = "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"
GROQ_API_KEY = "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"
#Setup  LLM clients
client = OpenAI(api_key=OPEN_AI_API_KEY)
client = Groq(api_key=GROQ_API_KEY)



if __name__ == '__main__':
     transcribe_result = transcribe.record_and_transcribe()
     print(f"Transcription result: {transcribe_result}")
     if transcribe_result != "":
       #  call_gpt("Help me to understand history, answer in the same language the question was formulated", transcribe_result)
         llm_result = call_groq("Help me to understand history, answer in the same language the question was formulated", transcribe_result)
         speech_output.generate_speech_output(llm_result)

         wave_obj = sa.WaveObject.from_wave_file('synthesized_speech.wav')
         play_obj = wave_obj.play()
         play_obj.wait_done()  # Wait until sound has finished playing
