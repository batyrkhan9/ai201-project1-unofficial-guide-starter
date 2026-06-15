from sentence_transformers import SentenceTransformer
import chromadb
from ingest import load_chunks

def embed_and_store():
    chunks, metadatas = load_chunks()
    
    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    print("Embedding chunks...")
    embeddings = model.encode(chunks).tolist()
    
    print("Storing in ChromaDB...")
    client = chromadb.Client()
    collection = client.get_or_create_collection("professor_reviews")
    
    ids = [str(i) for i in range(len(chunks))]
    
    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )
    
    print(f"Stored {len(chunks)} chunks in ChromaDB")
    return client, collection

if __name__ == "__main__":
    client, collection = embed_and_store()
    
    print("\nTesting retrieval...")
    results = collection.query(
        query_texts=["harsh grader"],
        n_results=3
    )
    
    for i, doc in enumerate(results["documents"][0]):
        print(f"\n--- Result {i+1} ---")
        print(doc)
        print(f"Source: {results['metadatas'][0][i]['source']}")