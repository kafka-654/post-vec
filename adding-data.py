from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_cohere import CohereEmbeddings
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pgvector.sqlalchemy import Vector
import numpy as np
from sap_api import get_embedding
# Adding data ################################################

import psycopg2

conn = psycopg2.connect(database="dGWchdgQddET",
                        host="127.0.0.1",
                        user="6362e8e9779e",
                        password="813fc7bad5c3f52a1ba83079b75",
                        port="63306")
cur = conn.cursor()


# Reading from the pdf
loader = PyMuPDFLoader("data/olympic-games.pdf")
data = loader.load()
#print(data[1])
#print(len(data))

# Creating chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size =1000, chunk_overlap=80)
chunks = text_splitter.split_documents(data)
# print(len(chunks))
# print(chunks[0].metadata["source"])

#Creating vectors
# embeddings_model = CohereEmbeddings(model="embed-english-v3.0",cohere_api_key="BJAoyx28LByErLlTRKR2q7uC8GKLaYHyrCLGtNgg")
# embeddings_1 = embeddings_model.embed_documents([c.page_content for c in chunks])
embeddings_1 = get_embedding([c.page_content for c in chunks])
embeddings_1 = [e.embedding for e in embeddings_1]
#print(len(embeddings_1), len(embeddings_1[0]))
try:
    cur.execute("SELECT COALESCE(MAX(id), 0) FROM documents")
    last_id = cur.fetchone()[0]
    print(f"Last ID in documents table: {last_id}")
    for i in range(len(chunks)):
        new_id = i +last_id + 1
        topic, text = chunks[i].metadata["source"], chunks[i].page_content.replace('\x00', '')
        embdgs = embeddings_1[i]
        print("topic : ",topic)
        print("text : ",text)
        print("embeddings : ",len(embdgs))
        print("id", new_id)
        print()
        print("-------------------------------------------------")
        print()
        
        cur.execute("""
                    INSERT INTO documents (id, topic, content)
                    VALUES (%s,%s, %s)
                """, (str(new_id), topic, text)
        )


        cur.execute("""
                    INSERT INTO document_embeddings (id, embedding)
                    VALUES (%s,%s)
                """, (str(new_id),embdgs)
        )
    conn.commit()
    print("Data uploaded ")
except Exception as E:
    print(E)
    conn.rollback()

cur.close()
conn.close()

