# 🤖 Multi-Agent Chatbot Template

A production-ready template for building AI chatbots and conversational agents using modern best practices. This template provides everything you need to quickly start developing sophisticated chatbots powered by Groq's LLM API, featuring document processing, memory management, and flexible conversation handling.

## 🎯 Why Use This Template?

- **Quick Start**: Get a production-ready chatbot running in minutes
- **Dual Interfaces**: Choose between CLI or Web interface
- **Best Practices**: Built-in logging, configuration, and security features
- **Flexible Architecture**: Easy to extend and customize for your specific needs
- **Modern Stack**: Async support, type hints, and modern Python patterns
- **Production Ready**: Includes error handling, testing, and deployment configurations
- **Advanced Features**: Vector-based memory, document processing, and more

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Groq API key (sign up at [console.groq.com](https://console.groq.com))
- Git

### Setup Steps

1. **Clone the template:**

   ```bash
   git clone https://github.com/yourusername/multi-agent-chatbot-template.git
   cd multi-agent-chatbot-template
   ```

2. **Create and activate a virtual environment:**

   ```bash
   # Create virtual environment
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

4. **Configure environment variables:**

   ```bash
   # Copy the example environment file
   cp .env.example .env
   ```

   Edit `.env` with your configuration:

   ```env
   # Required: Your Groq API key
   GROQ_API_KEY=gsk_your_api_key_here

   # Optional: Model configuration (defaults shown)
   MODEL_NAME=mixtral-8x7b-32768
   MODEL_TEMPERATURE=0.7
   MODEL_MAX_TOKENS=4096

   # Optional: Memory configuration
   MEMORY_TYPE=vector
   MEMORY_PATH=./data/memory
   ```

## 🖥️ Running the Application

You can run the application in two ways:

### 1. Command Line Interface (CLI)

Run the traditional command-line interface:

```bash
python main.py
```

The CLI interface provides:

- Simple text-based interaction
- Command history
- Help commands
- Quick testing and debugging

### 2. Streamlit Web Interface

Run the modern web interface:

```bash
streamlit run frontend/streamlit_app.py
```

The web interface offers:

- Modern chat-like UI
- Message history with user/AI distinction
- Clear chat functionality
- Helpful sidebar with tips
- Progress indicators
- Error handling with visual feedback

Access the web interface at:

- Local: <http://localhost:8501>
- Network: <http://your-ip:8501>

## 📁 Project Structure

```curl
multi-agent-chatbot/
├── app/                    # Main application code
│   ├── agents/            # Agent implementations
│   │   ├── chat_agent.py # Main chat agent
│   │   └── document_processor.py
│   ├── core/             # Core functionality
│   │   ├── config.py    # Configuration management
│   │   └── logging.py   # Logging setup
│   └── utils/            # Utilities
│       └── memory.py    # Memory management
├── frontend/             # Frontend interfaces
│   └── streamlit_app.py # Streamlit web interface
├── data/                 # Data storage
│   └── memory/          # Vector store for conversation memory
├── tests/                # Test suite
├── .env                  # Environment variables (create this)
├── .env.example         # Example environment file
├── requirements.txt     # Project dependencies
└── main.py             # CLI application entry point
```

## 🔧 Configuration Options

### Model Configuration

The template uses Groq's LLM API with the following configurable options in `.env`:

- `MODEL_NAME`: The LLM model to use (default: mixtral-8x7b-32768)
- `MODEL_TEMPERATURE`: Controls response randomness (0.0-1.0, default: 0.7)
- `MODEL_MAX_TOKENS`: Maximum response length (default: 4096)

### Memory System

The chat system includes a vector-based memory system for context retention:

- `MEMORY_TYPE`: Memory system type (options: vector, buffer)
- `MEMORY_PATH`: Storage location for conversation history

## 💡 Creating Your Own Agent

1. **Create a new agent class:**

   ```python
   from app.agents.chat_agent import ChatAgent
   
   class MyCustomAgent(ChatAgent):
       def __init__(self, config: dict):
           super().__init__(config)
           # Add your custom initialization
   
       async def process_message(self, message: str) -> dict:
           # Implement your custom message processing
           return await super().process_message(message)
   ```

2. **Initialize your agent:**

   ```python
   config = {
       'api_key': 'your-groq-api-key',
       'model': 'mixtral-8x7b-32768',
       'temperature': 0.7
   }
   agent = MyCustomAgent(config)
   ```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Warnings

1. **Hugging Face Warnings**

   ```curl
   FutureWarning: `resume_download` is deprecated...
   ```

   This is a harmless warning from the Hugging Face library and can be safely ignored.

2. **LangChain Memory Warning**

   ```curl
   LangChainDeprecationWarning: Please see the migration guide...
   ```

   This warning indicates future LangChain updates. The current implementation is stable.

3. **Torch Classes Warning**

   ```curl
   Examining the path of torch.classes raised...
   ```

   This is a known warning from PyTorch and doesn't affect functionality.

### Common Issues

1. **Connection Errors**
   - Verify your Groq API key is correct and properly set in `.env`
   - Check your internet connection
   - Ensure you can access api.groq.com
   - Try disabling VPN if you're using one

2. **Memory System Errors**
   - Ensure the `data/memory` directory exists
   - Check write permissions for the memory directory

3. **Model Response Issues**
   - Try adjusting the `MODEL_TEMPERATURE` for different response styles
   - Ensure `MODEL_MAX_TOKENS` is appropriate for your use case

For more help, please open an issue on the GitHub repository.
