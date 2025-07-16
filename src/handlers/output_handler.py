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

# import logging
# import json
# import re
# import sys
# import os
# from datetime import datetime, UTC
# from typing import Dict, Optional, List, Any

# # Add path for potential imports from other folders
# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# # Configure logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

# class OutputHandler:
#     """
#     Enhanced output handler for RAG pipeline with comprehensive formatting and error handling.
#     Updated: 2025-07-15 07:38:02 UTC
#     User: TIRUMALA MANAV
#     """

#     def __init__(self):
#         """Initialize output handler with configuration settings."""
#         self.current_user = "TIRUMALA MANAV"
#         self.initialization_time = datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC')

#         # Output statistics
#         self.total_outputs_processed = 0
#         self.successful_outputs = 0
#         self.failed_outputs = 0

#         # Formatting preferences
#         self.max_response_display_length = 2000
#         self.include_metadata = True
#         self.use_emoji_indicators = True
#         self.format_code_blocks = True

#         logger.info(f"OutputHandler initialized for user {self.current_user} at {self.initialization_time}")

#     def format_code_blocks(self, text: str) -> str:
#         """Enhance code block formatting for better readability."""
#         if not self.format_code_blocks:
#             return text

#         try:
#             # Add syntax highlighting indicators for common languages
#             language_emojis = {
#                 'python': '🐍',
#                 'javascript': '💛',
#                 'java': '☕',
#                 'cpp': '⚙️',
#                 'c++': '⚙️',
#                 'html': '🌐',
#                 'css': '🎨',
#                 'sql': '🗃️'
#             }

#             # Pattern to find code blocks
#             code_block_pattern = r'```(\w+)?\n?(.*?)\n?```'

#             def replace_code_block(match):
#                 language = match.group(1) if match.group(1) else 'code'
#                 code = match.group(2)
#                 emoji = language_emojis.get(language.lower(), '💻')

#                 return f"\n{emoji} **{language.title()} Code:**\n```{language}\n{code}\n```\n"

#             formatted_text = re.sub(code_block_pattern, replace_code_block, text, flags=re.DOTALL)
#             return formatted_text

#         except Exception as e:
#             logger.warning(f"Code block formatting failed: {e}")
#             return text

#     def format_response_by_type(self, response_text: str, query_type: str = "general") -> str:
#         """Format response based on the type of query."""
#         try:
#             if query_type == "debugging":
#                 return self._format_debugging_response(response_text)
#             elif query_type == "implementation":
#                 return self._format_implementation_response(response_text)
#             elif query_type == "explanation":
#                 return self._format_explanation_response(response_text)
#             elif query_type == "comparison":
#                 return self._format_comparison_response(response_text)
#             elif query_type == "dsa_problem":
#                 return self._format_dsa_response(response_text)
#             else:
#                 return self._format_general_response(response_text)
#         except Exception as e:
#             logger.warning(f"Type-specific formatting failed: {e}")
#             return response_text

#     def _format_debugging_response(self, text: str) -> str:
#         """Format debugging responses with problem/solution structure."""
#         if "**Problem:**" not in text and "**Solution:**" not in text:
#             # Add debugging structure if not present
#             text = f"🐛 **Debug Analysis:**\n\n{text}"
#         return text

#     def _format_implementation_response(self, text: str) -> str:
#         """Format implementation responses to highlight code sections."""
#         # Already handled by format_code_blocks
#         return text

#     def _format_explanation_response(self, text: str) -> str:
#         """Format explanation responses for better readability."""
#         if not text.startswith("📚"):
#             text = f"📚 **Explanation:**\n\n{text}"
#         return text

#     def _format_comparison_response(self, text: str) -> str:
#         """Format comparison responses with clear distinctions."""
#         if "vs" in text.lower() or "difference" in text.lower():
#             if not text.startswith("⚖️"):
#                 text = f"⚖️ **Comparison:**\n\n{text}"
#         return text

