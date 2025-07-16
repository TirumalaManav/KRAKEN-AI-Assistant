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

import re
import logging
import sys
import os
from datetime import datetime, UTC
from typing import Dict, Optional, List, Any

# Add path for potential imports from other folders
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class InputHandler:
    """
    Enhanced input handler for RAG pipeline with comprehensive validation and preprocessing.
    Updated: 2025-07-15 07:38:02 UTC
    User: TIRUMALA MANAV
    """

    def __init__(self):
        """Initialize input handler with configuration settings."""
        self.current_user = "TIRUMALA MANAV"
        self.max_input_length = 2000  # Increased for coding queries
        self.min_input_length = 3
        self.initialization_time = datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC')

        # Input statistics
        self.total_inputs_processed = 0
        self.valid_inputs = 0
        self.invalid_inputs = 0

        # Coding-specific patterns
        self.coding_keywords = [
            "algorithm", "code", "python", "java", "javascript", "c++", "programming",
            "function", "class", "method", "variable", "loop", "if", "else", "return",
            "array", "list", "tree", "graph", "sort", "search", "debug", "error",
            "leetcode", "dsa", "data structure", "implement", "explain", "how to"
        ]

        logger.info(f"InputHandler initialized for user {self.current_user} at {self.initialization_time}")

    def detect_query_type(self, text: str) -> str:
        """Detect the type of coding query for better processing."""
        text_lower = text.lower()

        if any(word in text_lower for word in ["error", "debug", "fix", "bug", "issue"]):
            return "debugging"
        elif any(word in text_lower for word in ["implement", "code", "write", "create"]):
            return "implementation"
        elif any(word in text_lower for word in ["explain", "what is", "how does", "describe"]):
            return "explanation"
        elif any(word in text_lower for word in ["compare", "difference", "vs", "versus"]):
            return "comparison"
        elif any(word in text_lower for word in ["optimize", "improve", "better", "performance"]):
            return "optimization"
        elif any(word in text_lower for word in ["leetcode", "dsa", "algorithm", "complexity"]):
            return "dsa_problem"
        else:
            return "general"

    def sanitize_input(self, raw_input: str) -> str:
        """Enhanced input sanitization with coding context preservation."""
        if not raw_input or not isinstance(raw_input, str):
            return ""

        try:
            # Remove excessive whitespace but preserve code structure
            sanitized = re.sub(r'\n\s*\n\s*\n', '\n\n', raw_input)  # Max 2 consecutive newlines
            sanitized = re.sub(r'[ \t]+', ' ', sanitized)  # Normalize spaces/tabs
            sanitized = sanitized.strip()

            # Preserve common coding characters but remove potentially harmful ones
            # Keep: letters, numbers, spaces, basic punctuation, coding symbols
            sanitized = re.sub(r'[^\w\s.,!?()[\]{};:\'"`\-+=*/<>@#$%^&|\\~_]', '', sanitized)

            # Truncate if too long
            if len(sanitized) > self.max_input_length:
                sanitized = sanitized[:self.max_input_length]
                sanitized += "... [truncated]"
                logger.warning(f"Input truncated to {self.max_input_length} characters")

            return sanitized

        except Exception as e:
            logger.error(f"Error in input sanitization: {e}")
            return raw_input[:100]  # Return first 100 chars as fallback

    def validate_input(self, input_text: str) -> Dict[str, Any]:
        """Enhanced validation with detailed feedback."""
        validation_result = {
            "is_valid": True,
            "errors": [],
            "warnings": [],
            "suggestions": []
        }

        # Check for empty input
        if not input_text or len(input_text.strip()) == 0:
            validation_result["is_valid"] = False
            validation_result["errors"].append("Input cannot be empty")
            logger.warning("Empty input received")
            return validation_result

        # Check minimum length
        if len(input_text.strip()) < self.min_input_length:
            validation_result["is_valid"] = False
            validation_result["errors"].append(f"Input too short (minimum {self.min_input_length} characters)")
            logger.warning(f"Input too short: {len(input_text)} characters")
            return validation_result

        # Check maximum length
        if len(input_text) > self.max_input_length:
            validation_result["warnings"].append(f"Input will be truncated (max {self.max_input_length} characters)")
            logger.warning(f"Input exceeds maximum length: {len(input_text)} characters")

        # Check for potential code injection patterns
        suspicious_patterns = [
            r'exec\s*\(',
            r'eval\s*\(',
            r'__import__\s*\(',
            r'subprocess\.',
            r'os\.system',
            r'open\s*\('
        ]

        for pattern in suspicious_patterns:
            if re.search(pattern, input_text, re.IGNORECASE):
                validation_result["warnings"].append("Input contains potentially unsafe code patterns")
                logger.warning("Suspicious code pattern detected in input")
                break

        # Provide suggestions for better queries
        if not any(keyword in input_text.lower() for keyword in self.coding_keywords):
            validation_result["suggestions"].append("Consider adding programming-related keywords for better results")

        return validation_result

    def extract_code_blocks(self, text: str) -> List[Dict[str, str]]:
        """Extract code blocks from input for special handling."""
        code_blocks = []

        # Pattern for markdown code blocks
        code_block_pattern = r'```(\w+)?\n?(.*?)\n?```'
        matches = re.finditer(code_block_pattern, text, re.DOTALL)

        for i, match in enumerate(matches):
            language = match.group(1) if match.group(1) else "unknown"
            code = match.group(2).strip()

            code_blocks.append({
                "id": i,
                "language": language,
                "code": code,
                "start_pos": match.start(),
                "end_pos": match.end()
            })

        # Pattern for inline code
        inline_code_pattern = r'`([^`]+)`'
        inline_matches = re.finditer(inline_code_pattern, text)

        for i, match in enumerate(inline_matches):
            code_blocks.append({
                "id": f"inline_{i}",
                "language": "inline",
                "code": match.group(1),
                "start_pos": match.start(),
                "end_pos": match.end()
            })

        return code_blocks

    def enhance_query_context(self, query: str, session_id: str) -> str:
        """Enhance query with additional context for better processing."""
        query_type = self.detect_query_type(query)

        # Add context hints based on query type
        context_hints = {
            "debugging": "Focus on error analysis and solution steps.",
            "implementation": "Provide working code examples with explanations.",
            "explanation": "Give clear, educational explanations with examples.",
            "comparison": "Show differences with pros/cons and use cases.",
            "optimization": "Suggest performance improvements and best practices.",
            "dsa_problem": "Include time/space complexity analysis."
        }

        if query_type in context_hints:
            enhanced_query = f"{query}\n\n[Context: {context_hints[query_type]}]"
            return enhanced_query

        return query

    def process_input(self, raw_input: str, session_id: str = "default",
                     enhance_context: bool = True) -> Optional[Dict[str, Any]]:
        """Enhanced input processing with comprehensive analysis."""
        try:
            processing_start = datetime.now(UTC)
            self.total_inputs_processed += 1

            # Step 1: Sanitize input
            sanitized_input = self.sanitize_input(raw_input)

            # Step 2: Validate input
            validation = self.validate_input(sanitized_input)

            if not validation["is_valid"]:
                self.invalid_inputs += 1
                logger.error(f"Input validation failed: {validation['errors']}")
                return {
                    "success": False,
                    "error": "Input validation failed",
                    "validation_errors": validation["errors"],
                    "metadata": {
                        "user": self.current_user,
                        "timestamp": datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC'),
                        "session_id": session_id
                    }
                }

            # Step 3: Extract code blocks if present
            code_blocks = self.extract_code_blocks(sanitized_input)

            # Step 4: Detect query type
            query_type = self.detect_query_type(sanitized_input)

            # Step 5: Enhance with context if requested
            final_query = self.enhance_query_context(sanitized_input, session_id) if enhance_context else sanitized_input

            # Step 6: Calculate processing time
            processing_time = (datetime.now(UTC) - processing_start).total_seconds()

            self.valid_inputs += 1

            processed_input = {
                "success": True,
                "query": final_query,
                "original_query": raw_input,
                "sanitized_query": sanitized_input,
                "session_id": session_id,
                "query_type": query_type,
                "code_blocks": code_blocks,
                "validation": validation,
                "metadata": {
                    "user": self.current_user,
                    "timestamp": datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC'),
                    "input_length": len(sanitized_input),
                    "original_length": len(raw_input),
                    "processing_time": f"{processing_time:.3f}s",
                    "has_code_blocks": len(code_blocks) > 0,
                    "query_number": self.total_inputs_processed
                }
            }

            logger.info(f"Successfully processed {query_type} query: '{sanitized_input[:50]}...' for session {session_id}")
            return processed_input

        except Exception as e:
            self.invalid_inputs += 1
            logger.error(f"Error processing input: {e}")
            return {
                "success": False,
                "error": f"Input processing failed: {str(e)}",
                "metadata": {
                    "user": self.current_user,
                    "timestamp": datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC'),
                    "session_id": session_id
                }
            }

    def get_input_statistics(self) -> Dict[str, Any]:
        """Get statistics about input processing."""
        success_rate = (self.valid_inputs / max(self.total_inputs_processed, 1)) * 100

        return {
            "total_inputs_processed": self.total_inputs_processed,
            "valid_inputs": self.valid_inputs,
            "invalid_inputs": self.invalid_inputs,
            "success_rate": f"{success_rate:.1f}%",
            "current_user": self.current_user,
            "initialization_time": self.initialization_time,
            "max_input_length": self.max_input_length,
            "supported_query_types": ["debugging", "implementation", "explanation", "comparison", "optimization", "dsa_problem", "general"]
        }

    def reset_statistics(self):
        """Reset input processing statistics."""
        self.total_inputs_processed = 0
        self.valid_inputs = 0
        self.invalid_inputs = 0
        logger.info("Input processing statistics reset")

