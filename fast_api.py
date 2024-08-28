from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import psycopg2
import numpy as np

app = FastAPI()

# Database connection parameters
db_config = {
    "dbname": "dGWchdgQddET",
    "user": "6362e8e9779e",
    "password": "813fc7bad5c3f52a1ba83079b75",
    "host": "127.0.0.1",
    "port": "63306"
}

# SAP API
from gen_ai_hub.proxy.native.openai import embeddings

def get_embedding(input, model="text-embedding-ada-002") -> str:
    response = embeddings.create(
        model_name=model,
        input=input
    )
    return response.data

def connect_db():
    return psycopg2.connect(**db_config)


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