#     def _format_dsa_response(self, text: str) -> str:
#         """Format DSA responses with algorithm focus."""
#         if not text.startswith("🔬"):
#             text = f"🔬 **Algorithm Analysis:**\n\n{text}"
#         return text

#     def _format_general_response(self, text: str) -> str:
#         """Format general responses."""
#         return text

#     def extract_metadata_summary(self, metadata: Dict) -> str:
#         """Extract and format key metadata information."""
#         if not metadata:
#             return ""

#         summary_parts = []

#         # Processing time
#         if 'processing_time' in metadata:
#             summary_parts.append(f"⏱️ **Processing Time:** {metadata['processing_time']}")

#         # Context sources
#         if 'context_sources' in metadata and metadata['context_sources']:
#             sources = ', '.join(metadata['context_sources'])
#             summary_parts.append(f"📚 **Sources:** {sources}")

#         # Query type
#         if 'query_type' in metadata:
#             summary_parts.append(f"🏷️ **Query Type:** {metadata['query_type']}")

#         # Session info
#         if 'session_id' in metadata:
#             summary_parts.append(f"💬 **Session:** {metadata['session_id']}")

#         # Timestamp
#         if 'timestamp' in metadata:
#             summary_parts.append(f"📅 **Time:** {metadata['timestamp']}")

#         return "\n".join(summary_parts) if summary_parts else ""

#     def format_error_response(self, response_data: Dict) -> str:
#         """Format error responses with helpful information."""
#         error_message = response_data.get("response", "An unknown error occurred.")
#         error_details = response_data.get("error", "No additional error details available.")
#         metadata = response_data.get("metadata", {})

#         formatted_error = f"❌ **Error Response for {self.current_user}**\n\n"
#         formatted_error += f"**Issue:** {error_message}\n\n"

#         if error_details != error_message:
#             formatted_error += f"**Details:** {error_details}\n\n"

#         # Add troubleshooting suggestions
#         formatted_error += "**💡 Troubleshooting Suggestions:**\n"
#         formatted_error += "- Try rephrasing your question\n"
#         formatted_error += "- Ensure your query is clear and specific\n"
#         formatted_error += "- Check for any special characters that might cause issues\n"
#         formatted_error += "- If the problem persists, try a simpler version of your question\n\n"

#         # Add metadata if available
#         metadata_summary = self.extract_metadata_summary(metadata)
#         if metadata_summary:
#             formatted_error += "**📊 Technical Details:**\n" + metadata_summary

#         return formatted_error

#     def format_success_response(self, response_data: Dict) -> str:
#         """Format successful responses with enhanced presentation."""
#         response_text = response_data.get("response", "Response generated successfully.")
#         metadata = response_data.get("metadata", {})

#         # Get query type for specialized formatting
#         query_type = metadata.get("query_type", "general")

#         # Apply type-specific formatting
#         formatted_response = self.format_response_by_type(response_text, query_type)

#         # Apply code block formatting
#         formatted_response = self.format_code_blocks(formatted_response)

#         # Truncate if too long
#         if len(formatted_response) > self.max_response_display_length:
#             formatted_response = formatted_response[:self.max_response_display_length]
#             formatted_response += "\n\n**[Response truncated - ask for continuation if needed]**"

#         # Add header
#         final_response = f"✅ **Response for {self.current_user}**\n\n{formatted_response}\n\n"

#         # Add metadata summary if enabled
#         if self.include_metadata:
#             metadata_summary = self.extract_metadata_summary(metadata)
#             if metadata_summary:
#                 final_response += "---\n**📊 Response Details:**\n" + metadata_summary

#         return final_response

#     def format_response(self, response_data: Dict) -> str:
#         """Main response formatting method with comprehensive error handling."""
#         try:
#             if not response_data or not isinstance(response_data, dict):
#                 return "❌ **Error:** No response data available or invalid format."

#             success = response_data.get("success", False)

#             if success:
#                 return self.format_success_response(response_data)
#             else:
#                 return self.format_error_response(response_data)

