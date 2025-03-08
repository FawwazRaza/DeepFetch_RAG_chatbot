from fastapi import FastAPI, Query
from pydantic import BaseModel
from response_generator import generate_response, select_best_context
from retrieval import search_documents

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.get("/query/")
def get_query_response(q: str):
    """API endpoint to process user queries and return chatbot responses."""
    
    retrieved_chunks = search_documents(q, top_k=3)
    
    best_context = select_best_context(q, retrieved_chunks)

    response = generate_response(q, context=best_context)
    
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
