# API Documentation

## Overview

This document describes the APIs and interfaces available in the Program_and_Chill project.

## Agent System API

### Agent Creation

```python
from app.agents import BaseAgent

class CustomAgent(BaseAgent):
    def __init__(self, config: dict):
        super().__init__(config)
        self.capabilities = ["text", "code", "analysis"]
```

### Agent Communication

```python
async def communicate(message: str) -> str:
    """Send message to agent and get response."""
    return await agent.process_message(message)
```

## REST API Endpoints

### Authentication Endpoints

```bash
POST /api/auth/token
Content-Type: application/json

{
    "username": "string",
    "password": "string"
}
```

### Agent Interaction

```bash
POST /api/agent/chat
Authorization: Bearer <token>
Content-Type: application/json

{
    "message": "string",
    "agent_id": "string",
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
    "agent_id": "string",
    "timestamp": "ISO-8601"
}
```

## Error Handling

### Error Codes

- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

### Error Response Format

```json
{
    "error": {
        "code": "string",
        "message": "string",
        "details": {}
    }
}
```

## Rate Limiting

- 100 requests per minute per IP
- 1000 requests per hour per user
- Exponential backoff recommended

## Security

### Authentication Implementation

- JWT-based authentication
- Tokens expire after 24 hours
- Refresh tokens available

### Authorization

- Role-based access control
- Scoped permissions
- API key management

## Examples

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

## Migration Guide

### v1.x to v2.0

- Updated authentication flow
- New response format
- Additional endpoints

## Support

For API support:

- Email: <api@example.com>
- Documentation: /docs/api
- Status: status.example.com

## API Error Format

```json
{
    "error": {
        "code": "string",
        "message": "string",
        "details": {}
    }
}