#         except Exception as e:
#             logger.error(f"Error in response formatting: {e}")
#             return f"❌ **Formatting Error:** Failed to format response - {str(e)}"

#     def handle_output(self, response_data: Dict, output_method: str = "console") -> Dict[str, Any]:
#         """Enhanced output handling with multiple output methods and statistics."""
#         handling_start = datetime.now(UTC)
#         self.total_outputs_processed += 1

#         try:
#             if not response_data:
#                 logger.error("Empty response data received")
#                 self.failed_outputs += 1
#                 error_output = "❌ **Error:** No response data to handle."

#                 if output_method == "console":
#                     print(error_output)

#                 return {
#                     "success": False,
#                     "formatted_output": error_output,
#                     "error": "Empty response data"
#                 }

#             # Format the response
#             formatted_output = self.format_response(response_data)

#             # Handle output based on method
#             if output_method == "console":
#                 print(formatted_output)
#             elif output_method == "file":
#                 self._save_to_file(formatted_output, response_data)
#             elif output_method == "json":
#                 self._output_as_json(response_data, formatted_output)

#             # Calculate processing time
#             processing_time = (datetime.now(UTC) - handling_start).total_seconds()

#             self.successful_outputs += 1
#             logger.info(f"Successfully handled output in {processing_time:.3f}s via {output_method}")

#             return {
#                 "success": True,
#                 "formatted_output": formatted_output,
#                 "processing_time": f"{processing_time:.3f}s",
#                 "output_method": output_method,
#                 "metadata": {
#                     "output_length": len(formatted_output),
#                     "timestamp": datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC'),
#                     "user": self.current_user
#                 }
#             }

#         except Exception as e:
#             self.failed_outputs += 1
#             logger.error(f"Error handling output: {e}")
#             error_message = f"❌ **Output Handling Error:** Failed to handle output - {str(e)}"

#             if output_method == "console":
#                 print(error_message)

#             return {
#                 "success": False,
#                 "formatted_output": error_message,
#                 "error": str(e)
#             }

#     def _save_to_file(self, formatted_output: str, response_data: Dict):
#         """Save output to file with timestamp."""
#         try:
#             timestamp = datetime.now(UTC).strftime('%Y%m%d_%H%M%S')
#             filename = f"output_{self.current_user}_{timestamp}.txt"

#             with open(filename, 'w', encoding='utf-8') as f:
#                 f.write(formatted_output)
#                 f.write("\n\n" + "="*50 + "\n")
#                 f.write(f"Raw Response Data:\n{json.dumps(response_data, indent=2)}")

#             logger.info(f"Output saved to file: {filename}")
#         except Exception as e:
#             logger.error(f"Failed to save output to file: {e}")

#     def _output_as_json(self, response_data: Dict, formatted_output: str):
#         """Output as JSON format."""
#         try:
#             json_output = {
#                 "formatted_response": formatted_output,
#                 "raw_data": response_data,
#                 "handler_metadata": {
#                     "user": self.current_user,
#                     "timestamp": datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC'),
#                     "output_handler_version": "enhanced_v1.0"
#                 }
#             }
#             print(json.dumps(json_output, indent=2))
#         except Exception as e:
#             logger.error(f"Failed to output as JSON: {e}")

#     def get_output_statistics(self) -> Dict[str, Any]:
#         """Get statistics about output processing."""
#         success_rate = (self.successful_outputs / max(self.total_outputs_processed, 1)) * 100

#         return {
#             "total_outputs_processed": self.total_outputs_processed,
#             "successful_outputs": self.successful_outputs,
#             "failed_outputs": self.failed_outputs,
#             "success_rate": f"{success_rate:.1f}%",
#             "current_user": self.current_user,
#             "initialization_time": self.initialization_time,
#             "formatting_preferences": {
#                 "max_display_length": self.max_response_display_length,
#                 "include_metadata": self.include_metadata,
#                 "use_emojis": self.use_emoji_indicators,
#                 "format_code_blocks": self.format_code_blocks
#             }
#         }

