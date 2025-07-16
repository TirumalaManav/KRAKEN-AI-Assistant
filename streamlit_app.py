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

# In-memory ChromaDB function (SOLVES SQLITE ISSUE)
def create_memory_chroma():
    """Create in-memory ChromaDB that works without SQLite issues"""
    try:
        import chromadb

        # Use in-memory client (no SQLite dependency)
        client = chromadb.Client()

        # Create collection
        collection = client.create_collection(
            name="kraken_knowledge",
            metadata={"description": "In-memory knowledge base"}
        )

        # Add programming knowledge
        docs = [
            "Python is a versatile programming language with clean syntax and dynamic typing",
            "JavaScript powers web development and runs in browsers and Node.js servers",
            "React is a popular JavaScript library for building interactive user interfaces",
            "Node.js enables JavaScript server-side development and API creation",
            "Git tracks code changes and enables distributed version control",
            "SQL manages relational database operations and data queries",
            "APIs enable communication between different software systems and services",
            "HTML structures web page content with semantic markup elements",
            "CSS styles HTML elements for visual presentation and responsive design",
            "JSON is a lightweight format for data exchange between applications",
            "REST APIs use HTTP methods for stateless communication",
            "MongoDB is a NoSQL database that stores data in flexible documents",
            "Docker containerizes applications for consistent deployment",
            "AWS provides cloud computing services and infrastructure",
            "Machine Learning algorithms learn patterns from data to make predictions"
        ]

        for i, doc in enumerate(docs):
            collection.add(
                documents=[doc],
                ids=[f"doc_{i}"],
                metadatas=[{"source": "programming", "type": "knowledge"}]
            )

        return client, collection

    except Exception as e:
        st.sidebar.error(f"Memory ChromaDB failed: {e}")
        return None, None

# Simple RAG function
def simple_rag_query(query, collection):
    """Simple RAG query using in-memory ChromaDB"""
    try:
        # Search for relevant documents
        results = collection.query(
            query_texts=[query],
            n_results=3
        )

        if results['documents'] and results['documents'][0]:
            context = " ".join(results['documents'][0])

            # Generate response with context
            import google.generativeai as genai
            api_key = get_config_value("GEMINI_API_KEY")
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')

            enhanced_prompt = f"""Context from knowledge base: {context}

Question: {query}

As KRAKEN, your AI coding assistant, provide a comprehensive response using the context above and your programming expertise. Be helpful, detailed, and practical:"""

            response = model.generate_content(enhanced_prompt)
            return response.text, True
        else:
            return None, False

    except Exception as e:
        st.sidebar.error(f"RAG query failed: {e}")
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
    st.sidebar.subheader("🔍 API Keys Status")

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
            st.sidebar.warning("⚠️ Tavily: Not found (optional)")
            tavily_ready = False
    except Exception as e:
        st.sidebar.warning(f"⚠️ Tavily: {e}")
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

# UPDATED safe_import_modules function (FIXES SQLITE ISSUE)
def safe_import_modules():
    """Safely import modules with detailed error reporting"""
    modules_status = {}

    # Try in-memory RAG instead of file-based RAG (SQLITE FIX)
    try:
        client, collection = create_memory_chroma()
        if client and collection:
            modules_status['rag_pipeline'] = True
            st.sidebar.success("✅ Memory RAG loaded")
            # Store in session state
            st.session_state.chroma_client = client
            st.session_state.chroma_collection = collection
        else:
            modules_status['rag_pipeline'] = False
            st.sidebar.warning("⚠️ Memory RAG failed, using direct AI")

    except Exception as e:
        modules_status['rag_pipeline'] = False
        st.sidebar.error(f"❌ RAG System: {e}")

    # Keep handlers as they are (optional)
    try:
        from input_handler import InputHandler
        from output_handler import OutputHandler
        modules_status['handlers'] = True
        st.sidebar.success("✅ Handlers loaded")
    except Exception as e:
        modules_status['handlers'] = False
        st.sidebar.warning(f"⚠️ Handlers: {e} (using built-in handlers)")

    return modules_status

# Import modules
modules_status = safe_import_modules()
pipeline_ready = modules_status.get('rag_pipeline', False)
handlers_ready = modules_status.get('handlers', False)

# Session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Determine system readiness
system_ready = pipeline_ready and gemini_ready

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
if system_ready and 'chroma_collection' in st.session_state:
    st.success("🚀 KRAKEN System is fully operational with Memory RAG!")
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
            You can also upload documents (PDF, DOCX, TXT, and more) for analysis.
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

    # UPDATED Generate response (SQLITE FIX APPLIED)
    with st.chat_message("assistant"):
        typing_placeholder = st.empty()
        typing_placeholder.markdown('<p class="typing-indicator">🐙 KRAKEN is thinking...</p>', unsafe_allow_html=True)

        # Try memory-based RAG first (SQLITE SOLUTION)
        if system_ready and 'chroma_collection' in st.session_state:
            try:
                rag_response, success = simple_rag_query(prompt, st.session_state.chroma_collection)
                typing_placeholder.empty()

                if success and rag_response:
                    response = rag_response
                    st.sidebar.info("🧠 Used Memory RAG")
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
            prompt_lower = prompt.lower()

            if any(word in prompt_lower for word in ["hello", "hi", "hey"]):
                response = "👋 Hello! I'm KRAKEN, but I need API configuration to provide full AI responses. Please check the sidebar for status."

            elif "help" in prompt_lower:
                response = """I can assist you with:

🐍 **Python Programming** - Write, debug, and optimize code
🔧 **Problem Solving** - Algorithm design and implementation
📚 **Code Explanation** - Understand complex programming concepts
🐛 **Debugging** - Find and fix errors in your code

⚠️ Note: I need API keys configured to provide full AI responses."""

            else:
                response = f"I understand you're asking about: \"{prompt}\"\n\n⚠️ I need API configuration to provide intelligent responses. Please check the sidebar for status and ensure your API keys are properly set up."

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
