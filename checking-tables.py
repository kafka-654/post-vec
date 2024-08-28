# Checking the tables #####################################################
import psycopg2

conn = psycopg2.connect(database="dGWchdgQddET",
                        host="127.0.0.1",
                        user="6362e8e9779e",
                        password="813fc7bad5c3f52a1ba83079b75",
                        port="63306")
cur = conn.cursor()

try:
    # Select all data from documents table
    cur.execute("SELECT * FROM documents")
    documents = cur.fetchall()
    if documents:
        print("Documents Table length:")
        #for document in documents:
        #    print(document)
        print(len(documents))
    else:
        print("No data found in documents table.")
    
    # Select all data from document_embeddings table
    cur.execute("SELECT * FROM document_embeddings")
    embeddings = cur.fetchall()
    if embeddings:
        print("\nDocument Embeddings Table length:")
        #for embedding in embeddings:
        #    print(embedding)
        print(len(embeddings))
    else:
        print("No data found in document_embeddings table.")

except Exception as e:
    print("An error occurred:", e)
finally:
    cur.close()
    conn.close()
