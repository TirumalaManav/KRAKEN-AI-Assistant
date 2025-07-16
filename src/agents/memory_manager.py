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
from typing import Dict, List, Any, Optional
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from datetime import datetime

logger = logging.getLogger(__name__)

class MemoryManager:
    """Enhanced memory manager for coding chatbot with session management."""

    def __init__(self, llm: ChatGoogleGenerativeAI = None, max_history: int = 20):
        """Initialize memory manager optimized for coding conversations."""
        self.llm = llm
        self.max_history = max_history  # Increased for coding context
        self.store: Dict[str, BaseChatMessageHistory] = {}
        self.session_metadata: Dict[str, Dict] = {}
        logger.info(f"MemoryManager initialized with max history {max_history}")

    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        """Get or create a chat history for a given session."""
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()
            self.session_metadata[session_id] = {
                "created_at": datetime.utcnow().isoformat(),
                "last_active": datetime.utcnow().isoformat(),
                "query_count": 0,
                "topics": set(),
                "user": "TIRUMALA MANAV"  # Current user
            }
            logger.info(f"Created new session: {session_id} for user: TIRUMALA MANAV")
        else:
            # Update last active time
            self.session_metadata[session_id]["last_active"] = datetime.utcnow().isoformat()

        return self.store[session_id]

    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, Any], session_id: str = "default"):
        """Save context to memory with enhanced metadata for coding chatbot."""
        try:
            history = self.get_session_history(session_id)

            # Extract input message
            input_message = None
            if "query" in inputs:
                input_message = inputs["query"]
            elif "input" in inputs:
                input_message = inputs["input"]
            elif "question" in inputs:
                input_message = inputs["question"]

            # Extract output message
            output_message = None
            if "response" in outputs:
                output_message = outputs["response"]
            elif "output" in outputs:
                output_message = outputs["output"]
            elif "answer" in outputs:
                output_message = outputs["answer"]

            # Add messages to history
            if input_message:
                history.add_user_message(input_message)
                # Update session metadata
                self.session_metadata[session_id]["query_count"] += 1
                self._extract_topics(input_message, session_id)

            if output_message:
                history.add_ai_message(output_message)

            # Trim history if needed
            self._trim_history(session_id)

            logger.info(f"Context saved for session: {session_id}, query count: {self.session_metadata[session_id]['query_count']}")

        except Exception as e:
            logger.error(f"Failed to save context for session {session_id}: {e}")

    def _extract_topics(self, message: str, session_id: str):
        """Extract coding topics from user messages."""
        coding_topics = {
            "algorithms", "data structures", "python", "javascript", "java", "c++",
            "leetcode", "arrays", "trees", "graphs", "sorting", "searching", "recursion",
            "dynamic programming", "greedy", "backtracking", "binary search", "dfs", "bfs",
            "heap", "stack", "queue", "linked list", "hash table", "string manipulation",
            "debugging", "optimization", "complexity analysis", "object oriented programming",
            "functional programming", "design patterns", "system design", "databases",
            "web development", "api", "testing", "git", "machine learning", "ai"
        }

        message_lower = message.lower()
        found_topics = {topic for topic in coding_topics if topic in message_lower}

        if found_topics:
            self.session_metadata[session_id]["topics"].update(found_topics)
            logger.debug(f"Extracted topics for session {session_id}: {found_topics}")

    def _trim_history(self, session_id: str):
        """Trim history to max_history messages while preserving important coding context."""
        history = self.get_session_history(session_id)
        messages = history.messages

        if len(messages) > self.max_history * 2:  # *2 for human/ai message pairs
            # For coding chatbot, keep recent messages + any with code blocks
            important_messages = []
            recent_messages = messages[-(self.max_history):]

            # Find messages with code blocks or error discussions
            for message in messages[:-self.max_history]:
                content = message.content.lower()
                if any(keyword in content for keyword in ["```", "error", "exception", "algorithm", "complexity"]):
                    important_messages.append(message)

            # Combine important and recent messages, remove duplicates
            preserved_messages = important_messages + recent_messages

            # Clear and rebuild history
            history.clear()
            for message in preserved_messages[-self.max_history:]:  # Ensure we don't exceed limit
                history.add_message(message)

            logger.info(f"Trimmed history for session {session_id}, preserved {len(preserved_messages)} messages")

    def get_history(self, session_id: str = "default") -> List[BaseMessage]:
        """Get chat history for a session."""
        return self.get_session_history(session_id).messages

    def clear_history(self, session_id: str = "default"):
        """Clear chat history for a session."""
        if session_id in self.store:
            self.store[session_id].clear()
            # Reset metadata but keep creation info
            if session_id in self.session_metadata:
                created_at = self.session_metadata[session_id]["created_at"]
                user = self.session_metadata[session_id]["user"]
                self.session_metadata[session_id] = {
                    "created_at": created_at,
                    "last_active": datetime.utcnow().isoformat(),
                    "query_count": 0,
                    "topics": set(),
                    "user": user
                }
            logger.info(f"Cleared history for session: {session_id}")

    def get_all_sessions(self) -> List[str]:
        """Get all session IDs."""
        return list(self.store.keys())

    def get_session_info(self, session_id: str) -> Dict[str, Any]:
        """Get detailed information about a session."""
        if session_id not in self.session_metadata:
            return {"error": f"Session {session_id} not found"}

        metadata = self.session_metadata[session_id].copy()
        metadata["topics"] = list(metadata["topics"])  # Convert set to list for JSON serialization
        metadata["message_count"] = len(self.get_history(session_id))

        return metadata

    def summarize_history(self, session_id: str = "default", last_n: int = 6) -> str:
        """Summarize chat history for a session with coding context."""
        history = self.get_history(session_id)
        if not history:
            return "No conversation history available."

        summary_parts = []
        recent_messages = history[-last_n:] if len(history) > last_n else history

        # Add session info
        if session_id in self.session_metadata:
            metadata = self.session_metadata[session_id]
            topics = list(metadata["topics"])[:5]  # Top 5 topics
            summary_parts.append(f"**Session Summary for {metadata['user']}:**")
            summary_parts.append(f"Topics discussed: {', '.join(topics) if topics else 'General programming'}")
            summary_parts.append(f"Total queries: {metadata['query_count']}\n")

        # Add recent conversation
        summary_parts.append("**Recent Conversation:**")
        for i, message in enumerate(recent_messages):
            role = "👤 User" if message.type == "human" else "🤖 Assistant"
            content = message.content[:150] + "..." if len(message.content) > 150 else message.content
            summary_parts.append(f"{role}: {content}")

        return "\n".join(summary_parts)

    def get_context_window(self, session_id: str = "default", window_size: int = 8) -> List[BaseMessage]:
        """Get a context window of recent messages optimized for coding conversations."""
        history = self.get_history(session_id)
        return history[-window_size:] if len(history) > window_size else history

    def get_coding_context(self, session_id: str = "default") -> Dict[str, Any]:
        """Get coding-specific context from the conversation."""
        history = self.get_history(session_id)

        context = {
            "recent_languages": set(),
            "recent_topics": set(),
            "code_blocks": [],
            "errors_discussed": [],
            "algorithms_mentioned": set()
        }

        # Analyze recent messages for coding context
        for message in history[-10:]:  # Last 10 messages
            content = message.content.lower()

            # Extract programming languages
            languages = ["python", "javascript", "java", "c++", "c#", "go", "rust", "kotlin"]
            for lang in languages:
                if lang in content:
                    context["recent_languages"].add(lang)

            # Extract algorithms and data structures
            algo_terms = ["sorting", "searching", "tree", "graph", "array", "linked list",
                         "stack", "queue", "heap", "hash", "recursion", "dynamic programming"]
            for term in algo_terms:
                if term in content:
                    context["algorithms_mentioned"].add(term)

            # Find code blocks
            if "```" in message.content:
                # Extract code blocks
                code_start = message.content.find("```")
                if code_start != -1:
                    code_end = message.content.find("```", code_start + 3)
                    if code_end != -1:
                        code_block = message.content[code_start:code_end + 3]
                        context["code_blocks"].append(code_block[:200] + "..." if len(code_block) > 200 else code_block)

            # Find error discussions
            if any(error_term in content for error_term in ["error", "exception", "bug", "issue"]):
                context["errors_discussed"].append(message.content[:100] + "..." if len(message.content) > 100 else message.content)

        # Convert sets to lists for JSON serialization
        context["recent_languages"] = list(context["recent_languages"])
        context["recent_topics"] = list(context["recent_topics"])
        context["algorithms_mentioned"] = list(context["algorithms_mentioned"])

        return context

    def export_session(self, session_id: str) -> Dict[str, Any]:
        """Export complete session data for backup or analysis."""
        if session_id not in self.store:
            return {"error": f"Session {session_id} not found"}

        history = self.get_history(session_id)
        metadata = self.get_session_info(session_id)
        coding_context = self.get_coding_context(session_id)

        export_data = {
            "session_id": session_id,
            "metadata": metadata,
            "coding_context": coding_context,
            "messages": [
                {
                    "type": msg.type,
                    "content": msg.content,
                    "timestamp": datetime.utcnow().isoformat()  # In real implementation, you'd store actual timestamps
                }
                for msg in history
            ],
            "export_timestamp": datetime.utcnow().isoformat()
        }

        return export_data

    def get_session_statistics(self) -> Dict[str, Any]:
        """Get overall statistics across all sessions."""
        total_sessions = len(self.store)
        total_messages = sum(len(self.get_history(sid)) for sid in self.store.keys())

        all_topics = set()
        for metadata in self.session_metadata.values():
            all_topics.update(metadata.get("topics", set()))

        active_sessions = [sid for sid, metadata in self.session_metadata.items()
                          if metadata.get("query_count", 0) > 0]

        return {
            "total_sessions": total_sessions,
            "active_sessions": len(active_sessions),
            "total_messages": total_messages,
            "unique_topics": list(all_topics),
            "current_user": "TIRUMALA MANAV",
            "timestamp": datetime.utcnow().isoformat()
        }
