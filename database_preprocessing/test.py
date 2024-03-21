import os
import bs4
import csv 

from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain import hub
from langchain_groq import ChatGroq
from langchain_community.embeddings import CohereEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
# fixes a bug with asyncio and jupyter
from pathlib import Path
from langchain_community.document_loaders import BSHTMLLoader
os.environ["COHERE_API_KEY"] = "2eidazDqcsW3aRIDoIZKcsroe92z5Wx97L53cZk5"

def format_docs(documents):
    return "\n\n".join(doc.page_content for doc in documents)

documents = []
def find_html_files(directory):
    root_dir = Path(directory)
    # This will recursively search for all files matching "*.html" pattern
    html_files = list(root_dir.rglob("*.html"))
    return html_files
# Example usage
root_directory = "data"  # Replace with your root directory path
html_files = find_html_files(root_directory)
# html_files = html_files[:10] 

documents = []
for file_path in html_files:
    loader = BSHTMLLoader(str(file_path))
    loaded_docs = loader.load()
    documents.extend(loaded_docs)

embeddings_model = CohereEmbeddings(model="embed-multilingual-v3.0")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(documents)
print(len(splits))
vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings_model)

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

x = rag_chain.invoke("Wer führt im Auftrag der Ostschweizer Regierungskonferenz?")
print(x)
