"""
KRAKEN - Advanced AI Coding Assistant
=====================================

Description: [Brief description of this module's functionality]

Author: Tirumala Manav
Email: tirumalamanav@example.com
GitHub:https://github.com/TirumalaManav
LinkedIn: https://linkedin.com/in/tirumalamanav

Project: KRAKEN AI Assistant
Repository: https://github.com/TirumalaManav/KRAKEN-AI-Assistant
Created: 2025-07-16
Last Modified: 2025-07-16

License: MIT License
Copyright (c) 2025 Tirumala Manav

Technology Stack:
- LangChain for AI orchestration
- ChromaDB for vector storage
- Streamlit for web interface
- Google Gemini API for LLM capabilities
- Sentence Transformers for embeddings

"""

import os
from sentence_transformers import SentenceTransformer
import numpy as np
from vector_db import store_embeddings, initialize_vector_db  # Import vector DB functions

def generate_embeddings(chunks, model_name="all-MiniLM-L6-v2"):
    """
    Generate embeddings for a list of text chunks using a pre-trained model.
    Args:
        chunks (list): List of text chunks to embed.
        model_name (str): Name of the pre-trained model (default: 'all-MiniLM-L6-v2').
    Returns:
        list: List of numpy arrays representing embeddings.
    """
    try:
        if not chunks or not isinstance(chunks, list):
            raise ValueError("Input must be a non-empty list of chunks.")
        model = SentenceTransformer(model_name)
        embeddings = model.encode(chunks, convert_to_numpy=True)
        return embeddings.tolist()  # Convert to list for storage
    except Exception as e:
        print(f"Error generating embeddings: {str(e)}")
        return []

def process_chunks_directory(chunk_dir):
    """
    Process all chunk files in a directory and generate/store embeddings.
    Args:
        chunk_dir (str): Directory containing chunked text files.
    Returns:
        dict: Mapping of filenames to their embeddings.
    """
    try:
        if not os.path.exists(chunk_dir):
            raise FileNotFoundError(f"Chunk directory not found: {chunk_dir}")

        embeddings_data = {}
        client = initialize_vector_db()  # Initialize DB once
        if not client:
            raise ValueError("Failed to initialize vector database.")

        chunk_files = [f for f in os.listdir(chunk_dir) if f.endswith(".txt")]
        model = SentenceTransformer("all-MiniLM-L6-v2")  # Load once for efficiency
        for chunk_file in chunk_files:
            file_path = os.path.join(chunk_dir, chunk_file)
            with open(file_path, "r", encoding="utf-8") as file:
                chunks = [file.read()]  # Process each file as one chunk
                embeddings = generate_embeddings(chunks)
                if embeddings:
                    base_name = os.path.splitext(chunk_file)[0]
                    metadatas = [{"source": base_name, "chunk_idx": i} for i in range(len(embeddings))]
                    ids = [f"{base_name}_id_{i}" for i in range(len(embeddings))]
                    store_embeddings(client, base_name, embeddings, metadatas=metadatas, ids=ids)
                    embeddings_data[base_name] = embeddings
                    print(f"Generated and stored embeddings for {base_name}")
        return embeddings_data
    except Exception as e:
        print(f"Error processing chunks: {str(e)}")
        return {}

if __name__ == "__main__":
    # Suppress Chroma telemetry
    os.environ["CHROMA_TELEMETRY"] = "false"
    chunk_dir = r"C:\Users\ursti\Downloads\Code Explainer\src\data_processing\chunked_data"
    embeddings_data = process_chunks_directory(chunk_dir)
    if embeddings_data:
        print(f"Total embeddings generated: {sum(len(v) for v in embeddings_data.values())}")
