import os
import bs4
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import CohereEmbeddings
from pathlib import Path
from langchain_community.document_loaders import BSHTMLLoader
import re
from langchain_community.document_loaders import TextLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_core.documents.base import Document
from dotenv import load_dotenv
from tqdm import tqdm
import argparse

# Setup argparse
parser = argparse.ArgumentParser(description='Process HTML files and add them to a vector store.')
parser.add_argument('--db-destination', type=str, help='Override the database destination path specified in the .env file')
args = parser.parse_args()

print("Setting up the environment variables.")
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)
# This is actually not needed. As long as they are in the env is enough. 
cohere_api_key = os.getenv('COHERE_API_KEY') 
db_destination = args.db_destination if args.db_destination else os.getenv('CHROMA_DB_RES_PATH')

def normalize_whitespace_and_breaklines(text):
    # Collapse multiple newline characters into a single newline
    text = re.sub(r'\n+', '\n', text)
    # Replace sequences of whitespace characters (excluding newlines) with a single space
    text = re.sub(r'[ \t]+', ' ', text)
    # Trim leading and trailing whitespace
    text = text.strip()
    text = text.replace('Ã¤', 'ä').replace('Ã¶', 'ö').replace('Ã¼', 'ü').replace('ÃŸ', 'ß').replace('Ã„', 'Ä').replace('Ã–', 'Ö').replace('Ãœ', 'Ü')
    return text

def find_html_files(directory):
    root_dir = Path(directory)
    html_files = list(root_dir.rglob("*.html"))
    return html_files

def create_document(page_content, source, title):
    metadata = {
        'source': source,
        'title': title
    }
    return Document(page_content=page_content, metadata=metadata)

def extract_text_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    soup = bs4.BeautifulSoup(content, 'html.parser')
    title_element = soup.find('title')
    title_text = title_element.text.strip() if title_element else 'No Title'
    content_element = soup.find('div', id='content')
     # Remove any script and style elements

    if content_element:
        for script in soup(["script", "style", "nav","button","form"]):
            script.extract()
        purified_text = normalize_whitespace_and_breaklines(content_element.text.strip()) 
        return create_document(purified_text, str(file_path), title_text)

def add_documents_to_vectorstore_in_batches( documents, embeddings_model, text_splitter, batch_size=96):
    # Split the documents according to the text splitter logic
    splits = text_splitter.split_documents(documents)
    total_splits = len(splits)
    print(f"Total splits to process: {total_splits}")
    total_batches = (total_splits + batch_size - 1) // batch_size
    vectorstore = Chroma.from_documents(documents=documents[:1], embedding=embeddings_model,persist_directory=db_destination)
    print("Processing batches...")
    for start_index in tqdm(range(1, total_splits, batch_size), desc="Batches", total=total_batches, unit="batch"):
        end_index = min(start_index + batch_size, total_splits)
        batch_splits = splits[start_index:end_index]
        vectorstore.add_documents(documents=batch_splits, embedding=embeddings_model)

    vectorstore.persist() 
    return vectorstore

root_directory = "data"  

# This gets all html files paths recursevely
print("Finding HTML files...")
html_files = find_html_files(root_directory)[1:100]

documents = []
print("Extracting text from HTML files...")
for file_path in tqdm(html_files, desc="Extracting HTML", unit="file"):
    # Extract the text content of the html file
    extracted_text = extract_text_from_html(str(file_path)) 
    if extracted_text:
        loaded_doc = extracted_text
        # Loads content into a document obj
        documents.append(loaded_doc)

embeddings_model = CohereEmbeddings(model="embed-multilingual-v3.0")

text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=100)
vectorstore = add_documents_to_vectorstore_in_batches(documents, embeddings_model, text_splitter)