#     def update_preferences(self, **kwargs):
#         """Update output formatting preferences."""
#         valid_preferences = {
#             "max_response_display_length", "include_metadata",
#             "use_emoji_indicators", "format_code_blocks"
#         }

#         updated = []
#         for key, value in kwargs.items():
#             if key in valid_preferences and hasattr(self, key):
#                 setattr(self, key, value)
#                 updated.append(f"{key}={value}")

#         if updated:
#             logger.info(f"Updated output preferences: {', '.join(updated)}")
#         else:
#             logger.warning("No valid preferences provided for update")

#     def reset_statistics(self):
#         """Reset output processing statistics."""
#         self.total_outputs_processed = 0
#         self.successful_outputs = 0
#         self.failed_outputs = 0
#         logger.info("Output processing statistics reset")

# # Test function
# def run_output_handler_tests():
#     """Run comprehensive tests for the OutputHandler."""
#     print(f"🧪 OutputHandler Test Suite - {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S')} UTC")
#     print(f"👤 User: TIRUMALA MANAV\n")

#     handler = OutputHandler()

#     # Test cases
#     test_cases = [
#         # Successful response
#         {
#             "success": True,
#             "response": "Merge sort is a divide-and-conquer algorithm.\n\n```python\ndef merge_sort(arr):\n    if len(arr) > 1:\n        mid = len(arr) // 2\n        return merge(merge_sort(arr[:mid]), merge_sort(arr[mid:]))\n```",
#             "metadata": {
#                 "timestamp": "2025-07-15 07:38:02 UTC",
#                 "processing_time": "2.34s",
#                 "context_sources": ["web"],
#                 "query_type": "implementation"
#             }
#         },

#         # Error response
#         {
#             "success": False,
#             "response": "Failed to process query.",
#             "error": "Agent timeout occurred",
#             "metadata": {"timestamp": "2025-07-15 07:38:05 UTC"}
#         },

#         # Debug response
#         {
#             "success": True,
#             "response": "The IndexError occurs when accessing array index out of bounds.",
#             "metadata": {
#                 "query_type": "debugging",
#                 "processing_time": "1.23s"
#             }
#         }
#     ]

#     print("📝 Running test cases:")
#     for i, test_case in enumerate(test_cases, 1):
#         print(f"\n🧪 Test {i}: {'Success' if test_case.get('success') else 'Error'} response")

#         result = handler.handle_output(test_case, output_method="console")

#         if result["success"]:
#             print(f"  ✅ Formatting successful")
#             print(f"  📊 Output length: {result['metadata']['output_length']} chars")
#             print(f"  ⏱️ Processing: {result['processing_time']}")
#         else:
#             print(f"  ❌ Formatting failed: {result.get('error', 'Unknown error')}")

#     # Print statistics
#     print(f"\n📊 Final Statistics:")
#     stats = handler.get_output_statistics()
#     for key, value in stats.items():
#         if isinstance(value, dict):
#             print(f"  {key}:")
#             for sub_key, sub_value in value.items():
#                 print(f"    {sub_key}: {sub_value}")
#         else:
#             print(f"  {key}: {value}")

# if __name__ == "__main__":
#     run_output_handler_tests()


import logging
import json
import re
import sys
import os
from datetime import datetime, UTC
from typing import Dict, Optional, List, Any

