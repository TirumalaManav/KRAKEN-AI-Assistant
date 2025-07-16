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
from chromadb import Client
from chromadb.config import Settings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from dotenv import load_dotenv
from tools import get_tools
from typing import Dict, List

# Configure logging to DEBUG level
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AgentManager:
    def __init__(self, db_path: str = r"D:\Code Explainer\src\embeddings\vector_db"):
        """Initialize the agent manager with database, LLM, and tools."""
        try:
            logger.debug("Initializing AgentManager")
            # Validate environment variables
            if not os.getenv("GEMINI_API_KEY"):
                raise ValueError("GEMINI_API_KEY environment variable is not set.")

            os.makedirs(db_path, exist_ok=True)
            self.client = Client(Settings(persist_directory=db_path))
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                api_key=os.getenv("GEMINI_API_KEY"),
                temperature=0.1
            )
            logger.debug("LLM initialized: %s", self.llm)

            self.tools = get_tools(self.client)
            logger.debug("Tools initialized: %s", [tool.name for tool in self.tools])

            # Use the official React prompt from LangChain hub
            self.prompt = hub.pull("hwchase17/react")
            logger.debug("Official React prompt retrieved from hub")

            # Create the agent with the official prompt
            self.agent = create_react_agent(
                llm=self.llm,
                tools=self.tools,
                prompt=self.prompt
            )
            logger.debug("Agent created: %s", self.agent)

            # Create AgentExecutor
            self.executor = AgentExecutor(
                agent=self.agent,
                tools=self.tools,
                verbose=True,
                handle_parsing_errors=True,
                max_iterations=5,
                early_stopping_method="force"
            )
            logger.debug("AgentExecutor created: %s", self.executor)

            # Store for chat histories
            self.store = {}

            # Create the agent with message history
            self.agent_with_chat_history = RunnableWithMessageHistory(
                self.executor,
                self.get_session_history,
                input_messages_key="input",
                history_messages_key="chat_history"
            )
            logger.debug("Agent with chat history initialized")

            logger.info("AgentManager initialized successfully with official React prompt")
        except Exception as e:
            logger.error("AgentManager initialization failed: %s", str(e))
            raise

    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        """Get or create a chat history for a given session."""
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()
        logger.debug("Session history retrieved for session_id: %s", session_id)
        return self.store[session_id]

    def process_query(self, query: str, session_id: str = "default") -> Dict:
        """Process user query with memory and agent executor."""
        try:
            logger.debug("Processing query: %s, session_id: %s", query, session_id)

            # Use the agent with chat history - DO NOT pass agent_scratchpad manually
            response = self.agent_with_chat_history.invoke(
                {"input": query},  # Only pass input, let the agent handle scratchpad
                config={"configurable": {"session_id": session_id}}
            )
            logger.debug("Agent response: %s", response)

            final_answer = response.get("output", str(response))
            logger.info("Successfully processed query: %s", query[:50])
            return {
                "response": final_answer,
                "source": "agent",
                "session_id": session_id,
                "success": True
            }
        except Exception as e:
            logger.error("Query processing failed: %s", str(e))
            return {
                "response": f"I apologize, but I encountered an error while processing your query: {str(e)}",
                "source": "error",
                "session_id": session_id,
                "success": False,
                "error": str(e)
            }

    def process_query_simple(self, query: str) -> Dict:
        """Simple query processing without chat history for testing."""
        try:
            logger.debug("Processing simple query: %s", query)

            response = self.executor.invoke({"input": query})
            logger.debug("Simple agent response: %s", response)

            final_answer = response.get("output", str(response))
            return {
                "response": final_answer,
                "source": "agent_simple",
                "success": True
            }
        except Exception as e:
            logger.error("Simple query processing failed: %s", str(e))
            return {
                "response": f"Error processing query: {str(e)}",
                "source": "error",
                "success": False,
                "error": str(e)
            }

    def get_chat_history(self, session_id: str = "default") -> List:
        """Get chat history for a session."""
        if session_id in self.store:
            logger.debug("Chat history retrieved for session: %s", session_id)
            return self.store[session_id].messages
        logger.debug("No chat history found for session: %s", session_id)
        return []

    def clear_chat_history(self, session_id: str = "default"):
        """Clear chat history for a session."""
        if session_id in self.store:
            self.store[session_id].clear()
            logger.info(f"Cleared chat history for session: {session_id}")

    def get_all_sessions(self) -> List:
        """Get all session IDs."""
        logger.debug("Retrieving all session IDs")
        return list(self.store.keys())

    def get_agent_info(self) -> Dict:
        """Get information about the agent configuration."""
        return {
            "tools": [tool.name for tool in self.tools],
            "llm_model": "gemini-1.5-flash",
            "prompt_type": "official_react",
            "max_iterations": 5,
            "sessions_count": len(self.store)
        }
