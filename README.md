# 🤖 Advanced Multi-Agent AI Chat System

A sophisticated, context-aware conversational AI application built with modern async Python. Powered by Groq's Mixtral LLM, LangChain, and Streamlit, this system demonstrates production-ready practices for building intelligent conversational agents with advanced memory management and intent classification capabilities.

## 🌟 Key Features

- **Intelligent Intent Classification**: LLM-powered understanding of user intentions
- **Context-Aware Responses**: Vector-based memory for enhanced conversation history
- **Advanced Memory Management**: Semantic search and conversation tracking using ChromaDB
- **Modern Tech Stack**: Groq LLM, LangChain, HuggingFace Embeddings, Streamlit UI
- **Async Architecture**: Non-blocking design with proper resource management
- **Production Ready**: Comprehensive error handling and graceful shutdown

## 🛠️ Technical Stack

- **Core Framework**: Python 3.12+
- **LLM Integration**: Groq API (Mixtral-8x7b-32768)
- **Memory & Embeddings**:
  - LangChain for memory management
  - HuggingFace Embeddings (all-MiniLM-L6-v2)
  - ChromaDB for vector storage
- **Frontend**: Streamlit
- **Dependencies**: Redis, TensorFlow, PyTorch

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
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

5. **Run the application:**

   ```bash
   streamlit run frontend/streamlit_app.py
   ```

## 🏗️ System Architecture

### Core Components

1. **ChatAgent** (`app/agents/chat_agent.py`)
   - Async message processing
   - Intent classification using LLM reasoning
   - Context-aware response generation
   - Resource management and cleanup

2. **MemoryManager** (`app/utils/memory.py`)
   - LangChain-based memory management
   - Vector-based semantic search with ChromaDB
   - Conversation history tracking
   - Redis integration for scalable storage

3. **Streamlit Frontend** (`frontend/streamlit_app.py`)
   - Modern, responsive UI
   - Async message handling
   - Real-time response streaming
   - Session state management

### Key Features

#### Async Operations

- Non-blocking I/O for better performance
- Proper async initialization and cleanup
- Graceful error handling

#### Memory Management

- ChatMessageHistory for conversation tracking
- Vector-based semantic search
- Efficient cleanup and resource management
- Redis integration for scalable storage

#### LLM Integration

- Groq API with Mixtral model
- Temperature and context-length control
- Fallback handling for API issues

## 📚 Project Structure

```curl
multi-agent-chat-system/
├── app/
│   ├── agents/
│   │   └── chat_agent.py
│   ├── utils/
│   │   └── memory.py
│   └── core/
│       └── config.py
├── frontend/
│   └── streamlit_app.py
├── data/
│   └── memory/
├── scripts/
│   └── text_scraper.py
├── requirements.txt
└── .env
```

## 🔧 Configuration

### Environment Variables

- `GROQ_API_KEY`: Your Groq API key
- `APP_ENV`: development/production
- `DEBUG`: true/false
- `LOG_LEVEL`: INFO/DEBUG/WARNING
- `MODEL_NAME`: mixtral-8x7b-32768
- `MODEL_TEMPERATURE`: 0.7 (default)

### Memory Settings

- Vector store location: `./data/memory`
- Redis configuration (optional)
- Cleanup timeout: 5 seconds (default)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Groq Team for the LLM API
- LangChain community
- HuggingFace for embeddings
- Streamlit team