# Add path for potential imports from other folders
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OutputHandler:
    """
    Enhanced output handler for RAG pipeline with comprehensive formatting and error handling.
    Updated: 2025-07-15 07:42:08 UTC
    User: TIRUMALA MANAV
    """

    def __init__(self):
        """Initialize output handler with configuration settings."""
        self.current_user = "TIRUMALA MANAV"
        self.initialization_time = datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC')

        # Output statistics
        self.total_outputs_processed = 0
        self.successful_outputs = 0
        self.failed_outputs = 0

        # Formatting preferences
        self.max_response_display_length = 2000
        self.include_metadata = True
        self.use_emoji_indicators = True
        self.enable_code_formatting = True  # ✅ Fixed: renamed from format_code_blocks

        logger.info(f"OutputHandler initialized for user {self.current_user} at {self.initialization_time}")

    def format_code_blocks(self, text: str) -> str:  # ✅ Method name stays the same
        """Enhance code block formatting for better readability."""
        if not self.enable_code_formatting:  # ✅ Fixed: use renamed variable
            return text

        try:
            # Add syntax highlighting indicators for common languages
            language_emojis = {
                'python': '🐍',
                'javascript': '💛',
                'java': '☕',
                'cpp': '⚙️',
                'c++': '⚙️',
                'html': '🌐',
                'css': '🎨',
                'sql': '🗃️'
            }

            # Pattern to find code blocks
            code_block_pattern = r'```(\w+)?\n?(.*?)\n?```'

            def replace_code_block(match):
                language = match.group(1) if match.group(1) else 'code'
                code = match.group(2)
                emoji = language_emojis.get(language.lower(), '💻')

                return f"\n{emoji} **{language.title()} Code:**\n```{language}\n{code}\n```\n"

            formatted_text = re.sub(code_block_pattern, replace_code_block, text, flags=re.DOTALL)
            return formatted_text

        except Exception as e:
            logger.warning(f"Code block formatting failed: {e}")
            return text

    def format_response_by_type(self, response_text: str, query_type: str = "general") -> str:
        """Format response based on the type of query."""
        try:
            if query_type == "debugging":
                return self._format_debugging_response(response_text)
            elif query_type == "implementation":
                return self._format_implementation_response(response_text)
            elif query_type == "explanation":
                return self._format_explanation_response(response_text)
            elif query_type == "comparison":
                return self._format_comparison_response(response_text)
            elif query_type == "dsa_problem":
                return self._format_dsa_response(response_text)
            else:
                return self._format_general_response(response_text)
        except Exception as e:
            logger.warning(f"Type-specific formatting failed: {e}")
            return response_text

    def _format_debugging_response(self, text: str) -> str:
        """Format debugging responses with problem/solution structure."""
        if "**Problem:**" not in text and "**Solution:**" not in text:
            # Add debugging structure if not present
            text = f"🐛 **Debug Analysis:**\n\n{text}"
        return text

    def _format_implementation_response(self, text: str) -> str:
        """Format implementation responses to highlight code sections."""
        # Already handled by format_code_blocks
        return text

    def _format_explanation_response(self, text: str) -> str:
        """Format explanation responses for better readability."""
        if not text.startswith("📚"):
            text = f"📚 **Explanation:**\n\n{text}"
        return text

    def _format_comparison_response(self, text: str) -> str:
        """Format comparison responses with clear distinctions."""
        if "vs" in text.lower() or "difference" in text.lower():
            if not text.startswith("⚖️"):
                text = f"⚖️ **Comparison:**\n\n{text}"
        return text

    def _format_dsa_response(self, text: str) -> str:
        """Format DSA responses with algorithm focus."""
        if not text.startswith("🔬"):
            text = f"🔬 **Algorithm Analysis:**\n\n{text}"
        return text

    def _format_general_response(self, text: str) -> str:
        """Format general responses."""
        return text

    def extract_metadata_summary(self, metadata: Dict) -> str:
        """Extract and format key metadata information."""
        if not metadata:
            return ""

        summary_parts = []

        # Processing time
        if 'processing_time' in metadata:
            summary_parts.append(f"⏱️ **Processing Time:** {metadata['processing_time']}")

        # Context sources
        if 'context_sources' in metadata and metadata['context_sources']:
            sources = ', '.join(metadata['context_sources'])
            summary_parts.append(f"📚 **Sources:** {sources}")

        # Query type
        if 'query_type' in metadata:
            summary_parts.append(f"🏷️ **Query Type:** {metadata['query_type']}")

        # Session info
        if 'session_id' in metadata:
            summary_parts.append(f"💬 **Session:** {metadata['session_id']}")

        # Timestamp
        if 'timestamp' in metadata:
            summary_parts.append(f"📅 **Time:** {metadata['timestamp']}")

        return "\n".join(summary_parts) if summary_parts else ""

    def format_error_response(self, response_data: Dict) -> str:
        """Format error responses with helpful information."""
        error_message = response_data.get("response", "An unknown error occurred.")
        error_details = response_data.get("error", "No additional error details available.")
        metadata = response_data.get("metadata", {})

        formatted_error = f"❌ **Error Response for {self.current_user}**\n\n"
        formatted_error += f"**Issue:** {error_message}\n\n"

        if error_details != error_message:
            formatted_error += f"**Details:** {error_details}\n\n"

        # Add troubleshooting suggestions
        formatted_error += "**💡 Troubleshooting Suggestions:**\n"
        formatted_error += "- Try rephrasing your question\n"
        formatted_error += "- Ensure your query is clear and specific\n"
        formatted_error += "- Check for any special characters that might cause issues\n"
        formatted_error += "- If the problem persists, try a simpler version of your question\n\n"

        # Add metadata if available
        metadata_summary = self.extract_metadata_summary(metadata)
        if metadata_summary:
            formatted_error += "**📊 Technical Details:**\n" + metadata_summary

        return formatted_error

    def format_success_response(self, response_data: Dict) -> str:
        """Format successful responses with enhanced presentation."""
        response_text = response_data.get("response", "Response generated successfully.")
        metadata = response_data.get("metadata", {})

        # Get query type for specialized formatting
        query_type = metadata.get("query_type", "general")

        # Apply type-specific formatting
        formatted_response = self.format_response_by_type(response_text, query_type)

        # Apply code block formatting
        formatted_response = self.format_code_blocks(formatted_response)

        # Truncate if too long
        if len(formatted_response) > self.max_response_display_length:
            formatted_response = formatted_response[:self.max_response_display_length]
            formatted_response += "\n\n**[Response truncated - ask for continuation if needed]**"

        # Add header
        final_response = f"✅ **Response for {self.current_user}**\n\n{formatted_response}\n\n"

        # Add metadata summary if enabled
        if self.include_metadata:
            metadata_summary = self.extract_metadata_summary(metadata)
            if metadata_summary:
                final_response += "---\n**📊 Response Details:**\n" + metadata_summary

        return final_response

    def format_response(self, response_data: Dict) -> str:
        """Main response formatting method with comprehensive error handling."""
        try:
            if not response_data or not isinstance(response_data, dict):
                return "❌ **Error:** No response data available or invalid format."

            success = response_data.get("success", False)

            if success:
                return self.format_success_response(response_data)
            else:
                return self.format_error_response(response_data)

        except Exception as e:
            logger.error(f"Error in response formatting: {e}")
            return f"❌ **Formatting Error:** Failed to format response - {str(e)}"

    def handle_output(self, response_data: Dict, output_method: str = "console") -> Dict[str, Any]:
        """Enhanced output handling with multiple output methods and statistics."""
        handling_start = datetime.now(UTC)
        self.total_outputs_processed += 1

        try:
            if not response_data:
                logger.error("Empty response data received")
                self.failed_outputs += 1
                error_output = "❌ **Error:** No response data to handle."

                if output_method == "console":
                    print(error_output)

                return {
                    "success": False,
                    "formatted_output": error_output,
                    "error": "Empty response data"
                }

            # Format the response
            formatted_output = self.format_response(response_data)

            # Handle output based on method
            if output_method == "console":
                print(formatted_output)
            elif output_method == "file":
                self._save_to_file(formatted_output, response_data)
            elif output_method == "json":
                self._output_as_json(response_data, formatted_output)

            # Calculate processing time
            processing_time = (datetime.now(UTC) - handling_start).total_seconds()

            self.successful_outputs += 1
            logger.info(f"Successfully handled output in {processing_time:.3f}s via {output_method}")

            return {
                "success": True,
                "formatted_output": formatted_output,
                "processing_time": f"{processing_time:.3f}s",
                "output_method": output_method,
                "metadata": {
                    "output_length": len(formatted_output),
                    "timestamp": datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC'),
                    "user": self.current_user
                }
            }

        except Exception as e:
            self.failed_outputs += 1
            logger.error(f"Error handling output: {e}")
            error_message = f"❌ **Output Handling Error:** Failed to handle output - {str(e)}"

            if output_method == "console":
                print(error_message)

            return {
                "success": False,
                "formatted_output": error_message,
                "error": str(e)
            }

    def get_output_statistics(self) -> Dict[str, Any]:
        """Get statistics about output processing."""
        success_rate = (self.successful_outputs / max(self.total_outputs_processed, 1)) * 100

        return {
            "total_outputs_processed": self.total_outputs_processed,
            "successful_outputs": self.successful_outputs,
            "failed_outputs": self.failed_outputs,
            "success_rate": f"{success_rate:.1f}%",
            "current_user": self.current_user,
            "initialization_time": self.initialization_time,
            "formatting_preferences": {
                "max_display_length": self.max_response_display_length,
                "include_metadata": self.include_metadata,
                "use_emojis": self.use_emoji_indicators,
                "enable_code_formatting": self.enable_code_formatting  # ✅ Fixed
            }
        }

    def _save_to_file(self, formatted_output: str, response_data: Dict):
        """Save output to file with timestamp."""
        try:
            timestamp = datetime.now(UTC).strftime('%Y%m%d_%H%M%S')
            filename = f"output_{self.current_user}_{timestamp}.txt"

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(formatted_output)
                f.write("\n\n" + "="*50 + "\n")
                f.write(f"Raw Response Data:\n{json.dumps(response_data, indent=2)}")

            logger.info(f"Output saved to file: {filename}")
        except Exception as e:
            logger.error(f"Failed to save output to file: {e}")

    def _output_as_json(self, response_data: Dict, formatted_output: str):
        """Output as JSON format."""
        try:
            json_output = {
                "formatted_response": formatted_output,
                "raw_data": response_data,
                "handler_metadata": {
                    "user": self.current_user,
                    "timestamp": datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC'),
                    "output_handler_version": "enhanced_v1.0"
                }
            }
            print(json.dumps(json_output, indent=2))
        except Exception as e:
            logger.error(f"Failed to output as JSON: {e}")

