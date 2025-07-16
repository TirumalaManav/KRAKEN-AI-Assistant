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

# import streamlit as st
# import sys
# import os
# import time
# from datetime import datetime

# # Silent setup
# current_dir = os.path.dirname(os.path.abspath(__file__))
# src_path = os.path.join(current_dir, 'src')
# sys.path.insert(0, src_path)

# for module_dir in ['agents', 'pipeline', 'handlers', 'monitoring', 'embeddings', 'data_processing']:
#     sys.path.insert(0, os.path.join(src_path, module_dir))

# # Page config - ChatGPT style
# st.set_page_config(
#     page_title="KRAKEN",
#     page_icon="🐙",
#     layout="centered",
#     initial_sidebar_state="collapsed"
# )

# # Silent imports
# try:
#     from rag_pipeline import RAGPipeline
#     pipeline_ready = True
# except:
#     pipeline_ready = False

# try:
#     from input_handler import InputHandler
#     from output_handler import OutputHandler
#     handlers_ready = True
# except:
#     handlers_ready = False

# # Session state
# if 'messages' not in st.session_state:
#     st.session_state.messages = []

# if 'pipeline' not in st.session_state and pipeline_ready:
#     try:
#         st.session_state.pipeline = RAGPipeline(enable_monitoring=True)
#         system_ready = True
#     except:
#         system_ready = False
# else:
#     system_ready = pipeline_ready

# # Function to clear chat
# def clear_chat():
#     st.session_state.messages = []
#     st.rerun()

# # Custom CSS for ChatGPT-like aesthetics
# st.markdown("""
# <style>
# /* Hide Streamlit branding */
# #MainMenu {visibility: hidden;}
# footer {visibility: hidden;}
# header {visibility: hidden;}

# /* ChatGPT-like styling */
# .main {
#     padding-top: 2rem;
# }

# /* Animated gradient background for header */
# @keyframes glow {
#     0% { text-shadow: 0 0 20px #00d4aa; }
#     50% { text-shadow: 0 0 30px #00d4aa, 0 0 40px #00d4aa; }
#     100% { text-shadow: 0 0 20px #00d4aa; }
# }

# .kraken-title {
#     animation: glow 2s ease-in-out infinite alternate;
# }

# /* Welcome box styling */
# .welcome-box {
#     background: linear-gradient(135deg, #1e1e1e 0%, #2d2d2d 100%);
#     border: 1px solid rgba(0, 212, 170, 0.3);
#     border-radius: 12px;
#     padding: 1.5rem;
#     margin: 2rem auto;
#     max-width: 600px;
#     box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
#     position: relative;
#     overflow: hidden;
# }

# .welcome-box::before {
#     content: '';
#     position: absolute;
#     top: 0;
#     left: -100%;
#     width: 100%;
#     height: 100%;
#     background: linear-gradient(90deg, transparent, rgba(0, 212, 170, 0.1), transparent);
#     animation: shine 3s infinite;
# }

# @keyframes shine {
#     0% { left: -100%; }
#     100% { left: 100%; }
# }

# /* Chat container */
# .chat-container {
#     max-width: 700px;
#     margin: 0 auto;
# }

# /* Typing animation */
# @keyframes typing {
#     0% { opacity: 0.3; }
#     50% { opacity: 1; }
#     100% { opacity: 0.3; }
# }

# .typing-indicator {
#     animation: typing 1.5s ease-in-out infinite;
# }

# /* File upload button styling */
# .upload-btn {
#     background: rgba(0, 212, 170, 0.1);
#     border: 1px solid rgba(0, 212, 170, 0.3);
#     border-radius: 8px;
#     padding: 8px 12px;
#     color: #00d4aa;
#     cursor: pointer;
#     font-size: 14px;
#     transition: all 0.3s ease;
#     display: inline-flex;
#     align-items: center;
#     gap: 8px;
#     margin-right: 10px;
# }

# .upload-btn:hover {
#     background: rgba(0, 212, 170, 0.2);
#     border-color: rgba(0, 212, 170, 0.5);
# }

# /* Chat input container styling */
# .chat-input-container {
#     position: relative;
# }

# /* New chat button that actually works */
# .working-new-chat-btn {
#     position: fixed;
#     bottom: 100px;
#     right: 30px;
#     z-index: 999;
#     background: #00d4aa;
#     width: 50px;
#     height: 50px;
#     border-radius: 50%;
#     display: flex;
#     align-items: center;
#     justify-content: center;
#     box-shadow: 0 4px 12px rgba(0, 212, 170, 0.4);
#     cursor: pointer;
#     transition: all 0.3s ease;
#     border: none;
#     outline: none;
# }

# .working-new-chat-btn:hover {
#     transform: scale(1.1);
#     box-shadow: 0 6px 20px rgba(0, 212, 170, 0.6);
# }

# /* Light effect for developer name */
# @keyframes light-glow {
#     0% { text-shadow: 0 0 10px rgba(0, 212, 170, 0.5); }
#     50% { text-shadow: 0 0 20px rgba(0, 212, 170, 0.8), 0 0 30px rgba(0, 212, 170, 0.6); }
#     100% { text-shadow: 0 0 10px rgba(0, 212, 170, 0.5); }
# }

# .developer-name {
#     animation: light-glow 3s ease-in-out infinite;
# }
# </style>
# """, unsafe_allow_html=True)

# # KRAKEN Header - Clean & Animated with Updated Developer Info
# st.markdown("""
# <div style='text-align: center; margin-bottom: 3rem;'>
#     <h1 class='kraken-title' style='font-size: 3.5rem; margin: 0; color: #00d4aa; font-weight: 700;'>
#         🐙 KRAKEN
#     </h1>
#     <p style='font-size: 1.1rem; color: #888; margin: 0.5rem 0; font-weight: 300;'>
#         AI Assistant Coding Chat Bot
#     </p>
#     <p class='developer-name' style='font-size: 0.9rem; color: #00d4aa; margin: 0; font-weight: 500;'>
#         <strong>Tirumala Manav</strong> - Machine Learning Engineer, Computer Science Graduate
#     </p>
# </div>
# """, unsafe_allow_html=True)

# # Welcome Message - Exactly like NOVA but prettier
# if not st.session_state.messages:
#     st.markdown("""
#     <div class='welcome-box'>
#         <div style='display: flex; align-items: center; margin-bottom: 1rem;'>
#             <div style='background: #00d4aa; width: 32px; height: 32px; border-radius: 50%;
#                         display: flex; align-items: center; justify-content: center; margin-right: 12px;'>
#                 🐙
#             </div>
#             <strong style='color: #fff; font-size: 1.1rem;'>Hi! I'm KRAKEN, your AI coding assistant.</strong>
#         </div>
#         <p style='margin: 0; color: #ccc; line-height: 1.5;'>
#             I can help you with programming questions, debugging, code explanation, and implementation guidance.
#             You can also upload documents (PDF, DOCX, TXT, and more) for analysis.
#         </p>
#         <p style='margin: 1rem 0 0 0; color: #00d4aa; font-weight: 500;'>
#             What can I help you with today?
#         </p>
#     </div>
#     """, unsafe_allow_html=True)

# # Chat Messages Container
# st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# # Display messages
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# st.markdown('</div>', unsafe_allow_html=True)

# # File upload in chat input area (like Claude/ChatGPT)
# if st.session_state.messages:
#     # File upload expander
#     with st.expander("📎 Upload Files"):
#         uploaded_files = st.file_uploader(
#             "Choose files to upload",
#             accept_multiple_files=True,
#             type=['py', 'js', 'java', 'cpp', 'c', 'txt', 'md', 'json', 'html', 'css', 'sql', 'r', 'php', 'go', 'rs', 'kt', 'swift', 'pdf', 'docx'],
#             help="Upload code files or documents for KRAKEN to analyze"
#         )

#         if uploaded_files:
#             st.success(f"✅ {len(uploaded_files)} file(s) uploaded!")
#             for file in uploaded_files:
#                 file_size = f"{file.size / 1024:.1f} KB" if file.size < 1024*1024 else f"{file.size / (1024*1024):.1f} MB"
#                 st.markdown(f"📄 **{file.name}** ({file_size})")

