from services.Pinecone import PineconeService
from services.Google import GoogleService
from services.Groq import GroqService
from helpers.vectors import create_vectors
from helpers.bot import get_bot_response
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # allow all origins
    allow_credentials=True,
    allow_methods=["*"],      # FIX: allow OPTIONS, GET, POST etc.
    allow_headers=["*"],      # allow all headers
)

pineconeService = PineconeService()
googleService = GoogleService()
groqService = GroqService()

class TraffixModel(BaseModel):
    query: str

@app.get("/")
def root():
    return {"message": "Traffix Bot is running!"}

@app.post("/create-vectors")
def create_vectors_endpoint():
    create_vectors(pineconeService, googleService)
    return {"message": "Vector creation process started."}

@app.post("/traffic-query")
def traffic_query_endpoint(query: TraffixModel):
    system_message = "You are an AI assistant specialized in traffic laws. Provide accurate and concise answers based on the indexed documents."

    response = get_bot_response(
        system_message=system_message,
        user_query=query.query,
        model="openai/gpt-oss-20b",
        googleService=googleService,
        groqService=groqService,
        pineConeService=pineconeService
    )

    return {"response": response}

if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",   
        port=port,
        reload=False      
    )



    
