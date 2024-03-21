from dataclasses import dataclass
from datetime import datetime
from enum import Enum
@dataclass
class User:
    name: str
    gender: str
    telnr: str
    email: str

class Classifcation(Enum):
    INFORMATION = "Information"
    FORWARDING = "Forwarding"
    UNKNOWN = "Unknown"

@dataclass
class Topics:
    topic: str
    classifcation: Classifcation
    department: str
    description: str
    keywords: list
    done: bool

@dataclass
class Call_protokoll:
    number: int = 0
    start_time: datetime = None
    end_time: datetime = None
    topic: list[Topics] = None
    user: User = None
    language: str = "de"

@dataclass
class Chatbot_personality:
    name: str = "Toni"
    age: int = 25
    task: str = "Du bist ein KI-Chatbot von Kanton St.Gallen. Deine Aufgabe ist es, menschenähnliche, korrekte und hilfreiche Antworten zu geben, wenn Benutzer Fragen stellen oder Konversationen führen. Deine Personalität: freundlich, hilfsbereit und professionell. Dein Name ist Toni und dein alter ist 25. Du greifst auf eine Vielzahl von Informationen über den Kanton St.Gallen zurück halte dich streng an diese Informationen, bleibst aber stets neutral und respektvoll. Beginne das Gespräch, indem du dich dem Benutzer vorstellst und ihn fragst, wie du helfen kannst."




