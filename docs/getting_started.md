# Getting Started with Dynamic AI Assistant

This guide will help you set up and start using the Dynamic AI Assistant framework. Follow these steps to get your development environment ready and begin working with the AI assistant.

## Prerequisites

- Python 3.12 or higher
- Git
- A Groq API key
- Basic understanding of Python and AI concepts

## Quick Start

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Hams-Ollo/Dynamic-AI-Assistant-dev-base.git
   cd Dynamic-AI-Assistant-dev-base
   ```

2. **Set Up Virtual Environment**

   ```bash
   # Create virtual environment
   python -m venv venv

   # Activate it on Windows
   .\venv\Scripts\activate

   # Or on Unix/MacOS
   source venv/bin/activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**

   ```bash
   # Copy example environment file
   cp .env.example .env

   # Edit .env with your API keys
   # Required:
   GROQ_API_KEY=your-groq-api-key
   
   # Optional:
   LOG_LEVEL=INFO
   MEMORY_TYPE=buffer
   MEMORY_PATH=./data/memory
   ```

5. **Run the Application**

   ```bash
   python main.py
   ```

## Project Structure Overview

```curl
multi-agent-chatbot/
├── app/                    # Main application code
│   ├── agents/            # Agent implementations
│   │   ├── chat_agent.py # Main chat agent
│   │   └── document_processor.py
│   ├── core/             # Core functionality
│   └── utils/            # Utilities
├── tests/                # Test suite
└── main.py              # Entry point
```

## Basic Usage

### 1. Simple Chat Interaction

```python
from app.agents.chat_agent import ChatAgent

# Initialize the chat agent
agent = ChatAgent(api_key="your-groq-api-key")

# Process a message
response = agent.process_message("Hello! How can you help me?")
print(response["response"])
```

### 2. Document Processing

```python
from app.agents.document_processor import DocumentProcessor

# Initialize the document processor
processor = DocumentProcessor()

# Process a text document
docs = processor.process_text("Your document text here")
```

### 3. Memory Management

```python
from app.utils.memory import MemoryManager

# Initialize memory manager
memory = MemoryManager({
    'type': 'buffer',
    'path': './data/memory'
})

# Store and retrieve context
memory.add_context("Hello!", "Hi there!")
context = memory.get_relevant_context("Hello")
```

## Next Steps

1. Check out the [Configuration Guide](guides/configuration.md) for advanced settings
2. Learn how to [create custom agents](guides/agents.md)
3. Review the [development guidelines](development_guidelines.md)
4. Run the test suite: `pytest tests/`

## Common Issues

### 1. API Key Issues

```curl
Error: Invalid API key provided
Solution: Ensure GROQ_API_KEY is properly set in your .env file
```

### 2. Memory Errors

```curl
Error: Memory path not found
Solution: Create the data/memory directory manually if it doesn't exist
```

### 3. Import Errors

```curl
Error: Module not found
Solution: Ensure you're in the project root and virtual environment is activated
```

## Getting Help

If you encounter any issues:

1. Check the [documentation](index.md)
2. Look for similar issues on GitHub
3. Open a new issue if needed

## Next Section

- [Environment Setup](environment_setup.md) - Detailed environment configuration
- [Agent Development](guides/agents.md) - Learn how to create custom agents
