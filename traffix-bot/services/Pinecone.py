from pinecone import Pinecone, ServerlessSpec
import os
from dotenv import load_dotenv
load_dotenv()


class PineconeService:
    def __init__(self):
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.index_name = os.getenv("PINECONE_INDEX_NAME")

        if not self.pc.has_index(self.index_name):
            self.pc.create_index(
                name=self.index_name,
                dimension=3072,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                ),
            )

        self.index = self.pc.Index(self.index_name)
    
    def getIndex(self):
        return self.index
    
    def knn_query(self, vector, top_k):
        return self.index.query(
            vector=vector,
            top_k=top_k,
            include_metadata=True
        )
    
