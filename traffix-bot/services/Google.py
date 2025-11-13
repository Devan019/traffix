from google import genai
import os
from dotenv import load_dotenv
load_dotenv()
class GoogleService:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    def embed_content(self, content: str):
        return self.client.models.embed_content(
            model="gemini-embedding-001",
            contents=content
        )
    