import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import chromadb
from groq import Groq
from ingest import load_chunks

load_dotenv()

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.Client()
collection = client.get_or_create_collection("professor_reviews")

chunks, metadatas = load_chunks()
embeddings = model.encode(chunks).tolist()
ids = [str(i) for i in range(len(chunks))]
collection.add(
    ids=ids,
    documents=chunks,
    embeddings=embeddings,
    metadatas=metadatas
)

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask(question):
    results = collection.query(
        query_texts=[question],
        n_results=5
    )
    
    retrieved_chunks = results["documents"][0]
    sources = [m["source"] for m in results["metadatas"][0]]
    
    context = "\n\n".join(retrieved_chunks)
    
    prompt = f"""You are a helpful assistant for Minerva University students.
Answer the question using ONLY the information provided in the documents below.
If the documents don't contain enough information to answer, say 'I don't have enough information on that.'
Always be specific and cite which professor you are referring to.

Documents:
{context}

Question: {question}"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    
    answer = response.choices[0].message.content
    
    return {
        "answer": answer,
        "sources": list(set(sources))
    }

if __name__ == "__main__":
    result = ask("Who is the harshest grader?")
    print(result["answer"])
    print("\nSources:", result["sources"])