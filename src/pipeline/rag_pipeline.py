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

import sys
import os
import logging
from typing import Dict, Optional, List, Any
from datetime import datetime, UTC

# Add paths for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'agents'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'handlers'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'monitoring'))

# Import from agents folder
try:
    from agent_manager import AgentManager
    from tools import get_tools
    from chromadb import Client
    from chromadb.config import Settings
    from langchain_core.messages import BaseMessage
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Make sure you're running from the pipeline folder and agents folder exists")
    sys.exit(1)

# Import from current folder
from api_client import APIClient

# Import handlers
try:
    from input_handler import InputHandler
    from output_handler import OutputHandler
except ImportError as e:
    print(f"⚠️ Handler Import Warning: {e}")
    print("Handlers not available - will use basic input/output processing")
    InputHandler = None
    OutputHandler = None

# Import monitoring
try:
    from monitoring import Monitoring
except ImportError as e:
    print(f"⚠️ Monitoring Import Warning: {e}")
    print("Monitoring not available - will proceed without monitoring")
    Monitoring = None

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RAGPipeline:
    """
    Enhanced RAG Pipeline with integrated monitoring, input/output handlers.
    Updated: 2025-07-15 07:52:29 UTC
    User: TIRUMALA MANAV
    """

    def __init__(self, db_path: str = r"D:\Code Explainer\src\embeddings\vector_db",
                 enable_monitoring: bool = True):
        """Initialize RAG pipeline with all necessary components including monitoring."""
        try:
            self.current_user = "TIRUMALA MANAV"
            self.initialization_time = datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S')

            logger.info(f"🚀 Initializing Enhanced RAG Pipeline for user {self.current_user} at {self.initialization_time} UTC...")

            # Initialize core components
            self.db_path = db_path
            self.client = Client(Settings(persist_directory=db_path))
            self.tools = get_tools(self.client)
            self.api_client = APIClient()
            self.agent_manager = AgentManager(db_path=db_path)

            # Initialize handlers if available
            self.input_handler = InputHandler() if InputHandler else None
            self.output_handler = OutputHandler() if OutputHandler else None

            # Initialize monitoring if available
            self.monitoring = Monitoring() if Monitoring and enable_monitoring else None
            self.enable_monitoring = bool(self.monitoring)

            # Pipeline configuration
            self.max_context_length = 4000
            self.enable_web_search = True
            self.enable_database_search = True
            self.context_enhancement = True
            self.use_handlers = bool(self.input_handler and self.output_handler)

            # Performance tracking (basic - monitoring provides advanced)
            self.query_count = 0
            self.successful_queries = 0
            self.failed_queries = 0

            # Validate initialization
            self._validate_components()

            logger.info("✅ Enhanced RAG Pipeline initialized successfully")
            logger.info(f"🎛️ Handlers enabled: {self.use_handlers}")
            logger.info(f"📊 Monitoring enabled: {self.enable_monitoring}")

            # Log API status for debugging
            api_status = self.api_client.validate_api_keys()
            logger.info(f"📊 API Status: {api_status}")

        except Exception as e:
            logger.error(f"❌ RAG Pipeline initialization failed: {e}")
            raise

    def _validate_components(self):
        """Validate that all components are properly initialized."""
        validations = {
            "database_client": bool(self.client),
            "tools_available": len(self.tools) > 0,
            "api_client": bool(self.api_client),
            "agent_manager": bool(self.agent_manager),
            "database_path_exists": os.path.exists(self.db_path),
            "input_handler": bool(self.input_handler),
            "output_handler": bool(self.output_handler),
            "monitoring": bool(self.monitoring)
        }

        failed_validations = [k for k, v in validations.items() if not v]

        if failed_validations:
            logger.warning(f"⚠️ Some components failed validation: {failed_validations}")
        else:
            logger.info("✅ All components validated successfully")

        return validations

    def retrieve_context(self, query: str, session_id: str = "default") -> Dict[str, Any]:
        """
        Retrieve context from multiple sources with enhanced error handling.
        Returns detailed context information including source metadata.
        """
        context_data = {
            "database_results": None,
            "web_results": None,
            "combined_context": "",
            "sources_used": [],
            "retrieval_time": 0,
            "success": False
        }

        retrieval_start = datetime.now(UTC)

        try:
            logger.debug(f"🔍 Starting context retrieval for query: {query[:50]}...")

            # Database Search
            if self.enable_database_search:
                context_data["database_results"] = self._search_database(query)
                if context_data["database_results"]:
                    context_data["sources_used"].append("database")
                    logger.info("✅ Database search successful")
                else:
                    logger.info("ℹ️ Database search returned no results")

            # Web Search
            if self.enable_web_search:
                context_data["web_results"] = self._search_web(query)
                if context_data["web_results"]:
                    context_data["sources_used"].append("web")
                    logger.info("✅ Web search successful")
                else:
                    logger.info("ℹ️ Web search returned no results")

            # Combine contexts
            context_data["combined_context"] = self._combine_contexts(
                context_data["database_results"],
                context_data["web_results"]
            )

            # Calculate retrieval time
            context_data["retrieval_time"] = (datetime.now(UTC) - retrieval_start).total_seconds()
            context_data["success"] = bool(context_data["combined_context"])

            logger.info(f"📊 Context retrieval completed in {context_data['retrieval_time']:.2f}s")
            logger.info(f"📚 Sources used: {', '.join(context_data['sources_used']) or 'none'}")

            return context_data

        except Exception as e:
            logger.error(f"❌ Context retrieval failed: {e}")
            context_data["retrieval_time"] = (datetime.now(UTC) - retrieval_start).total_seconds()
            context_data["error"] = str(e)
            return context_data

    def _search_database(self, query: str) -> Optional[str]:
        """Search database using available tools."""
        try:
            for tool in self.tools:
                if tool.name == "DatabaseSearch":
                    result = tool.func(query)
                    if result and "No coding knowledge collections found" not in result:
                        return f"**📚 Database Knowledge:**\n{result}"
                    break
            return None
        except Exception as e:
            logger.warning(f"Database search error: {e}")
            return None

    def _search_web(self, query: str) -> Optional[str]:
        """Search web using API client with fallback options."""
        try:
            # Try Tavily first
            web_result = self.api_client.search_tavily(query)
            if web_result:
                return web_result

            # Try Gemini fallback
            logger.info("🔄 Trying Gemini fallback for web search...")
            gemini_result = self.api_client.search_gemini_fallback(query)
            if gemini_result:
                return gemini_result

            return None

        except Exception as e:
            logger.warning(f"Web search error: {e}")
            return None

    def _combine_contexts(self, db_context: Optional[str], web_context: Optional[str]) -> str:
        """Combine multiple context sources into a coherent context string."""
        context_parts = []

        if db_context:
            context_parts.append(db_context)

        if web_context:
            context_parts.append(web_context)

        if context_parts:
            combined = "\n\n".join(context_parts)

            # Truncate if too long
            if len(combined) > self.max_context_length:
                combined = combined[:self.max_context_length] + "\n\n[Context truncated due to length limits]"

            return combined

        return "No additional context found. Proceeding with general knowledge."

    def _enhance_query_with_context(self, query: str, context_data: Dict[str, Any]) -> str:
        """Create an enhanced query that includes retrieved context."""
        if not context_data["success"] or not context_data["combined_context"]:
            return query

        if not self.context_enhancement:
            return query

        enhanced_query = f"""
**User Query:** {query}

**Retrieved Context:**
{context_data["combined_context"]}

**Instructions:**
Please provide a comprehensive answer using the above context when relevant, and supplement with your knowledge.
Focus on accuracy, include code examples where appropriate, and explain concepts clearly.

**Context Sources:** {', '.join(context_data["sources_used"])}
**User:** {self.current_user}
**Timestamp:** {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S')} UTC
"""
        return enhanced_query

    def process_query_with_handlers(self, raw_input: str, session_id: str = "default",
                                  output_method: str = "console") -> Dict[str, Any]:
        """
        Process query using input/output handlers and monitoring for enhanced user experience.
        This is the MAIN method to use when handlers are available.
        """
        if not self.use_handlers:
            logger.warning("Handlers not available, falling back to basic processing")
            return self.process_query(raw_input, session_id)

        pipeline_start = datetime.now(UTC)

        try:
            logger.info(f"🎛️ Processing query with handlers: {raw_input[:50]}...")

            # Step 1: Process input using InputHandler
            processed_input = self.input_handler.process_input(raw_input, session_id)

            if not processed_input or not processed_input.get("success"):
                error_response = {
                    "success": False,
                    "response": "Invalid input provided. Please check your query and try again.",
                    "error": processed_input.get("error") if processed_input else "Input processing failed",
                    "metadata": {
                        "timestamp": datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC'),
                        "user": self.current_user,
                        "session_id": session_id,
                        "processing_time": f"{(datetime.now(UTC) - pipeline_start).total_seconds():.2f}s"
                    }
                }

                # Update monitoring
                if self.enable_monitoring:
                    self.monitoring.update_metrics(error_response)

                # Handle output
                self.output_handler.handle_output(error_response, output_method)
                return error_response

            # Step 2: Process query using RAG pipeline
            query = processed_input["query"]
            rag_response = self.process_query(query, session_id)

            # Step 3: Enhance response with input handler metadata
            if rag_response.get("success") and "metadata" in rag_response:
                rag_response["metadata"]["query_type"] = processed_input.get("query_type", "general")
                rag_response["metadata"]["input_processing"] = processed_input.get("metadata", {})
                rag_response["metadata"]["code_blocks_detected"] = len(processed_input.get("code_blocks", []))
                rag_response["metadata"]["input_validation"] = processed_input.get("validation", {})

            # Step 4: Calculate total processing time
            total_processing_time = (datetime.now(UTC) - pipeline_start).total_seconds()
            if "metadata" in rag_response:
                rag_response["metadata"]["total_processing_time"] = f"{total_processing_time:.2f}s"

            # Step 5: Update monitoring
            if self.enable_monitoring:
                self.monitoring.update_metrics(rag_response)

            # Step 6: Handle output using OutputHandler
            output_result = self.output_handler.handle_output(rag_response, output_method)

            # Step 7: Return combined result
            return {
                **rag_response,
                "output_handling": output_result,
                "handlers_used": True,
                "monitoring_enabled": self.enable_monitoring,
                "total_processing_time": f"{total_processing_time:.2f}s"
            }

        except Exception as e:
            logger.error(f"❌ Handler-based processing failed: {e}")
            error_response = {
                "success": False,
                "response": f"Pipeline processing failed: {str(e)}",
                "error": str(e),
                "metadata": {
                    "timestamp": datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC'),
                    "user": self.current_user,
                    "session_id": session_id,
                    "processing_time": f"{(datetime.now(UTC) - pipeline_start).total_seconds():.2f}s"
                }
            }

            # Update monitoring even for errors
            if self.enable_monitoring:
                self.monitoring.update_metrics(error_response)

            if self.output_handler:
                self.output_handler.handle_output(error_response, output_method)

            return error_response

    def process_query(self, query: str, session_id: str = "default") -> Dict[str, Any]:
        """
        Process query with full RAG pipeline including retrieval and generation.
        Maintains conversation history and provides detailed response metadata.
        """
        query_start_time = datetime.now(UTC)
        self.query_count += 1

        try:
            logger.info(f"🎯 Processing RAG query #{self.query_count}: {query[:50]}...")

            # Step 1: Retrieve context from multiple sources
            context_data = self.retrieve_context(query, session_id)

            # Step 2: Enhance query with retrieved context
            enhanced_query = self._enhance_query_with_context(query, context_data)

            # Step 3: Generate response using agent manager
            logger.debug("🤖 Generating response with agent manager...")
            agent_response = self.agent_manager.process_query(enhanced_query, session_id)

            # Step 4: Process and format final response
            if agent_response.get("success", False):
                processing_time = (datetime.now(UTC) - query_start_time).total_seconds()
                self.successful_queries += 1

                final_response = {
                    "response": agent_response["response"],
                    "original_query": query,
                    "enhanced_query": enhanced_query if enhanced_query != query else None,
                    "context_data": context_data,
                    "source": "rag_pipeline",
                    "session_id": session_id,
                    "success": True,
                    "metadata": {
                        "query_number": self.query_count,
                        "processing_time": f"{processing_time:.2f}s",
                        "context_sources": context_data["sources_used"],
                        "context_retrieval_time": f"{context_data['retrieval_time']:.2f}s",
                        "agent_response_metadata": agent_response,
                        "user": self.current_user,
                        "timestamp": datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC'),
                        "pipeline_stats": {
                            "total_queries": self.query_count,
                            "successful_queries": self.successful_queries,
                            "failed_queries": self.failed_queries
                        }
                    }
                }

                logger.info(f"✅ RAG query processed successfully in {processing_time:.2f}s")

                # Update monitoring if enabled (for direct process_query calls)
                if self.enable_monitoring:
                    self.monitoring.update_metrics(final_response)

                return final_response

            else:
                # Agent processing failed
                self.failed_queries += 1
                processing_time = (datetime.now(UTC) - query_start_time).total_seconds()

                logger.error(f"❌ Agent processing failed for query: {query[:50]}...")
                error_response = {
                    "response": f"I apologize, but I encountered an issue processing your request: {agent_response.get('response', 'Unknown agent error')}",
                    "original_query": query,
                    "context_data": context_data,
                    "source": "rag_pipeline_agent_error",
                    "session_id": session_id,
                    "success": False,
                    "error": agent_response.get("error"),
                    "metadata": {
                        "query_number": self.query_count,
                        "processing_time": f"{processing_time:.2f}s",
                        "user": self.current_user,
                        "timestamp": datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC')
                    }
                }

                # Update monitoring if enabled
                if self.enable_monitoring:
                    self.monitoring.update_metrics(error_response)

                return error_response

        except Exception as e:
            self.failed_queries += 1
            processing_time = (datetime.now(UTC) - query_start_time).total_seconds()

            logger.error(f"❌ RAG Pipeline processing failed: {e}")
            error_response = {
                "response": f"I apologize, but I encountered a technical error while processing your request. Please try again or rephrase your question. Error details: {str(e)}",
                "original_query": query,
                "source": "rag_pipeline_error",
                "session_id": session_id,
                "success": False,
                "error": str(e),
                "metadata": {
                    "query_number": self.query_count,
                    "processing_time": f"{processing_time:.2f}s",
                    "user": self.current_user,
                    "timestamp": datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC')
                }
            }

            # Update monitoring if enabled
            if self.enable_monitoring:
                self.monitoring.update_metrics(error_response)

            return error_response

    def get_monitoring_status(self) -> Dict[str, Any]:
        """Get comprehensive monitoring status if monitoring is enabled."""
        if not self.enable_monitoring:
            return {"monitoring_enabled": False, "message": "Monitoring is not enabled"}

        try:
            status = self.monitoring.log_status(detailed=True)
            health = self.monitoring.check_health()

            return {
                "monitoring_enabled": True,
                "status": status,
                "health": health,
                "timestamp": datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC')
            }
        except Exception as e:
            logger.error(f"Error getting monitoring status: {e}")
            return {"monitoring_enabled": True, "error": str(e)}

    def get_performance_report(self) -> Dict[str, Any]:
        """Get detailed performance report if monitoring is enabled."""
        if not self.enable_monitoring:
            return {"monitoring_enabled": False, "message": "Monitoring is not enabled"}

        try:
            return self.monitoring.get_performance_report()
        except Exception as e:
            logger.error(f"Error generating performance report: {e}")
            return {"error": str(e)}

    def get_pipeline_status(self) -> Dict[str, Any]:
        """Get comprehensive status of all pipeline components including monitoring."""
        try:
            # Get database info
            try:
                collections = self.client.list_collections()
                db_status = {
                    "path": self.db_path,
                    "collections_count": len(collections),
                    "collections_names": [c.name for c in collections] if collections else [],
                    "status": "✅ Connected"
                }
            except Exception as e:
                db_status = {
                    "path": self.db_path,
                    "status": f"❌ Error: {str(e)[:50]}..."
                }

            # Get tools info
            tools_status = {
                "count": len(self.tools),
                "names": [tool.name for tool in self.tools],
                "status": "✅ Available" if self.tools else "❌ No tools loaded"
            }

            # Get API status
            api_status = self.api_client.get_api_status()

            # Get agent info
            try:
                agent_info = self.agent_manager.get_agent_info()
            except Exception as e:
                agent_info = {"error": str(e)}

            # Get handler info
            handlers_status = {
                "input_handler": "✅ Available" if self.input_handler else "❌ Not available",
                "output_handler": "✅ Available" if self.output_handler else "❌ Not available",
                "handlers_enabled": self.use_handlers
            }

            # Add handler statistics if available
            if self.input_handler:
                handlers_status["input_stats"] = self.input_handler.get_input_statistics()
            if self.output_handler:
                handlers_status["output_stats"] = self.output_handler.get_output_statistics()

            # Get monitoring info
            monitoring_status = {
                "monitoring_enabled": self.enable_monitoring,
                "monitoring_available": bool(self.monitoring)
            }

            if self.enable_monitoring and self.monitoring:
                try:
                    monitoring_status["current_metrics"] = dict(self.monitoring.metrics)
                    monitoring_status["health"] = self.monitoring.check_health()
                except Exception as e:
                    monitoring_status["error"] = str(e)

            # Pipeline performance stats
            performance_stats = {
                "total_queries": self.query_count,
                "successful_queries": self.successful_queries,
                "failed_queries": self.failed_queries,
                "success_rate": f"{(self.successful_queries / max(self.query_count, 1)) * 100:.1f}%",
                "initialization_time": self.initialization_time
            }

            # Overall status
            working_components = sum([
                "✅" in db_status["status"],
                "✅" in tools_status["status"],
                "✅" in api_status.get("overall", ""),
                "error" not in agent_info,
                self.use_handlers,
                self.enable_monitoring
            ])

            overall_status = f"✅ {working_components}/6 components operational" if working_components > 0 else "❌ Pipeline not operational"

            return {
                "overall_status": overall_status,
                "timestamp": datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC'),
                "user": self.current_user,
                "database": db_status,
                "tools": tools_status,
                "api_client": api_status,
                "agent_manager": agent_info,
                "handlers": handlers_status,
                "monitoring": monitoring_status,
                "performance": performance_stats,
                "configuration": {
                    "max_context_length": self.max_context_length,
                    "web_search_enabled": self.enable_web_search,
                    "database_search_enabled": self.enable_database_search,
                    "context_enhancement_enabled": self.context_enhancement,
                    "handlers_enabled": self.use_handlers,
                    "monitoring_enabled": self.enable_monitoring
                }
            }

        except Exception as e:
            logger.error(f"Failed to get pipeline status: {e}")
            return {
                "overall_status": f"❌ Status check failed: {str(e)}",
                "error": str(e),
                "timestamp": datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC'),
                "user": self.current_user
            }

    # Keep all your existing methods...
    def process_simple_query(self, query: str) -> Dict[str, Any]:
        """Process query without session memory for testing purposes."""
        try:
            logger.info(f"🧪 Processing simple test query: {query[:50]}...")

            context_data = self.retrieve_context(query)
            enhanced_query = self._enhance_query_with_context(query, context_data)

            response = self.agent_manager.process_query_simple(enhanced_query)

            result = {
                "response": response["response"],
                "original_query": query,
                "context_used": context_data["combined_context"] if context_data["success"] else None,
                "source": "rag_pipeline_simple",
                "success": response.get("success", False),
                "metadata": {
                    "context_sources": context_data["sources_used"],
                    "context_retrieval_time": f"{context_data['retrieval_time']:.2f}s",
                    "user": self.current_user,
                    "timestamp": datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC')
                }
            }

            # Update monitoring for simple queries too
            if self.enable_monitoring:
                self.monitoring.update_metrics(result)

            return result

        except Exception as e:
            logger.error(f"❌ Simple RAG query failed: {e}")
            error_result = {
                "response": f"Test query failed: {str(e)}",
                "original_query": query,
                "source": "rag_pipeline_simple_error",
                "success": False,
                "error": str(e)
            }

            # Update monitoring for errors too
            if self.enable_monitoring:
                self.monitoring.update_metrics(error_result)

            return error_result

