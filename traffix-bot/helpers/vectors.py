import fitz
import math
from services.Pinecone import PineconeService
from services.Google import GoogleService


def convert_into_chunks(text:str, chunk_size:int, overlap:int, index:int)->str:
  if index == 0:
    return text[:chunk_size]

  st:int = index*(chunk_size - overlap)
  return text[st:min(st+chunk_size, len(text))] 


def convert_pdf_to_text(pdf_path:str)->str:
  text:str = ""
  with fitz.open(pdf_path) as pdf:
    for page in pdf:
      text += page.get_text()
  
  return text


def create_vectors(pineconeService: PineconeService, googleService: GoogleService):
  extract_text:str = convert_pdf_to_text("./data/vehicle-act.pdf")
  extract_text += convert_pdf_to_text("./data/MV Act English.pdf")


  text:str = extract_text
  chunk_size:int = 2000
  overlap:int = 200

  total_chunks:int = math.ceil(len(text)/(chunk_size-overlap)) 

  for i in range (total_chunks) :
    chunk:str = convert_into_chunks(text, chunk_size, overlap, index=i)
    result = googleService.embed_content(chunk)
    
    vector = result.embeddings[0].values

    if not vector:
      print("Failed to get embedding for chunk index:", i)
      continue

    metadata = {
      "text": chunk,
      "chunk_index": i
    }

    pineconeService.getIndex().upsert(
      vectors=[
        {
          "id": f"chunk-{i}",
          "values": vector,
          "metadata": metadata
        }
      ]
    )

  print("🎉 All chunks processed successfully!")
  

  
  