# Test function
def run_input_handler_tests():
    """Run comprehensive tests for the InputHandler."""
    print(f"🧪 InputHandler Test Suite - {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print(f"👤 User: TIRUMALA MANAV\n")

    handler = InputHandler()

    test_cases = [
        # Valid inputs
        ("Explain merge sort algorithm", "test_session_1"),
        ("Debug this Python error: IndexError", "test_session_2"),
        ("```python\ndef hello():\n    print('world')\n```", "test_session_3"),
        ("What's the difference between lists and arrays?", "test_session_4"),

        # Edge cases
        ("", "empty_test"),  # Empty input
        ("Hi", "short_test"),  # Too short
        ("A" * 2500, "long_test"),  # Too long
        ("exec('malicious code')", "suspicious_test")  # Suspicious content
    ]

    print("📝 Running test cases:")
    for i, (test_input, session_id) in enumerate(test_cases, 1):
        print(f"\n🧪 Test {i}: '{test_input[:30]}{'...' if len(test_input) > 30 else ''}'")

        result = handler.process_input(test_input, session_id)

        if result and result.get("success"):
            print(f"  ✅ Success: {result['query_type']} query")
            print(f"  📊 Length: {result['metadata']['input_length']} chars")
            print(f"  ⏱️ Processing: {result['metadata']['processing_time']}")
        else:
            print(f"  ❌ Failed: {result.get('error', 'Unknown error') if result else 'No result'}")

    # Print statistics
    print(f"\n📊 Final Statistics:")
    stats = handler.get_input_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    run_input_handler_tests()
