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
import chromadb
from chromadb.config import Settings

def initialize_vector_db(db_path=r"C:\Users\ursti\Downloads\Code Explainer\src\embeddings\vector_db"):
    """
    Initialize or connect to a Chroma vector database.
    Args:
        db_path (str): Directory to store the database (default: absolute path).
    Returns:
        chromadb.Client: Chroma database client.
    """
    try:
        os.makedirs(db_path, exist_ok=True)  # Ensure directory exists
        client = chromadb.Client(Settings(persist_directory=db_path, is_persistent=True))
        print(f"Database initialized at: {db_path}")  # Debug print to confirm path
        with open(os.path.join(db_path, "test_write.txt"), "w") as f:
            f.write("Test write successful")
        return client
    except Exception as e:
        print(f"Error initializing vector database: {str(e)}")
        return None

def store_embeddings(client, collection_name, embeddings, metadatas=None, ids=None):
    """
    Store embeddings in a Chroma collection.
    Args:
        client (chromadb.Client): Chroma database client.
        collection_name (str): Name of the collection.
        embeddings (list): List of embedding vectors.
        metadatas (list, optional): Metadata for each embedding.
        ids (list, optional): Unique IDs for each embedding.
    """
    try:
        if client is None:
            client = initialize_vector_db()
        if not client:
            raise ValueError("Database client could not be initialized.")
        collection = client.get_or_create_collection(name=collection_name)
        if not ids:
            ids = [f"{collection_name}_id_{i}" for i in range(len(embeddings))]
        if not metadatas:
            metadatas = [{} for _ in range(len(embeddings))]  # Default to empty dicts
        collection.add(embeddings=embeddings, metadatas=metadatas, ids=ids)
        print(f"Stored {len(embeddings)} embeddings in {collection_name}")
    except Exception as e:
        print(f"Error storing embeddings: {str(e)}")

def query_vector_db(client, collection_name, query_embedding, n_results=5):
    """
    Query the vector database for similar embeddings.
    Args:
        client (chromadb.Client): Chroma database client.
        collection_name (str): Name of the collection.
        query_embedding (list): Embedding to query with.
        n_results (int): Number of similar results to return.
    Returns:
        list: List of similar document IDs and distances.
    """
    try:
        if not client:
            raise ValueError("Database client is not initialized.")
        collection = client.get_collection(name=collection_name)
        results = collection.query(query_embeddings=[query_embedding], n_results=n_results)
        return results
    except Exception as e:
        print(f"Error querying vector database: {str(e)}")
        return None

if __name__ == "__main__":
    pass
