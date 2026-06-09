import os
import chromadb
from chromadb.utils import embedding_functions
from groq import Groq
from dotenv import load_dotenv

load_dotenv()  # reads your GROQ_API_KEY from .env

# --- connect to your existing vector store ---
embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)
client = chromadb.PersistentClient(path="chroma_store")
collection = client.get_collection(name="reviews", embedding_function=embed_fn)

# --- connect to Groq ---
groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])

SYSTEM_PROMPT = """You are a helpful guide that answers questions about professors using ONLY the student reviews provided as context.
Rules:
- Answer using only the information in the provided reviews.
- If the reviews do not contain enough information, reply exactly: "I don't have enough information on that."
- Do not use any outside knowledge.
- When opinions conflict, mention both sides."""

def ask(question):
    # 1. retrieve top chunks
    results = collection.query(query_texts=[question], n_results=5)
    chunks = results["documents"][0]
    metas = results["metadatas"][0]

    # 2. build the context block from retrieved chunks
    context = "\n\n".join(
        f"[Review of {m['professor']}]: {c}" for c, m in zip(chunks, metas)
    )

    # 3. ask the LLM, grounded in that context
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ],
    )
def ask(question):
    results = collection.query(query_texts=[question], n_results=5)
    chunks = results["documents"][0]
    metas = results["metadatas"][0]

    context = "\n\n".join(
        f"[Review of {m['professor']}]: {c}" for c, m in zip(chunks, metas)
    )

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ],
    )
    answer = response.choices[0].message.content

    # --- build a guaranteed source list from the retrieved chunks' metadata ---
    seen = set()
    sources = []
    for m in metas:
        key = (m["professor"], m["source"])
        if key not in seen:
            seen.add(key)
            sources.append(f"{m['professor']} — {m['source']}")

    return {"answer": answer, "sources": sources}

if __name__ == "__main__":
    result = ask("What is the parking situation like on campus?")
    print(result["answer"])
    print("\nSources:")
    for s in result["sources"]:
        print(" -", s)