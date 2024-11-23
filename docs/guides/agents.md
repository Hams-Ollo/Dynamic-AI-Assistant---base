# Agent Development Guide

This guide explains how to create and customize agents using the Multi-Agent Chatbot Template.

## Overview

The template provides a flexible architecture for creating chatbot agents with:

- Document processing capabilities
- Memory management
- LLM integration
- Error handling
- Logging

## Base Agent Structure

The base agent provides core functionality that all agents inherit:

```python
from typing import Dict, Any, Optional
from app.utils.memory import MemoryManager

class BaseAgent:
    def __init__(self, api_key: str):
        """Initialize base agent.
        
        Args:
            api_key: API key for LLM service
        """
        self.api_key = api_key
        self.memory = MemoryManager({
            'type': 'buffer',
            'path': './data/memory'
        })
    
    def process_message(self, message: str) -> Dict[str, Any]:
        """Process a user message.
        
        Args:
            message: User's input message
            
        Returns:
            Dict containing response and any additional data
        """
        raise NotImplementedError
```

## Creating a Custom Agent

### 1. Basic Chat Agent

```python
from app.agents.base.base_agent import BaseAgent
from app.agents.document_processor import DocumentProcessor

class CustomChatAgent(BaseAgent):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.doc_processor = DocumentProcessor()
        
    def process_message(self, message: str) -> Dict[str, Any]:
        try:
            # Get relevant context
            context = self.memory.get_relevant_context(message)
            
            # Process response
            response = "Your custom response logic here"
            
            return {
                "response": response,
                "source_documents": []
            }
        except Exception as e:
            logging.error(f"Error processing message: {e}")
            return {
                "response": "Error processing your message",
                "error": str(e)
            }
```

### 2. Document-Aware Agent

```python
class DocumentAgent(BaseAgent):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.doc_processor = DocumentProcessor()
        
    def add_document(self, text: str) -> bool:
        """Add a document to the agent's knowledge."""
        try:
            docs = self.doc_processor.process_text(text)
            self.memory.add_documents(docs)
            return True
        except Exception as e:
            logging.error(f"Error adding document: {e}")
            return False
            
    def process_message(self, message: str) -> Dict[str, Any]:
        try:
            # Get relevant documents
            docs = self.memory.get_relevant_documents(message)
            
            # Build context from documents
            context = "\n".join(doc.page_content for doc in docs)
            
            # Process with context
            response = f"Processed message with context: {len(docs)} documents"
            
            return {
                "response": response,
                "source_documents": docs
            }
        except Exception as e:
            logging.error(f"Error in document agent: {e}")
            return {
                "response": "Error processing with documents",
                "error": str(e)
            }
```

## Advanced Features

### 1. Memory Management

```python
class MemoryAwareAgent(BaseAgent):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.memory = MemoryManager({
            'type': 'vector',
            'path': './data/memory',
            'cleanup_interval': 3600
        })
        
    def cleanup_old_conversations(self):
        """Remove old conversations."""
        self.memory.cleanup()
        
    def get_conversation_history(self) -> List[Dict]:
        """Get recent conversation history."""
        return self.memory.get_recent_messages(5)
```

### 2. Custom LLM Integration

```python
from app.core.llm import CustomLLMProvider

class CustomLLMAgent(BaseAgent):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.llm = CustomLLMProvider(api_key)
        
    async def generate_response(self, prompt: str) -> str:
        """Generate response using custom LLM."""
        try:
            response = await self.llm.generate(prompt)
            return response
        except Exception as e:
            logging.error(f"LLM error: {e}")
            raise
```

### 3. Streaming Responses

```python
class StreamingAgent(BaseAgent):
    async def process_message_stream(self, message: str):
        """Process message with streaming response."""
        try:
            async for token in self.llm.generate_stream(message):
                yield {
                    "token": token,
                    "finished": False
                }
            yield {
                "token": "",
                "finished": True
            }
        except Exception as e:
            yield {
                "error": str(e),
                "finished": True
            }
```

## Best Practices

### 1. Error Handling

```python
class RobustAgent(BaseAgent):
    def process_message(self, message: str) -> Dict[str, Any]:
        try:
            # Input validation
            if not message.strip():
                return {"error": "Empty message"}
                
            # Rate limiting
            if not self._check_rate_limit():
                return {"error": "Rate limit exceeded"}
                
            # Process message
            response = self._generate_response(message)
            
            # Validate response
            if not self._validate_response(response):
                return {"error": "Invalid response"}
                
            return {"response": response}
            
        except Exception as e:
            logging.error(f"Agent error: {e}")
            return {
                "error": "Internal error",
                "details": str(e)
            }
```

### 2. Logging

```python
import logging

class LoggingAgent(BaseAgent):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.logger = logging.getLogger(__name__)
        
    def process_message(self, message: str) -> Dict[str, Any]:
        self.logger.info(f"Processing message: {message[:50]}...")
        try:
            response = self._generate_response(message)
            self.logger.info("Successfully generated response")
            return {"response": response}
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
            return {"error": str(e)}
```

### 3. Testing

```python
# test_custom_agent.py
import pytest
from app.agents.custom_agent import CustomAgent

def test_custom_agent_initialization():
    agent = CustomAgent(api_key="test_key")
    assert agent.memory is not None
    assert agent.doc_processor is not None

@pytest.mark.asyncio
async def test_process_message():
    agent = CustomAgent(api_key="test_key")
    response = await agent.process_message("Test message")
    assert "response" in response
    assert isinstance(response["response"], str)
```

## Configuration

### 1. Environment Variables

```env
# .env
AGENT_MODEL=llama3-groq-70b-8192-tool-use-preview
AGENT_TEMPERATURE=0.7
AGENT_MAX_TOKENS=4096
AGENT_MEMORY_TYPE=vector
```

### 2. Agent Config

```python
class ConfigurableAgent(BaseAgent):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config["api_key"])
        self.model = config.get("model", "default_model")
        self.temperature = config.get("temperature", 0.7)
        self.max_tokens = config.get("max_tokens", 4096)
```

## Usage Examples

### 1. Basic Usage

```python
from app.agents import CustomAgent

agent = CustomAgent(api_key="your-api-key")
response = agent.process_message("Hello!")
print(response["response"])
```

### 2. With Document Processing

```python
from app.agents import DocumentAgent

agent = DocumentAgent(api_key="your-api-key")
agent.add_document("Important information here...")
response = agent.process_message("What's in the document?")
print(response["response"])
```

### 3. Streaming Response

```python
async for chunk in agent.process_message_stream("Generate a long response"):
    if chunk["finished"]:
        break
    print(chunk["token"], end="", flush=True)
```

## Next Steps

1. Review the [Configuration Guide](configuration.md)
2. Check the [Memory Management Guide](memory.md)
3. Explore [API Documentation](../api/README.md)

## Resources

- [LangChain Documentation](https://python.langchain.com/docs/)
- [Groq API Reference](https://groq.com/docs/)
