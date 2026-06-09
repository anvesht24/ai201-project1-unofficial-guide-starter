import chromadb
from chromadb.utils import embedding_functions

embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)
client = chromadb.PersistentClient(path="chroma_store")
collection = client.get_collection(name="reviews", embedding_function=embed_fn)

query = "Which professor has confusing or unfair exams?"

results = collection.query(query_texts=[query], n_results=5)

print(f"Query: {query}\n")
for i, (doc, meta) in enumerate(zip(results["documents"][0], results["metadatas"][0]), 1):
    print(f"--- Result {i} | {meta['professor']} ---")
    print(doc)
    print()