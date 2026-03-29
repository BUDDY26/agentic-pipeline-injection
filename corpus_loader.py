# corpus_loader.py
# Loads, tags, chunks, embeds, and indexes the corpus into FAISS.

import os
import json
import pickle
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

CORPUS_DIR = Path(__file__).parent / 'corpus'
INDEX_DIR  = Path(__file__).parent / 'faiss_index'
CHUNK_SIZE = 512  # characters per chunk (not tokens)
CHUNK_OVERLAP = 50  # overlap between consecutive chunks


def tag_document(filename: str) -> str:
    """Return 'adversarial' if filename starts with 'adversarial_', else 'benign'."""
    return 'adversarial' if filename.startswith('adversarial_') else 'benign'


def chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP):
    """Split text into overlapping character-based chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + size, len(text))
        chunks.append(text[start:end].strip())
        start += size - overlap
    return [c for c in chunks if c]


def load_corpus():
    """
    Read all .txt files in corpus/, tag each, chunk each, return a list of dicts:
    { 'document_id': str, 'label': str, 'chunk_index': int, 'text': str }
    """
    records = []
    for path in sorted(CORPUS_DIR.glob('*.txt')):
        label = tag_document(path.name)
        text  = path.read_text(encoding='utf-8')
        chunks = chunk_text(text)
        for i, chunk in enumerate(chunks):
            records.append({
                'document_id': path.stem,
                'label':       label,
                'chunk_index': i,
                'text':        chunk
            })
    return records


def build_index(records, model_name='all-MiniLM-L6-v2'):
    """
    Embed all chunks and build a FAISS IndexFlatIP.
    Saves index.faiss and index.pkl to INDEX_DIR.
    Returns (faiss_index, metadata_list).
    """
    print(f'Loading embedding model: {model_name}')
    model = SentenceTransformer(model_name)
    texts = [r['text'] for r in records]
    print(f'Embedding {len(texts)} chunks...')
    embeddings = model.encode(texts, show_progress_bar=True, normalize_embeddings=True)
    embeddings = np.array(embeddings).astype('float32')
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)  # Inner product == cosine sim on normalized vectors
    index.add(embeddings)
    INDEX_DIR.mkdir(exist_ok=True)
    faiss.write_index(index, str(INDEX_DIR / 'index.faiss'))
    with open(INDEX_DIR / 'index.pkl', 'wb') as f:
        pickle.dump({'records': records, 'model_name': model_name}, f)
    print(f'Index built: {index.ntotal} vectors. Saved to {INDEX_DIR}/')
    return index, records


def load_index():
    """Load a previously built FAISS index and metadata from INDEX_DIR."""
    index = faiss.read_index(str(INDEX_DIR / 'index.faiss'))
    with open(INDEX_DIR / 'index.pkl', 'rb') as f:
        meta = pickle.load(f)
    return index, meta['records'], meta['model_name']


def retrieve(query: str, index, records, model_name='all-MiniLM-L6-v2', k: int = 3):
    """
    Retrieve top-k chunks for a query.
    Returns list of dicts with 'text', 'document_id', 'label', 'score', 'rank'.
    """
    model = SentenceTransformer(model_name)
    q_emb = model.encode([query], normalize_embeddings=True).astype('float32')
    scores, indices = index.search(q_emb, k)
    results = []
    for rank, (score, idx) in enumerate(zip(scores[0], indices[0]), start=1):
        r = records[idx].copy()
        r['score'] = float(score)
        r['rank']  = rank
        results.append(r)
    return results


if __name__ == '__main__':
    records = load_corpus()
    print(f'Loaded {len(records)} chunks from {CORPUS_DIR}/')
    for r in records:
        print(f"  [{r['label']:12s}] {r['document_id']} chunk {r['chunk_index']}")
    build_index(records)
