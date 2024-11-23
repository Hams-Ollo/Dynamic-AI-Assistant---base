# API Documentation

## Overview

The Multi-Agent Project Template provides a comprehensive API for creating, managing, and interacting with AI agents. This documentation covers the core APIs available in the system.

## Table of Contents

1. [Agent API](#agent-api)
2. [Memory API](#memory-api)
3. [Configuration API](#configuration-api)
4. [REST API](#rest-api)
5. [WebSocket API](#websocket-api)

## Agent API

### BaseAgent Class

The foundation for all agents in the system.

```python
from src.agents.base.base_agent import BaseAgent

class MyAgent(BaseAgent):
    async def process(self, input_data: Any) -> Any:
        # Process input data
        return result

    async def handle_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        # Handle inter-agent communication
        return response
```

#### Key Methods

- `process(input_data)`: Process input and return results
- `handle_message(message)`: Handle communication between agents
- `save_state()`: Persist agent state
- `load_state(state)`: Restore agent state
- `update_config(config)`: Update agent configuration

### Agent Manager

Manages agent lifecycle and communication.

```python
from src.core.agent_manager import AgentManager

# Initialize manager
manager = AgentManager(config)

# Create agent
agent = manager.create_agent("my_agent", "MyAgentType", config)

# Get agent
agent = manager.get_agent("my_agent")

# Send message
response = await manager.send_message("my_agent", message)
```

## Memory API

### Memory Manager

Manages different types of memory systems.

```python
from src.core.memory.memory_manager import MemoryManager

# Initialize manager
memory_manager = MemoryManager(config)

# Get memory instance
memory = memory_manager.get_memory("agent_memory")

# Create new memory
memory = memory_manager.create_memory(
    "new_memory",
    memory_type="vector",
    max_items=1000
)
```

### Memory Types

#### Simple Memory

```python
memory = SimpleMemory(max_items=1000)
memory.add("key", "value")
value = memory.get("key")
results = memory.search("query")
```

#### Vector Memory

```python
memory = VectorMemory(
    embedding_model="sentence-transformers/all-mpnet-base-v2",
    dimension=768
)
memory.add("doc1", "Document content")
similar = memory.search("query", k=5)
```

## Configuration API

### Config Manager

Manages hierarchical configuration system.

```python
from src.core.utils.config_manager import ConfigManager

# Initialize
config = ConfigManager()

# Get values
api_key = config.get("security.api_key")
memory_config = config.get("memory.default_store")

# Update configuration
config.save_custom_config({
    "agents": {
        "my_agent": {
            "enabled": True
        }
    }
})
```

## REST API

### Authentication

```http
POST /api/v1/auth/token
Content-Type: application/json

{
    "api_key": "your-api-key"
}
```

### Agents

#### Create Agent

```http
POST /api/v1/agents
Authorization: Bearer <token>
Content-Type: application/json

{
    "agent_id": "my_agent",
    "agent_type": "MyAgentType",
    "config": {
        "memory_type": "vector",
        "llm_model": "gpt-4"
    }
}
```

#### Process Input

```http
POST /api/v1/agents/{agent_id}/process
Authorization: Bearer <token>
Content-Type: application/json

{
    "input_data": "Your input here"
}
```

#### Send Message

```http
POST /api/v1/agents/{agent_id}/message
Authorization: Bearer <token>
Content-Type: application/json

{
    "message": {
        "type": "request",
        "content": "Message content"
    }
}
```

### Memory

#### Store Data

```http
POST /api/v1/memory/{memory_id}/store
Authorization: Bearer <token>
Content-Type: application/json

{
    "key": "item_key",
    "value": "Item value or object"
}
```

#### Search Memory

```http
GET /api/v1/memory/{memory_id}/search?query=search_term
Authorization: Bearer <token>
```

## WebSocket API

### Connect to Agent

```javascript
const ws = new WebSocket('ws://localhost:8001/ws/agents/{agent_id}');

ws.onmessage = (event) => {
    const message = JSON.parse(event.data);
    console.log('Received:', message);
};

// Send message
ws.send(JSON.stringify({
    type: 'message',
    content: 'Hello agent!'
}));
```

### Message Types

#### Agent Status Update

```json
{
    "type": "status",
    "agent_id": "my_agent",
    "status": "processing"
}
```

#### Agent Response

```json
{
    "type": "response",
    "agent_id": "my_agent",
    "content": "Response content",
    "timestamp": "2024-01-20T10:30:00Z"
}
```

## Error Handling

### Error Response Format

```json
{
    "error": {
        "code": "ERROR_CODE",
        "message": "Error description",
        "details": {
            "field": "Additional information"
        }
    }
}
```

### Common Error Codes

- `AUTH_ERROR`: Authentication failed
- `INVALID_REQUEST`: Invalid request format
- `AGENT_NOT_FOUND`: Agent not found
- `MEMORY_ERROR`: Memory operation failed
- `PROCESSING_ERROR`: Agent processing error

## Rate Limiting

The API implements rate limiting per API key:

- 100 requests per minute for REST API
- 10 concurrent WebSocket connections
- 1000 messages per hour for WebSocket

## Security

- All endpoints require authentication
- API keys must be kept secure
- HTTPS required in production
- CORS restrictions apply
- Rate limiting prevents abuse

## Best Practices

1. **Error Handling**
   - Always check response status
   - Implement proper error handling
   - Log errors appropriately

2. **Performance**
   - Use WebSocket for real-time communication
   - Implement caching where appropriate
   - Batch operations when possible

3. **Security**
   - Rotate API keys regularly
   - Use secure connections
   - Validate all input

4. **Development**
   - Use TypeScript for type safety
   - Follow API versioning
   - Document API changes
