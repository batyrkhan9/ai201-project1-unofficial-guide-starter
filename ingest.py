import os

def load_chunks(data_folder="data"):
    chunks = []
    metadatas = []
    
    for filename in os.listdir(data_folder):
        if filename.endswith(".txt"):
            filepath = os.path.join(data_folder, filename)
            with open(filepath, "r") as f:
                content = f.read()
            
            reviews = content.split("---")
            
            for review in reviews:
                review = review.strip()
                if len(review) > 0:
                    chunks.append(review)
                    metadatas.append({"source": filename})
    
    return chunks, metadatas

if __name__ == "__main__":
    chunks, metadatas = load_chunks()
    print(f"Total chunks: {len(chunks)}")
    for i in range(5):
        print(f"\n--- Chunk {i+1} ---")
        print(chunks[i])
        print(f"Source: {metadatas[i]['source']}")