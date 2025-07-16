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

import streamlit as st
import sys
import os
import time
from datetime import datetime, timezone
import json
import hashlib

import datetime as dt
if not hasattr(dt, 'UTC'):
    dt.UTC = dt.timezone.utc

# Universal configuration function for both local and cloud
def get_config_value(key: str, default=None):
    """Get configuration value from Streamlit secrets or environment variables"""
    try:
        # Try Streamlit secrets first (cloud deployment)
        return st.secrets[key]
    except (KeyError, AttributeError, FileNotFoundError):
        # Fallback to environment variables (local development)
        from dotenv import load_dotenv
        load_dotenv()
        return os.getenv(key, default)

# Simple Vector Store (NO CHROMADB!)
class SimpleVectorStore:
    """Simple in-memory vector store using sentence similarity"""

    def __init__(self):
        self.documents = []
        self.embeddings = []
        self.metadata = []

    def add_documents(self, docs, metadatas=None):
        """Add documents to the store"""
        for i, doc in enumerate(docs):
            self.documents.append(doc)
            # Simple hash-based "embedding" (good enough for basic similarity)
            embedding = self._simple_embed(doc)
            self.embeddings.append(embedding)

            if metadatas:
                self.metadata.append(metadatas[i])
            else:
                self.metadata.append({"source": "default"})

    def _simple_embed(self, text):
        """Create simple text embedding using word frequency"""
        words = text.lower().split()
        word_count = {}
        for word in words:
            word_count[word] = word_count.get(word, 0) + 1
        return word_count

    def search(self, query, top_k=3):
        """Search for similar documents"""
        query_embedding = self._simple_embed(query)

        # Calculate similarity scores
        scores = []
        for i, doc_embedding in enumerate(self.embeddings):
            score = self._calculate_similarity(query_embedding, doc_embedding)
            scores.append((score, i))

        # Sort by similarity and return top results
        scores.sort(reverse=True)
        results = []

        for score, idx in scores[:top_k]:
            if score > 0:  # Only return if there's some similarity
                results.append({
                    'document': self.documents[idx],
                    'metadata': self.metadata[idx],
                    'score': score
                })

        return results

    def _calculate_similarity(self, embed1, embed2):
        """Calculate simple similarity between embeddings"""
        common_words = set(embed1.keys()) & set(embed2.keys())
        if not common_words:
            return 0

        similarity = 0
        for word in common_words:
            similarity += min(embed1[word], embed2[word])

        return similarity

# Initialize the simple vector store
@st.cache_resource
def create_simple_rag():
    """Create simple RAG system without any external dependencies"""
    try:
        vector_store = SimpleVectorStore()

        # Programming knowledge base
        programming_docs = [
            "Python is a high-level programming language with clean syntax, dynamic typing, and extensive libraries for web development, data science, and automation",
            "JavaScript is the programming language of the web, used for front-end development, back-end with Node.js, and mobile app development",
            "React is a JavaScript library for building user interfaces with component-based architecture and virtual DOM for efficient rendering",
            "Node.js is a JavaScript runtime that allows server-side development, API creation, and real-time applications using event-driven architecture",
            "Git is a distributed version control system for tracking changes in source code, enabling collaboration and code history management",
            "SQL is a programming language for managing relational databases, performing queries, and manipulating structured data",
            "HTML (HyperText Markup Language) structures web content using semantic elements like headers, paragraphs, links, and forms",
            "CSS (Cascading Style Sheets) styles HTML elements, controls layout, typography, colors, and responsive design for web pages",
            "REST APIs use HTTP methods (GET, POST, PUT, DELETE) for stateless communication between client and server applications",
            "JSON (JavaScript Object Notation) is a lightweight data interchange format used for API responses and configuration files",
            "MongoDB is a NoSQL database that stores data in flexible JSON-like documents, ideal for modern web applications",
            "Docker containerizes applications with their dependencies, ensuring consistent deployment across different environments",
            "AWS (Amazon Web Services) provides cloud computing services including EC2, S3, Lambda, and RDS for scalable applications",
            "Machine Learning algorithms learn patterns from data to make predictions, including supervised, unsupervised, and reinforcement learning",
            "APIs (Application Programming Interfaces) define how software components communicate, enabling integration between different systems",
            "Debugging is the process of finding and fixing errors in code using tools like debuggers, logging, and testing frameworks",
            "Version control with Git tracks code changes, enables branching and merging, and facilitates team collaboration on projects",
            "Web frameworks like Django (Python), Express (Node.js), and Spring (Java) simplify web application development",
            "Databases store and organize data, with SQL databases being relational and NoSQL databases offering flexible schemas",
            "Frontend development focuses on user interface and experience using HTML, CSS, JavaScript, and frameworks like React or Vue"
        ]

        # Add metadata for each document
        metadatas = [{"topic": f"topic_{i}", "category": "programming"} for i in range(len(programming_docs))]

        vector_store.add_documents(programming_docs, metadatas)

        return vector_store

    except Exception as e:
        st.sidebar.error(f"Simple RAG creation failed: {e}")
        return None