# Test function with monitoring
def run_comprehensive_test():
    """Run comprehensive test of the RAG pipeline with monitoring."""
    print(f"🧪 Enhanced RAG Pipeline Test Suite with Monitoring")
    print(f"📅 Date: {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print(f"👤 User: TIRUMALA MANAV\n")

    try:
        # Initialize pipeline
        print("🔧 Initializing Enhanced RAG Pipeline...")
        pipeline = RAGPipeline(enable_monitoring=True)

        # Check pipeline status
        print("\n📊 Pipeline Status Check:")
        status = pipeline.get_pipeline_status()
        print(f"  Overall Status: {status['overall_status']}")
        print(f"  Database: {status['database']['status']}")
        print(f"  Tools: {status['tools']['status']}")
        print(f"  API Client: {status['api_client']['overall']}")
        print(f"  Handlers: Input {status['handlers']['input_handler']}, Output {status['handlers']['output_handler']}")
        print(f"  Monitoring: {'✅ Enabled' if status['monitoring']['monitoring_enabled'] else '❌ Disabled'}")

        # Test with handlers and monitoring if available
        if pipeline.use_handlers and pipeline.enable_monitoring:
            print(f"\n🎛️ Testing with Input/Output Handlers and Monitoring...")

            test_queries = [
                "Explain merge sort algorithm with code examples",
                "Debug this error: IndexError list index out of range",
                "What's the difference between Python lists and arrays?"
            ]

            for i, query in enumerate(test_queries, 1):
                print(f"\n📝 Handler Test {i}: {query}")
                result = pipeline.process_query_with_handlers(query, f"handler_test_{i}")

                if result.get("success"):
                    print(f"  ✅ Success with handlers and monitoring")
                    print(f"  📊 Query type: {result['metadata'].get('query_type', 'unknown')}")
                    print(f"  ⏱️ Total time: {result.get('total_processing_time', 'N/A')}")
                else:
                    print(f"  ❌ Failed: {result.get('error', 'Unknown error')}")

            # Show monitoring report
            print(f"\n📈 Monitoring Report:")
            monitoring_status = pipeline.get_monitoring_status()
            if monitoring_status.get("monitoring_enabled"):
                status_data = monitoring_status.get("status", {})
                print(f"  Total Queries: {status_data.get('total_queries', 0)}")
                print(f"  Success Rate: {status_data.get('success_rate', 0):.1f}%")
                print(f"  Avg Response Time: {status_data.get('avg_response_time', 0):.2f}s")
                print(f"  API Calls: {status_data.get('api_calls', {})}")

                health = monitoring_status.get("health", {})
                print(f"  Health Status: {'✅ Healthy' if health.get('overall_healthy') else '❌ Issues detected'}")

        else:
            print(f"\n⚠️ Handlers or monitoring not available, testing basic functionality...")

            # Test basic functionality
            result = pipeline.process_simple_query("Explain binary search")
            success_icon = "✅" if result["success"] else "❌"
            print(f"  {success_icon} Basic test: {result['response'][:50]}...")

        print(f"\n✅ Enhanced RAG Pipeline test completed!")

    except Exception as e:
        print(f"❌ Enhanced RAG Pipeline test failed: {e}")
        import traceback
        traceback.print_exc()

# Main execution
if __name__ == "__main__":
    run_comprehensive_test()
