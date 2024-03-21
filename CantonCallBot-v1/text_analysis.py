
from langchain import hub
import langchain_core.prompts
from langchain_community.chat_message_histories.in_memory import ChatMessageHistory
from langchain_community.embeddings.cohere import CohereEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from data_models import *
from langchain_community.vectorstores import Chroma
from datetime import datetime


class Call:
    def __init__(self, number: int, chat: ChatGroq, embeddings_model: CohereEmbeddings = None, path_db: str = None):
        self.protokoll = Call_protokoll(number=number, start_time=datetime.now())
        self.chat_history = ChatMessageHistory()
        self.chat = chat
        prompt = ChatPromptTemplate.from_messages([
            ("system", Chatbot_personality.task), MessagesPlaceholder(variable_name="messages")
        ])
        self.chain = prompt | chat
        if embeddings_model and path_db:
            self.embeddings_model = embeddings_model
            self.vectorstore = Chroma(persist_directory=path_db, embedding_function=embeddings_model)
            retriever = self.vectorstore.as_retriever()
            prompt = hub.pull("rlm/rag-prompt")

            # TODO: Missing ChatHistory
            self.rag_chain = ({"context": retriever | self._format_docs | MessagesPlaceholder(variable_name="chat_history"), "question": RunnablePassthrough()}
                              | prompt
                              | self.chat
                              | StrOutputParser()
                              )

    def process(self, text: str, language: str = "de") -> str:
        """Process the user's input keeping the chat history and return the AI's response."""
        self.protokoll.language = language
        self.chat_history.add_user_message(text)
        response = self.chain.invoke({"messages": self.chat_history.messages})
        self.chat_history.add_ai_message(response.content)
        return response.content

    def _format_docs(self, docs) -> str:
        return "\n\n".join(doc.page_content for doc in docs)

    def process_with_retrieval(self, text: str, language: str = "de") -> str:
        """Process the user's input keeping the chat history, retrieval and return the AI's response."""
        self.chat_history.add_user_message(text)
        response = self.rag_chain.invoke(text)
        self.chat_history.add_ai_message(response)
        return response

    def end_call(self):
        self.protokoll.end_time = datetime.now()
        return self.protokoll





"""
chat = ChatGroq(temperature=0, groq_api_key="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",model_name="mixtral-8x7b-32768")
embeddings_model = CohereEmbeddings(model="embed-multilingual-v3.0")


x = Call(1, chat, embeddings_model)# path

print(x.process("Hallo"))

"""