# Test function
def run_output_handler_tests():
    """Run comprehensive tests for the OutputHandler."""
    print(f"🧪 OutputHandler Test Suite - {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print(f"👤 User: TIRUMALA MANAV\n")

    handler = OutputHandler()

    # Test cases
    test_cases = [
        # Successful response
        {
            "success": True,
            "response": "Merge sort is a divide-and-conquer algorithm.\n\n```python\ndef merge_sort(arr):\n    if len(arr) > 1:\n        mid = len(arr) // 2\n        return merge(merge_sort(arr[:mid]), merge_sort(arr[mid:]))\n```",
            "metadata": {
                "timestamp": "2025-07-15 07:42:08 UTC",
                "processing_time": "2.34s",
                "context_sources": ["web"],
                "query_type": "implementation"
            }
        },

        # Error response
        {
            "success": False,
            "response": "Failed to process query.",
            "error": "Agent timeout occurred",
            "metadata": {"timestamp": "2025-07-15 07:42:08 UTC"}
        }
    ]

    print("📝 Running test cases:")
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Test {i}: {'Success' if test_case.get('success') else 'Error'} response")

        result = handler.handle_output(test_case, output_method="console")

        if result["success"]:
            print(f"  ✅ Formatting successful")
        else:
            print(f"  ❌ Formatting failed: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    run_output_handler_tests()
