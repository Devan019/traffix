from services.Groq import GroqService
from services.Google import GoogleService
from services.Pinecone import PineconeService


def get_bot_response(system_message: str, user_query: str, model: str, googleService: GoogleService, groqService: GroqService, pineConeService: PineconeService) -> str:

    # Step 1: Embed the user query using Google Gemini
    vector = googleService.embed_content(user_query)
    query_vector = vector.embeddings[0].values

    # Step 2: Query Pinecone to retrieve relevant chunks
    context_chunks = pineConeService.knn_query(query_vector, top_k=3)
    text = ""
    for match in context_chunks.matches:
        text += match.metadata['text'] + "\n\n"

    # print("Retrieved Context Chunks:", text)

    # Step 3: Construct the prompt with retrieved context
    prompt = f"""
You are *TraffixBot*, an expert AI assistant trained strictly on Indian Motor Vehicle (MV) Act,
traffic laws, legal sections, fines, offences, and procedures.

Below is the context retrieved from your internal legal knowledge base:

--- Retrieved Context ---
{text}
--- End Context ---

--- User Query ---
{user_query}
-----------------------

### Your Job:
Provide the **most accurate answer ONLY based on the above context**. 
Do NOT hallucinate any information.

### RULES YOU MUST FOLLOW
1. **If the answer exists in the context**, extract it clearly and concisely.
2. NEVER fabricate legal sections or laws—only use what is present in the context.
3. If multiple relevant context chunks exist, combine them logically.
4. Keep the answer short, clear, and easy to understand.
5. Use simple language like a law assistant, not like a chat model.

### Output Format:
- Short direct answer (2-5 sentences), but if needed, provide detailed explanation.
- Mention the specific law/section ONLY if provided in context
- No disclaimers, no extra text

Now generate the most accurate answer.
"""

    # Step 4: Generate response using Groq
    response = groqService.genrateContent(
        prompt=prompt,
        model=model,
        system_message=system_message
    )

    return response
