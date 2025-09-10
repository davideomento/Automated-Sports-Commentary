import json
from sentence_transformers import SentenceTransformer
import faiss

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_embeddings(texts, model):
    return model.encode(texts, show_progress_bar=True, convert_to_numpy=True, normalize_embeddings=True)

def build_faiss_index(embeddings):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)  # Inner Product for cosine similarity with normalized vectors
    index.add(embeddings)
    return index

def save_index(index, index_file):
    faiss.write_index(index, index_file)

def save_metadata(metadata_list, metadata_file):
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata_list, f, indent=2)

def main():
    # Modifica con i tuoi file JSON
    season_file = 'data/preprocessed/RAG/rag_documents_season.json'
    week_file = 'data/preprocessed/RAG/rag_documents_week.json'

    # Carica dati
    season_data = load_json(season_file)
    week_data = load_json(week_file)

    # Modello embedding
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Estrai testi e metadata
    season_texts = [item['content'] for item in season_data]
    season_metadata = [item['metadata'] for item in season_data]

    week_texts = [item['content'] for item in week_data]
    week_metadata = [item['metadata'] for item in week_data]

    # Crea embeddings
    season_embeddings = create_embeddings(season_texts, model)
    week_embeddings = create_embeddings(week_texts, model)

    # Costruisci indici
    season_index = build_faiss_index(season_embeddings)
    week_index = build_faiss_index(week_embeddings)

    # Salva indici e metadata
    save_index(season_index, 'season_index.faiss')
    save_metadata(season_metadata, 'season_metadata.json')

    save_index(week_index, 'week_index.faiss')
    save_metadata(week_metadata, 'week_metadata.json')

    print("Indexing completato!")

if __name__ == '__main__':
    main()