# # Chat Input - Full width like ChatGPT
# if prompt := st.chat_input("Message KRAKEN..."):
#     # Add user message
#     st.session_state.messages.append({"role": "user", "content": prompt})

#     with st.chat_message("user"):
#         st.markdown(prompt)

#     # Generate response with typing animation
#     with st.chat_message("assistant"):
#         if system_ready and st.session_state.pipeline:
#             # Full system response
#             try:
#                 # Show typing indicator
#                 typing_placeholder = st.empty()
#                 typing_placeholder.markdown('<p class="typing-indicator">🐙 KRAKEN is thinking...</p>', unsafe_allow_html=True)

#                 result = st.session_state.pipeline.process_query_with_handlers(
#                     prompt,
#                     f"user_{int(time.time())}",
#                     output_method="streamlit"
#                 )

#                 typing_placeholder.empty()  # Remove typing indicator

#                 if result.get("success"):
#                     response = result["response"]
#                 else:
#                     response = "I'm having trouble processing that request right now. Could you try rephrasing it?"

#             except Exception as e:
#                 typing_placeholder.empty()
#                 response = "I encountered an issue processing your request. Please try again."

#         else:
#             # Fallback responses with typing animation
#             typing_placeholder = st.empty()
#             typing_placeholder.markdown('<p class="typing-indicator">🐙 KRAKEN is thinking...</p>', unsafe_allow_html=True)

#             time.sleep(1.5)  # Realistic thinking time
#             typing_placeholder.empty()

#             # Smart responses based on input
#             prompt_lower = prompt.lower()

#             if any(word in prompt_lower for word in ["hello", "hi", "hey"]):
#                 response = "👋 Hello TIRUMALA MANAV! I'm KRAKEN, ready to help with your coding questions. What programming challenge can I assist you with today?"

#             elif "help" in prompt_lower:
#                 response = """I can assist you with:

# 🐍 **Python Programming** - Write, debug, and optimize code
# 🔧 **Problem Solving** - Algorithm design and implementation
# 📚 **Code Explanation** - Understand complex programming concepts
# 🐛 **Debugging** - Find and fix errors in your code
# 💡 **Best Practices** - Learn coding standards and patterns
# 📄 **Document Analysis** - Upload and analyze your files

# What specific coding challenge are you working on?"""

#             elif any(word in prompt_lower for word in ["python", "code", "programming"]):
#                 response = "💻 I'd love to help with your coding question! Could you share more details about what you're trying to implement or debug?"

#             elif "kraken" in prompt_lower:
#                 response = "🐙 That's me! KRAKEN - your advanced AI coding assistant built by Tirumala Manav. I specialize in helping with programming challenges, code analysis, and debugging. What would you like to work on?"

#             else:
#                 response = f"I understand you're asking about: \"{prompt}\"\n\nAs your coding assistant, I work best with programming questions. Could you share some code or describe a programming challenge you're facing? I'm here to help! 🚀"

#         st.markdown(response)
#         st.session_state.messages.append({"role": "assistant", "content": response})

# # Working New Chat Button
# if st.session_state.messages:
#     # Create an invisible Streamlit button
#     if st.button("New Chat", key="invisible_new_chat", help="Start a new conversation",
#                  type="primary", use_container_width=False):
#         clear_chat()

#     # JavaScript to make the floating button work
#     st.markdown("""
#     <button class="working-new-chat-btn" onclick="
#         const buttons = parent.document.querySelectorAll('button');
#         for (let button of buttons) {
#             if (button.textContent.includes('New Chat')) {
#                 button.click();
#                 break;
#             }
#         }
#     ">
#         <span style='color: white; font-size: 24px;'>+</span>
#     </button>
#     """, unsafe_allow_html=True)

# # Clean footer with light effect
# st.markdown("""
# <div style='text-align: center; margin-top: 4rem; padding: 2rem; color: #666; font-size: 0.8rem;'>
#     <span class='developer-name'>🐙 KRAKEN v1.0 • Built with ❤️ by Tirumala Manav</span>
# </div>
# """, unsafe_allow_html=True)


#RAG Pipeline and Input/Output Handlers
# import sys
# import os
# import logging
# from typing import Dict, Optional, List, Any
# from datetime import datetime

# # Add agents folder to Python path for imports
# sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'agents'))

# # Import from agents folder
# try:
#     from agent_manager import AgentManager
#     from tools import get_tools
#     from chromadb import Client
#     from chromadb.config import Settings
#     from langchain_core.messages import BaseMessage
# except ImportError as e:
#     print(f"❌ Import Error: {e}")
#     print("Make sure you're running from the pipeline folder and agents folder exists")
#     sys.exit(1)

# # Import from current folder
# from api_client import APIClient

# # Configure logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

# class RAGPipeline:
#     """
#     Orchestrates the RAG (Retrieval-Augmented Generation) process for coding chatbot.
#     Updated: 2025-07-15 07:09:47 UTC
#     User: TIRUMALA MANAV
#     """

#     def __init__(self, db_path: str = r"D:\Code Explainer\src\embeddings\vector_db"):
#         """Initialize RAG pipeline with all necessary components."""
#         try:
#             self.current_user = "TIRUMALA MANAV"
#             self.initialization_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

#             logger.info(f"🚀 Initializing RAG Pipeline for user {self.current_user} at {self.initialization_time} UTC...")

#             # Initialize core components
#             self.db_path = db_path
#             self.client = Client(Settings(persist_directory=db_path))
#             self.tools = get_tools(self.client)
#             self.api_client = APIClient()
#             self.agent_manager = AgentManager(db_path=db_path)

#             # Pipeline configuration
#             self.max_context_length = 4000
#             self.enable_web_search = True
#             self.enable_database_search = True
#             self.context_enhancement = True

#             # Performance tracking
#             self.query_count = 0
#             self.successful_queries = 0
#             self.failed_queries = 0

#             # Validate initialization
#             self._validate_components()

#             logger.info("✅ RAG Pipeline initialized successfully")

#             # Log API status for debugging
#             api_status = self.api_client.validate_api_keys()
#             logger.info(f"📊 API Status: {api_status}")

#         except Exception as e:
#             logger.error(f"❌ RAG Pipeline initialization failed: {e}")
#             raise

#     def _validate_components(self):
#         """Validate that all components are properly initialized."""
#         validations = {
#             "database_client": bool(self.client),
#             "tools_available": len(self.tools) > 0,
#             "api_client": bool(self.api_client),
#             "agent_manager": bool(self.agent_manager),
#             "database_path_exists": os.path.exists(self.db_path)
#         }

#         failed_validations = [k for k, v in validations.items() if not v]

#         if failed_validations:
#             logger.warning(f"⚠️ Some components failed validation: {failed_validations}")
#         else:
#             logger.info("✅ All components validated successfully")

#         return validations

#     def retrieve_context(self, query: str, session_id: str = "default") -> Dict[str, Any]:
#         """
#         Retrieve context from multiple sources with enhanced error handling.
#         Returns detailed context information including source metadata.
#         """
#         context_data = {
#             "database_results": None,
#             "web_results": None,
#             "combined_context": "",
#             "sources_used": [],
#             "retrieval_time": 0,
#             "success": False
#         }

#         retrieval_start = datetime.utcnow()

#         try:
#             logger.debug(f"🔍 Starting context retrieval for query: {query[:50]}...")

#             # Database Search
#             if self.enable_database_search:
#                 context_data["database_results"] = self._search_database(query)
#                 if context_data["database_results"]:
#                     context_data["sources_used"].append("database")
#                     logger.info("✅ Database search successful")
#                 else:
#                     logger.info("ℹ️ Database search returned no results")

#             # Web Search
#             if self.enable_web_search:
#                 context_data["web_results"] = self._search_web(query)
#                 if context_data["web_results"]:
#                     context_data["sources_used"].append("web")
#                     logger.info("✅ Web search successful")
#                 else:
#                     logger.info("ℹ️ Web search returned no results")

#             # Combine contexts
#             context_data["combined_context"] = self._combine_contexts(
#                 context_data["database_results"],
#                 context_data["web_results"]
#             )

