from services.Pinecone import PineconeService
from services.Google import GoogleService
from services.Groq import GroqService
from helpers.vectors import create_vectors
from helpers.bot import get_bot_response
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum  

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

handler = Mangum(app)
