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

os.environ["COHERE_API_KEY"] = "2eidazDqcsW3aRIDoIZKcsroe92z5Wx97L53cZk5"
database_path = './chroma_db_full'
def format_docs(documents):
    return "\n\n".join(doc.page_content for doc in documents)

def find_html_files(directory):
    root_dir = Path(directory)
    html_files = list(root_dir.rglob("*.html"))
    return html_files

def add_documents_to_vectorstore_in_batches( documents, embeddings_model, text_splitter, batch_size=96):
    # Split the documents according to the text splitter logic
    splits = text_splitter.split_documents(documents)
    total_splits = len(splits)
    print(f"Total splits to process: {total_splits}")

    vectorstore = Chroma.from_documents(documents=documents[:1], embedding=embeddings_model,persist_directory=database_path)
    # Process in batches of 'batch_size'
    for start_index in range(1, total_splits, batch_size):
        end_index = min(start_index + batch_size, total_splits)
        batch_splits = splits[start_index:end_index]
        vectorstore.add_documents(documents=batch_splits, embedding=embeddings_model)

        print(f"Processed batch {start_index//batch_size + 1}/{(total_splits + batch_size - 1) // batch_size}")
    vectorstore.persist() 
    return vectorstore

root_directory = "data/bildung-sport"  

# This gets all html files paths recursevely
html_files = find_html_files(root_directory)

html_files = html_files
documents = []
for file_path in html_files:
    # Extract the text content of the html file
    loader = BSHTMLLoader(str(file_path))
    # Loads content into a document obj
    loaded_docs = loader.load()
    documents.extend(loaded_docs)

embeddings_model = CohereEmbeddings(model="embed-multilingual-v3.0")

text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
splits = text_splitter.split_documents(documents)
vectorstore = add_documents_to_vectorstore_in_batches(documents, embeddings_model, text_splitter)

# The vectorstore is saved on the repo. To access to it you can do this:
# db3 = Chroma(persist_directory="./chroma_db", embedding_function=embedding_function)

#--------------------FOR TESTING PURPOSES---------------------
# Retrieve and generate using the relevant snippets of the blog.
# retriever = vectorstore.as_retriever()
# llm = ChatGroq(temperature=0, groq_api_key="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",model_name="mixtral-8x7b-32768")
# prompt = hub.pull("rlm/rag-prompt")
#
#
# rag_chain = (
#     {"context": retriever | format_docs, "question": RunnablePassthrough()}
#     | prompt
#     | llm
#     | StrOutputParser()
# )
#
# x = rag_chain.invoke("Wer führt im Auftrag der Ostschweizer Regierungskonferenz?")
# print(x)
