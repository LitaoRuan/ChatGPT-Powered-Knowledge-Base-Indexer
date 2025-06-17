import os
import faiss
import numpy as np
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()  # Load from .env

api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_version = os.getenv("AZURE_OPENAI_API_VERSION1")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")


# Azure OpenAI Config
client = AzureOpenAI(
    api_key=api_key,
    azure_endpoint=f"{endpoint}/openai/deployments/{deployment}/embeddings",
    api_version=api_version
)

# remove key, hide environment variables

embedding_model = "text-embedding-ada-002"
input_folder = "data"

# Embed a single chunk
def get_embedding(text: str) -> list[float]:
    response = client.embeddings.create(input=[text], model=embedding_model)
    return response.data[0].embedding

# Load & chunk text files
def chunk_text(text: str, max_tokens: int = 300) -> list[str]:
    sentences = text.split(". ")
    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        word_count = len(sentence.split())
        if current_length + word_count > max_tokens:
            chunks.append(". ".join(current_chunk))
            current_chunk = [sentence]
            current_length = word_count
        else:
            current_chunk.append(sentence)
            current_length += word_count

    if current_chunk:
        chunks.append(". ".join(current_chunk))

    return chunks

# Prepare data
documents = []
texts = []

for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):
        with open(os.path.join(input_folder, filename), "r", encoding="utf-8") as f:
            content = f.read()
        chunks = chunk_text(content)
        for chunk in chunks:
            embedding = get_embedding(chunk)
            texts.append(chunk)
            documents.append(np.array(embedding, dtype="float32"))

# Convert to FAISS index
dimension = len(documents[0])
index = faiss.IndexFlatL2(dimension)
index.add(np.array(documents))

# Save index and text chunks
faiss.write_index(index, "faiss_index.index")
with open("text_chunks.txt", "w", encoding="utf-8") as f:
    for chunk in texts:
        f.write(chunk + "\n<--CHUNK-END-->\n")

print(f"Stored {len(texts)} chunks in FAISS.")
