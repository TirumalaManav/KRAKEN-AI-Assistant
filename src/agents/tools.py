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
import logging
import requests
from chromadb import Client
from chromadb.config import Settings
from dotenv import load_dotenv
from langchain_core.tools import Tool
from langchain_huggingface import HuggingFaceEmbeddings
from typing import Dict, Optional, List, Any
import json
import google.generativeai as genai

# Load environment variables
load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DatabaseTool:
    """Enhanced database retrieval tool with embeddings for coding questions."""

    def __init__(self, client: Client):
        self.client = client
        self.embeddings = None
        self._initialize_embeddings()

    def _initialize_embeddings(self):
        """Initialize embeddings for better query matching."""
        try:
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
            logger.info("Embeddings initialized successfully")
        except Exception as e:
            logger.warning(f"Failed to initialize embeddings: {e}")
            self.embeddings = None

    def retrieve_from_db(self, query: str) -> str:
        """Retrieve relevant coding information from Chroma database."""
        try:
            collections = self.client.list_collections()
            if not collections:
                return "No coding knowledge collections found in the database. Please ensure your coding database is properly set up."

            results_found = []

            # Search through all collections for coding-related content
            for collection_info in collections:
                try:
                    collection = self.client.get_collection(name=collection_info.name)

                    # Generate query embedding if available
                    if self.embeddings:
                        query_embedding = self.embeddings.embed_query(query)
                        results = collection.query(
                            query_embeddings=[query_embedding],
                            n_results=3,
                            include=["documents", "metadatas", "distances"]
                        )
                    else:
                        # Fallback to text search
                        results = collection.query(
                            query_texts=[query],
                            n_results=3,
                            include=["documents", "metadatas"]
                        )

                    # Process results from this collection
                    if results["documents"][0]:
                        for i, doc in enumerate(results["documents"][0]):
                            metadata = results["metadatas"][0][i] if results["metadatas"][0] else {}
                            distance = results.get("distances", [[]])[0][i] if results.get("distances") else None

                            # Filter for relevant coding content
                            if self._is_coding_related(doc, metadata):
                                results_found.append({
                                    "content": doc[:800] + "..." if len(doc) > 800 else doc,
                                    "metadata": metadata,
                                    "collection": collection_info.name,
                                    "relevance_score": 1.0 - distance if distance else 0.5
                                })

                except Exception as e:
                    logger.warning(f"Error searching collection {collection_info.name}: {e}")
                    continue

            if not results_found:
                return "No relevant coding information found in the database for your query. Try rephrasing your question or ask about general programming concepts."

            # Sort by relevance and return top results
            results_found.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
            top_results = results_found[:3]

            formatted_output = "**Relevant Coding Information from Database:**\n\n"
            for i, result in enumerate(top_results, 1):
                formatted_output += f"**Result {i}:**\n"
                formatted_output += f"Content: {result['content']}\n"
                if result['metadata']:
                    formatted_output += f"Source: {result['metadata']}\n"
                formatted_output += f"Collection: {result['collection']}\n"
                formatted_output += f"Relevance: {result['relevance_score']:.2f}\n\n"

            return formatted_output

        except Exception as e:
            logger.error(f"Database retrieval failed: {e}")
            return f"Database search encountered an error: {str(e)}. Please try a different search approach."

    def _is_coding_related(self, document: str, metadata: dict) -> bool:
        """Check if the document contains coding-related content."""
        coding_keywords = [
            "algorithm", "data structure", "programming", "code", "function", "class",
            "python", "javascript", "java", "c++", "array", "tree", "graph", "sort",
            "search", "recursion", "iteration", "complexity", "leetcode", "coding",
            "development", "software", "debugging", "optimization", "performance"
        ]

        doc_lower = document.lower()
        return any(keyword in doc_lower for keyword in coding_keywords)

