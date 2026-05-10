import os

import chromadb
from dotenv import load_dotenv
from openai import OpenAI

from pdf_loader import load_pdf
from text_chunker import chunk_text

from metadata_extractor import extract_metadata

# Loads OPENAI_API_KEY
load_dotenv()

# OpenAI client for embedding and answer generation
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Converts text into numerical embedding vector
def get_embedding(text: str) -> list[float]:

    response= client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
    )

    return response.data[0].embedding

# Opens or create the ChromaDB collection to store filing chunks
def get_collection():
    chroma_client = chromadb.PersistentClient(path="chroma_db")

    return chroma_client.get_or_create_collection(name="financial_reports")

# Deletes the old vector collection and creates a new one
def reset_collection():
    chroma_client = chromadb.PersistentClient(path="chroma_db")

    try:
        chroma_client.delete_collection(name="financial_reports")
    except Exception:
        pass

    return chroma_client.get_or_create_collection(name="financial_reports")

# Loads PDF texts, chunk texts, extract metadata, embeds each chunk, and stores chunks in ChromaDB
def build_store_vector(pdf_path: str):

    text = load_pdf(pdf_path)
    chunks = chunk_text(text)
    # Extracts company name, filing type, year, and path
    metadata = extract_metadata(text, pdf_path)

    print("Extracted metadata:", metadata)

    # Start with fresh collection for current file
    collection = reset_collection()

    for chunk in chunks:
        print(f"Processing {chunk['id']}")

        # Converts chunk text into an embedding vector
        embedding = get_embedding(chunk["text"])

        # Stores text, embedding, and metadata in ChromaDB
        collection.add(
            ids=[chunk["id"]],
            documents=[chunk["text"]],
            embeddings=[embedding],
            metadatas=[metadata],
        )

    print(f"Stored {len(chunks)} chunks in ChromaDB.")

# Retrieves the top matching chunks for a user question
# The query embedded and compared against store chunk embeddings
def retrieve_chunks(query: str, n_results: int = 3):
    collection = get_collection()
    query_embedding = get_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    return results

# Prompt generation for final answer using GPT-4o-mini
def generate_results(query: str, retrieved_docs: list[str]) -> str:
    # Combines retrieved chunks into one context block for prompting
    context = "\n\n".join(retrieved_docs)

    # Prompt constraints
    prompt = f"""
You are a financial report assistant.

Answer the user's question using only the context below.
If the answer is not in the context, say: "I cannot determine that from the provided filing."

When finacnial values are listed in millions, convert major figures to billions. For example:
648,125 million should be written as $648,125,000,000.

Context:
{context}

Question:
{query}

Answer:
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt},
        ],
        temperature=0.2
    )

    return response.choices[0].message.content

# Testing
if __name__ == "__main__":
    query = "What were Walmart's net sales by merchandise category in fiscal 2024?"

    results = retrieve_chunks(query)

    retrieved_docs = results["documents"][0]

    answer = generate_results(query, retrieved_docs)

    print("\nQuery:", query)
    print("\nAnswer:")
    print(answer)

    print("\nSources:")
    for i, doc in enumerate(retrieved_docs, start=1):
        print(f"\n--- Source {i} ---")
        print(doc[:700])