#             # Calculate retrieval time
#             context_data["retrieval_time"] = (datetime.utcnow() - retrieval_start).total_seconds()
#             context_data["success"] = bool(context_data["combined_context"])

#             logger.info(f"📊 Context retrieval completed in {context_data['retrieval_time']:.2f}s")
#             logger.info(f"📚 Sources used: {', '.join(context_data['sources_used']) or 'none'}")

#             return context_data

#         except Exception as e:
#             logger.error(f"❌ Context retrieval failed: {e}")
#             context_data["retrieval_time"] = (datetime.utcnow() - retrieval_start).total_seconds()
#             context_data["error"] = str(e)
#             return context_data

#     def _search_database(self, query: str) -> Optional[str]:
#         """Search database using available tools."""
#         try:
#             for tool in self.tools:
#                 if tool.name == "DatabaseSearch":
#                     result = tool.func(query)
#                     if result and "No coding knowledge collections found" not in result:
#                         return f"**📚 Database Knowledge:**\n{result}"
#                     break
#             return None
#         except Exception as e:
#             logger.warning(f"Database search error: {e}")
#             return None

#     def _search_web(self, query: str) -> Optional[str]:
#         """Search web using API client with fallback options."""
#         try:
#             # Try Tavily first
#             web_result = self.api_client.search_tavily(query)
#             if web_result:
#                 return web_result

#             # Try Gemini fallback
#             logger.info("🔄 Trying Gemini fallback for web search...")
#             gemini_result = self.api_client.search_gemini_fallback(query)
#             if gemini_result:
#                 return gemini_result

#             return None

#         except Exception as e:
#             logger.warning(f"Web search error: {e}")
#             return None

#     def _combine_contexts(self, db_context: Optional[str], web_context: Optional[str]) -> str:
#         """Combine multiple context sources into a coherent context string."""
#         context_parts = []

#         if db_context:
#             context_parts.append(db_context)

#         if web_context:
#             context_parts.append(web_context)

#         if context_parts:
#             combined = "\n\n".join(context_parts)

#             # Truncate if too long
#             if len(combined) > self.max_context_length:
#                 combined = combined[:self.max_context_length] + "\n\n[Context truncated due to length limits]"

#             return combined

#         return "No additional context found. Proceeding with general knowledge."

#     def _enhance_query_with_context(self, query: str, context_data: Dict[str, Any]) -> str:
#         """Create an enhanced query that includes retrieved context."""
#         if not context_data["success"] or not context_data["combined_context"]:
#             return query

#         if not self.context_enhancement:
#             return query

#         enhanced_query = f"""
# **User Query:** {query}

# **Retrieved Context:**
# {context_data["combined_context"]}

# **Instructions:**
# Please provide a comprehensive answer using the above context when relevant, and supplement with your knowledge.
# Focus on accuracy, include code examples where appropriate, and explain concepts clearly.

# **Context Sources:** {', '.join(context_data["sources_used"])}
# **User:** {self.current_user}
# **Timestamp:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC
# """
#         return enhanced_query

#     def process_query(self, query: str, session_id: str = "default") -> Dict[str, Any]:
#         """
#         Process query with full RAG pipeline including retrieval and generation.
#         Maintains conversation history and provides detailed response metadata.
#         """
#         query_start_time = datetime.utcnow()
#         self.query_count += 1

#         try:
#             logger.info(f"🎯 Processing RAG query #{self.query_count}: {query[:50]}...")

#             # Step 1: Retrieve context from multiple sources
#             context_data = self.retrieve_context(query, session_id)

#             # Step 2: Enhance query with retrieved context
#             enhanced_query = self._enhance_query_with_context(query, context_data)

#             # Step 3: Generate response using agent manager
#             logger.debug("🤖 Generating response with agent manager...")
#             agent_response = self.agent_manager.process_query(enhanced_query, session_id)

#             # Step 4: Process and format final response
#             if agent_response.get("success", False):
#                 processing_time = (datetime.utcnow() - query_start_time).total_seconds()
#                 self.successful_queries += 1

#                 final_response = {
#                     "response": agent_response["response"],
#                     "original_query": query,
#                     "enhanced_query": enhanced_query if enhanced_query != query else None,
#                     "context_data": context_data,
#                     "source": "rag_pipeline",
#                     "session_id": session_id,
#                     "success": True,
#                     "metadata": {
#                         "query_number": self.query_count,
#                         "processing_time": f"{processing_time:.2f}s",
#                         "context_sources": context_data["sources_used"],
#                         "context_retrieval_time": f"{context_data['retrieval_time']:.2f}s",
#                         "agent_response_metadata": agent_response,
#                         "user": self.current_user,
#                         "timestamp": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC'),
#                         "pipeline_stats": {
#                             "total_queries": self.query_count,
#                             "successful_queries": self.successful_queries,
#                             "failed_queries": self.failed_queries
#                         }
#                     }
#                 }

#                 logger.info(f"✅ RAG query processed successfully in {processing_time:.2f}s")
#                 return final_response

#             else:
#                 # Agent processing failed
#                 self.failed_queries += 1
#                 processing_time = (datetime.utcnow() - query_start_time).total_seconds()

#                 logger.error(f"❌ Agent processing failed for query: {query[:50]}...")
#                 return {
#                     "response": f"I apologize, but I encountered an issue processing your request: {agent_response.get('response', 'Unknown agent error')}",
#                     "original_query": query,
#                     "context_data": context_data,
#                     "source": "rag_pipeline_agent_error",
#                     "session_id": session_id,
#                     "success": False,
#                     "error": agent_response.get("error"),
#                     "metadata": {
#                         "query_number": self.query_count,
#                         "processing_time": f"{processing_time:.2f}s",
#                         "user": self.current_user,
#                         "timestamp": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
#                     }
#                 }

#         except Exception as e:
#             self.failed_queries += 1
#             processing_time = (datetime.utcnow() - query_start_time).total_seconds()

#             logger.error(f"❌ RAG Pipeline processing failed: {e}")
#             return {
#                 "response": f"I apologize, but I encountered a technical error while processing your request. Please try again or rephrase your question. Error details: {str(e)}",
#                 "original_query": query,
#                 "source": "rag_pipeline_error",
#                 "session_id": session_id,
#                 "success": False,
#                 "error": str(e),
#                 "metadata": {
#                     "query_number": self.query_count,
#                     "processing_time": f"{processing_time:.2f}s",
#                     "user": self.current_user,
#                     "timestamp": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
#                 }
#             }

#     def process_simple_query(self, query: str) -> Dict[str, Any]:
#         """Process query without session memory for testing purposes."""
#         try:
#             logger.info(f"🧪 Processing simple test query: {query[:50]}...")

#             context_data = self.retrieve_context(query)
#             enhanced_query = self._enhance_query_with_context(query, context_data)

#             response = self.agent_manager.process_query_simple(enhanced_query)

#             return {
#                 "response": response["response"],
#                 "original_query": query,
#                 "context_used": context_data["combined_context"] if context_data["success"] else None,
#                 "source": "rag_pipeline_simple",
#                 "success": response.get("success", False),
#                 "metadata": {
#                     "context_sources": context_data["sources_used"],
#                     "context_retrieval_time": f"{context_data['retrieval_time']:.2f}s",
#                     "user": self.current_user,
#                     "timestamp": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
#                 }
#             }

#         except Exception as e:
#             logger.error(f"❌ Simple RAG query failed: {e}")
#             return {
#                 "response": f"Test query failed: {str(e)}",
#                 "original_query": query,
#                 "source": "rag_pipeline_simple_error",
#                 "success": False,
#                 "error": str(e)
#             }

#     def get_chat_history(self, session_id: str = "default") -> List[BaseMessage]:
#         """Get chat history for a session from agent manager."""
#         try:
#             return self.agent_manager.get_chat_history(session_id)
#         except Exception as e:
#             logger.error(f"Failed to get chat history for session {session_id}: {e}")
#             return []

#     def clear_chat_history(self, session_id: str = "default"):
#         """Clear chat history for a session."""
#         try:
#             self.agent_manager.clear_chat_history(session_id)
#             logger.info(f"✅ Cleared chat history for session: {session_id}")
#         except Exception as e:
#             logger.error(f"Failed to clear chat history for session {session_id}: {e}")

