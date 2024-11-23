# 🤖 Multi-Agent Chatbot Template

A production-ready template for building AI chatbots and conversational agents using modern best practices. This template provides everything you need to quickly start developing sophisticated chatbots with features like document processing, memory management, and flexible LLM integration.

## 🎯 Why Use This Template?

- **Quick Start**: Get a production-ready chatbot running in minutes
- **Best Practices**: Built-in logging, configuration, and security features
- **Flexible Architecture**: Easy to extend and customize for your specific needs
- **Modern Stack**: Async support, type hints, and modern Python patterns
- **Production Ready**: Includes error handling, testing, and deployment configurations

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- A Groq API key (get one at [groq.com](https://groq.com))
- Git

### Setup

1. **Clone the template:**

   ```bash
   git clone https://github.com/yourusername/multi-agent-chatbot-template.git
   cd multi-agent-chatbot-template
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   
   # Windows
   .\venv\Scripts\activate
   
   # Unix/MacOS
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your environment:**

   ```bash
   cp .env.example .env
   ```

   Then edit `.env` with your API keys:

   ```env
   GROQ_API_KEY=your-api-key-here
   ```

5. **Run the chatbot:**

   ```bash
   python main.py
   ```

## 📁 Project Structure

```curl
multi-agent-chatbot/
├── app/                    # Main application code
│   ├── agents/            # Agent implementations
│   │   ├── base/         # Base agent classes
│   │   ├── specialized/  # Specialized agents
│   │   ├── chat_agent.py # Main chat agent
│   │   └── document_processor.py
│   ├── api/              # API endpoints
│   ├── core/             # Core functionality
│   │   ├── config.py    # Configuration management
│   │   └── logging.py   # Logging setup
│   └── utils/            # Utilities
│       └── memory.py    # Memory management
├── tests/                 # Test suite
├── .env                   # Environment variables
├── .env.example          # Example environment file
├── requirements.txt       # Project dependencies
└── main.py               # Application entry point
```

## 💡 Creating Your Own Agent

1. **Create a new agent class:**

   ```python
   from app.agents.base.base_agent import BaseAgent
   
   class MyCustomAgent(BaseAgent):
       def __init__(self, api_key: str):
           super().__init__(api_key)
           # Add your custom initialization
   
       def process_message(self, message: str) -> dict:
           # Add your custom message processing
           return {
               "response": "Your processed response",
               "source_documents": []
           }
   ```

2. **Use the built-in features:**

   ```python
   from app.utils.memory import MemoryManager
   from app.agents.document_processor import DocumentProcessor
   
   class MyAgent:
       def __init__(self):
           # Initialize memory
           self.memory = MemoryManager({
               'type': 'buffer',
               'path': './data/memory'
           })
           
           # Initialize document processor
           self.doc_processor = DocumentProcessor()
           
           # Process documents
           docs = self.doc_processor.process_text("Your text here")
   ```

## 🔧 Configuration

### Environment Variables

Required variables in your `.env` file:

```env
# Required
GROQ_API_KEY=your-groq-api-key

# Optional
LOG_LEVEL=INFO
MEMORY_TYPE=buffer
MEMORY_PATH=./data/memory
```

### Memory Configuration

The template supports multiple memory types:

```python
# Buffer Memory (Default)
memory_config = {
    'type': 'buffer',
    'path': './data/memory'
}

# Vector Memory
memory_config = {
    'type': 'vector',
    'path': './data/memory',
    'embedding_model': 'openai'
}
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/
```

## 📚 Best Practices

1. **Error Handling**
   - Always use try-except blocks for external API calls
   - Log errors with appropriate levels
   - Provide user-friendly error messages

2. **Memory Management**
   - Regularly clean up old conversations
   - Use appropriate memory types for your use case
   - Monitor memory usage in production

3. **Security**
   - Never commit API keys
   - Use environment variables for sensitive data
   - Implement rate limiting for production

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Getting Help

- Create an issue for bug reports or feature requests
- Check existing issues for common problems
- Read the documentation in the `docs` folder

---

Built with ❤️ by [Your Name/Organization]
