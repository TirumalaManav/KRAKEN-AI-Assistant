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
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def load_code_files(data_dir=None):
    """
    Load all .txt files from a specified directory and return their content.
    Args:
        data_dir (str, optional): Directory path containing .txt files. Defaults to environment variable or None.
    Returns:
        dict: Dictionary with filenames as keys and list of lines as values.
    """
    try:
        if data_dir is None:
            data_dir = os.getenv("DATA_DIR", r"C:\Users\ursti\Downloads\Code Explainer\data")
        if not os.path.exists(data_dir):
            raise FileNotFoundError(f"Data directory not found: {data_dir}")

        code_data = {}
        for filename in os.listdir(data_dir):
            if filename.lower().endswith((".txt", ".py")):
                file_path = os.path.join(data_dir, filename)
                with open(file_path, "r", encoding="utf-8") as file:
                    code_data[filename] = file.read().splitlines()
        if not code_data:
            print("No valid files found in the directory.")
        return code_data
    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
        return {}
    except Exception as e:
        print(f"Unexpected error loading files: {str(e)}")
        return {}

def clean_code(lines):
    """
    Remove extra spaces from the start and end of each line.
    Args:
        lines (list): List of text lines to clean.
    Returns:
        list: Cleaned list of lines.
    """
    try:
        if not lines or not isinstance(lines, list):
            raise ValueError("Input must be a non-empty list of lines.")
        return [line.strip() for line in lines if line.strip()]
    except Exception as e:
        print(f"Error cleaning code: {str(e)}")
        return []

def save_cleaned_data(code_data, output_dir=r"C:\Users\ursti\Downloads\Code Explainer\src\data_processing\cleaned_data"):
    """
    Save cleaned data to a new directory with original filenames.
    Args:
        code_data (dict): Dictionary of filename:lines pairs.
        output_dir (str): Directory to save cleaned files (default: specified path).
    """
    try:
        if not code_data:
            raise ValueError("No data to save.")
        os.makedirs(output_dir, exist_ok=True)
        for filename, lines in code_data.items():
            cleaned_filename = os.path.join(output_dir, filename)  # Keep original filename
            with open(cleaned_filename, "w", encoding="utf-8") as file:
                file.write("\n".join(clean_code(lines)))
    except Exception as e:
        print(f"Error saving cleaned data: {str(e)}")

if __name__ == "__main__":
    code_data = load_code_files()
    save_cleaned_data(code_data)
    for filename in code_data.keys():
        print(f"Processed {filename}")