#     def get_session_info(self, session_id: str = "default") -> Dict[str, Any]:
#         """Get detailed information about a session."""
#         try:
#             history = self.get_chat_history(session_id)
#             agent_sessions = self.agent_manager.get_all_sessions()

#             return {
#                 "session_id": session_id,
#                 "message_count": len(history),
#                 "session_exists": session_id in agent_sessions,
#                 "all_sessions": agent_sessions,
#                 "user": self.current_user,
#                 "timestamp": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
#             }
#         except Exception as e:
#             logger.error(f"Failed to get session info for {session_id}: {e}")
#             return {"error": str(e)}

#     def get_pipeline_status(self) -> Dict[str, Any]:
#         """Get comprehensive status of all pipeline components."""
#         try:
#             # Get database info
#             try:
#                 collections = self.client.list_collections()
#                 db_status = {
#                     "path": self.db_path,
#                     "collections_count": len(collections),
#                     "collections_names": [c.name for c in collections] if collections else [],
#                     "status": "✅ Connected"
#                 }
#             except Exception as e:
#                 db_status = {
#                     "path": self.db_path,
#                     "status": f"❌ Error: {str(e)[:50]}..."
#                 }

#             # Get tools info
#             tools_status = {
#                 "count": len(self.tools),
#                 "names": [tool.name for tool in self.tools],
#                 "status": "✅ Available" if self.tools else "❌ No tools loaded"
#             }

#             # Get API status
#             api_status = self.api_client.get_api_status()

#             # Get agent info
#             try:
#                 agent_info = self.agent_manager.get_agent_info()
#             except Exception as e:
#                 agent_info = {"error": str(e)}

#             # Pipeline performance stats
#             performance_stats = {
#                 "total_queries": self.query_count,
#                 "successful_queries": self.successful_queries,
#                 "failed_queries": self.failed_queries,
#                 "success_rate": f"{(self.successful_queries / max(self.query_count, 1)) * 100:.1f}%",
#                 "initialization_time": self.initialization_time
#             }

#             # Overall status
#             working_components = sum([
#                 "✅" in db_status["status"],
#                 "✅" in tools_status["status"],
#                 "✅" in api_status.get("overall", ""),
#                 "error" not in agent_info
#             ])

#             overall_status = f"✅ {working_components}/4 components operational" if working_components > 0 else "❌ Pipeline not operational"

#             return {
#                 "overall_status": overall_status,
#                 "timestamp": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC'),
#                 "user": self.current_user,
#                 "database": db_status,
#                 "tools": tools_status,
#                 "api_client": api_status,
#                 "agent_manager": agent_info,
#                 "performance": performance_stats,
#                 "configuration": {
#                     "max_context_length": self.max_context_length,
#                     "web_search_enabled": self.enable_web_search,
#                     "database_search_enabled": self.enable_database_search,
#                     "context_enhancement_enabled": self.context_enhancement
#                 }
#             }

#         except Exception as e:
#             logger.error(f"Failed to get pipeline status: {e}")
#             return {
#                 "overall_status": f"❌ Status check failed: {str(e)}",
#                 "error": str(e),
#                 "timestamp": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC'),
#                 "user": self.current_user
#             }

#     def update_configuration(self, **kwargs):
#         """Update pipeline configuration settings."""
#         valid_configs = {
#             "max_context_length", "enable_web_search",
#             "enable_database_search", "context_enhancement"
#         }

#         updated = []
#         for key, value in kwargs.items():
#             if key in valid_configs and hasattr(self, key):
#                 setattr(self, key, value)
#                 updated.append(f"{key}={value}")

#         if updated:
#             logger.info(f"✅ Updated pipeline configuration: {', '.join(updated)}")
#         else:
#             logger.warning("⚠️ No valid configuration parameters provided")

#     def reset_stats(self):
#         """Reset pipeline performance statistics."""
#         self.query_count = 0
#         self.successful_queries = 0
#         self.failed_queries = 0
#         logger.info("✅ Pipeline statistics reset")

# # Test and demonstration functions
# def run_comprehensive_test():
#     """Run comprehensive test of the RAG pipeline."""
#     print(f"🧪 RAG Pipeline Comprehensive Test Suite")
#     print(f"📅 Date: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
#     print(f"👤 User: TIRUMALA MANAV\n")

#     try:
#         # Initialize pipeline
#         print("🔧 Initializing RAG Pipeline...")
#         pipeline = RAGPipeline()

#         # Check pipeline status
#         print("\n📊 Pipeline Status Check:")
#         status = pipeline.get_pipeline_status()
#         print(f"  Overall Status: {status['overall_status']}")
#         print(f"  Database: {status['database']['status']}")
#         print(f"  Tools: {status['tools']['status']}")
#         print(f"  API Client: {status['api_client']['overall']}")

#         # Test queries
#         test_queries = [
#             "Explain merge sort algorithm",
#             "How do I implement a binary tree in Python?",
#             "What is the difference between Python lists and arrays?",
#             "Debug this error: IndexError in Python list"
#         ]

#         print(f"\n🧪 Testing with {len(test_queries)} sample queries...")

#         for i, query in enumerate(test_queries, 1):
#             print(f"\n📝 Test {i}: {query}")

#             # Test simple query (no session)
#             result = pipeline.process_simple_query(query)
#             success_icon = "✅" if result["success"] else "❌"

#             print(f"  {success_icon} Result: {result['response'][:100]}...")
#             print(f"  📊 Context sources: {result['metadata'].get('context_sources', [])}")
#             print(f"  ⏱️ Retrieval time: {result['metadata'].get('context_retrieval_time', 'N/A')}")

#         # Test with session
#         print(f"\n🔄 Testing session-based conversation...")
#         session_result = pipeline.process_query(
#             "Can you explain how recursion works with an example?",
#             session_id="test_session"
#         )

#         success_icon = "✅" if session_result["success"] else "❌"
#         print(f"  {success_icon} Session test: {session_result['response'][:100]}...")

#         # Final stats
#         final_status = pipeline.get_pipeline_status()
#         print(f"\n📈 Final Performance Stats:")
#         print(f"  Total Queries: {final_status['performance']['total_queries']}")
#         print(f"  Success Rate: {final_status['performance']['success_rate']}")

#         print(f"\n✅ RAG Pipeline test completed successfully!")

#     except Exception as e:
#         print(f"❌ RAG Pipeline test failed: {e}")
#         import traceback
#         traceback.print_exc()

# # Main execution
# if __name__ == "__main__":
#     run_comprehensive_test()



#Below Code is of Intergrated RAG Pipeline with Input Output Handlers

# import sys
# import os
# import logging
# from typing import Dict, Optional, List, Any
# from datetime import datetime, UTC

# # Add paths for imports
# sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'agents'))
# sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'handlers'))

# # Import from agents folder
# try:
#     from agent_manager import AgentManager
#     from tools import get_tools
#     from chromadb import Client
#     from chromadb.config import Settings
#     from langchain_core.messages import BaseMessage
# except ImportError as e:
#     print(f"❌ Import Error: {e}")
#     print("Make sure you're running from the pipeline folder and agents folder exists")
#     sys.exit(1)

# # Import from current folder
# from api_client import APIClient

# # Import handlers
# try:
#     from input_handler import InputHandler
#     from output_handler import OutputHandler
# except ImportError as e:
#     print(f"⚠️ Handler Import Warning: {e}")
#     print("Handlers not available - will use basic input/output processing")
#     InputHandler = None
#     OutputHandler = None

# # Configure logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

# class RAGPipeline:
#     """
#     Enhanced RAG Pipeline with integrated input/output handlers.
#     Updated: 2025-07-15 07:42:08 UTC
#     User:  TIRUMALA MANAV
#     """

#     def __init__(self, db_path: str = r"D:\Code Explainer\src\embeddings\vector_db"):
#         """Initialize RAG pipeline with all necessary components including handlers."""
#         try:
#             self.current_user = "TIRUMALA MANAV"
#             self.initialization_time = datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S')

