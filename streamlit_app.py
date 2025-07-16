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
#     bottom: 20px; /* Moved up for visibility */
#     right: 20px; /* Adjusted for better placement */
#     z-index: 999;
#     background: #00d4aa;
#     width: 40px;
#     height: 40px;
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

# # File upload in chat input area with attach symbol
# st.button("📎", key="attach_button", help="Upload files", on_click=lambda: st.session_state.update({"uploaded_files": st.file_uploader(
#     "Choose files to upload",
#     accept_multiple_files=True,
#     type=['py', 'js', 'java', 'cpp', 'c', 'txt', 'md', 'json', 'html', 'css', 'sql', 'r', 'php', 'go', 'rs', 'kt', 'swift', 'pdf', 'docx'],
#     key="dynamic_uploader"
# )}))

# if "uploaded_files" in st.session_state and st.session_state.uploaded_files:
#     st.success(f"✅ {len(st.session_state.uploaded_files)} file(s) uploaded!")
#     for file in st.session_state.uploaded_files:
#         file_size = f"{file.size / 1024:.1f} KB" if file.size < 1024*1024 else f"{file.size / (1024*1024):.1f} MB"
#         st.markdown(f"📄 **{file.name}** ({file_size})")

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

# # Working New Chat Button with plus symbol
# if st.session_state.messages:
#     # Create an invisible Streamlit button
#     if st.button("New Chat", key="invisible_new_chat", help="Start a new conversation",
#                  type="primary", use_container_width=False):
#         clear_chat()

#     # JavaScript to make the floating button work with plus symbol
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

# Enhanced imports with better error handling
def safe_import_modules():
    """Safely import modules with detailed error reporting"""
    modules_status = {}

    try:
        from rag_pipeline import RAGPipeline
        modules_status['rag_pipeline'] = True
        st.sidebar.success("✅ RAG Pipeline loaded")
    except ImportError as e:
        modules_status['rag_pipeline'] = False
        st.sidebar.error(f"❌ RAG Pipeline: {e}")
    except Exception as e:
        modules_status['rag_pipeline'] = False
        st.sidebar.error(f"❌ RAG Pipeline: Unexpected error - {e}")

    try:
        from input_handler import InputHandler
        from output_handler import OutputHandler
        modules_status['handlers'] = True
        st.sidebar.success("✅ Handlers loaded")
    except ImportError as e:
        modules_status['handlers'] = False
        st.sidebar.error(f"❌ Handlers: {e}")
    except Exception as e:
        modules_status['handlers'] = False
        st.sidebar.error(f"❌ Handlers: Unexpected error - {e}")

    return modules_status

# Import modules
modules_status = safe_import_modules()
pipeline_ready = modules_status.get('rag_pipeline', False)
handlers_ready = modules_status.get('handlers', False)

# Session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Initialize pipeline with better error handling
if 'pipeline' not in st.session_state and pipeline_ready and gemini_ready:
    try:
        # Import here to avoid early import issues
        from rag_pipeline import RAGPipeline
        st.session_state.pipeline = RAGPipeline(enable_monitoring=True)
        system_ready = True
        st.sidebar.success("✅ KRAKEN System Ready!")
    except Exception as e:
        system_ready = False
        st.sidebar.error(f"❌ Pipeline init failed: {e}")
else:
    system_ready = pipeline_ready and gemini_ready

# Function to clear chat
def clear_chat():
    st.session_state.messages = []
    st.rerun()

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

        response = model.generate_content(f"As a coding assistant named KRAKEN, respond to: {prompt}")
        return response.text, None

    except Exception as e:
        return None, str(e)

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
if system_ready:
    st.success("🚀 KRAKEN System is fully operational!")
elif gemini_ready:
    st.warning("⚡ KRAKEN is running in basic mode (Direct AI without RAG)")
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

    # Generate response
    with st.chat_message("assistant"):
        typing_placeholder = st.empty()
        typing_placeholder.markdown('<p class="typing-indicator">🐙 KRAKEN is thinking...</p>', unsafe_allow_html=True)

        if system_ready and 'pipeline' in st.session_state:
            # Full RAG system response
            try:
                result = st.session_state.pipeline.process_query_with_handlers(
                    prompt,
                    f"user_{int(time.time())}",
                    output_method="streamlit"
                )
                typing_placeholder.empty()

                if result.get("success"):
                    response = result["response"]
                else:
                    response = "I'm having trouble with the RAG system. Let me try direct AI response..."
                    # Fallback to direct AI
                    ai_response, error = test_ai_response(prompt)
                    if ai_response:
                        response = ai_response
                    else:
                        response = f"I encountered an issue: {error}"

            except Exception as e:
                typing_placeholder.empty()
                st.error(f"RAG Pipeline error: {e}")
                # Try direct AI as fallback
                ai_response, error = test_ai_response(prompt)
                if ai_response:
                    response = ai_response
                else:
                    response = "I'm having technical difficulties. Please try again."

        elif gemini_ready:
            # Direct AI response (no RAG)
            ai_response, error = test_ai_response(prompt)
            typing_placeholder.empty()

            if ai_response:
                response = ai_response
            else:
                response = f"AI Error: {error}"

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
