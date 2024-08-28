from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_cohere import CohereEmbeddings
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pgvector.sqlalchemy import Vector
import numpy as np
import json
from sap_api import get_embedding

#embeddings_model = CohereEmbeddings(model="embed-english-v3.0",cohere_api_key="BJAoyx28LByErLlTRKR2q7uC8GKLaYHyrCLGtNgg")
#embeddings_1 = embeddings_model.embed_documents(["India's response to climate change"])
embeddings_1 = get_embedding("How will data help businesses?")
# print(embeddings_1[0].embedding)
file_path = 'embeddings.json'

# Write the embeddings to a file
with open(file_path, 'w') as file:
    json.dump(embeddings_1[0].embedding, file)

print(f"Embeddings have been written to {file_path}")