#             logger.info(f"🚀 Initializing Enhanced RAG Pipeline for user {self.current_user} at {self.initialization_time} UTC...")

#             # Initialize core components
#             self.db_path = db_path
#             self.client = Client(Settings(persist_directory=db_path))
#             self.tools = get_tools(self.client)
#             self.api_client = APIClient()
#             self.agent_manager = AgentManager(db_path=db_path)

#             # Initialize handlers if available
#             self.input_handler = InputHandler() if InputHandler else None
#             self.output_handler = OutputHandler() if OutputHandler else None

#             # Pipeline configuration
#             self.max_context_length = 4000
#             self.enable_web_search = True
#             self.enable_database_search = True
#             self.context_enhancement = True
#             self.use_handlers = bool(self.input_handler and self.output_handler)

#             # Performance tracking
#             self.query_count = 0
#             self.successful_queries = 0
#             self.failed_queries = 0

#             # Validate initialization
#             self._validate_components()

#             logger.info("✅ Enhanced RAG Pipeline initialized successfully")
#             logger.info(f"🎛️ Handlers enabled: {self.use_handlers}")

#             # Log API status for debugging
#             api_status = self.api_client.validate_api_keys()
#             logger.info(f"📊 API Status: {api_status}")

#         except Exception as e:
#             logger.error(f"❌ RAG Pipeline initialization failed: {e}")
#             raise

#     def _validate_components(self):
#         """Validate that all components are properly initialized."""
#         validations = {
#             "database_client": bool(self.client),
#             "tools_available": len(self.tools) > 0,
#             "api_client": bool(self.api_client),
#             "agent_manager": bool(self.agent_manager),
#             "database_path_exists": os.path.exists(self.db_path),
#             "input_handler": bool(self.input_handler),
#             "output_handler": bool(self.output_handler)
#         }

#         failed_validations = [k for k, v in validations.items() if not v]

#         if failed_validations:
#             logger.warning(f"⚠️ Some components failed validation: {failed_validations}")
#         else:
#             logger.info("✅ All components validated successfully")

#         return validations

#     def retrieve_context(self, query: str, session_id: str = "default") -> Dict[str, Any]:
#         """
#         Retrieve context from multiple sources with enhanced error handling.
#         Returns detailed context information including source metadata.
#         """
#         context_data = {
#             "database_results": None,
#             "web_results": None,
#             "combined_context": "",
#             "sources_used": [],
#             "retrieval_time": 0,
#             "success": False
#         }

#         retrieval_start = datetime.now(UTC)

#         try:
#             logger.debug(f"🔍 Starting context retrieval for query: {query[:50]}...")

#             # Database Search
#             if self.enable_database_search:
#                 context_data["database_results"] = self._search_database(query)
#                 if context_data["database_results"]:
#                     context_data["sources_used"].append("database")
#                     logger.info("✅ Database search successful")
#                 else:
#                     logger.info("ℹ️ Database search returned no results")

#             # Web Search
#             if self.enable_web_search:
#                 context_data["web_results"] = self._search_web(query)
#                 if context_data["web_results"]:
#                     context_data["sources_used"].append("web")
#                     logger.info("✅ Web search successful")
#                 else:
#                     logger.info("ℹ️ Web search returned no results")

#             # Combine contexts
#             context_data["combined_context"] = self._combine_contexts(
#                 context_data["database_results"],
#                 context_data["web_results"]
#             )

#             # Calculate retrieval time
#             context_data["retrieval_time"] = (datetime.now(UTC) - retrieval_start).total_seconds()
#             context_data["success"] = bool(context_data["combined_context"])

#             logger.info(f"📊 Context retrieval completed in {context_data['retrieval_time']:.2f}s")
#             logger.info(f"📚 Sources used: {', '.join(context_data['sources_used']) or 'none'}")

#             return context_data

#         except Exception as e:
#             logger.error(f"❌ Context retrieval failed: {e}")
#             context_data["retrieval_time"] = (datetime.now(UTC) - retrieval_start).total_seconds()
#             context_data["error"] = str(e)
#             return context_data

#     def _search_database(self, query: str) -> Optional[str]:
#         """Search database using available tools."""
#         try:
#             for tool in self.tools:
#                 if tool.name == "DatabaseSearch":
#                     result = tool.func(query)
#                     if result and "No coding knowledge collections found" not in result:
#                         return f"**📚 Database Knowledge:**\n{result}"
#                     break
#             return None
#         except Exception as e:
#             logger.warning(f"Database search error: {e}")
#             return None

#     def _search_web(self, query: str) -> Optional[str]:
#         """Search web using API client with fallback options."""
#         try:
#             # Try Tavily first
#             web_result = self.api_client.search_tavily(query)
#             if web_result:
#                 return web_result

#             # Try Gemini fallback
#             logger.info("🔄 Trying Gemini fallback for web search...")
#             gemini_result = self.api_client.search_gemini_fallback(query)
#             if gemini_result:
#                 return gemini_result

#             return None

#         except Exception as e:
#             logger.warning(f"Web search error: {e}")
#             return None

#     def _combine_contexts(self, db_context: Optional[str], web_context: Optional[str]) -> str:
#         """Combine multiple context sources into a coherent context string."""
#         context_parts = []

#         if db_context:
#             context_parts.append(db_context)

#         if web_context:
#             context_parts.append(web_context)

#         if context_parts:
#             combined = "\n\n".join(context_parts)

#             # Truncate if too long
#             if len(combined) > self.max_context_length:
#                 combined = combined[:self.max_context_length] + "\n\n[Context truncated due to length limits]"

#             return combined

#         return "No additional context found. Proceeding with general knowledge."

#     def _enhance_query_with_context(self, query: str, context_data: Dict[str, Any]) -> str:
#         """Create an enhanced query that includes retrieved context."""
#         if not context_data["success"] or not context_data["combined_context"]:
#             return query

#         if not self.context_enhancement:
#             return query

#         enhanced_query = f"""
# **User Query:** {query}

# **Retrieved Context:**
# {context_data["combined_context"]}

# **Instructions:**
# Please provide a comprehensive answer using the above context when relevant, and supplement with your knowledge.
# Focus on accuracy, include code examples where appropriate, and explain concepts clearly.

# **Context Sources:** {', '.join(context_data["sources_used"])}
# **User:** {self.current_user}
# **Timestamp:** {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S')} UTC
# """
#         return enhanced_query

#     def process_query_with_handlers(self, raw_input: str, session_id: str = "default",
#                                   output_method: str = "console") -> Dict[str, Any]:
#         """
#         Process query using input/output handlers for enhanced user experience.
#         This is the main method to use when handlers are available.
#         """
#         if not self.use_handlers:
#             logger.warning("Handlers not available, falling back to basic processing")
#             return self.process_query(raw_input, session_id)

#         pipeline_start = datetime.now(UTC)

#         try:
#             logger.info(f"🎛️ Processing query with handlers: {raw_input[:50]}...")

#             # Step 1: Process input using InputHandler
#             processed_input = self.input_handler.process_input(raw_input, session_id)

#             if not processed_input or not processed_input.get("success"):
#                 error_response = {
#                     "success": False,
#                     "response": "Invalid input provided. Please check your query and try again.",
#                     "error": processed_input.get("error") if processed_input else "Input processing failed",
#                     "metadata": {
#                         "timestamp": datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC'),
#                         "user": self.current_user,
#                         "session_id": session_id
#                     }
#                 }

#                 # Handle output
#                 self.output_handler.handle_output(error_response, output_method)
#                 return error_response

#             # Step 2: Process query using RAG pipeline
#             query = processed_input["query"]
#             rag_response = self.process_query(query, session_id)

#             # Step 3: Enhance response with input handler metadata
#             if rag_response.get("success") and "metadata" in rag_response:
#                 rag_response["metadata"]["query_type"] = processed_input.get("query_type", "general")
#                 rag_response["metadata"]["input_processing"] = processed_input.get("metadata", {})
#                 rag_response["metadata"]["code_blocks_detected"] = len(processed_input.get("code_blocks", []))
#                 rag_response["metadata"]["input_validation"] = processed_input.get("validation", {})

