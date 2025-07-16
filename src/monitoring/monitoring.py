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
import json
import os
import sys
from datetime import datetime, UTC, timedelta
from typing import Dict, Optional, List, Any
from collections import defaultdict, deque
import threading

# Add path for potential imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Monitoring:
    """
    Advanced monitoring system for RAG pipeline with comprehensive metrics tracking.
    Updated: 2025-07-15 07:52:29 UTC
    User: TIRUMALA MANAV
    """

    def __init__(self, save_to_file: bool = True, max_history: int = 1000):
        """Initialize monitoring system with configurable options."""
        self.current_user = "TIRUMALA MANAV"
        self.initialization_time = datetime.now(UTC)
        self.save_to_file = save_to_file
        self.max_history = max_history

        # Core metrics
        self.metrics = {
            "total_queries": 0,
            "successful_queries": 0,
            "failed_queries": 0,
            "avg_response_time": 0.0,
            "total_response_time": 0.0,
            "min_response_time": float('inf'),
            "max_response_time": 0.0,
            "api_calls": defaultdict(int),
            "query_types": defaultdict(int),
            "error_types": defaultdict(int),
            "context_sources_used": defaultdict(int)
        }

        # Historical data for trend analysis
        self.query_history = deque(maxlen=max_history)
        self.response_times = deque(maxlen=max_history)
        self.hourly_stats = defaultdict(lambda: {"queries": 0, "success": 0, "fail": 0})

        # Health monitoring
        self.health_thresholds = {
            "min_success_rate": 0.70,  # 70%
            "max_avg_response_time": 15.0,  # 15 seconds
            "max_consecutive_failures": 5,
            "max_api_errors": 10
        }

        self.consecutive_failures = 0
        self.api_errors = defaultdict(int)
        self.alerts_sent = []

        # Performance tracking
        self.performance_trends = {
            "response_time_trend": [],  # Last 10 averages
            "success_rate_trend": [],   # Last 10 success rates
            "api_usage_trend": defaultdict(list)
        }

        # Thread safety
        self._lock = threading.Lock()

        logger.info(f"Monitoring system initialized for user {self.current_user} at {self.initialization_time}")

    def update_metrics(self, response_data: Dict) -> None:
        """Enhanced metrics update with comprehensive data collection."""
        with self._lock:
            try:
                timestamp = datetime.now(UTC)

                # Basic counters
                self.metrics["total_queries"] += 1
                success = response_data.get("success", False)

                if success:
                    self.metrics["successful_queries"] += 1
                    self.consecutive_failures = 0
                else:
                    self.metrics["failed_queries"] += 1
                    self.consecutive_failures += 1

                    # Track error types
                    error_type = self._categorize_error(response_data.get("error", "Unknown"))
                    self.metrics["error_types"][error_type] += 1

                # Processing time analysis
                processing_time = self._extract_processing_time(response_data)
                if processing_time > 0:
                    self.metrics["total_response_time"] += processing_time
                    self.metrics["avg_response_time"] = self.metrics["total_response_time"] / self.metrics["total_queries"]
                    self.metrics["min_response_time"] = min(self.metrics["min_response_time"], processing_time)
                    self.metrics["max_response_time"] = max(self.metrics["max_response_time"], processing_time)
                    self.response_times.append(processing_time)

                # API usage tracking
                self._track_api_usage(response_data)

                # Query type tracking
                query_type = response_data.get("metadata", {}).get("query_type", "unknown")
                self.metrics["query_types"][query_type] += 1

                # Context sources tracking
                context_sources = response_data.get("metadata", {}).get("context_sources", [])
                for source in context_sources:
                    self.metrics["context_sources_used"][source] += 1

                # Store historical data
                query_record = {
                    "timestamp": timestamp.isoformat(),
                    "success": success,
                    "processing_time": processing_time,
                    "query_type": query_type,
                    "context_sources": context_sources,
                    "error": response_data.get("error") if not success else None
                }
                self.query_history.append(query_record)

                # Update hourly statistics
                hour_key = timestamp.strftime("%Y-%m-%d_%H")
                self.hourly_stats[hour_key]["queries"] += 1
                if success:
                    self.hourly_stats[hour_key]["success"] += 1
                else:
                    self.hourly_stats[hour_key]["fail"] += 1

                # Update performance trends
                self._update_performance_trends()

                # Save to file if enabled
                if self.save_to_file:
                    self._save_metrics_to_file()

                logger.debug(f"Metrics updated for query #{self.metrics['total_queries']}")

            except Exception as e:
                logger.error(f"Error updating metrics: {e}")

    def _extract_processing_time(self, response_data: Dict) -> float:
        """Extract processing time from response data."""
        try:
            metadata = response_data.get("metadata", {})

            # Try different possible time fields
            time_fields = ["processing_time", "total_processing_time", "response_time"]

            for field in time_fields:
                if field in metadata:
                    time_str = str(metadata[field])
                    # Remove 's' suffix if present
                    time_str = time_str.replace("s", "").strip()
                    return float(time_str)

            return 0.0
        except (ValueError, TypeError):
            return 0.0

    def _track_api_usage(self, response_data: Dict) -> None:
        """Track API usage from response data."""
        try:
            context_sources = response_data.get("metadata", {}).get("context_sources", [])

            for source in context_sources:
                if source == "web":
                    self.metrics["api_calls"]["tavily"] += 1
                elif source == "ai_fallback":
                    self.metrics["api_calls"]["gemini_fallback"] += 1
                elif source == "database":
                    self.metrics["api_calls"]["database"] += 1

            # Track general API usage
            if context_sources:
                self.metrics["api_calls"]["total"] += len(context_sources)

        except Exception as e:
            logger.warning(f"Error tracking API usage: {e}")

    def _categorize_error(self, error_message: str) -> str:
        """Categorize errors for better tracking."""
        error_lower = error_message.lower()

        if "timeout" in error_lower or "time" in error_lower:
            return "timeout"
        elif "api" in error_lower or "key" in error_lower:
            return "api_error"
        elif "agent" in error_lower:
            return "agent_error"
        elif "network" in error_lower or "connection" in error_lower:
            return "network_error"
        elif "validation" in error_lower or "input" in error_lower:
            return "input_error"
        else:
            return "other"

    def _update_performance_trends(self) -> None:
        """Update performance trend data for analysis."""
        try:
            # Update response time trend (last 10 queries average)
            if len(self.response_times) >= 10:
                recent_avg = sum(list(self.response_times)[-10:]) / 10
                self.performance_trends["response_time_trend"].append(recent_avg)
                if len(self.performance_trends["response_time_trend"]) > 50:
                    self.performance_trends["response_time_trend"].pop(0)

            # Update success rate trend
            if self.metrics["total_queries"] >= 10:
                recent_success_rate = self.metrics["successful_queries"] / self.metrics["total_queries"]
                self.performance_trends["success_rate_trend"].append(recent_success_rate)
                if len(self.performance_trends["success_rate_trend"]) > 50:
                    self.performance_trends["success_rate_trend"].pop(0)

        except Exception as e:
            logger.warning(f"Error updating performance trends: {e}")

    def log_status(self, detailed: bool = False) -> Dict[str, Any]:
        """Enhanced status logging with optional detailed information."""
        try:
            uptime = (datetime.now(UTC) - self.initialization_time).total_seconds()
            success_rate = (self.metrics["successful_queries"] / max(self.metrics["total_queries"], 1)) * 100

            # Basic status
            status_data = {
                "timestamp": datetime.now(UTC).isoformat(),
                "user": self.current_user,
                "uptime_seconds": uptime,
                "uptime_formatted": str(timedelta(seconds=int(uptime))),
                "total_queries": self.metrics["total_queries"],
                "success_rate": success_rate,
                "avg_response_time": self.metrics["avg_response_time"],
                "consecutive_failures": self.consecutive_failures,
                "api_calls": dict(self.metrics["api_calls"])
            }

            if detailed:
                # Add detailed metrics
                status_data.update({
                    "response_time_stats": {
                        "min": self.metrics["min_response_time"] if self.metrics["min_response_time"] != float('inf') else 0,
                        "max": self.metrics["max_response_time"],
                        "avg": self.metrics["avg_response_time"]
                    },
                    "query_types": dict(self.metrics["query_types"]),
                    "error_types": dict(self.metrics["error_types"]),
                    "context_sources": dict(self.metrics["context_sources_used"]),
                    "recent_queries": list(self.query_history)[-10:] if self.query_history else []
                })

            # Log formatted status
            status_text = self._format_status_message(status_data)
            logger.info(status_text)

            return status_data

        except Exception as e:
            logger.error(f"Error logging status: {e}")
            return {"error": str(e)}

    def _format_status_message(self, status_data: Dict) -> str:
        """Format status data into readable message."""
        try:
            message = f"""
📊 **Monitoring Status for {self.current_user}**
📅 Timestamp: {status_data['timestamp']}
⏰ Uptime: {status_data['uptime_formatted']}
🔢 Total Queries: {status_data['total_queries']}
✅ Success Rate: {status_data['success_rate']:.1f}%
⏱️ Avg Response Time: {status_data['avg_response_time']:.2f}s
🔄 Consecutive Failures: {status_data['consecutive_failures']}
🌐 API Calls: {', '.join([f'{k}={v}' for k, v in status_data['api_calls'].items()])}
"""
            return message.strip()

        except Exception as e:
            return f"Error formatting status: {e}"

    def check_health(self, detailed: bool = True) -> Dict[str, Any]:
        """Comprehensive health check with detailed diagnostics."""
        try:
            health_status = {
                "overall_healthy": True,
                "timestamp": datetime.now(UTC).isoformat(),
                "issues": [],
                "warnings": [],
                "recommendations": []
            }

            # Success rate check
            if self.metrics["total_queries"] > 0:
                success_rate = self.metrics["successful_queries"] / self.metrics["total_queries"]
                if success_rate < self.health_thresholds["min_success_rate"]:
                    health_status["overall_healthy"] = False
                    health_status["issues"].append(
                        f"Success rate {success_rate:.1%} below threshold {self.health_thresholds['min_success_rate']:.1%}"
                    )
                elif success_rate < 0.85:  # Warning threshold
                    health_status["warnings"].append(
                        f"Success rate {success_rate:.1%} is concerning (below 85%)"
                    )

            # Response time check
            if self.metrics["avg_response_time"] > self.health_thresholds["max_avg_response_time"]:
                health_status["overall_healthy"] = False
                health_status["issues"].append(
                    f"Avg response time {self.metrics['avg_response_time']:.2f}s exceeds {self.health_thresholds['max_avg_response_time']}s"
                )
            elif self.metrics["avg_response_time"] > 10.0:  # Warning threshold
                health_status["warnings"].append(
                    f"Avg response time {self.metrics['avg_response_time']:.2f}s is slow (above 10s)"
                )

            # Consecutive failures check
            if self.consecutive_failures >= self.health_thresholds["max_consecutive_failures"]:
                health_status["overall_healthy"] = False
                health_status["issues"].append(
                    f"Too many consecutive failures: {self.consecutive_failures}"
                )

            # API error rate check
            total_api_calls = self.metrics["api_calls"].get("total", 0)
            if total_api_calls > 0:
                error_rate = sum(self.api_errors.values()) / total_api_calls
                if error_rate > 0.3:  # 30% error rate
                    health_status["overall_healthy"] = False
                    health_status["issues"].append(f"High API error rate: {error_rate:.1%}")

            # Add recommendations
            if self.metrics["total_queries"] > 0:
                if self.metrics["query_types"].get("unknown", 0) / self.metrics["total_queries"] > 0.2:
                    health_status["recommendations"].append("Consider improving query type detection")

                if not self.metrics["context_sources_used"]:
                    health_status["recommendations"].append("No context sources being used - check search functionality")

            # Log health status
            status_icon = "✅" if health_status["overall_healthy"] else "❌"
            logger.info(f"{status_icon} Health check completed - Healthy: {health_status['overall_healthy']}")

            if health_status["issues"]:
                for issue in health_status["issues"]:
                    logger.warning(f"🚨 Health Issue: {issue}")

            if health_status["warnings"]:
                for warning in health_status["warnings"]:
                    logger.warning(f"⚠️ Health Warning: {warning}")

            return health_status

        except Exception as e:
            logger.error(f"Error during health check: {e}")
            return {"overall_healthy": False, "error": str(e)}

    def get_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report."""
        try:
            report = {
                "generation_time": datetime.now(UTC).isoformat(),
                "monitoring_period": {
                    "start": self.initialization_time.isoformat(),
                    "duration_hours": (datetime.now(UTC) - self.initialization_time).total_seconds() / 3600
                },
                "query_statistics": dict(self.metrics),
                "performance_trends": dict(self.performance_trends),
                "hourly_breakdown": dict(self.hourly_stats),
                "top_error_types": dict(sorted(self.metrics["error_types"].items(), key=lambda x: x[1], reverse=True)[:5]),
                "query_type_distribution": dict(self.metrics["query_types"]),
                "recommendations": self._generate_recommendations()
            }

            logger.info("Performance report generated successfully")
            return report

        except Exception as e:
            logger.error(f"Error generating performance report: {e}")
            return {"error": str(e)}

    def _generate_recommendations(self) -> List[str]:
        """Generate performance optimization recommendations."""
        recommendations = []

        try:
            # Response time recommendations
            if self.metrics["avg_response_time"] > 10:
                recommendations.append("Consider optimizing response times - current average is above 10 seconds")

            # API usage recommendations
            total_queries = self.metrics["total_queries"]
            if total_queries > 0:
                api_ratio = self.metrics["api_calls"].get("total", 0) / total_queries
                if api_ratio > 2:
                    recommendations.append("High API usage per query - consider caching or optimization")

            # Error rate recommendations
            if self.metrics["failed_queries"] / max(total_queries, 1) > 0.2:
                recommendations.append("High failure rate - investigate error patterns and improve error handling")

            # Context source recommendations
            if not self.metrics["context_sources_used"]:
                recommendations.append("No context sources being utilized - verify search and database connectivity")

            return recommendations

        except Exception as e:
            logger.warning(f"Error generating recommendations: {e}")
            return ["Error generating recommendations"]

    def _save_metrics_to_file(self) -> None:
        """Save current metrics to file for persistence."""
        try:
            if not self.save_to_file:
                return

            # Create monitoring directory if it doesn't exist
            monitoring_dir = os.path.dirname(__file__)
            if not monitoring_dir:
                monitoring_dir = "."

            # Save main metrics
            metrics_file = os.path.join(monitoring_dir, f"metrics_{self.current_user}.json")
            with open(metrics_file, 'w') as f:
                save_data = {
                    "timestamp": datetime.now(UTC).isoformat(),
                    "metrics": dict(self.metrics),
                    "hourly_stats": dict(self.hourly_stats),
                    "initialization_time": self.initialization_time.isoformat()
                }
                # Convert defaultdict to regular dict for JSON serialization
                for key, value in save_data["metrics"].items():
                    if isinstance(value, defaultdict):
                        save_data["metrics"][key] = dict(value)

                json.dump(save_data, f, indent=2, default=str)

        except Exception as e:
            logger.warning(f"Failed to save metrics to file: {e}")

    def reset_metrics(self) -> None:
        """Reset all monitoring metrics with backup option."""
        try:
            # Backup current metrics before reset
            if self.save_to_file:
                backup_file = os.path.join(
                    os.path.dirname(__file__) or ".",
                    f"metrics_backup_{self.current_user}_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}.json"
                )

                try:
                    with open(backup_file, 'w') as f:
                        backup_data = {
                            "reset_timestamp": datetime.now(UTC).isoformat(),
                            "final_metrics": dict(self.metrics),
                            "query_history": list(self.query_history),
                            "hourly_stats": dict(self.hourly_stats)
                        }
                        json.dump(backup_data, f, indent=2, default=str)
                    logger.info(f"Metrics backed up to {backup_file}")
                except Exception as e:
                    logger.warning(f"Failed to backup metrics: {e}")

            # Reset all metrics
            self.metrics = {
                "total_queries": 0,
                "successful_queries": 0,
                "failed_queries": 0,
                "avg_response_time": 0.0,
                "total_response_time": 0.0,
                "min_response_time": float('inf'),
                "max_response_time": 0.0,
                "api_calls": defaultdict(int),
                "query_types": defaultdict(int),
                "error_types": defaultdict(int),
                "context_sources_used": defaultdict(int)
            }

            self.query_history.clear()
            self.response_times.clear()
            self.hourly_stats.clear()
            self.consecutive_failures = 0
            self.api_errors.clear()
            self.alerts_sent.clear()

            # Reset performance trends
            self.performance_trends = {
                "response_time_trend": [],
                "success_rate_trend": [],
                "api_usage_trend": defaultdict(list)
            }

            self.initialization_time = datetime.now(UTC)
            logger.info("✅ All metrics reset successfully")

        except Exception as e:
            logger.error(f"Error resetting metrics: {e}")

    def export_data(self, format_type: str = "json") -> Optional[str]:
        """Export monitoring data to specified format."""
        try:
            timestamp = datetime.now(UTC).strftime('%Y%m%d_%H%M%S')

            if format_type.lower() == "json":
                filename = f"monitoring_export_{self.current_user}_{timestamp}.json"
                export_data = {
                    "export_timestamp": datetime.now(UTC).isoformat(),
                    "user": self.current_user,
                    "metrics": dict(self.metrics),
                    "query_history": list(self.query_history),
                    "hourly_stats": dict(self.hourly_stats),
                    "performance_trends": dict(self.performance_trends),
                    "health_thresholds": self.health_thresholds
                }

                with open(filename, 'w') as f:
                    json.dump(export_data, f, indent=2, default=str)

                logger.info(f"Data exported to {filename}")
                return filename

            else:
                logger.error(f"Unsupported export format: {format_type}")
                return None

        except Exception as e:
            logger.error(f"Error exporting data: {e}")
            return None

def run_monitoring_tests():
    """Comprehensive test suite for monitoring system."""
    print(f"🧪 Monitoring System Test Suite - {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print(f"👤 User: TIRUMALA MANAV\n")

    try:
        # Initialize monitoring
        print("🔧 Initializing Monitoring System...")
        monitor = Monitoring(save_to_file=False)  # Disable file saving for tests

        # Test data - simulating various scenarios
        test_responses = [
            {
                "success": True,
                "metadata": {
                    "processing_time": "2.5s",
                    "context_sources": ["web"],
                    "query_type": "implementation"
                }
            },
            {
                "success": False,
                "error": "API timeout occurred",
                "metadata": {
                    "processing_time": "15.0s",
                    "context_sources": [],
                    "query_type": "debugging"
                }
            },
            {
                "success": True,
                "metadata": {
                    "processing_time": "3.2s",
                    "context_sources": ["web", "database"],
                    "query_type": "explanation"
                }
            },
            {
                "success": True,
                "metadata": {
                    "processing_time": "1.8s",
                    "context_sources": ["database"],
                    "query_type": "comparison"
                }
            },
            {
                "success": False,
                "error": "Agent processing failed",
                "metadata": {
                    "processing_time": "0.5s",
                    "context_sources": [],
                    "query_type": "general"
                }
            }
        ]

        print("📊 Processing test queries...")
        for i, response in enumerate(test_responses, 1):
            print(f"  Processing query {i}/5...")
            monitor.update_metrics(response)

        # Test status logging
        print("\n📋 Current Status:")
        status = monitor.log_status(detailed=True)

        # Test health check
        print("\n🏥 Health Check:")
        health = monitor.check_health()
        print(f"  Overall Health: {'✅ Healthy' if health['overall_healthy'] else '❌ Unhealthy'}")

        if health['issues']:
            print("  Issues found:")
            for issue in health['issues']:
                print(f"    - {issue}")

        if health['warnings']:
            print("  Warnings:")
            for warning in health['warnings']:
                print(f"    - {warning}")

        # Test performance report
        print("\n📈 Performance Report:")
        report = monitor.get_performance_report()
        print(f"  Monitoring Duration: {report['monitoring_period']['duration_hours']:.2f} hours")
        print(f"  Query Types: {report['query_type_distribution']}")
        print(f"  Top Error Types: {report['top_error_types']}")

        # Test export
        print("\n💾 Testing Data Export...")
        export_file = monitor.export_data()
        if export_file:
            print(f"  ✅ Data exported to: {export_file}")
            # Clean up test file
            try:
                os.remove(export_file)
                print(f"  🗑️ Test export file cleaned up")
            except:
                pass

        # Test reset
        print("\n🔄 Testing Metrics Reset...")
        monitor.reset_metrics()
        final_status = monitor.log_status()
        print(f"  ✅ Metrics reset - Total queries now: {final_status['total_queries']}")

        print(f"\n✅ Monitoring system test completed successfully!")

    except Exception as e:
        print(f"❌ Monitoring test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_monitoring_tests()
