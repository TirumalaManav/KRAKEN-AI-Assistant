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
# from langchain import hub
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.agents import AgentExecutor, create_react_agent
# from langchain_core.tools import Tool

# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

# llm = ChatGoogleGenerativeAI(
#     model="gemini-1.5-flash",
#     google_api_key="AIzaSyC0Z8xe1G4m9z8j9hmPPnKeLyV8yuHX0x4"
# )

# def dummy_tool(input_text):
#     return f"Tool used with input: {input_text}"

# tools = [
#     Tool(
#         name="DummyTool",
#         func=dummy_tool,
#         description="A tool that echoes the input."
#     )
# ]

# # Use the official React prompt from LangChain hub
# prompt = hub.pull("hwchase17/react")

# agent = create_react_agent(llm, tools, prompt)
# executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

# logger.debug("Invoking with input: hi")
# response = executor.invoke({"input": "hi"})
# logger.debug("Response: %s", response)
# print(response)


# Test script
from agent_manager import AgentManager

# Initialize the agent
agent = AgentManager()

# Test simple query (without chat history)
result = agent.process_query_simple("Explain binary search algorithm")
print(result)

# Test with chat history
result = agent.process_query("How do I implement a binary tree in Python?", session_id="test_session")
print(result)
