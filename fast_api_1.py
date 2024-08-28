from fastapi import FastAPI, HTTPException, File, UploadFile, Query
from pydantic import BaseModel
import psycopg2
from langchain.text_splitter import RecursiveCharacterTextSplitter
import fitz  # PyMuPDF
from gen_ai_hub.proxy.native.openai import embeddings

app = FastAPI()

# Database connection parameters
db_config = {
    "dbname": "dGWchdgQddET",
    "user": "6362e8e9779e",
    "password": "813fc7bad5c3f52a1ba83079b75",
    "host": "127.0.0.1",
    "port": "63306"
}

def get_embedding(input, model="text-embedding-ada-002"):
    response = embeddings.create(
        model_name=model,
        input=input
    )
    return response.data

def connect_db():
    return psycopg2.connect(**db_config)

def extract_text_from_pdf(pdf_file):
    text = ""
    pdf_document = fitz.open(stream=pdf_file, filetype="pdf")
    for page in pdf_document:
        text += page.get_text()
    return text

@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        # Extract text from the uploaded PDF file
        pdf_content = await file.read()
        text = extract_text_from_pdf(pdf_content)
        pdf_filename = file.filename

        # Create text chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=80)
        chunks = text_splitter.split_text(text)
        print(len(chunks), chunks)
        # Embed the text chunks
        embeddings_1 = get_embedding(chunks)
        embeddings_1 = [e.embedding for e in embeddings_1]
        print(len(embeddings_1))
        # Connect to the database
        conn = connect_db()
        cur = conn.cursor()

        # Find the last ID in the documents table
        cur.execute("SELECT COALESCE(MAX(id), 0) FROM documents")
        last_id = cur.fetchone()[0]

        # Insert the chunks and embeddings into the database
        for i in range(len(chunks)):
            new_id = last_id + i + 1
            topic = pdf_filename
            text = chunks[i].replace('\x00', '')  # Remove any null characters
            embedding = embeddings_1[i]

            # Insert document content
            cur.execute("""
                INSERT INTO documents (id, topic, content)
                VALUES (%s, %s, %s)
            """, (new_id, topic, text))

            # Insert document embedding
            cur.execute("""
                INSERT INTO document_embeddings (id, embedding)
                VALUES (%s, %s)
            """, (new_id, embedding))

        # Commit the transaction
        conn.commit()
        return {"message": "PDF content and embeddings uploaded successfully."}

    except Exception as e:
        print(e)
        conn.rollback()  # Rollback in case of error
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        cur.close()
        conn.close()

@app.get("/search/")
async def search_similar_documents(query_text : str = Query(...), top_n: int = Query(5)):
    try:
        # Convert the query string into a vector
        query_vector = (get_embedding(query_text)[0]).embedding

        conn = connect_db()
        cur = conn.cursor()

        # Construct the SQL query to find the most similar vectors
        cur.execute("""
            SELECT  documents.content from documents
                    Inner join document_embeddings ON documents.id = document_embeddings.id
                    ORDER BY embedding <=> %s::vector 
                    LIMIT %s;;
        """, (query_vector, top_n))

        results = cur.fetchall()

        if not results:
            return {"message": "No similar documents found."}

        return {"results": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

# To run the app use: uvicorn filename:app --reload


