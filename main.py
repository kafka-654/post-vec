from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_cohere import CohereEmbeddings
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pgvector.sqlalchemy import Vector
import numpy as np

# Reading from the pdf
# loader = PyMuPDFLoader("btp-installation.pdf")
# data = loader.load()
#print(data[1])
#print(len(data))

# Creating chunks
# text_splitter = RecursiveCharacterTextSplitter(chunk_size =1000, chunk_overlap=80)
# chunks = text_splitter.split_documents(data)
# print(len(chunks))
# print(chunks[0].metadata["source"])

#Creating vectors ################################################################
# embeddings_model = CohereEmbeddings(model="embed-english-light-v3.0",cohere_api_key="BJAoyx28LByErLlTRKR2q7uC8GKLaYHyrCLGtNgg")
# embeddings_1 = embeddings_model.embed_documents([c.page_content for c in chunks])
# print(len(embeddings_1), len(embeddings_1[0]))


# # Creating tables ##############################################################
# import psycopg2

# conn = psycopg2.connect(database="dGWchdgQddET",
#                         host="127.0.0.1",
#                         user="6362e8e9779e",
#                         password="813fc7bad5c3f52a1ba83079b75",
#                         port="63306")
# cur = conn.cursor()


# # Creating document table and embedding table
# try:
#     cur.execute("""
#         CREATE TABLE documents(
#                 id SERIAL PRIMARY KEY,
#                 content TEXT NOT NULL
#         );
#         CREATE TABLE document_embeddings(
#                 id SERIAL PRIMARY KEY,
#                 embedding vector(384) NOT NULL
#         );
#     """)
#     conn.commit()
#     print("tables created")
# except Exception as e:
#     print(e)
#     conn.rollback()


# cur.close()
# conn.close()



# # Altering documents table ################################################
# import psycopg2

# conn = psycopg2.connect(database="dGWchdgQddET",
#                         host="127.0.0.1",
#                         user="6362e8e9779e",
#                         password="813fc7bad5c3f52a1ba83079b75",
#                         port="63306")
# cur = conn.cursor()

# try:

#     # Add a new column 'topic' to the documents table
#     cur.execute("""
#         ALTER TABLE documents
#         ADD COLUMN topic TEXT;
#     """)
    
#     conn.commit()
#     print("Tables created and 'topic' column added successfully.")
# except Exception as e:
#     print("An error occurred:", e)
#     conn.rollback()
# finally:
#     cur.close()
#     conn.close()

# Adding data ################################################

# import psycopg2

# conn = psycopg2.connect(database="dGWchdgQddET",
#                         host="127.0.0.1",
#                         user="6362e8e9779e",
#                         password="813fc7bad5c3f52a1ba83079b75",
#                         port="63306")
# cur = conn.cursor()


# # Reading from the pdf
# loader = PyMuPDFLoader("btp-installation.pdf")
# data = loader.load()
# #print(data[1])
# #print(len(data))

# # Creating chunks
# text_splitter = RecursiveCharacterTextSplitter(chunk_size =1000, chunk_overlap=80)
# chunks = text_splitter.split_documents(data)
# # print(len(chunks))
# # print(chunks[0].metadata["source"])

# #Creating vectors
# embeddings_model = CohereEmbeddings(model="embed-english-light-v3.0",cohere_api_key="BJAoyx28LByErLlTRKR2q7uC8GKLaYHyrCLGtNgg")
# embeddings_1 = embeddings_model.embed_documents([c.page_content for c in chunks])
# # print(len(embeddings_1), len(embeddings_1[0]))
# try:
#     for i in range(len(chunks)):
#         topic, text = chunks[i].metadata["source"], chunks[i].page_content
#         embdgs = embeddings_1[i]
#         print("topic : ",topic)
#         print("text : ",text)
#         print("embeddings : ",embdgs)
#         print()
#         print("-------------------------------------------------")
#         print()
        
#         cur.execute("""
#                     INSERT INTO documents (id, topic, content)
#                     VALUES (%s,%s, %s)
#                 """, (str(i), topic, text)
#         )


#         cur.execute("""
#                     INSERT INTO document_embeddings (id, embedding)
#                     VALUES (%s,%s)
#                 """, (str(i),embdgs)
#         )
#     conn.commit()
#     print("Data uploaded ")
# except Exception as E:
#     print(E)
#     conn.rollback()

# cur.close()
# conn.close()


# # Checking the tables #####################################################
# import psycopg2

# conn = psycopg2.connect(database="dGWchdgQddET",
#                         host="127.0.0.1",
#                         user="6362e8e9779e",
#                         password="813fc7bad5c3f52a1ba83079b75",
#                         port="63306")
# cur = conn.cursor()

# try:
#     # Select all data from documents table
#     cur.execute("SELECT * FROM documents")
#     documents = cur.fetchall()
#     if documents:
#         print("Documents Table:")
#         for document in documents:
#             print(document)
#     else:
#         print("No data found in documents table.")
    
#     # Select all data from document_embeddings table
#     cur.execute("SELECT * FROM document_embeddings")
#     embeddings = cur.fetchall()
#     if embeddings:
#         print("\nDocument Embeddings Table:")
#         for embedding in embeddings:
#             print(embedding)
#     else:
#         print("No data found in document_embeddings table.")

# except Exception as e:
#     print("An error occurred:", e)
# finally:
#     cur.close()
#     conn.close()

# # Dropping the tables ##################################################################
# import psycopg2

# # Database connection parameters
# conn = psycopg2.connect(database="dGWchdgQddET",
#                         host="127.0.0.1",
#                         user="6362e8e9779e",
#                         password="813fc7bad5c3f52a1ba83079b75",
#                         port="63306")
# cur = conn.cursor()

# try:
#     # Drop the tables if they exist
#     cur.execute("DROP TABLE IF EXISTS documents;")
#     cur.execute("DROP TABLE IF EXISTS document_embeddings;")
    
#     conn.commit()
#     print("Tables dropped successfully.")

# except Exception as e:
#     print("An error occurred:", e)
#     conn.rollback()

# finally:
#     cur.close()
#     conn.close()
   
    

embeddings_model = CohereEmbeddings(model="embed-english-light-v3.0",cohere_api_key="BJAoyx28LByErLlTRKR2q7uC8GKLaYHyrCLGtNgg")
embeddings_1 = embeddings_model.embed_documents(["How to configure SAP build apps"])
print(embeddings_1)
