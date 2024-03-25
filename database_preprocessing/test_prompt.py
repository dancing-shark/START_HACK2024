
import os
from langchain_community import embeddings
from langchain_community import vectorstores
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain import hub
from langchain_groq import ChatGroq
from langchain_community.embeddings import CohereEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from pathlib import Path
from langchain_community.document_loaders import BSHTMLLoader

def format_docs(documents):
    return "\n\n".join(doc.page_content for doc in documents)

database_path = './chroma_db_full'
os.environ["COHERE_API_KEY"] = "2eidazDqcsW3aRIDoIZKcsroe92z5Wx97L53cZk5"
embeddings_model = CohereEmbeddings(model="embed-multilingual-v3.0")
# load from disk
vectorstore = Chroma(persist_directory=database_path, embedding_function=embeddings_model)
# Retrieve and generate using the relevant snippets of the blog.
retriever = vectorstore.as_retriever()
llm = ChatGroq(temperature=0, groq_api_key="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",model_name="mixtral-8x7b-32768")
prompt = hub.pull("rlm/rag-prompt")


rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

x = rag_chain.invoke("Kosten von den Neubau des Staatsarchivs")
print(x)
