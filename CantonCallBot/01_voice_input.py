import speech_recognition as sr

def record() -> any:
    r = sr.Recognizer()
    with sr.Microphone() as source:
       print("Say something!")
       audio = r.listen(source)
    return audio
