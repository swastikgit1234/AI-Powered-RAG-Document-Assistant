import os
import re
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer


# Embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# FAISS database
vector_db = None

# Store chunks in memory
document_chunks = []


def clean_text(text):
    """
    Clean unnecessary spaces and characters.
    """
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def split_text(text, chunk_size=800, overlap=150):
    """
    Split document text into overlapping chunks.
    """

    text = clean_text(text)

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk.strip())

        start += chunk_size - overlap

    return chunks


def create_embeddings(chunks):
    """
    Generate embeddings for document chunks.
    """

    embeddings = embedding_model.encode(
        chunks,
        convert_to_numpy=True
    )

    embeddings = embeddings.astype("float32")

    # Normalize embeddings so inner product behaves like cosine similarity
    faiss.normalize_L2(embeddings)

    return embeddings


def create_vector_database(chunks):
    """
    Create FAISS vector database.
    """

    global vector_db
    global document_chunks

    document_chunks = chunks

    embeddings = create_embeddings(chunks)

    dimension = embeddings.shape[1]

    vector_db = faiss.IndexFlatIP(dimension)

    vector_db.add(embeddings)

    return len(chunks)


def search_similar_chunks(question, top_k=4):
    """
    Search for chunks relevant to the user's question.
    """

    if vector_db is None or len(document_chunks) == 0:
        return []

    question_embedding = embedding_model.encode(
        [question],
        convert_to_numpy=True
    ).astype("float32")

    faiss.normalize_L2(question_embedding)

    scores, indexes = vector_db.search(
        question_embedding,
        top_k
    )

    results = []

    for score, index in zip(scores[0], indexes[0]):

        if index == -1:
            continue

        results.append({
            "text": document_chunks[index],
            "score": float(score)
        })

    return results