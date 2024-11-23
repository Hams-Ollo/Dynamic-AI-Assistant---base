"""
Agent System Package
------------------

This package provides the foundation for building intelligent chatbot agents.
It includes both base classes for extension and specialized implementations
for common use cases.

Package Structure:
    - base/: Abstract base classes and interfaces for building agents
    - specialized/: Ready-to-use agent implementations for specific use cases

Quick Start:
    from app.agents.base import BaseAgent
    from app.agents.specialized import CustomerSupportAgent

    # Create a custom agent
    class MyAgent(BaseAgent):
        async def process_message(self, message: str) -> str:
            # Add your custom logic here
            return f"Processed: {message}"

    # Or use a specialized agent
    support_agent = CustomerSupportAgent(config)
    response = await support_agent.process_message("Need help!")

Key Features:
    - Modular agent architecture
    - Easy-to-extend base classes
    - Built-in state management
    - Memory system integration
    - Async/await support
    - Type hints throughout
"""

# Version of the agents package
__version__ = "1.0.0"

# List of public classes/functions for better IDE support
__all__ = [
    'BaseAgent',
    'ChatAgent',
]