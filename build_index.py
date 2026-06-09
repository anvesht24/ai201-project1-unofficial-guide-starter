import chromadb
from chromadb.utils import embedding_functions
from pipeline import load_documents, clean_document, chunk_document

# 1. Build all chunks using your Milestone 3 pipeline
docs = [clean_document(d) for d in load_documents()]
all_chunks = []
for doc in docs:
    all_chunks.extend(chunk_document(doc))

print(f"Embedding {len(all_chunks)} chunks...")

# 2. Set up the embedding model (your planning.md choice)
embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# 3. Create a local ChromaDB collection
client = chromadb.PersistentClient(path="chroma_store")
collection = client.get_or_create_collection(
    name="reviews",
    embedding_function=embed_fn,
)

# 4. Add chunks with their text, metadata, and an id each
collection.add(
    ids=[f"chunk_{i}" for i in range(len(all_chunks))],
    documents=[c["text"] for c in all_chunks],
    metadatas=[
        {"professor": c["professor"], "source": c["source"], "filename": c["filename"]}
        for c in all_chunks
    ],
)

print(f"Done. Collection now has {collection.count()} chunks.")