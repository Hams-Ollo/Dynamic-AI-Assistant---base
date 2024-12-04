# API Documentation

## Overview

This document outlines the API structure for both the template and current implementation.

## Core Components

### Agent System

#### Base Agent Interface

```python
class BaseAgent:
    def __init__(self, config: dict):
        """Initialize base agent with configuration."""
        self.config = config
        self.capabilities = []

    async def process_message(self, message: str) -> dict:
        """Process incoming message and return response."""
        raise NotImplementedError
```

#### Current Implementation: Chat Agent

```python
class ChatAgent(BaseAgent):
    def __init__(self, config: dict):
        super().__init__(config)
        self.llm = GroqChatModel(
            api_key=config["api_key"],
            model=config.get("model", "mixtral-8x7b-32768")
        )
```

## REST API Endpoints

### Authentication

```bash
POST /api/auth/token
Content-Type: application/json

{
    "username": "string",
    "password": "string"
}
```

### Agent Communication

```bash
POST /api/agent/chat
Authorization: Bearer <token>
Content-Type: application/json

{
    "message": "string",
    "context": {}
}
```

## WebSocket API

### Connection

```javascript
const ws = new WebSocket('ws://localhost:8501/ws/agent');
```

### Message Format

```javascript
{
    "type": "message",
    "content": "string",
    "timestamp": "ISO-8601"
}
```

## Error Handling

### Standard Error Response

```json
{
    "error": {
        "code": "string",
        "message": "string",
        "details": {}
    }
}
```

### Error Codes

- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

## Rate Limiting

- Default: 100 requests per minute per IP
- Authenticated: 1000 requests per hour per user
- Recommended: Implement exponential backoff

## Security

### Authentication Implementation

- JWT-based authentication
- 24-hour token expiration
- Refresh token support

### Authorization

- Role-based access control
- Scoped permissions
- API key management

## Client Examples

### Python Client

```python
import requests

class APIClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {api_key}"}

    async def chat_with_agent(self, message: str) -> dict:
        response = await requests.post(
            f"{self.base_url}/api/agent/chat",
            headers=self.headers,
            json={"message": message}
        )
        return response.json()
```

### JavaScript Client

```javascript
class AgentClient {
    constructor(baseUrl, apiKey) {
        this.baseUrl = baseUrl;
        this.headers = {
            'Authorization': `Bearer ${apiKey}`,
            'Content-Type': 'application/json'
        };
    }

    async chatWithAgent(message) {
        const response = await fetch(`${this.baseUrl}/api/agent/chat`, {
            method: 'POST',
            headers: this.headers,
            body: JSON.stringify({ message })
        });
        return response.json();
    }
}
```

## Versioning

API versioning follows semantic versioning:

- Major version: Breaking changes
- Minor version: New features
- Patch version: Bug fixes

## Support

For API support:

- Email: <api-support@example.com>
- Documentation: /docs/api
- Status: status.example.com

---
*This API documentation serves as both a reference for the current implementation and a template for future projects.*
