# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import speech_recognition as sr
import transcribe
import speech_output
import simpleaudio as sa


from openai import OpenAI
from groq import Groq

OPEN_AI_API_KEY = "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"
GROQ_API_KEY = "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"
#Setup  LLM clients
client = OpenAI(api_key=OPEN_AI_API_KEY)
client = Groq(api_key=GROQ_API_KEY)


# obtain path to "english.wav" in the same folder as this script
from os import path
AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "Die Stadt Zürich lie.wav")
# AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "french.aiff")
# AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "chinese.flac")

# use the audio file as the audio source
def record_and_transcribe_test() -> str:
    r = sr.Recognizer()
    with sr.Microphone() as source:
       print("Say something!")
       audio = r.listen(source)

   # with sr.AudioFile(AUDIO_FILE) as source:
  #      audio = r.record(source)  # read the entire audio file

    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return "error"
# Press the green button in the gutter to run the script.


def call_gpt(context, user_query):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"{context}"},
            {"role": "user", "content": f"{user_query}"}
        ]
    )
    print(response.choices[0].message.content)

def call_groq(context,user_query)-> str:
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f"{context}"
            },
            {
                "role": "user",
                "content": f"{user_query}",
            }
        ],
        model="mixtral-8x7b-32768",
    )
    print(chat_completion.choices[0].message.content)
    return chat_completion.choices[0].message.content

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