# Enhanced RAG query function
def enhanced_rag_query(query, vector_store):
    """Perform RAG query using simple vector store"""
    try:
        # Search for relevant documents
        results = vector_store.search(query, top_k=3)

        if results:
            # Combine relevant documents as context
            context_docs = [result['document'] for result in results]
            context = " ".join(context_docs)

            # Generate response with context
            import google.generativeai as genai
            api_key = get_config_value("GEMINI_API_KEY")
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')

            enhanced_prompt = f"""You are KRAKEN, an expert AI coding assistant created by Tirumala Manav.

RELEVANT CONTEXT from knowledge base:
{context}

USER QUESTION: {query}

Provide a comprehensive, helpful response that:
1. Uses the context information when relevant
2. Adds your own expertise and knowledge
3. Gives practical examples and code snippets if applicable
4. Maintains a friendly, professional tone

Response:"""

            response = model.generate_content(enhanced_prompt)
            return response.text, True
        else:
            return None, False

    except Exception as e:
        st.sidebar.error(f"Enhanced RAG query failed: {e}")
        return None, False

# Test AI response function
def test_ai_response(prompt):
    """Test direct AI response using Gemini API"""
    try:
        import google.generativeai as genai

        api_key = get_config_value("GEMINI_API_KEY")
        if not api_key:
            return None, "No API key found"

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')

        enhanced_prompt = f"""You are KRAKEN, an expert AI coding assistant created by Tirumala Manav. You specialize in:
- Programming languages (Python, JavaScript, Java, C++, etc.)
- Web development (HTML, CSS, React, Node.js)
- Database design and SQL
- Git version control and DevOps
- API development and integration
- Debugging and code optimization
- Software architecture and best practices

User question: {prompt}

Provide a helpful, detailed, and practical response:"""

        response = model.generate_content(enhanced_prompt)
        return response.text, None

    except Exception as e:
        return None, str(e)

# Test API keys access and show debug info
def test_api_access():
    """Test if API keys are accessible"""
    st.sidebar.subheader("🔍 System Status")

    try:
        gemini_key = get_config_value("GEMINI_API_KEY")
        if gemini_key:
            st.sidebar.success(f"✅ Gemini: ...{gemini_key[-8:]}")
            gemini_ready = True
        else:
            st.sidebar.error("❌ Gemini: Not found")
            gemini_ready = False
    except Exception as e:
        st.sidebar.error(f"❌ Gemini: {e}")
        gemini_ready = False

    try:
        tavily_key = get_config_value("TAVILY_API_KEY")
        if tavily_key:
            st.sidebar.success(f"✅ Tavily: ...{tavily_key[-8:]}")
            tavily_ready = True
        else:
            st.sidebar.info("ℹ️ Tavily: Not configured (optional)")
            tavily_ready = False
    except Exception as e:
        st.sidebar.info(f"ℹ️ Tavily: {e}")
        tavily_ready = False

    return gemini_ready, tavily_ready