#             # Step 4: Calculate total processing time
#             total_processing_time = (datetime.now(UTC) - pipeline_start).total_seconds()
#             if "metadata" in rag_response:
#                 rag_response["metadata"]["total_processing_time"] = f"{total_processing_time:.2f}s"

#             # Step 5: Handle output using OutputHandler
#             output_result = self.output_handler.handle_output(rag_response, output_method)

#             # Step 6: Return combined result
#             return {
#                 **rag_response,
#                 "output_handling": output_result,
#                 "handlers_used": True,
#                 "total_processing_time": f"{total_processing_time:.2f}s"
#             }

#         except Exception as e:
#             logger.error(f"❌ Handler-based processing failed: {e}")
#             error_response = {
#                 "success": False,
#                 "response": f"Pipeline processing failed: {str(e)}",
#                 "error": str(e),
#                 "metadata": {
#                     "timestamp": datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC'),
#                     "user": self.current_user,
#                     "session_id": session_id
#                 }
#             }

#             if self.output_handler:
#                 self.output_handler.handle_output(error_response, output_method)

#             return error_response

#     def process_query(self, query: str, session_id: str = "default") -> Dict[str, Any]:
#         """
#         Process query with full RAG pipeline including retrieval and generation.
#         Maintains conversation history and provides detailed response metadata.
#         """
#         query_start_time = datetime.now(UTC)
#         self.query_count += 1

#         try:
#             logger.info(f"🎯 Processing RAG query #{self.query_count}: {query[:50]}...")

#             # Step 1: Retrieve context from multiple sources
#             context_data = self.retrieve_context(query, session_id)

#             # Step 2: Enhance query with retrieved context
#             enhanced_query = self._enhance_query_with_context(query, context_data)

#             # Step 3: Generate response using agent manager
#             logger.debug("🤖 Generating response with agent manager...")
#             agent_response = self.agent_manager.process_query(enhanced_query, session_id)

#             # Step 4: Process and format final response
#             if agent_response.get("success", False):
#                 processing_time = (datetime.now(UTC) - query_start_time).total_seconds()
#                 self.successful_queries += 1

#                 final_response = {
#                     "response": agent_response["response"],
#                     "original_query": query,
#                     "enhanced_query": enhanced_query if enhanced_query != query else None,
#                     "context_data": context_data,
#                     "source": "rag_pipeline",
#                     "session_id": session_id,
#                     "success": True,
#                     "metadata": {
#                         "query_number": self.query_count,
#                         "processing_time": f"{processing_time:.2f}s",
#                         "context_sources": context_data["sources_used"],
#                         "context_retrieval_time": f"{context_data['retrieval_time']:.2f}s",
#                         "agent_response_metadata": agent_response,
#                         "user": self.current_user,
#                         "timestamp": datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC'),
#                         "pipeline_stats": {
#                             "total_queries": self.query_count,
#                             "successful_queries": self.successful_queries,
#                             "failed_queries": self.failed_queries
#                         }
#                     }
#                 }

#                 logger.info(f"✅ RAG query processed successfully in {processing_time:.2f}s")
#                 return final_response

#             else:
#                 # Agent processing failed
#                 self.failed_queries += 1
#                 processing_time = (datetime.now(UTC) - query_start_time).total_seconds()

#                 logger.error(f"❌ Agent processing failed for query: {query[:50]}...")
#                 return {
#                     "response": f"I apologize, but I encountered an issue processing your request: {agent_response.get('response', 'Unknown agent error')}",
#                     "original_query": query,
#                     "context_data": context_data,
#                     "source": "rag_pipeline_agent_error",
#                     "session_id": session_id,
#                     "success": False,
#                     "error": agent_response.get("error"),
#                     "metadata": {
#                         "query_number": self.query_count,
#                         "processing_time": f"{processing_time:.2f}s",
#                         "user": self.current_user,
#                         "timestamp": datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC')
#                     }
#                 }

#         except Exception as e:
#             self.failed_queries += 1
#             processing_time = (datetime.now(UTC) - query_start_time).total_seconds()

#             logger.error(f"❌ RAG Pipeline processing failed: {e}")
#             return {
#                 "response": f"I apologize, but I encountered a technical error while processing your request. Please try again or rephrase your question. Error details: {str(e)}",
#                 "original_query": query,
#                 "source": "rag_pipeline_error",
#                 "session_id": session_id,
#                 "success": False,
#                 "error": str(e),
#                 "metadata": {
#                     "query_number": self.query_count,
#                     "processing_time": f"{processing_time:.2f}s",
#                     "user": self.current_user,
#                     "timestamp": datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC')
#                 }
#             }

#     def get_pipeline_status(self) -> Dict[str, Any]:
#         """Get comprehensive status of all pipeline components including handlers."""
#         try:
#             # Get database info
#             try:
#                 collections = self.client.list_collections()
#                 db_status = {
#                     "path": self.db_path,
#                     "collections_count": len(collections),
#                     "collections_names": [c.name for c in collections] if collections else [],
#                     "status": "✅ Connected"
#                 }
#             except Exception as e:
#                 db_status = {
#                     "path": self.db_path,
#                     "status": f"❌ Error: {str(e)[:50]}..."
#                 }

#             # Get tools info
#             tools_status = {
#                 "count": len(self.tools),
#                 "names": [tool.name for tool in self.tools],
#                 "status": "✅ Available" if self.tools else "❌ No tools loaded"
#             }

#             # Get API status
#             api_status = self.api_client.get_api_status()

#             # Get agent info
#             try:
#                 agent_info = self.agent_manager.get_agent_info()
#             except Exception as e:
#                 agent_info = {"error": str(e)}

#             # Get handler info
#             handlers_status = {
#                 "input_handler": "✅ Available" if self.input_handler else "❌ Not available",
#                 "output_handler": "✅ Available" if self.output_handler else "❌ Not available",
#                 "handlers_enabled": self.use_handlers
#             }

#             # Add handler statistics if available
#             if self.input_handler:
#                 handlers_status["input_stats"] = self.input_handler.get_input_statistics()
#             if self.output_handler:
#                 handlers_status["output_stats"] = self.output_handler.get_output_statistics()

#             # Pipeline performance stats
#             performance_stats = {
#                 "total_queries": self.query_count,
#                 "successful_queries": self.successful_queries,
#                 "failed_queries": self.failed_queries,
#                 "success_rate": f"{(self.successful_queries / max(self.query_count, 1)) * 100:.1f}%",
#                 "initialization_time": self.initialization_time
#             }

#             # Overall status
#             working_components = sum([
#                 "✅" in db_status["status"],
#                 "✅" in tools_status["status"],
#                 "✅" in api_status.get("overall", ""),
#                 "error" not in agent_info,
#                 self.use_handlers
#             ])

#             overall_status = f"✅ {working_components}/5 components operational" if working_components > 0 else "❌ Pipeline not operational"

#             return {
#                 "overall_status": overall_status,
#                 "timestamp": datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC'),
#                 "user": self.current_user,
#                 "database": db_status,
#                 "tools": tools_status,
#                 "api_client": api_status,
#                 "agent_manager": agent_info,
#                 "handlers": handlers_status,
#                 "performance": performance_stats,
#                 "configuration": {
#                     "max_context_length": self.max_context_length,
#                     "web_search_enabled": self.enable_web_search,
#                     "database_search_enabled": self.enable_database_search,
#                     "context_enhancement_enabled": self.context_enhancement,
#                     "handlers_enabled": self.use_handlers
#                 }
#             }

#         except Exception as e:
#             logger.error(f"Failed to get pipeline status: {e}")
#             return {
#                 "overall_status": f"❌ Status check failed: {str(e)}",
#                 "error": str(e),
#                 "timestamp": datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC'),
#                 "user": self.current_user
#             }

#     # Keep all your existing methods...
#     def process_simple_query(self, query: str) -> Dict[str, Any]:
#         """Process query without session memory for testing purposes."""
#         try:
#             logger.info(f"🧪 Processing simple test query: {query[:50]}...")

#             context_data = self.retrieve_context(query)
#             enhanced_query = self._enhance_query_with_context(query, context_data)

#             response = self.agent_manager.process_query_simple(enhanced_query)

