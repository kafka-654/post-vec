# Creating tables ##############################################################
import psycopg2

conn = psycopg2.connect(database="dGWchdgQddET",
                        host="127.0.0.1",
                        user="6362e8e9779e",
                        password="813fc7bad5c3f52a1ba83079b75",
                        port="63306")
cur = conn.cursor()


# Creating document table and embedding table
try:
    cur.execute("""
        CREATE TABLE documents(
                id SERIAL PRIMARY KEY,
                content TEXT NOT NULL,
                topic TEXT NOT NULL
        );
        CREATE TABLE document_embeddings(
                id SERIAL PRIMARY KEY,
                embedding vector(1536) NOT NULL
        );
    """)
    conn.commit()
    print("tables created")
except Exception as e:
    print(e)
    conn.rollback()


cur.close()
conn.close()

