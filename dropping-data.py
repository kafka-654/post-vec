# Dropping the tables ##################################################################
import psycopg2

# Database connection parameters
conn = psycopg2.connect(database="dGWchdgQddET",
                        host="127.0.0.1",
                        user="6362e8e9779e",
                        password="813fc7bad5c3f52a1ba83079b75",
                        port="63306")
cur = conn.cursor()

try:
    # Drop the tables if they exist
    cur.execute("DROP TABLE IF EXISTS documents;")
    cur.execute("DROP TABLE IF EXISTS document_embeddings;")
    
    conn.commit()
    print("Tables dropped successfully.")

except Exception as e:
    print("An error occurred:", e)
    conn.rollback()

finally:
    cur.close()
    conn.close()
