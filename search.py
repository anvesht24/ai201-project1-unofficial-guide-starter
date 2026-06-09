import chromadb
from chromadb.utils import embedding_functions

embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)
client = chromadb.PersistentClient(path="chroma_store")
collection = client.get_collection(name="reviews", embedding_function=embed_fn)

query =  "What are Mihaela Cardei's tests and homework based on?"

results = collection.query(
    query_texts=[query],
    n_results=5,
    include=["documents", "metadatas", "distances"],   # <-- add distances
)

print(f"Query: {query}\n")
for i, (doc, meta, dist) in enumerate(zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]), 1):
    print(f"--- Result {i} | {meta['professor']} | distance: {dist:.3f} ---")
    print(doc)
    print()