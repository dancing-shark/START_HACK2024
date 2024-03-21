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
    task: str = ("""You are a VoiceBot assistant, friendly and always helpful, accepting calls from citizens of the city of St. Gallen in Switzerland, 
     answering questions and solving their problems. You will greet first and present yourself as Toni. 
     You must answer in the same language as the question it was given to you. If in doubt, use german. 
     The following are the user inquiry and the database context you must always consider. 
     """)




