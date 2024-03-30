from langchain import hub
import langchain_core.prompts
from langchain_community.chat_message_histories.in_memory import ChatMessageHistory
from langchain_community.embeddings.cohere import CohereEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from core.data_models import *
from langchain_community.vectorstores import Chroma
from datetime import datetime
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

class Call:
    def __init__(self, number: int, chat: ChatGroq, embeddings_model: CohereEmbeddings, path_db: str):
        self.protokoll = Call_protokoll(number=number, start_time=datetime.now())
        self.chat_history = ChatMessageHistory()
        self.chat = chat
        prompt = SystemMessage(content=Chatbot_personality.task)
        prompt = (
            prompt +"{context}"+"{question}"
        ) 
        self.chain = prompt | chat
        if embeddings_model and path_db:
            self.embeddings_model = embeddings_model
            self.vectorstore = Chroma(persist_directory=path_db, embedding_function=self.embeddings_model)
            retriever = self.vectorstore.as_retriever(search_type="mmr", search_kwargs={'k': 6, 'lambda_mult': 0.25})
            print(prompt)

            # TODO: Missing ChatHistory
            self.rag_chain = ({"context": retriever | self._format_docs, "question": RunnablePassthrough()}
                              | prompt
                              | self.chat
                              | StrOutputParser()
                              )

            print(self.rag_chain.dict())

    def _format_docs(self, docs) -> str:
        return "\n\n".join(doc.page_content for doc in docs)

    def process_with_retrieval(self, text: str, language: str = "de") -> str:
        """Process the user's input keeping the chat history, retrieval and return the AI's response."""
        print("Processing with retrieval")
        self.protokoll.language = language

        # Give message history
        self.chat_history.add_user_message(text)
        # self.chain.invoke({"messages": self.chat_history.messages})
        response = self.rag_chain.invoke(text)
        self.chat_history.add_ai_message(response)
        return response

    def end_call(self):
        self.protokoll.end_time = datetime.now()
        return self.protokoll

