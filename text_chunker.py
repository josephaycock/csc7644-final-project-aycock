from pdf_loader import load_pdf

def chunk_text(text: str, chunk_size: int = 1200, overlap: int = 200) -> list[dict]:

    if not text:
        return []

    if overlap >= chunk_size:
        raise ValueError(f"Error: Overlap must be smaller than chunk_size.")

    chunks = []
    start = 0
    chunk_id = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append({
                "id": f"chunk_{chunk_id}",
                "text": chunk
            })
            chunk_id += 1

        start += chunk_size - overlap

    return chunks

if __name__ == "__main__":
    pdf_path = "data/raw/walmart-10k.pdf"

    text = load_pdf(pdf_path)
    chunks = chunk_text(text)

    print("Total characters:", len(text))
    print("Total chunks:", len(chunks))
    print("First chunk total:",len(chunks[0]["text"]))

    print("\nFirst chunk ID:", chunks[0]["id"])
    print("Preview:", chunks[0]["text"][:300])