# Silent setup
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
sys.path.insert(0, src_path)

for module_dir in ['agents', 'pipeline', 'handlers', 'monitoring', 'embeddings', 'data_processing']:
    sys.path.insert(0, os.path.join(src_path, module_dir))

# Page config - ChatGPT style
st.set_page_config(
    page_title="KRAKEN",
    page_icon="🐙",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Test API access first
gemini_ready, tavily_ready = test_api_access()

# Initialize simple RAG system
simple_rag_store = create_simple_rag()
if simple_rag_store:
    st.sidebar.success("✅ Simple RAG System loaded")
    system_ready = gemini_ready
else:
    st.sidebar.warning("⚠️ RAG System failed")
    system_ready = gemini_ready

# Session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Function to clear chat
def clear_chat():
    st.session_state.messages = []
    st.rerun()

# Custom CSS for ChatGPT-like aesthetics
st.markdown("""
<style>
/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* ChatGPT-like styling */
.main {
    padding-top: 2rem;
}

/* Animated gradient background for header */
@keyframes glow {
    0% { text-shadow: 0 0 20px #00d4aa; }
    50% { text-shadow: 0 0 30px #00d4aa, 0 0 40px #00d4aa; }
    100% { text-shadow: 0 0 20px #00d4aa; }
}

.kraken-title {
    animation: glow 2s ease-in-out infinite alternate;
}

/* Welcome box styling */
.welcome-box {
    background: linear-gradient(135deg, #1e1e1e 0%, #2d2d2d 100%);
    border: 1px solid rgba(0, 212, 170, 0.3);
    border-radius: 12px;
    padding: 1.5rem;
    margin: 2rem auto;
    max-width: 600px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    position: relative;
    overflow: hidden;
}

.welcome-box::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(0, 212, 170, 0.1), transparent);
    animation: shine 3s infinite;
}

@keyframes shine {
    0% { left: -100%; }
    100% { left: 100%; }
}

/* Chat container */
.chat-container {
    max-width: 700px;
    margin: 0 auto;
}

/* Typing animation */
@keyframes typing {
    0% { opacity: 0.3; }
    50% { opacity: 1; }
    100% { opacity: 0.3; }
}

.typing-indicator {
    animation: typing 1.5s ease-in-out infinite;
}

/* Working New Chat Button */
.working-new-chat-btn {
    position: fixed;
    bottom: 20px;
    right: 20px;
    z-index: 999;
    background: #00d4aa;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 12px rgba(0, 212, 170, 0.4);
    cursor: pointer;
    transition: all 0.3s ease;
    border: none;
    outline: none;
}

.working-new-chat-btn:hover {
    transform: scale(1.1);
    box-shadow: 0 6px 20px rgba(0, 212, 170, 0.6);
}

/* Light effect for developer name */
@keyframes light-glow {
    0% { text-shadow: 0 0 10px rgba(0, 212, 170, 0.5); }
    50% { text-shadow: 0 0 20px rgba(0, 212, 170, 0.8), 0 0 30px rgba(0, 212, 170, 0.6); }
    100% { text-shadow: 0 0 10px rgba(0, 212, 170, 0.5); }
}

.developer-name {
    animation: light-glow 3s ease-in-out infinite;
}
</style>
""", unsafe_allow_html=True)

# KRAKEN Header
st.markdown("""
<div style='text-align: center; margin-bottom: 3rem;'>
    <h1 class='kraken-title' style='font-size: 3.5rem; margin: 0; color: #00d4aa; font-weight: 700;'>
        🐙 KRAKEN
    </h1>
    <p style='font-size: 1.1rem; color: #888; margin: 0.5rem 0; font-weight: 300;'>
        AI Assistant Coding Chat Bot
    </p>
    <p class='developer-name' style='font-size: 0.9rem; color: #00d4aa; margin: 0; font-weight: 500;'>
        <strong>Tirumala Manav</strong> - Machine Learning Engineer, Computer Science Graduate
    </p>
</div>
""", unsafe_allow_html=True)

# System status indicator
if system_ready and simple_rag_store:
    st.success("🚀 KRAKEN System is fully operational with Simple RAG!")
elif gemini_ready:
    st.warning("⚡ KRAKEN is running in enhanced AI mode")
else:
    st.error("🔧 KRAKEN needs configuration - check API keys")

# Welcome Message
if not st.session_state.messages:
    st.markdown("""
    <div class='welcome-box'>
        <div style='display: flex; align-items: center; margin-bottom: 1rem;'>
            <div style='background: #00d4aa; width: 32px; height: 32px; border-radius: 50%;
                        display: flex; align-items: center; justify-content: center; margin-right: 12px;'>
                🐙
            </div>
            <strong style='color: #fff; font-size: 1.1rem;'>Hi! I'm KRAKEN, your AI coding assistant.</strong>
        </div>
        <p style='margin: 0; color: #ccc; line-height: 1.5;'>
            I can help you with programming questions, debugging, code explanation, and implementation guidance.
            I'm equipped with a knowledge base and advanced AI capabilities.
        </p>
        <p style='margin: 1rem 0 0 0; color: #00d4aa; font-weight: 500;'>
            What can I help you with today?
        </p>
    </div>
    """, unsafe_allow_html=True)

# Chat Messages Container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

st.markdown('</div>', unsafe_allow_html=True)

# Chat Input
if prompt := st.chat_input("Message KRAKEN..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        typing_placeholder = st.empty()
        typing_placeholder.markdown('<p class="typing-indicator">🐙 KRAKEN is thinking...</p>', unsafe_allow_html=True)

        # Try simple RAG first
        if system_ready and simple_rag_store:
            try:
                rag_response, success = enhanced_rag_query(prompt, simple_rag_store)
                typing_placeholder.empty()

                if success and rag_response:
                    response = rag_response
                    st.sidebar.info("🧠 Used Simple RAG")
                else:
                    # Fallback to direct AI
                    ai_response, error = test_ai_response(prompt)
                    response = ai_response if ai_response else f"Error: {error}"
                    st.sidebar.info("🤖 Used Direct AI")

            except Exception as e:
                typing_placeholder.empty()
                # Fallback to direct AI
                ai_response, error = test_ai_response(prompt)
                response = ai_response if ai_response else f"Error: {error}"
                st.sidebar.warning("⚠️ RAG failed, used Direct AI")

        elif gemini_ready:
            # Direct AI response
            ai_response, error = test_ai_response(prompt)
            typing_placeholder.empty()
            response = ai_response if ai_response else f"Error: {error}"
            st.sidebar.info("🤖 Used Enhanced AI")

        else:
            # Fallback responses
            typing_placeholder.empty()
            response = "⚠️ I need API configuration to provide intelligent responses. Please check the sidebar for status."

        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# New Chat Button
if st.session_state.messages:
    if st.button("New Chat", key="invisible_new_chat", help="Start a new conversation"):
        clear_chat()

    st.markdown("""
    <button class="working-new-chat-btn" onclick="
        const buttons = parent.document.querySelectorAll('button');
        for (let button of buttons) {
            if (button.textContent.includes('New Chat')) {
                button.click();
                break;
            }
        }
    ">
        <span style='color: white; font-size: 24px;'>+</span>
    </button>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div style='text-align: center; margin-top: 4rem; padding: 2rem; color: #666; font-size: 0.8rem;'>
    <span class='developer-name'>🐙 KRAKEN v1.0 • Built with ❤️ by Tirumala Manav</span>
</div>
""", unsafe_allow_html=True)
