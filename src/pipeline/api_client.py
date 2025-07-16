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
import json
import google.generativeai as genai
from dotenv import load_dotenv
from typing import Optional, Dict, List
from datetime import datetime, UTC

# Load environment variables
load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class APIClient:
    """Handles API interactions for the RAG pipeline - Updated 2025-07-15."""

    def __init__(self):
        """Initialize API client with Gemini and Tavily configurations."""
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.tavily_api_key = os.getenv("TAVILY_API_KEY")
        self.current_user = "TIRUMALA MANAV"
        self.initialization_time = datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S')

        self._configure_gemini()
        logger.info(f"APIClient initialized for user {self.current_user} at {self.initialization_time} UTC")

    def _configure_gemini(self) -> None:
        """Configure Gemini API if key is available."""
        if self.gemini_api_key:
            try:
                genai.configure(api_key=self.gemini_api_key)
                logger.info("Gemini API configured successfully")
            except Exception as e:
                logger.error(f"Failed to configure Gemini API: {e}")
                self.gemini_api_key = None
        else:
            logger.warning("GEMINI_API_KEY not set in environment variables")

    def get_gemini_response(self, prompt: str, temperature: float = 0.1) -> Optional[str]:
        """Get response from Gemini API with enhanced error handling."""
        if not self.gemini_api_key:
            logger.error("Gemini API key not available")
            return None

        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            enhanced_prompt = f"""
            User: {self.current_user}
            Timestamp: {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S')} UTC
            Query: {prompt}
            Please provide a comprehensive, educational response suitable for a coding chatbot.
            Include code examples, explanations, and best practices where applicable.
            """
            response = model.generate_content(
                enhanced_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=2048,
                )
            )
            if response.text:
                logger.info(f"Gemini response generated successfully (length: {len(response.text)})")
                return response.text
            else:
                logger.warning("Gemini API returned empty response")
                return None
        except Exception as e:
            logger.error(f"Gemini API request failed: {e}")
            return None

    def search_tavily(self, query: str, max_results: int = 5) -> Optional[str]:
        """Perform web search using Tavily API with enhanced formatting."""
        if not self.tavily_api_key:
            logger.warning("Tavily API key not available, skipping web search")
            return None

        try:
            url = "https://api.tavily.com/search"
            headers = {"Content-Type": "application/json"}
            enhanced_query = self._enhance_coding_query(query)
            data = {
                "api_key": self.tavily_api_key,
                "query": enhanced_query,
                "max_results": max_results,
                "search_depth": "advanced",
                "include_answer": True,
                "include_raw_content": False,
                "include_domains": [
                    "stackoverflow.com", "github.com", "geeksforgeeks.org",
                    "leetcode.com", "tutorialspoint.com", "w3schools.com",
                    "developer.mozilla.org", "docs.python.org", "python.org"
                ]
            }
            logger.debug(f"Tavily search request: {enhanced_query}")
            response = requests.post(url, json=data, headers=headers, timeout=15)
            response.raise_for_status()
            result = response.json()
            return self._format_tavily_results(result)
        except requests.exceptions.Timeout:
            logger.error("Tavily search timed out after 15 seconds")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Tavily search failed: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in Tavily search: {e}")
            return None

    def _enhance_coding_query(self, query: str) -> str:
        """Enhance query for better coding-related search results."""
        query_lower = query.lower()
        programming_terms = ["algorithm", "code", "programming", "python", "javascript", "java", "c++", "implementation", "tutorial", "example"]
        has_programming_context = any(term in query_lower for term in programming_terms)

        if not has_programming_context:
            if any(term in query_lower for term in ["dsa", "data structure", "leetcode"]):
                query += " programming algorithm implementation tutorial"
            elif any(term in query_lower for term in ["compare", "vs", "difference"]):
                query += " programming language comparison tutorial"
            elif any(term in query_lower for term in ["sort", "search", "tree", "graph"]):
                query += " algorithm implementation code example"
            else:
                query += " programming tutorial code example"
        return query

    def _format_tavily_results(self, result: Dict) -> Optional[str]:
        """Format Tavily search results for better presentation."""
        try:
            formatted_parts = []
            if result.get("answer"):
                formatted_parts.append(f"**🎯 Direct Answer:**\n{result.get('answer')}\n")
            results = result.get("results", [])
            if results:
                formatted_parts.append("**🔍 Search Results:**")
                for i, item in enumerate(results[:4], 1):
                    title = item.get("title", "No title available")
                    url = item.get("url", "No URL available")
                    content = item.get("content", "No content available")[:400] + "..." if len(item.get("content", "")) > 400 else item.get("content", "")
                    formatted_parts.append(f"\n**{i}. {title}**\n🔗 URL: {url}\n📄 Content: {content}\n")
            formatted_parts.extend([
                f"**ℹ️ Search performed at:** {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S')} UTC",
                f"**👤 Requested by:** {self.current_user}"
            ])
            return "\n".join(formatted_parts) if formatted_parts else None
        except Exception as e:
            logger.error(f"Error formatting Tavily results: {e}")
            return None

    def search_gemini_fallback(self, query: str) -> Optional[str]:
        """Use Gemini as fallback for web search when Tavily is unavailable."""
        if not self.gemini_api_key:
            logger.warning("Gemini API not available for fallback search")
            return None

        try:
            enhanced_prompt = f"""
            As a coding expert, provide a comprehensive answer for this programming query: {query}
            Include: 1. Explanation, 2. Code examples with ```language```, 3. Step-by-step implementation if applicable,
            4. Time/space complexity if relevant, 5. Best practices, 6. Common pitfalls, 7. Alternatives.
            User: {self.current_user}, Timestamp: {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S')} UTC,
            Source: Gemini AI Fallback Search
            """
            response = self.get_gemini_response(enhanced_prompt, temperature=0.2)
            if response:
                return f"**🤖 AI Knowledge Base:**\n\n{response}\n\n**ℹ️ Generated at:** {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S')} UTC\n**👤 Requested by:** {self.current_user}"
            return None
        except Exception as e:
            logger.error(f"Gemini fallback search failed: {e}")
            return None

    def validate_api_keys(self) -> Dict[str, bool]:
        """Validate availability and functionality of API keys."""
        validation_results = {
            "gemini_key_present": bool(self.gemini_api_key),
            "tavily_key_present": bool(self.tavily_api_key),
            "gemini_functional": False,
            "tavily_functional": False,
            "any_available": False
        }
        if self.gemini_api_key:
            try:
                test_response = self.get_gemini_response("Hello, this is a test.", temperature=0.1)
                validation_results["gemini_functional"] = bool(test_response)
            except Exception:
                pass
        validation_results["tavily_functional"] = bool(self.tavily_api_key)
        validation_results["any_available"] = validation_results["gemini_functional"] or validation_results["tavily_functional"]
        return validation_results

    def get_api_status(self) -> Dict[str, str]:
        """Get detailed status of all APIs with timestamps."""
        status = {
            "timestamp": datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC'),
            "user": self.current_user,
            "initialization_time": self.initialization_time
        }
        if self.gemini_api_key:
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                test_response = model.generate_content("Test")
                status["gemini"] = "✅ Working properly" if test_response.text else "⚠️ Not responding correctly"
            except Exception as e:
                status["gemini"] = f"❌ Error: {str(e)[:100]}..."
        else:
            status["gemini"] = "❌ No API key configured"
        status["tavily"] = "✅ API key available (functional test requires search)" if self.tavily_api_key else "❌ No API key configured"
        status["overall"] = f"✅ {sum(1 for v in [status['gemini'], status['tavily']] if '✅' in v)}/2 APIs operational" if any("✅" in v for v in [status['gemini'], status['tavily']]) else "❌ No APIs operational"
        return status

    def test_all_apis(self, test_query: str = "Explain binary search algorithm") -> Dict[str, any]:
        """Test all APIs with a sample query and return results."""
        test_results = {
            "test_query": test_query,
            "timestamp": datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC'),
            "user": self.current_user,
            "results": {}
        }
        logger.info("Testing Gemini API...")
        gemini_start = datetime.now(UTC)
        gemini_result = self.get_gemini_response(test_query)
        gemini_time = (datetime.now(UTC) - gemini_start).total_seconds()
        test_results["results"]["gemini"] = {
            "success": bool(gemini_result),
            "response_length": len(gemini_result) if gemini_result else 0,
            "response_time": f"{gemini_time:.2f}s",
            "preview": gemini_result[:100] + "..." if gemini_result else "No response"
        }
        logger.info("Testing Tavily API...")
        tavily_start = datetime.now(UTC)
        tavily_result = self.search_tavily(test_query, max_results=2)
        tavily_time = (datetime.now(UTC) - tavily_start).total_seconds()
        test_results["results"]["tavily"] = {
            "success": bool(tavily_result),
            "response_length": len(tavily_result) if tavily_result else 0,
            "response_time": f"{tavily_time:.2f}s",
            "preview": tavily_result[:100] + "..." if tavily_result else "No response"
        }
        test_results["overall_success"] = sum(1 for result in test_results["results"].values() if result["success"]) > 0
        test_results["successful_apis"] = f"{sum(1 for result in test_results['results'].values() if result['success'])}/2"
        return test_results

if __name__ == "__main__":
    print(f"🧪 APIClient Test Suite - {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print(f"👤 User: TIRUMALA MANAV\n")
    try:
        print("🔧 Initializing API Client...")
        client = APIClient()
        print("\n📊 API Status Check:")
        for key, value in client.get_api_status().items():
            print(f"  {key}: {value}")
        print("\n🔑 API Key Validation:")
        for key, value in client.validate_api_keys().items():
            status_icon = "✅" if value else "❌"
            print(f"  {status_icon} {key}: {value}")
        print("\n🧪 Running Comprehensive API Tests...")
        test_results = client.test_all_apis()
        print(f"\n📋 Test Results Summary:")
        print(f"  Query: {test_results['test_query']}")
        print(f"  Overall Success: {'✅' if test_results['overall_success'] else '❌'}")
        print(f"  Successful APIs: {test_results['successful_apis']}")
        for api_name, result in test_results['results'].items():
            status_icon = "✅" if result['success'] else "❌"
            print(f"  {status_icon} {api_name.title()}: {result['response_time']} | {result['response_length']} chars")
        print(f"\n✅ API Client test completed successfully!")
    except Exception as e:
        print(f"❌ API Client test failed: {e}")
        import traceback
        traceback.print_exc()
