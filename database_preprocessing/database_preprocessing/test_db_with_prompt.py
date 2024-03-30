
import os
from langchain_community.vectorstores import Chroma
from langchain import hub
from langchain_groq import ChatGroq
from langchain_community.embeddings import CohereEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv

def format_docs(documents):
    return "\n\n".join(doc.page_content for doc in documents)

print("Setting up the environment variables.")
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)
cohere_api_key = os.getenv('COHERE_API_KEY') 
groq_api_key = os.getenv('GROQ_API_KEY') 
database_path = os.getenv('CHROMA_DB_PATH') 
embeddings_model = CohereEmbeddings(model="embed-multilingual-v3.0")
# load from disk
vectorstore = Chroma(persist_directory=database_path, embedding_function=embeddings_model)
# Retrieve and generate using the relevant snippets of the blog.
retriever = vectorstore.as_retriever()
llm = ChatGroq(temperature=0, groq_api_key=groq_api_key,model_name="mixtral-8x7b-32768")
prompt = hub.pull("rlm/rag-prompt")


rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

x = rag_chain.invoke("Kosten von den Neubau des Staatsarchivs")
print(x)