class WebSearchTool:
    """Enhanced web search tool optimized for coding and programming queries."""

    def __init__(self):
        self.tavily_api_key = os.getenv("TAVILY_API_KEY")
        if not self.tavily_api_key:
            logger.warning("Tavily API key is not set. WebSearch tool may have limited functionality.")

        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        if self.gemini_api_key:
            try:
                genai.configure(api_key=self.gemini_api_key)
                logger.info("Gemini API configured successfully for web search")
            except Exception as e:
                logger.warning(f"Failed to configure Gemini API: {e}")
                self.gemini_api_key = None

    def search_web(self, query: str) -> str:
        """Perform web search for coding and programming information."""
        # Enhance query for coding-specific searches
        enhanced_query = self._enhance_coding_query(query)

        # Try Tavily first for real-time web search
        if self.tavily_api_key:
            result = self._search_tavily(enhanced_query)
            if result:
                return result

        # Try Gemini API as fallback for coding knowledge
        if self.gemini_api_key:
            result = self._search_gemini(enhanced_query)
            if result:
                return result

        return "Web search is currently unavailable. Please configure API keys for Tavily or Gemini to enable web search functionality."

    def _enhance_coding_query(self, query: str) -> str:
        """Enhance query for better coding-related search results."""
        query_lower = query.lower()

        # Add programming context if not present
        programming_terms = ["algorithm", "code", "programming", "python", "javascript", "java", "c++"]
        has_programming_context = any(term in query_lower for term in programming_terms)

        if not has_programming_context:
            # Add programming context for better results
            if "dsa" in query_lower or "data structure" in query_lower:
                query += " programming algorithm implementation"
            elif any(term in query_lower for term in ["compare", "vs", "difference"]):
                query += " programming language comparison"
            else:
                query += " programming tutorial example"

        return query

    def _search_tavily(self, query: str) -> Optional[str]:
        """Search using Tavily API for real-time coding information."""
        try:
            url = "https://api.tavily.com/search"
            headers = {"Content-Type": "application/json"}
            data = {
                "api_key": self.tavily_api_key,
                "query": query,
                "max_results": 5,
                "search_depth": "advanced",
                "include_answer": True,
                "include_domains": [
                    "stackoverflow.com", "github.com", "leetcode.com",
                    "geeksforgeeks.org", "python.org", "developer.mozilla.org",
                    "docs.python.org", "tutorialspoint.com", "w3schools.com"
                ]
            }

            response = requests.post(url, json=data, headers=headers, timeout=15)
            response.raise_for_status()

            result = response.json()

            # Format results for coding context
            formatted_results = []

            # Include direct answer if available
            if result.get("answer"):
                formatted_results.append({
                    "title": "Direct Answer",
                    "content": result.get("answer"),
                    "source": "Tavily AI",
                    "type": "answer"
                })

            # Include search results
            for item in result.get("results", [])[:4]:
                formatted_results.append({
                    "title": item.get("title", "No title available"),
                    "url": item.get("url", "No URL available"),
                    "content": item.get("content", "No content available")[:600] + "..." if len(item.get("content", "")) > 600 else item.get("content", ""),
                    "source": "Web Search",
                    "type": "result"
                })

            if not formatted_results:
                return None

            # Create formatted output
            output = "**Web Search Results:**\n\n"
            for i, result in enumerate(formatted_results, 1):
                if result["type"] == "answer":
                    output += f"**🎯 {result['title']}:**\n{result['content']}\n\n"
                else:
                    output += f"**{i}. {result['title']}**\n"
                    output += f"URL: {result['url']}\n"
                    output += f"Content: {result['content']}\n\n"

            return output

        except requests.exceptions.RequestException as e:
            logger.error(f"Tavily search failed: {e}")
            return None

    def _search_gemini(self, query: str) -> Optional[str]:
        """Generate coding response using Gemini API."""
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')

            # Create a coding-focused prompt
            coding_prompt = f"""
As a coding expert, provide a comprehensive answer for the following programming query: {query}

Please include:
1. Clear explanation of the concept/problem
2. Code examples if applicable (use proper syntax highlighting)
3. Best practices and common pitfalls
4. Time/space complexity if relevant
5. Alternative approaches if applicable

Make your response practical and educational for a coding chatbot.
"""

            response = model.generate_content(coding_prompt)

            if not response.text:
                logger.warning("No content returned from Gemini API")
                return None

            formatted_output = f"**Gemini AI Response:**\n\n{response.text}"
            return formatted_output

        except Exception as e:
            logger.error(f"Gemini API request failed: {e}")
            return None

def get_tools(client: Client) -> List[Tool]:
    """Initialize and return a list of tools optimized for coding chatbot."""
    try:
        # Validate environment variables
        if not os.getenv("GEMINI_API_KEY"):
            logger.warning("GEMINI_API_KEY not set. Some tools may have limited functionality.")

        # Initialize tool instances
        db_tool = DatabaseTool(client)
        web_tool = WebSearchTool()

        # Create LangChain Tool objects with detailed descriptions
        tools = [
            Tool(
                name="DatabaseSearch",
                func=db_tool.retrieve_from_db,
                description="Search the local knowledge database for coding tutorials, algorithms, data structures, programming concepts, and previously stored coding solutions. Use this for: DSA problems, coding theory, algorithm explanations, data structure implementations, programming best practices."
            ),
            Tool(
                name="WebSearch",
                func=web_tool.search_web,
                description="Search the web for the latest coding information, programming tutorials, documentation, Stack Overflow solutions, GitHub repositories, and current programming trends. Use this for: latest framework updates, real-time coding solutions, community discussions, official documentation, new programming concepts."
            )
        ]

        logger.info("Coding chatbot tools initialized successfully")
        logger.info(f"Available tools: {[tool.name for tool in tools]}")
        return tools

    except Exception as e:
        logger.error(f"Failed to initialize tools: {e}")
        return []

# Test function for tools
def test_tools():
    """Test function to verify tools are working correctly."""
    try:
        # Create a test client
        test_client = Client(Settings(persist_directory="./test_db"))
        tools = get_tools(test_client)

        print(f"✅ Successfully initialized {len(tools)} tools")
        for tool in tools:
            print(f"   - {tool.name}: {tool.description[:100]}...")

        return True
    except Exception as e:
        print(f"❌ Tool initialization failed: {e}")
        return False

if __name__ == "__main__":
    test_tools()
