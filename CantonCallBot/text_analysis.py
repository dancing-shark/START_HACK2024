"""langchain"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
from langchain.memory import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder



chat = ChatGroq(temperature=0, groq_api_key="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",model_name="mixtral-8x7b-32768")

demo_chat_history = ChatMessageHistory()

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Answer all questions to the best of your ability. Your name is Peter",
        ),
        MessagesPlaceholder(variable_name="messages"), ("human", "{input}")
    ]
)

chain = prompt | chat
while(True):
    inputtext = input("Frage: ")
    demo_chat_history.add_user_message(inputtext)
    response = chain.invoke({"messages":demo_chat_history.messages})
    demo_chat_history.add_ai_message(response)
    print(response)

