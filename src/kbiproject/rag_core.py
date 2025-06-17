import faiss
import numpy as np
from openai import AzureOpenAI
from dotenv import load_dotenv
import os

load_dotenv()  # Load from .env

api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_version = os.getenv("AZURE_OPENAI_API_VERSION2")

# Azure OpenAI config
client = AzureOpenAI(
    api_key=api_key,
    azure_endpoint=f"{endpoint}",
    api_version=api_version
)

chat_model = "gpt-4o"
embedding_model = "text-embedding-ada-002"

# Load FAISS index and text chunks
index = faiss.read_index("faiss_index.index")

with open("text_chunks.txt", "r", encoding="utf-8") as f:
    raw_chunks = f.read().split("<--CHUNK-END-->\n")
    chunks = [c.strip() for c in raw_chunks if c.strip()]

# Embed user query
def get_embedding(text: str) -> list[float]:
    text = str(text).strip()[:8000]  # truncate overly long input
    response = client.embeddings.create(input=[text], model=embedding_model)
    return response.data[0].embedding

# Semantic search
def search_chunks(query: str, top_k=5):
    query_vector = np.array([get_embedding(query)], dtype="float32")
    distances, indices = index.search(query_vector, top_k)
    return [chunks[i] for i in indices[0]]

# Send context
def ask_with_context(user_question: str, retrieved_chunks: list[str]) -> str:
    context = "\n\n".join(retrieved_chunks)
    prompt = f"""Use the following lecture content to answer the question:

{context}

Question: {user_question}
"""

    response = client.chat.completions.create(
        model=chat_model,
        messages=[
            {"role": "system", "content": "You are a university-level assistant answering based on lecture notes. Answer only using the context provided. If the answer is not in the context, say 'I don't know.', except for greetings and thanks."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1024,
        temperature=0.3
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    print("Chatbot Ready! Type a question or 'exit' to quit.")
    while True:
        question = input("\n Your question: ")
        if question.strip().lower() == "exit":
            break

        top_chunks = search_chunks(question, top_k=5)
        
        answer = ask_with_context(question, top_chunks)
        print(f"\n Answer:\n{answer}")