from pathlib import Path

DOCS_DIR = Path("documents")

#Loading the documents with reviews we created 
def load_documents():
    docs = []
    for file in DOCS_DIR.glob("*.txt"):
        text = file.read_text(encoding="utf-8")
        docs.append({"filename": file.name, "text": text})
    return docs

#Cleaning the data extracted from the documents to get the filtered data
def clean_document(doc):
    lines = doc["text"].splitlines()

    source = ""
    professor = ""
    body_lines = []

    for line in lines:
        if line.lower().startswith("source:"):
            source = line.split(":", 1)[1].strip()
        elif line.lower().startswith("professor:"):
            professor = line.split(":", 1)[1].strip()
        else:
            body_lines.append(line)

    # join the review text, collapse big gaps of blank lines
    body = "\n".join(body_lines).strip()

    return {
        "filename": doc["filename"],
        "source": source,
        "professor": professor,
        "text": body,
    }

def chunk_document(doc):
    # split the body into reviews wherever there are blank lines
    raw_reviews = doc["text"].split("\n\n")

    chunks = []
    for review in raw_reviews:
        review = review.strip()
        if len(review) > 0:                 # skip empty pieces
            chunks.append({
                "text": review,
                "professor": doc["professor"],
                "source": doc["source"],
                "filename": doc["filename"],
            })
    return chunks


if __name__ == "__main__":
    docs = load_documents()
    cleaned = [clean_document(d) for d in docs]


    all_chunks = []
    for doc in cleaned:
        all_chunks.extend(chunk_document(doc))

    print(f"Total chunks: {len(all_chunks)}")
    print("\n===== Inspecting 5 chunks =====\n")

    import random
    for i, chunk in enumerate(random.sample(all_chunks, 5), 1):
        print(f"--- Chunk {i} | {chunk['professor']} ---")
        print(chunk["text"])
        print(f"(length: {len(chunk['text'])} chars)\n")