# 🤖 Advanced Multi-Agent AI Chat System

A sophisticated AI chat system featuring advanced intent classification, research capabilities, and context-aware response generation. Built with modern async Python and powered by Groq's LLM API, this system demonstrates production-ready practices for building intelligent conversational agents.

## 🌟 Key Features

- **Intelligent Intent Classification**: LLM-powered understanding of user intentions
- **Dynamic Research Capabilities**: Smart web scraping with quality scoring
- **Context-Aware Responses**: Vector-based memory for conversation history
- **Robust Architecture**: Async-first design with proper resource management
- **Production Ready**: Comprehensive error handling and graceful shutdown
- **Advanced Memory System**: Semantic search and conversation tracking
- **Modern Tech Stack**: Groq LLM, HuggingFace Embeddings, ChromaDB

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Groq API key (get one at [console.groq.com](https://console.groq.com))
- Git

### Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/multi-agent-chat-system.git
   cd multi-agent-chat-system
   ```

2. **Set up virtual environment:**

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

4. **Configure environment:**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` with your settings:

   ```env
   # Required
   GROQ_API_KEY=your_api_key_here
   
   # Optional
   APP_ENV=development
   DEBUG=true
   LOG_LEVEL=INFO
   
   # Model Settings
   MODEL_NAME=mixtral-8x7b-32768
   MODEL_TEMPERATURE=0.7
   
   # Memory Settings
   MEMORY_TYPE=vector
   MEMORY_BACKEND=chroma
   MEMORY_PATH=./data/memory
   ```

## 🏗️ System Architecture

### Core Components

1. **ChatAgent** (`app/agents/chat_agent.py`)
   - Intent classification using LLM reasoning
   - Context-aware message processing
   - Advanced response generation
   - Resource cleanup management

2. **TextScraper** (`scripts/text_scraper.py`)
   - Intelligent web content extraction
   - Content quality scoring
   - Caching mechanism
   - Async session management

3. **MemoryManager** (`app/utils/memory.py`)
   - Vector-based semantic search
   - Conversation history tracking
   - Persistent storage
   - Efficient cleanup handling

### Key Features

- **Async Operations**: Non-blocking I/O for better performance
- **Graceful Shutdown**: Proper resource cleanup and error handling
- **Intelligent Research**: Dynamic content discovery and evaluation
- **Context Understanding**: Advanced conversation memory management

## 💻 Usage

Run the chat system:

```bash
python main.py
```

### Commands

- Type your message and press Enter to chat
- Use 'exit', 'quit', or 'bye' to exit
- Press Ctrl+C for graceful shutdown

## 🛠️ Development

### Project Structure

```curl
multi-agent-chat-system/
├── app/
│   ├── agents/
│   │   └── chat_agent.py     # Main chat agent
│   ├── core/
│   │   ├── config.py         # Configuration
│   │   └── logging.py        # Logging setup
│   └── utils/
│       └── memory.py         # Memory management
├── scripts/
│   └── text_scraper.py       # Web scraping
├── data/
│   └── memory/              # Vector store
├── tests/
├── .env                     # Configuration
└── main.py                 # Entry point
```

### Error Handling

- Comprehensive exception handling
- Graceful cleanup on interruption
- Timeout protection for async operations
- Clear error messages and logging

## 🔧 Configuration

### Environment Variables

- `APP_ENV`: Environment (development/production)
- `DEBUG`: Enable debug mode
- `LOG_LEVEL`: Logging verbosity
- `GROQ_API_KEY`: API key for LLM
- `MODEL_NAME`: LLM model selection
- `MODEL_TEMPERATURE`: Response randomness
- `MEMORY_TYPE`: Memory system type
- `MEMORY_BACKEND`: Vector store backend
- `MEMORY_PATH`: Storage location

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

1. **Initialization Errors**
   - Ensure GROQ_API_KEY is set correctly
   - Check Python version (3.8+ required)
   - Verify all dependencies are installed

2. **Memory System Warnings**
   - Ensure MEMORY_PATH directory exists
   - Check disk space for vector store
   - Verify proper permissions

3. **Cleanup Timeouts**
   - Default timeout is 5 seconds
   - Adjust in code if needed for slower systems
   - Check for hanging network connections

### Debug Mode

Enable debug mode in `.env`:

```env
DEBUG=true
LOG_LEVEL=DEBUG
```

## 📚 Resources

- [Groq API Documentation](https://console.groq.com/docs)
- [HuggingFace Transformers](https://huggingface.co/docs/transformers)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [aiohttp Documentation](https://docs.aiohttp.org/)
