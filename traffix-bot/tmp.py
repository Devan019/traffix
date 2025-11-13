
from fastapi import FastAPI
import uvicorn

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      
    allow_credentials=True,
    allow_methods=["*"],      
    allow_headers=["*"],      
)



@app.get("/")
def root():
    return {"message": "Traffix Bot is running!"}

if __name__ == "__main__":
    import os
    uvicorn.run(
        "main:app",
        host="0.0.0.0",   
        port=8000,   
    )



    
