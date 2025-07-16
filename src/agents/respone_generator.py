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

import logging
from typing import Dict, List, Any, Optional, Tuple
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from prompt_engineering import PromptEngineer
from datetime import datetime
import re
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ResponseGenerator:
    """Enhanced response generator optimized for coding chatbot interactions."""

    def __init__(self, llm: ChatGoogleGenerativeAI):
        """Initialize response generator with LLM and coding-specific configurations."""
        self.llm = llm
        self.prompt_engineer = PromptEngineer()
        self.output_parser = StrOutputParser()

        # Coding chatbot specific settings
        self.max_response_length = 3000  # Increased for code examples
        self.include_code_formatting = True
        self.include_explanations = True
        self.include_complexity_analysis = True
        self.include_examples = True

        # Response enhancement patterns
        self.code_block_pattern = re.compile(r'```(\w+)?\n?(.*?)\n?```', re.DOTALL)
        self.function_pattern = re.compile(r'def\s+(\w+)\s*\(.*?\):', re.MULTILINE)
        self.class_pattern = re.compile(r'class\s+(\w+).*?:', re.MULTILINE)

        logger.info("ResponseGenerator initialized for coding chatbot with enhanced features")

    def generate_response(self, query: str, context: str = "", chat_history: List[BaseMessage] = None) -> Dict[str, Any]:
        """Generate a comprehensive coding response using modern LangChain patterns."""
        try:
            start_time = datetime.utcnow()

            # Analyze query for coding context
            query_analysis = self._analyze_coding_query(query)

            # Generate optimized prompt based on query type
            prompt_data = self.prompt_engineer.generate_prompt(query, context, chat_history)

            if prompt_data["confidence"] < 0.3:
                logger.warning(f"Low confidence response for query: {query[:50]}...")

            # Create the chain
            chain = prompt_data["prompt"] | self.llm | self.output_parser

            # Generate response with coding context
            enhanced_context = self._enhance_context_for_coding(context, query_analysis)
            response = chain.invoke({
                "query": query,
                "context": enhanced_context
            })

            # Post-process response for coding chatbot
            enhanced_response = self._enhance_coding_response(
                response,
                prompt_data["query_type"],
                query_analysis
            )

            # Calculate processing time
            processing_time = (datetime.utcnow() - start_time).total_seconds()

            # Create comprehensive metadata
            metadata = self._create_response_metadata(
                prompt_data,
                query_analysis,
                enhanced_response,
                processing_time
            )

            logger.info(f"Generated {prompt_data['query_type']} response in {processing_time:.2f}s with confidence {prompt_data['confidence']:.2f}")

            return {
                "response": enhanced_response,
                "metadata": metadata,
                "success": True,
                "query_analysis": query_analysis
            }

        except Exception as e:
            logger.error("Response generation failed: %s", str(e))
            return {
                "response": self._generate_error_response(str(e), query),
                "metadata": {
                    "query_type": "error",
                    "confidence": 0.0,
                    "success": False,
                    "error": str(e),
                    "timestamp": datetime.utcnow().isoformat()
                },
                "success": False
            }

    def _analyze_coding_query(self, query: str) -> Dict[str, Any]:
        """Analyze query for coding-specific patterns and requirements."""
        query_lower = query.lower()

        analysis = {
            "type": "general",
            "complexity": "basic",
            "languages": [],
            "topics": [],
            "requires_code": False,
            "requires_explanation": True,
            "requires_examples": False,
            "difficulty_level": "beginner"
        }

        # Detect programming languages
        languages = {
            "python": ["python", "py", "pandas", "numpy", "django", "flask"],
            "javascript": ["javascript", "js", "node", "react", "vue", "angular"],
            "java": ["java", "spring", "hibernate"],
            "cpp": ["c++", "cpp", "stl"],
            "csharp": ["c#", "csharp", ".net"],
            "go": ["golang", "go"],
            "rust": ["rust"],
            "kotlin": ["kotlin"]
        }

        for lang, keywords in languages.items():
            if any(keyword in query_lower for keyword in keywords):
                analysis["languages"].append(lang)

        # Detect coding topics
        topics_map = {
            "algorithms": ["algorithm", "sorting", "searching", "pathfinding"],
            "data_structures": ["array", "list", "tree", "graph", "stack", "queue", "heap", "hash"],
            "complexity": ["time complexity", "space complexity", "big o", "optimization"],
            "design_patterns": ["pattern", "singleton", "factory", "observer", "mvc"],
            "debugging": ["debug", "error", "exception", "bug", "issue"],
            "testing": ["test", "unit test", "integration", "tdd"],
            "web_development": ["api", "rest", "http", "web", "frontend", "backend"],
            "database": ["sql", "database", "query", "mongodb", "postgresql"]
        }

        for topic, keywords in topics_map.items():
            if any(keyword in query_lower for keyword in keywords):
                analysis["topics"].append(topic)

        # Determine if code is required
        code_indicators = [
            "implement", "code", "write", "function", "class", "algorithm",
            "solution", "program", "script", "example", "how to"
        ]
        analysis["requires_code"] = any(indicator in query_lower for indicator in code_indicators)

        # Determine complexity level
        if any(term in query_lower for term in ["advanced", "complex", "optimization", "performance"]):
            analysis["complexity"] = "advanced"
            analysis["difficulty_level"] = "advanced"
        elif any(term in query_lower for term in ["intermediate", "moderate"]):
            analysis["complexity"] = "intermediate"
            analysis["difficulty_level"] = "intermediate"
        elif any(term in query_lower for term in ["beginner", "basic", "simple", "learn"]):
            analysis["complexity"] = "basic"
            analysis["difficulty_level"] = "beginner"

        # Determine query type
        if any(term in query_lower for term in ["leetcode", "dsa", "algorithm", "data structure"]):
            analysis["type"] = "dsa_problem"
        elif any(term in query_lower for term in ["debug", "error", "fix", "issue"]):
            analysis["type"] = "debugging"
        elif any(term in query_lower for term in ["compare", "vs", "difference"]):
            analysis["type"] = "comparison"
        elif any(term in query_lower for term in ["review", "optimize", "improve"]):
            analysis["type"] = "code_review"
        else:
            analysis["type"] = "theory"

        return analysis

    def _enhance_context_for_coding(self, context: str, query_analysis: Dict[str, Any]) -> str:
        """Enhance context with coding-specific information."""
        enhanced_parts = []

        if context:
            enhanced_parts.append(f"**Base Context:**\n{context}")

        # Add coding-specific context
        if query_analysis["languages"]:
            enhanced_parts.append(f"**Programming Languages:** {', '.join(query_analysis['languages'])}")

        if query_analysis["topics"]:
            enhanced_parts.append(f"**Topics:** {', '.join(query_analysis['topics'])}")

        enhanced_parts.append(f"**Difficulty Level:** {query_analysis['difficulty_level']}")
        enhanced_parts.append(f"**Query Type:** {query_analysis['type']}")

        # Add current context
        enhanced_parts.append(f"**Current Time:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
        enhanced_parts.append(f"**User:** TIRUMALA MANAV")

        return "\n".join(enhanced_parts)

    def _enhance_coding_response(self, response: str, query_type: str, query_analysis: Dict[str, Any]) -> str:
        """Enhance response based on coding context and query analysis."""
        try:
            enhanced = response

            # Apply query-type specific enhancements
            if query_type == "ds_problem" or query_analysis["type"] == "dsa_problem":
                enhanced = self._enhance_dsa_response(enhanced, query_analysis)
            elif query_type == "comparison":
                enhanced = self._enhance_comparison_response(enhanced)
            elif query_type == "debugging":
                enhanced = self._enhance_debugging_response(enhanced)
            elif query_type == "code_review":
                enhanced = self._enhance_code_review_response(enhanced)

            # Apply general coding enhancements
            enhanced = self._apply_code_formatting(enhanced)
            enhanced = self._add_complexity_analysis(enhanced, query_analysis)
            enhanced = self._ensure_coding_examples(enhanced, query_analysis)
            enhanced = self._apply_length_limits(enhanced)

            return enhanced

        except Exception as e:
            logger.error(f"Response enhancement failed: {str(e)}")
            return response  # Return original if enhancement fails

    def _enhance_dsa_response(self, response: str, query_analysis: Dict[str, Any]) -> str:
        """Enhance responses for DSA problems with structured format."""
        if not any(marker in response for marker in ["Time Complexity", "Space Complexity", "Algorithm"]):
            # Add structure for DSA problems
            if "```python" in response or "def " in response:
                # Add complexity analysis section
                complexity_section = "\n\n**📊 Complexity Analysis:**\n"
                complexity_section += "- Time Complexity: O(?)\n"
                complexity_section += "- Space Complexity: O(?)\n"
                complexity_section += "- (Please analyze based on the solution above)\n"

                response += complexity_section

        # Ensure proper code formatting for algorithms
        if query_analysis.get("requires_code", False) and "```" not in response:
            response = self._wrap_code_in_blocks(response)

        return response

    def _enhance_comparison_response(self, response: str) -> str:
        """Enhance comparison responses with structured format."""
        if "vs" in response.lower() or "comparison" in response.lower():
            if not any(marker in response for marker in ["| Feature |", "**Pros:**", "**Cons:**"]):
                # Could add comparison table formatting here
                pass
        return response

    def _enhance_debugging_response(self, response: str) -> str:
        """Enhance debugging responses with structured problem-solving approach."""
        if "error" in response.lower() or "debug" in response.lower():
            if not any(marker in response for marker in ["**Problem:**", "**Solution:**", "**Prevention:**"]):
                # Add debugging structure
                debug_header = "**🐛 Debugging Analysis:**\n\n"
                response = debug_header + response
        return response

    def _enhance_code_review_response(self, response: str) -> str:
        """Enhance code review responses with structured feedback."""
        if not any(marker in response for marker in ["**Issues:**", "**Improvements:**", "**Good Practices:**"]):
            # Add code review structure
            review_header = "**📝 Code Review:**\n\n"
            response = review_header + response
        return response

    def _apply_code_formatting(self, response: str) -> str:
        """Apply proper code formatting throughout the response."""
        # Ensure code blocks have proper language specification
        response = re.sub(r'```\n(def |class |import |from )', r'```python\n\1', response)
        response = re.sub(r'```\n(function |const |let |var )', r'```javascript\n\1', response)
        response = re.sub(r'```\n(public |private |class .*{)', r'```java\n\1', response)

        # Add proper spacing around code blocks
        response = re.sub(r'```(\w+)?\n', r'\n```\1\n', response)
        response = re.sub(r'\n```\n', r'\n```\n\n', response)

        # Clean up excessive newlines
        response = re.sub(r'\n{3,}', '\n\n', response)

        return response.strip()

    def _wrap_code_in_blocks(self, response: str) -> str:
        """Wrap code snippets in proper code blocks if not already wrapped."""
        lines = response.split('\n')
        in_code_block = False
        result_lines = []

        for line in lines:
            # Check if line looks like code
            if (line.strip().startswith(('def ', 'class ', 'import ', 'from ', 'if ', 'for ', 'while ')) or
                re.match(r'^\s*\w+\s*=\s*', line) or
                line.strip().startswith(('#', '//', '/*'))):

                if not in_code_block:
                    result_lines.append('```python')
                    in_code_block = True
            elif in_code_block and line.strip() == '':
                # Empty line in code block
                pass
            elif in_code_block and not line.strip().startswith((' ', '\t')):
                # End of code block
                result_lines.append('```')
                in_code_block = False

            result_lines.append(line)

        # Close any open code block
        if in_code_block:
            result_lines.append('```')

        return '\n'.join(result_lines)

    def _add_complexity_analysis(self, response: str, query_analysis: Dict[str, Any]) -> str:
        """Add complexity analysis if appropriate."""
        if (query_analysis.get("type") == "dsa_problem" and
            "complexity" not in response.lower() and
            ("algorithm" in response.lower() or "```" in response)):

            complexity_footer = "\n\n**💡 Note:** Remember to analyze the time and space complexity of your solution!"
            response += complexity_footer

        return response

    def _ensure_coding_examples(self, response: str, query_analysis: Dict[str, Any]) -> str:
        """Ensure coding examples are included when appropriate."""
        if (query_analysis.get("requires_code", False) and
            "```" not in response and
            len(response) < 500):  # Short response without code

            example_note = "\n\n**📝 Note:** Would you like me to provide a code example for this concept?"
            response += example_note

        return response

    def _apply_length_limits(self, response: str) -> str:
        """Ensure response doesn't exceed length limits while preserving code blocks."""
        if len(response) <= self.max_response_length:
            return response

        # Try to truncate while preserving code blocks
        code_blocks = self.code_block_pattern.findall(response)

        if code_blocks:
            # Find the last complete sentence before the limit
            truncated = response[:self.max_response_length]
            last_period = truncated.rfind('.')
            last_code_end = truncated.rfind('```')

            # If we're in the middle of a code block, extend to include it
            if last_code_end != -1:
                code_start = truncated.rfind('```', 0, last_code_end)
                if code_start != -1 and truncated.count('```', code_start) % 2 == 1:
                    # We're in a code block, find the closing ```
                    code_end = response.find('```', self.max_response_length)
                    if code_end != -1:
                        truncated = response[:code_end + 3]

            elif last_period > self.max_response_length * 0.8:
                truncated = response[:last_period + 1]

            truncated += "\n\n**[Response truncated due to length limits. Ask for continuation if needed.]**"
            return truncated

        # No code blocks, simple truncation
        truncated = response[:self.max_response_length]
        last_period = truncated.rfind('.')
        if last_period > self.max_response_length * 0.8:
            response = truncated[:last_period + 1]
        else:
            response = truncated

        response += "\n\n**[Response truncated due to length limits. Ask for continuation if needed.]**"
        return response

    def _create_response_metadata(self, prompt_data: Dict, query_analysis: Dict, response: str, processing_time: float) -> Dict[str, Any]:
        """Create comprehensive metadata for the response."""
        # Analyze response content
        code_blocks = len(self.code_block_pattern.findall(response))
        functions_defined = len(self.function_pattern.findall(response))
        classes_defined = len(self.class_pattern.findall(response))

        return {
            "query_type": prompt_data["query_type"],
            "confidence": prompt_data["confidence"],
            "template_used": prompt_data["template_used"],
            "processing_time": processing_time,
            "response_length": len(response),
            "has_code": "```" in response,
            "code_blocks_count": code_blocks,
            "functions_defined": functions_defined,
            "classes_defined": classes_defined,
            "languages_detected": query_analysis.get("languages", []),
            "topics_covered": query_analysis.get("topics", []),
            "difficulty_level": query_analysis.get("difficulty_level", "unknown"),
            "requires_follow_up": len(response) >= self.max_response_length * 0.9,
            "timestamp": datetime.utcnow().isoformat(),
            "user": "TIRUMALA MANAV"
        }

    def _generate_error_response(self, error_message: str, query: str) -> str:
        """Generate a helpful error response for coding queries."""
        return f"""I apologize, but I encountered an error while processing your coding query.

**Error Details:** {error_message}

**Suggested Actions:**
1. Please try rephrasing your question
2. If asking about code, ensure it's properly formatted
3. For complex queries, try breaking them into smaller parts
4. Check if you're asking about a supported programming language

**Your Query:** {query[:100]}{'...' if len(query) > 100 else ''}

Feel free to ask your question again, and I'll do my best to help with your coding needs!
"""

    def generate_streaming_response(self, query: str, context: str = "", chat_history: List[BaseMessage] = None):
        """Generate streaming response (placeholder for future implementation)."""
        logger.info("Streaming response not implemented yet - falling back to regular response")
        return self.generate_response(query, context, chat_history)

    def set_response_preferences(self, max_length: int = 3000, include_code: bool = True,
                               include_explanations: bool = True, include_complexity: bool = True):
        """Set response generation preferences for coding chatbot."""
        self.max_response_length = max_length
        self.include_code_formatting = include_code
        self.include_explanations = include_explanations
        self.include_complexity_analysis = include_complexity

        logger.info(f"Response preferences updated: max_length={max_length}, code={include_code}, "
                   f"explanations={include_explanations}, complexity={include_complexity}")

    def get_response_statistics(self) -> Dict[str, Any]:
        """Get statistics about response generation capabilities."""
        return {
            "max_response_length": self.max_response_length,
            "include_code_formatting": self.include_code_formatting,
            "include_explanations": self.include_explanations,
            "include_complexity_analysis": self.include_complexity_analysis,
            "supported_languages": ["python", "javascript", "java", "c++", "c#", "go", "rust", "kotlin"],
            "available_templates": self.prompt_engineer.list_available_templates(),
            "current_user": "TIRUMALA MANAV",
            "timestamp": datetime.utcnow().isoformat()
        }

    def test_response_generation(self, test_query: str = "Explain binary search algorithm") -> Dict[str, Any]:
        """Test response generation with a sample coding query."""
        try:
            result = self.generate_response(test_query)
            return {
                "test_successful": True,
                "test_query": test_query,
                "response_length": len(result["response"]),
                "metadata": result["metadata"],
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {
                "test_successful": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }

# Test function
if __name__ == "__main__":
    # This would require a real LLM instance to test
    print("ResponseGenerator module loaded successfully!")
    print("To test, initialize with a ChatGoogleGenerativeAI instance.")
