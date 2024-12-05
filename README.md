# 🤖 Dynamic AI Assistant Base

A sophisticated, production-ready AI assistant framework built with LLaMA 3 70B (via Groq), LangChain, and Streamlit. This project provides a robust foundation for developing advanced AI applications with RAG capabilities and multi-modal interactions.

## 🌟 Key Features

- **Advanced Chat Interface**:
  - 💬 Context-aware conversations using RAG
  - 🧠 Intelligent response generation
  - 📝 Chat history management
  - 🔍 Semantic search capabilities

- **Document Management**:
  - 📄 Support for multiple formats (PDF, TXT, DOCX, MD)
  - 🔄 Advanced document processing and vectorization
  - 🏷️ Document tagging and categorization
  - 🔎 Full-text and semantic search

- **Modern Architecture**:
  - 🚀 LLaMA 3 70B via Groq for state-of-the-art responses
  - 🔗 LangChain for RAG and memory management
  - 💾 ChromaDB for efficient vector storage
  - 🎯 Streamlit for responsive UI
  - ⚙️ Unified configuration management

- **Enhanced Logging**:
  - 📝 Emoji-enhanced logging for better traceability

- **Improved UI**:
  - 🖥️ Updated chat interface with emoji roles

- **Document Upload Enhancements**:
  - 📤 Improved document processing capabilities

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Groq API key (get one at [console.groq.com](https://console.groq.com))

### Setup

1. **Clone the repository:**

   ```bash
   git clone [your-repository-url]
   cd Dynamic-AI-Assistant-base
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
   # Add your Groq API key and other settings to .env
   ```

5. **Run the application:**

   ```bash
   streamlit run frontend/Home.py
   ```

## 📁 Project Structure

```curl
Dynamic-AI-Assistant-base/
├── app/
│   ├── agents/
│   │   └── chat_agent.py        # Core chat and RAG functionality
│   ├── utils/
│   │   ├── config.py           # Unified configuration management
│   │   ├── document_processor.py # Document handling
│   │   └── memory.py           # Memory management
│   └── core/                   # Core application components
├── frontend/
│   ├── Home.py                 # Main entry point
│   └── pages/
│       ├── Chat.py             # Chat interface
│       └── Document_Upload.py   # Document management
├── data/                       # Data storage
│   └── memory/                 # Vector store and memory
├── docs/                       # Documentation
└── tests/                      # Test suite
```

## ⚙️ Configuration

The application uses a unified configuration system (`app/utils/config.py`) that manages:

- Model settings (temperature, tokens, etc.)
- API configurations
- Memory management
- Document processing parameters
- Path management

Configuration can be customized through:

1. Environment variables
2. `.env` file
3. Runtime configuration

## 🎯 Use Cases

- **Research Assistant**: Process and analyze academic papers
- **Documentation Helper**: Quick access to technical documentation
- **Knowledge Base**: Create smart FAQ systems
- **Legal Assistant**: Analyze legal documents
- **Training Support**: Process training materials

## 🔧 Customization

Key customization points:

1. **Document Processing**:
   - Adjust chunking in `document_processor.py`
   - Configure embedding models
   - Modify vector store settings

2. **Chat Behavior**:
   - Update prompts in `chat_agent.py`
   - Customize RAG integration
   - Adjust memory management

3. **User Interface**:
   - Modify Streamlit components
   - Add new pages
   - Customize styling

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📄 License

[Your License] - See LICENSE file for details

## 📦 Versioning

This release is version 1.1.0, featuring new enhancements and improvements.
