from langchain import hub
from operator import itemgetter
import langchain_core.prompts
from langchain_community.chat_message_histories.in_memory import ChatMessageHistory
from langchain_community.embeddings.cohere import CohereEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough,    ConfigurableFieldSpec, configurable
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from core.data_models import *
from langchain_community.vectorstores import Chroma
from datetime import datetime
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
store ={}
def get_session_history(user_id: str, conversation_id: str) -> BaseChatMessageHistory:
    if (user_id, conversation_id) not in store:
        store[(user_id, conversation_id)] = ChatMessageHistory()
    return store[(user_id, conversation_id)]

class Call:
    def __init__(self, number: int, chat: ChatGroq, embeddings_model: CohereEmbeddings, path_db: str):
        self.protokoll = Call_protokoll(number=number, start_time=datetime.now())
        self.chat_history = ChatMessageHistory()
        self.store = store
        self.chat = chat
        prompt = SystemMessage(content=Chatbot_personality.task)
        prompt = ( prompt +MessagesPlaceholder(variable_name="history")+"{context}"+"{question}"+"Make sure to respond in the correct language: {language}") 
        if embeddings_model and path_db:
            self.embeddings_model = embeddings_model
            self.vectorstore = Chroma(persist_directory=path_db, embedding_function=self.embeddings_model)
            retriever = self.vectorstore.as_retriever(search_type="mmr", search_kwargs={'k': 6, 'lambda_mult': 0.25})
            context = itemgetter("question") | retriever | self._format_docs
            first_step = RunnablePassthrough.assign(context=context)
            chain = first_step | prompt | self.chat | StrOutputParser()
            self.rag_chain = RunnableWithMessageHistory(
                chain,
                get_session_history=get_session_history,
                input_messages_key="question",
                history_messages_key="history",
                history_factory_config=[
                    ConfigurableFieldSpec(
                        id="user_id",
                        annotation=str,
                        name="User ID",
                        description="Unique identifier for the user.",
                        default="",
                        is_shared=True,
                    ),
                    ConfigurableFieldSpec(
                        id="conversation_id",
                        annotation=str,
                        name="Conversation ID",
                        description="Unique identifier for the conversation.",
                        default="",
                        is_shared=True,
                    ),
                ],
)

            print(self.rag_chain.dict())


    def _format_docs(self, docs) -> str:
        return "\n\n".join(doc.page_content for doc in docs)

    def process_with_retrieval(self, text: str, language: str = "de") -> str:
        """Process the user's input keeping the chat history, retrieval and return the AI's response."""
        print("Processing with retrieval")
        self.protokoll.language = language
        response = self.rag_chain.invoke({"question":text, "language":language},{"configurable":{"user_id":"1","conversation_id":"1"}})
        return response

    def end_call(self):
        self.protokoll.end_time = datetime.now()
        return self.protokoll

