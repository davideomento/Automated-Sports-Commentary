import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

def load_index_and_metadata(index_path, metadata_path):
    index = faiss.read_index(index_path)
    with open(metadata_path, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    return index, metadata

def embed_query(query, model):
    return model.encode([query], normalize_embeddings=True)

def retrieve_top_k(query_embedding, index, metadata, texts, k=3):
    D, I = index.search(query_embedding, k)
    results = []
    for i in I[0]:
        if i < len(metadata):
            results.append({
                "content": texts[i],
                "metadata": metadata[i]
            })
    return results

def load_contents(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return [item['content'] for item in data]

def main():
    # Load index, metadata and text data
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Season
    season_index, season_metadata = load_index_and_metadata(
        'mistral/retrieval/indexes/season_index.faiss', 'mistral/retrieval/indexes/season_metadata.json')
    season_texts = load_contents('mistral/RAG/rag_documents_season.json')

    # Week
    week_index, week_metadata = load_index_and_metadata(
        'mistral/retrieval/indexes/week_index.faiss', 'mistral/retrieval/indexes/week_metadata.json')
    week_texts = load_contents('mistral/RAG/rag_documents_week.json')

    # Query
    query = input("Your query: ")
    query_embedding = embed_query(query, model)

    season_results = retrieve_top_k(query_embedding, season_index, season_metadata, season_texts, k=3)
    week_results = retrieve_top_k(query_embedding, week_index, week_metadata, week_texts, k=3)

    combined_context = "\n\n".join([doc["content"] for doc in season_results + week_results])

    print("\n📄 Retrieved Context:\n")
    print(combined_context)

    # (Optional) now pass combined_context to your LLM to answer the query

if __name__ == "__main__":
    main()
