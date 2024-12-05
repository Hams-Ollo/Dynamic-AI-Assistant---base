# Configuration Guide

## Overview

This guide explains how to configure the Multi-Agent Project Template for your specific needs. The system uses a hierarchical configuration system that allows for flexible customization at different levels.

## Table of Contents

1. [Configuration Structure](#configuration-structure)
2. [Configuration Files](#configuration-files)
3. [Environment Variables](#environment-variables)
4. [Agent Configuration](#agent-configuration)
5. [Memory Configuration](#memory-configuration)
6. [Security Configuration](#security-configuration)
7. [Best Practices](#best-practices)

## Configuration Structure

The configuration system follows this hierarchy (highest to lowest precedence):

1. Environment Variables
2. Custom Configuration Files
3. Default Configuration Files

### Directory Structure

```curl
config/
├── default/           # Default configuration files
│   ├── config.json   # Main configuration
│   └── agents.json   # Agent-specific defaults
├── custom/           # Custom configuration files
│   ├── config.json   # Custom overrides
│   └── agents.json   # Custom agent settings
└── templates/        # Configuration templates
    └── config.json   # Template for new projects
```

## Configuration Files

### Default Configuration (config/default/config.json)

```json
{
    "system": {
        "log_level": "INFO",
        "max_retries": 3,
        "timeout": 30
    },
    "agents": {
        "defaults": {
            "memory": {
                "type": "simple",
                "max_items": 1000
            },
            "llm": {
                "provider": "openai",
                "model": "gpt-3.5-turbo",
                "temperature": 0.7
            }
        }
    },
    "memory": {
        "default_store": "local",
        "stores": {
            "local": {
                "type": "sqlite",
                "path": "data/memory.db"
            },
            "vector": {
                "type": "chroma",
                "path": "data/embeddings"
            }
        }
    },
    "security": {
        "api_key_required": true,
        "cors_origins": ["http://localhost:3000"],
        "rate_limit": {
            "requests": 100,
            "per_seconds": 60
        }
    }
}
```

### Custom Configuration (config/custom/config.json)

```json
{
    "system": {
        "log_level": "DEBUG"
    },
    "agents": {
        "my_agent": {
            "memory": {
                "type": "vector",
                "max_items": 10000
            },
            "llm": {
                "model": "gpt-4"
            }
        }
    }
}
```

## Environment Variables

Environment variables override all other configuration settings. They should be prefixed with `AGENT_`.

Example `.env` file:

```env
AGENT_LOG_LEVEL=DEBUG
AGENT_API_KEY=your_api_key
AGENT_LLM_PROVIDER=openai
AGENT_MEMORY_TYPE=vector
AGENT_MAX_RETRIES=5
```

### Loading Environment Variables

```python
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Access environment variables
log_level = os.getenv("AGENT_LOG_LEVEL", "INFO")
api_key = os.getenv("AGENT_API_KEY")
```

## Agent Configuration

### Basic Agent Configuration

```json
{
    "agents": {
        "chat_agent": {
            "type": "ConversationalAgent",
            "enabled": true,
            "memory": {
                "type": "vector",
                "max_items": 5000
            },
            "llm": {
                "provider": "openai",
                "model": "gpt-4",
                "temperature": 0.7,
                "max_tokens": 150
            }
        }
    }
}
```

### Advanced Agent Configuration

```json
{
    "agents": {
        "task_agent": {
            "type": "TaskAgent",
            "enabled": true,
            "memory": {
                "type": "hierarchical",
                "stores": {
                    "short_term": {
                        "type": "simple",
                        "max_items": 100
                    },
                    "long_term": {
                        "type": "vector",
                        "max_items": 10000
                    }
                }
            },
            "tools": {
                "web_search": {
                    "enabled": true,
                    "api_key": "${SEARCH_API_KEY}"
                },
                "calculator": {
                    "enabled": true
                }
            },
            "rate_limit": {
                "requests": 50,
                "per_minute": 1
            }
        }
    }
}
```

## Memory Configuration

### Simple Memory

```json
{
    "memory": {
        "type": "simple",
        "max_items": 1000,
        "cleanup_policy": "lru"
    }
}
```

### Vector Memory

```json
{
    "memory": {
        "type": "vector",
        "backend": "chroma",
        "embedding_model": "sentence-transformers/all-mpnet-base-v2",
        "dimension": 768,
        "similarity_metric": "cosine",
        "index_params": {
            "ef_construction": 200,
            "m": 48
        }
    }
}
```

### Hierarchical Memory

```json
{
    "memory": {
        "type": "hierarchical",
        "stores": {
            "working": {
                "type": "simple",
                "max_items": 100
            },
            "semantic": {
                "type": "vector",
                "max_items": 10000
            },
            "permanent": {
                "type": "sqlite",
                "path": "data/permanent.db"
            }
        }
    }
}
```

## Security Configuration

### API Security

```json
{
    "security": {
        "api_key_required": true,
        "jwt": {
            "secret_key": "${JWT_SECRET_KEY}",
            "algorithm": "HS256",
            "access_token_expire_minutes": 30
        },
        "cors_origins": [
            "http://localhost:3000",
            "https://your-domain.com"
        ],
        "rate_limit": {
            "requests": 100,
            "per_seconds": 60
        }
    }
}
```

### Agent Security

```json
{
    "security": {
        "agents": {
            "permissions": {
                "file_access": ["read", "write"],
                "network_access": true,
                "system_commands": false
            },
            "isolation": {
                "enabled": true,
                "max_memory_mb": 512,
                "max_cpu_percent": 50
            }
        }
    }
}
```

## New Configuration Options in v1.1.0

- **Logging**: Emoji-enhanced logging for better traceability.
- **Document Management**: New settings for stash clearing and processing.

## Best Practices

### 1. Environment Variables

- Use environment variables for sensitive data
- Keep `.env` file out of version control
- Use `.env.example` as a template
- Document all environment variables

### 2. Configuration Management

```python
from src.core.utils.config_manager import ConfigManager

# Initialize with custom path
config = ConfigManager(config_dir="path/to/config")

# Get configuration values
api_key = config.get("security.api_key")
memory_config = config.get("memory.default_store")

# Update configuration
config.save_custom_config({
    "system": {
        "log_level": "DEBUG"
    }
})
```

### 3. Validation

```python
from pydantic import BaseModel, Field

class AgentConfig(BaseModel):
    type: str
    enabled: bool = True
    memory: dict = Field(...)
    llm: dict = Field(...)

def validate_config(config: dict) -> None:
    try:
        AgentConfig(**config)
    except ValidationError as e:
        logger.error(f"Invalid configuration: {e}")
        raise
```

### 4. Security

1. Never commit sensitive data
2. Use environment variables for secrets
3. Implement proper access controls
4. Regular security audits
5. Keep dependencies updated

### 5. Maintenance

1. Regular configuration reviews
2. Document all changes
3. Version control configurations
4. Monitor for issues
5. Regular backups

## Configuration Examples

### Development Environment

```json
{
    "system": {
        "log_level": "DEBUG",
        "environment": "development",
        "debug": true
    },
    "security": {
        "api_key_required": false,
        "cors_origins": ["http://localhost:3000"]
    }
}
```

### Production Environment

```json
{
    "system": {
        "log_level": "INFO",
        "environment": "production",
        "debug": false
    },
    "security": {
        "api_key_required": true,
        "cors_origins": ["https://your-domain.com"],
        "rate_limit": {
            "requests": 100,
            "per_seconds": 60
        }
    }
}
```

### Testing Environment

```json
{
    "system": {
        "log_level": "DEBUG",
        "environment": "testing",
        "debug": true
    },
    "agents": {
        "defaults": {
            "memory": {
                "type": "simple",
                "max_items": 10
            }
        }
    }
}