#             return {
#                 "response": response["response"],
#                 "original_query": query,
#                 "context_used": context_data["combined_context"] if context_data["success"] else None,
#                 "source": "rag_pipeline_simple",
#                 "success": response.get("success", False),
#                 "metadata": {
#                     "context_sources": context_data["sources_used"],
#                     "context_retrieval_time": f"{context_data['retrieval_time']:.2f}s",
#                     "user": self.current_user,
#                     "timestamp": datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC')
#                 }
#             }

#         except Exception as e:
#             logger.error(f"❌ Simple RAG query failed: {e}")
#             return {
#                 "response": f"Test query failed: {str(e)}",
#                 "original_query": query,
#                 "source": "rag_pipeline_simple_error",
#                 "success": False,
#                 "error": str(e)
#             }

# # Test function with handlers
# def run_comprehensive_test():
#     """Run comprehensive test of the RAG pipeline with handlers."""
#     print(f"🧪 Enhanced RAG Pipeline Test Suite with Handlers")
#     print(f"📅 Date: {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S')} UTC")
#     print(f"👤 User: TIRUMALA MANAV\n")

#     try:
#         # Initialize pipeline
#         print("🔧 Initializing Enhanced RAG Pipeline...")
#         pipeline = RAGPipeline()

#         # Check pipeline status
#         print("\n📊 Pipeline Status Check:")
#         status = pipeline.get_pipeline_status()
#         print(f"  Overall Status: {status['overall_status']}")
#         print(f"  Database: {status['database']['status']}")
#         print(f"  Tools: {status['tools']['status']}")
#         print(f"  API Client: {status['api_client']['overall']}")
#         print(f"  Handlers: Input {status['handlers']['input_handler']}, Output {status['handlers']['output_handler']}")

#         # Test with handlers if available
#         if pipeline.use_handlers:
#             print(f"\n🎛️ Testing with Input/Output Handlers...")

#             test_queries = [
#                 "Explain merge sort algorithm with code examples",
#                 "Debug this error: IndexError list index out of range",
#                 "What's the difference between Python lists and arrays?"
#             ]

#             for i, query in enumerate(test_queries, 1):
#                 print(f"\n📝 Handler Test {i}: {query}")
#                 result = pipeline.process_query_with_handlers(query, f"handler_test_{i}")

#                 if result.get("success"):
#                     print(f"  ✅ Success with handlers")
#                     print(f"  📊 Query type: {result['metadata'].get('query_type', 'unknown')}")
#                     print(f"  ⏱️ Total time: {result.get('total_processing_time', 'N/A')}")
#                 else:
#                     print(f"  ❌ Failed: {result.get('error', 'Unknown error')}")
#         else:
#             print(f"\n⚠️ Handlers not available, testing basic functionality...")

#             # Test basic functionality
#             result = pipeline.process_simple_query("Explain binary search")
#             success_icon = "✅" if result["success"] else "❌"
#             print(f"  {success_icon} Basic test: {result['response'][:50]}...")

#         print(f"\n✅ Enhanced RAG Pipeline test completed!")

#     except Exception as e:
#         print(f"❌ Enhanced RAG Pipeline test failed: {e}")
#         import traceback
#         traceback.print_exc()

# # Main execution
# if __name__ == "__main__":
#     run_comprehensive_test()

#API Client
# import os
# import logging
# import requests
# import json
# import google.generativeai as genai
# from dotenv import load_dotenv
# from typing import Optional, Dict, List
# from datetime import datetime

# # Load environment variables
# load_dotenv()
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

# class APIClient:
#     """Handles API interactions for the RAG pipeline - Updated 2025-07-15."""

#     def __init__(self):
#         """Initialize API client with Gemini and Tavily configurations."""
#         self.gemini_api_key = os.getenv("GEMINI_API_KEY")
#         self.tavily_api_key = os.getenv("TAVILY_API_KEY")
#         self.current_user = "TIRUMALA MANAV"
#         self.initialization_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

#         self._configure_gemini()
#         logger.info(f"APIClient initialized for user {self.current_user} at {self.initialization_time} UTC")

#     def _configure_gemini(self) -> None:
#         """Configure Gemini API if key is available."""
#         if self.gemini_api_key:
#             try:
#                 genai.configure(api_key=self.gemini_api_key)
#                 logger.info("Gemini API configured successfully")
#             except Exception as e:
#                 logger.error(f"Failed to configure Gemini API: {e}")
#                 self.gemini_api_key = None
#         else:
#             logger.warning("GEMINI_API_KEY not set in environment variables")

#     def get_gemini_response(self, prompt: str, temperature: float = 0.1) -> Optional[str]:
#         """Get response from Gemini API with enhanced error handling."""
#         if not self.gemini_api_key:
#             logger.error("Gemini API key not available")
#             return None

#         try:
#             model = genai.GenerativeModel('gemini-1.5-flash')

#             # Enhanced prompt for coding chatbot
#             enhanced_prompt = f"""
#             User: {self.current_user}
#             Timestamp: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC

#             Query: {prompt}

#             Please provide a comprehensive, educational response suitable for a coding chatbot.
#             Include code examples, explanations, and best practices where applicable.
#             """

#             response = model.generate_content(
#                 enhanced_prompt,
#                 generation_config=genai.types.GenerationConfig(
#                     temperature=temperature,
#                     max_output_tokens=2048,
#                 )
#             )

#             if response.text:
#                 logger.info(f"Gemini response generated successfully (length: {len(response.text)})")
#                 return response.text
#             else:
#                 logger.warning("Gemini API returned empty response")
#                 return None

#         except Exception as e:
#             logger.error(f"Gemini API request failed: {e}")
#             return None

#     def search_tavily(self, query: str, max_results: int = 5) -> Optional[str]:
#         """Perform web search using Tavily API with enhanced formatting."""
#         if not self.tavily_api_key:
#             logger.warning("Tavily API key not available, skipping web search")
#             return None

#         try:
#             url = "https://api.tavily.com/search"
#             headers = {"Content-Type": "application/json"}

#             # Enhanced query for coding-specific searches
#             enhanced_query = self._enhance_coding_query(query)

#             data = {
#                 "api_key": self.tavily_api_key,
#                 "query": enhanced_query,
#                 "max_results": max_results,
#                 "search_depth": "advanced",
#                 "include_answer": True,
#                 "include_raw_content": False,
#                 "include_domains": [
#                     "stackoverflow.com", "github.com", "geeksforgeeks.org",
#                     "leetcode.com", "tutorialspoint.com", "w3schools.com",
#                     "developer.mozilla.org", "docs.python.org", "python.org"
#                 ]
#             }

#             logger.debug(f"Tavily search request: {enhanced_query}")
#             response = requests.post(url, json=data, headers=headers, timeout=15)
#             response.raise_for_status()
#             result = response.json()

#             # Format results for better readability
#             formatted_output = self._format_tavily_results(result)

#             if formatted_output:
#                 logger.info(f"Tavily search successful for query: {query[:50]}...")
#                 return formatted_output
#             else:
#                 logger.warning("Tavily search returned no useful results")
#                 return None

#         except requests.exceptions.Timeout:
#             logger.error("Tavily search timed out after 15 seconds")
#             return None
#         except requests.exceptions.RequestException as e:
#             logger.error(f"Tavily search failed: {e}")
#             return None
#         except Exception as e:
#             logger.error(f"Unexpected error in Tavily search: {e}")
#             return None

#     def _enhance_coding_query(self, query: str) -> str:
#         """Enhance query for better coding-related search results."""
#         query_lower = query.lower()

#         # Add programming context if not present
#         programming_terms = [
#             "algorithm", "code", "programming", "python", "javascript",
#             "java", "c++", "implementation", "tutorial", "example"
#         ]

#         has_programming_context = any(term in query_lower for term in programming_terms)

#         if not has_programming_context:
#             if any(term in query_lower for term in ["dsa", "data structure", "leetcode"]):
#                 query += " programming algorithm implementation tutorial"
#             elif any(term in query_lower for term in ["compare", "vs", "difference"]):
#                 query += " programming language comparison tutorial"
#             elif any(term in query_lower for term in ["sort", "search", "tree", "graph"]):
#                 query += " algorithm implementation code example"
#             else:
#                 query += " programming tutorial code example"

