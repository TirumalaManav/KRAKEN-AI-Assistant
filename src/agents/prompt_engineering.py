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
from typing import Dict, List
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain import hub

# Configure logging to DEBUG level
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PromptEngineer:
    def __init__(self):
        """Initialize prompt templates for modern chat interactions."""
        logger.debug("Initializing PromptEngineer")
        self.system_prompts = {
            "theory": """You are a knowledgeable coding instructor specializing in programming concepts and theory.

Your expertise includes:
- Programming fundamentals and best practices
- Code design patterns and architecture
- Latest coding trends and technologies
- Clear explanations with practical examples

Always provide:
- Clear, step-by-step explanations
- Code snippets with comments when helpful
- Real-world applications and use cases
- Best practices and common pitfalls to avoid

Context: {context}
""",
            "ds_problem": """You are a Data Structures and Algorithms expert helping solve coding problems.

Your approach:
1. Analyze the problem clearly
2. Explain the optimal solution approach
3. Provide clean, well-commented Python code
4. Analyze time and space complexity
5. Discuss alternative approaches if applicable

For DSA problems, always include:
- Problem breakdown and approach
- Step-by-step solution
- Optimized Python implementation
- Complexity analysis (Big O notation)
- Test cases and edge cases

Context: {context}
""",
            "comparison": """You are a technical consultant providing objective technology comparisons.

Your analysis includes:
- Key features and fundamental differences
- Performance characteristics and benchmarks
- Specific use cases and scenarios
- Pros and cons with real-world implications
- Recommendations based on requirements

Format your comparisons with:
- Clear feature comparison tables when appropriate
- Specific examples and use cases
- Performance metrics where relevant
- Decision-making guidelines

Context: {context}
""",
            "code_review": """You are a senior software developer conducting thorough code reviews.

Focus areas:
- Code quality and readability
- Performance optimizations
- Security considerations
- Best practices and design patterns
- Maintainability and scalability

Provide:
- Specific improvement suggestions
- Code examples for better implementations
- Explanation of why changes are recommended
- Priority levels for different improvements

Context: {context}
""",
            "debugging": """You are a debugging expert helping identify and resolve code issues.

Your debugging process:
1. Analyze the error/issue systematically
2. Identify the root cause
3. Provide step-by-step solution
4. Explain prevention strategies
5. Suggest debugging techniques

Always include:
- Clear error analysis
- Root cause identification
- Working code fixes with explanations
- Best practices to prevent similar issues
- Debugging tips and tools

Context: {context}
"""
        }

        self.chat_templates = {}
        self._initialize_chat_templates()
        logger.debug("Prompt templates initialized: %s", list(self.chat_templates.keys()))

    def _initialize_chat_templates(self):
        """Initialize ChatPromptTemplate objects for each category."""
        logger.debug("Initializing chat templates")
        for category, system_prompt in self.system_prompts.items():
            self.chat_templates[category] = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("human", "{query}")
            ])
            logger.debug("Initialized template for category: %s", category)

    def classify_query(self, query: str) -> str:
        """Classify the query type based on keywords and content."""
        query_lower = query.lower()
        logger.debug("Classifying query: %s", query_lower[:50])

        # Data structures and algorithms - Enhanced keywords
        ds_algo_keywords = {
            "array", "list", "tree", "binary tree", "bst", "graph", "linked list",
            "stack", "queue", "heap", "hash", "sort", "sorting", "search", "searching",
            "leetcode", "algorithm", "algorithms", "complexity", "big o", "time complexity",
            "space complexity", "dynamic programming", "dp", "recursion", "recursive",
            "iteration", "iterative", "dfs", "bfs", "traversal", "fibonacci", "palindrome",
            "two pointers", "sliding window", "backtracking", "greedy", "divide and conquer",
            "merge sort", "quick sort", "binary search", "linear search", "dijkstra",
            "floyd warshall", "topological sort", "union find", "disjoint set",
            "segment tree", "fenwick tree", "trie", "suffix", "lru cache", "lfu cache"
        }

        if any(kw in query_lower for kw in ds_algo_keywords):
            return "ds_problem"

        # Comparison queries
        comparison_keywords = {"vs", "versus", "compare", "comparison", "difference", "differences",
                             "better", "which is better", "pros and cons", "advantages", "disadvantages"}
        if any(kw in query_lower for kw in comparison_keywords):
            return "comparison"

        # Code review
        review_keywords = {"review", "improve", "optimize", "refactor", "best practice",
                          "best practices", "code quality", "clean code", "performance"}
        if any(kw in query_lower for kw in review_keywords):
            return "code_review"

        # Debugging
        debug_keywords = {"error", "bug", "debug", "debugging", "fix", "issue", "problem",
                         "exception", "traceback", "not working", "doesn't work", "fails",
                         "crash", "crashes", "syntax error", "runtime error", "logic error"}
        if any(kw in query_lower for kw in debug_keywords):
            return "debugging"

        # Default to theory for general programming questions
        return "theory"

    def generate_prompt(self, query: str, context: str = "", chat_history: List = None) -> Dict:
        """Generate a dynamic prompt based on query type and context."""
        try:
            query_type = self.classify_query(query)
            logger.debug("Query type classified: %s", query_type)

            # Get the appropriate template
            template = self.chat_templates.get(query_type, self.chat_templates["theory"])
            logger.debug("Using template: %s", query_type)

            # Format the prompt
            formatted_prompt = template.format(query=query, context=context or "No additional context provided.")
            logger.debug("Formatted prompt generated successfully")

            # Calculate confidence
            confidence = self.calibrate_confidence(context, query)

            # Check confidence threshold
            if confidence < 0.3:
                logger.warning(f"Low confidence ({confidence:.2f}) for query: {query}")

            logger.info(f"Generated {query_type} prompt for query: {query[:50]}...")
            return {
                "prompt": formatted_prompt,
                "query_type": query_type,
                "confidence": confidence,
                "template_used": query_type
            }

        except Exception as e:
            logger.error("Prompt generation failed: %s", str(e))
            return {
                "prompt": f"Error generating prompt: {str(e)}",
                "query_type": "error",
                "confidence": 0.0,
                "template_used": "none"
            }

    def calibrate_confidence(self, context: str, query: str) -> float:
        """Calibrate confidence based on context quality and query complexity."""
        try:
            # Base confidence factors
            context_score = 0.0
            query_score = 0.0

            # Context quality assessment
            if context:
                context_words = len(context.split())
                context_score = min(1.0, context_words / 200)  # Normalize to 200 words

                # Bonus for code blocks
                if "```" in context:
                    context_score += 0.2

                # Bonus for structured content
                if any(marker in context for marker in ["##", "###", "1.", "2.", "3."]):
                    context_score += 0.1

            # Query complexity assessment
            query_words = len(query.split())
            if query_words > 10:
                query_score = 0.9
            elif query_words > 5:
                query_score = 0.8
            elif query_words > 2:
                query_score = 0.6
            else:
                query_score = 0.4

            # Technical keywords boost confidence
            technical_keywords = {
                "python", "javascript", "java", "c++", "c#", "go", "rust", "kotlin",
                "algorithm", "data structure", "machine learning", "ai", "api", "rest",
                "database", "sql", "nosql", "web", "mobile", "frontend", "backend",
                "framework", "library", "docker", "kubernetes", "aws", "cloud",
                "git", "github", "testing", "unit test", "integration", "deployment"
            }

            if any(kw in query.lower() for kw in technical_keywords):
                query_score += 0.2

            # Combine scores
            final_confidence = min(1.0, (context_score * 0.6) + (query_score * 0.4))

            logger.debug(f"Confidence calibrated: context={context_score:.2f}, query={query_score:.2f}, final={final_confidence:.2f}")
            return final_confidence

        except Exception as e:
            logger.error("Confidence calibration failed: %s", str(e))
            return 0.5  # Default fallback confidence

    def get_react_prompt(self):
        """Get the official React prompt for agent use."""
        try:
            return hub.pull("hwchase17/react")
        except Exception as e:
            logger.error(f"Failed to get React prompt from hub: {e}")
            # Fallback to a basic React prompt
            return ChatPromptTemplate.from_messages([
                SystemMessage(content="Answer the following questions as best you can. You have access to the following tools:\n\n{tools}\n\nUse the following format:\n\nQuestion: the input question you must answer\nThought: you should always think about what to do\nAction: the action to take, should be one of [{tool_names}]\nAction Input: the input to the action\nObservation: the result of the action\n... (this Thought/Action/Action Input/Observation can repeat N times)\nThought: I now know the final answer\nFinal Answer: the final answer to the original input question"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ])

    def get_template_by_type(self, template_type: str) -> ChatPromptTemplate:
        """Get a specific template by type."""
        logger.debug("Retrieving template for type: %s", template_type)
        if template_type == "react_agent":
            return self.get_react_prompt()
        return self.chat_templates.get(template_type, self.chat_templates["theory"])

    def list_available_templates(self) -> List[str]:
        """List all available template types."""
        logger.debug("Listing available templates")
        return list(self.chat_templates.keys()) + ["react_agent"]

    def create_custom_template(self, name: str, system_prompt: str) -> bool:
        """Create a custom template."""
        try:
            self.system_prompts[name] = system_prompt
            self.chat_templates[name] = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("human", "{query}")
            ])
            logger.info(f"Created custom template: {name}")
            return True
        except Exception as e:
            logger.error(f"Failed to create custom template {name}: {str(e)}")
            return False
