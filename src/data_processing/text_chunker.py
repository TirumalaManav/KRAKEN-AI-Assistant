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
from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_text(text_lines, chunk_size=300, chunk_overlap=50):
    """
    Split text lines into chunks with configurable size and overlap.
    Args:
        text_lines (list): List of text lines to chunk.
        chunk_size (int): Maximum number of characters per chunk (default: 300).
        chunk_overlap (int): Number of overlapping characters between chunks (default: 50).
    Returns:
        list: List of chunked text strings.
    """
    try:
        if not text_lines or not isinstance(text_lines, list):
            raise ValueError("Input must be a non-empty list of text lines.")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len
        )
        chunks = text_splitter.split_text("\n".join(text_lines))
        return chunks
    except Exception as e:
        print(f"Error chunking text: {str(e)}")
        return []

def save_chunks(chunks, base_filename, output_dir="chunked_data"):
    """
    Save chunks to individual files in a specified directory.
    Args:
        chunks (list): List of text chunks to save.
        base_filename (str): Base name for output files (e.g., 'project1').
        output_dir (str): Directory to save chunks (default: 'chunked_data').
    """
    try:
        if not chunks:
            raise ValueError("No chunks to save.")
        os.makedirs(output_dir, exist_ok=True)
        for i, chunk in enumerate(chunks):
            chunk_file = os.path.join(output_dir, f"{base_filename}_chunk_{i}.txt")
            with open(chunk_file, "w", encoding="utf-8") as file:
                file.write(chunk)
    except Exception as e:
        print(f"Error saving chunks: {str(e)}")

def process_file(file_path, chunk_size=300, chunk_overlap=50, output_dir="chunked_data"):
    """
    Process a single file by loading, chunking, and saving its content.
    Args:
        file_path (str): Path to the input text file.
        chunk_size (int): Maximum characters per chunk.
        chunk_overlap (int): Overlap between chunks.
        output_dir (str): Directory to save chunks.
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.read().splitlines()
        chunks = chunk_text(lines, chunk_size, chunk_overlap)
        base_name = os.path.splitext(os.path.basename(file_path))[0]  # Use full filename
        save_chunks(chunks, base_name, output_dir)
        print(f"Processed {file_path} into {len(chunks)} chunks")
    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")

if __name__ == "__main__":
    # Updated file paths to match your cleaned data location
    input_files = [
        r"C:\Users\ursti\Downloads\Code Explainer\src\data_processing\cleaned_data\cleaned_1.txt",
        r"C:\Users\ursti\Downloads\Code Explainer\src\data_processing\cleaned_data\cleaned_2.txt",
        r"C:\Users\ursti\Downloads\Code Explainer\src\data_processing\cleaned_data\cleaned_3.txt",
        r"C:\Users\ursti\Downloads\Code Explainer\src\data_processing\cleaned_data\cleaned_4.txt"
    ]
    for file_path in input_files:
        process_file(file_path, chunk_size=300, chunk_overlap=50)