#         return query

#     def _format_tavily_results(self, result: Dict) -> Optional[str]:
#         """Format Tavily search results for better presentation."""
#         try:
#             formatted_parts = []

#             # Add direct answer if available
#             if result.get("answer"):
#                 formatted_parts.append(f"**🎯 Direct Answer:**\n{result.get('answer')}\n")

#             # Add search results
#             results = result.get("results", [])
#             if results:
#                 formatted_parts.append("**🔍 Search Results:**")

#                 for i, item in enumerate(results[:4], 1):  # Limit to top 4 results
#                     title = item.get("title", "No title available")
#                     url = item.get("url", "No URL available")
#                     content = item.get("content", "No content available")

#                     # Truncate content if too long
#                     if len(content) > 400:
#                         content = content[:400] + "..."

#                     formatted_parts.append(
#                         f"\n**{i}. {title}**\n"
#                         f"🔗 URL: {url}\n"
#                         f"📄 Content: {content}\n"
#                     )

#             # Add metadata
#             formatted_parts.append(f"**ℹ️ Search performed at:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
#             formatted_parts.append(f"**👤 Requested by:** {self.current_user}")

#             return "\n".join(formatted_parts) if formatted_parts else None

#         except Exception as e:
#             logger.error(f"Error formatting Tavily results: {e}")
#             return None

#     def search_gemini_fallback(self, query: str) -> Optional[str]:
#         """Use Gemini as fallback for web search when Tavily is unavailable."""
#         if not self.gemini_api_key:
#             logger.warning("Gemini API not available for fallback search")
#             return None

#         try:
#             enhanced_prompt = f"""
#             As a coding expert, provide a comprehensive answer for this programming query: {query}

#             Please include:
#             1. Clear explanation of the concept/problem
#             2. Code examples with proper syntax highlighting (use ```language``` format)
#             3. Step-by-step implementation if applicable
#             4. Time/space complexity analysis if relevant
#             5. Best practices and common pitfalls
#             6. Alternative approaches or related concepts

#             Make your response educational and practical for a coding chatbot.
#             Focus on accuracy and provide working code examples.

#             Current context:
#             - User: {self.current_user}
#             - Timestamp: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC
#             - Source: Gemini AI Fallback Search
#             """

#             response = self.get_gemini_response(enhanced_prompt, temperature=0.2)

#             if response:
#                 formatted_response = f"**🤖 AI Knowledge Base:**\n\n{response}\n\n"
#                 formatted_response += f"**ℹ️ Generated at:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC\n"
#                 formatted_response += f"**👤 Requested by:** {self.current_user}"
#                 return formatted_response

#             return None

#         except Exception as e:
#             logger.error(f"Gemini fallback search failed: {e}")
#             return None

#     def validate_api_keys(self) -> Dict[str, bool]:
#         """Validate availability and functionality of API keys."""
#         validation_results = {
#             "gemini_key_present": bool(self.gemini_api_key),
#             "tavily_key_present": bool(self.tavily_api_key),
#             "gemini_functional": False,
#             "tavily_functional": False,
#             "any_available": False
#         }

#         # Test Gemini functionality
#         if self.gemini_api_key:
#             try:
#                 test_response = self.get_gemini_response("Hello, this is a test.", temperature=0.1)
#                 validation_results["gemini_functional"] = bool(test_response)
#             except Exception as e:
#                 logger.warning(f"Gemini functionality test failed: {e}")

#         # Tavily functionality (just check if key is present - avoid unnecessary API calls)
#         validation_results["tavily_functional"] = bool(self.tavily_api_key)

#         # Overall availability
#         validation_results["any_available"] = (
#             validation_results["gemini_functional"] or
#             validation_results["tavily_functional"]
#         )

#         return validation_results

#     def get_api_status(self) -> Dict[str, str]:
#         """Get detailed status of all APIs with timestamps."""
#         status = {
#             "timestamp": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC'),
#             "user": self.current_user,
#             "initialization_time": self.initialization_time
#         }

#         # Check Gemini status
#         if self.gemini_api_key:
#             try:
#                 model = genai.GenerativeModel('gemini-1.5-flash')
#                 test_response = model.generate_content("Test")
#                 status["gemini"] = "✅ Working properly" if test_response.text else "⚠️ Not responding correctly"
#             except Exception as e:
#                 status["gemini"] = f"❌ Error: {str(e)[:100]}..."
#         else:
#             status["gemini"] = "❌ No API key configured"

#         # Check Tavily status
#         if self.tavily_api_key:
#             status["tavily"] = "✅ API key available (functional test requires search)"
#         else:
#             status["tavily"] = "❌ No API key configured"

#         # Overall status
#         working_apis = sum(1 for v in [status["gemini"], status["tavily"]] if "✅" in v)
#         status["overall"] = f"✅ {working_apis}/2 APIs operational" if working_apis > 0 else "❌ No APIs operational"

#         return status

#     def test_all_apis(self, test_query: str = "Explain binary search algorithm") -> Dict[str, any]:
#         """Test all APIs with a sample query and return results."""
#         test_results = {
#             "test_query": test_query,
#             "timestamp": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC'),
#             "user": self.current_user,
#             "results": {}
#         }

#         # Test Gemini
#         logger.info("Testing Gemini API...")
#         gemini_start = datetime.utcnow()
#         gemini_result = self.get_gemini_response(test_query)
#         gemini_time = (datetime.utcnow() - gemini_start).total_seconds()

#         test_results["results"]["gemini"] = {
#             "success": bool(gemini_result),
#             "response_length": len(gemini_result) if gemini_result else 0,
#             "response_time": f"{gemini_time:.2f}s",
#             "preview": gemini_result[:100] + "..." if gemini_result else "No response"
#         }

#         # Test Tavily
#         logger.info("Testing Tavily API...")
#         tavily_start = datetime.utcnow()
#         tavily_result = self.search_tavily(test_query, max_results=2)
#         tavily_time = (datetime.utcnow() - tavily_start).total_seconds()

#         test_results["results"]["tavily"] = {
#             "success": bool(tavily_result),
#             "response_length": len(tavily_result) if tavily_result else 0,
#             "response_time": f"{tavily_time:.2f}s",
#             "preview": tavily_result[:100] + "..." if tavily_result else "No response"
#         }

#         # Overall test result
#         successful_tests = sum(1 for result in test_results["results"].values() if result["success"])
#         test_results["overall_success"] = successful_tests > 0
#         test_results["successful_apis"] = f"{successful_tests}/2"

#         return test_results

# # Test function for standalone execution
# if __name__ == "__main__":
#     print(f"🧪 APIClient Test Suite - {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
#     print(f"👤 User: TIRUMALA MANAV\n")

#     try:
#         # Initialize client
#         print("🔧 Initializing API Client...")
#         client = APIClient()

#         # Check API status
#         print("\n📊 API Status Check:")
#         status = client.get_api_status()
#         for key, value in status.items():
#             print(f"  {key}: {value}")

#         # Validate API keys
#         print("\n🔑 API Key Validation:")
#         validation = client.validate_api_keys()
#         for key, value in validation.items():
#             status_icon = "✅" if value else "❌"
#             print(f"  {status_icon} {key}: {value}")

#         # Run comprehensive test
#         print("\n🧪 Running Comprehensive API Tests...")
#         test_results = client.test_all_apis()

#         print(f"\n📋 Test Results Summary:")
#         print(f"  Query: {test_results['test_query']}")
#         print(f"  Overall Success: {'✅' if test_results['overall_success'] else '❌'}")
#         print(f"  Successful APIs: {test_results['successful_apis']}")

#         for api_name, result in test_results['results'].items():
#             status_icon = "✅" if result['success'] else "❌"
#             print(f"  {status_icon} {api_name.title()}: {result['response_time']} | {result['response_length']} chars")

#         print(f"\n✅ API Client test completed successfully!")

#     except Exception as e:
#         print(f"❌ API Client test failed: {e}")
#         import traceback
#         traceback.print_exc()


#Output_Handler.py
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

