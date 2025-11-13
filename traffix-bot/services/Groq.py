from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()

class GroqService:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def genrateContent(self, prompt: str, model:str, system_message: str) -> str:
        
        response = self.client.chat.completions.create(
            model=model,
            messages=[
              {"role": "system", "content": system_message},
              {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content