# 🤖 hams_ollo AI | A Dynamic AI Assistant development base

A sophisticated, production-ready AI assistant framework built with LLaMA 3 70B (via Groq), LangChain, and Streamlit. This project provides a robust foundation for developing advanced AI applications with RAG capabilities and multi-modal interactions.

## 🌟 Key Features

- **Document-Enhanced Conversations**: RAG capabilities for context-aware responses
- **Multi-Page Interface**:
  - 💬 AI Chat Agent: Main conversation interface
  - 🏠 Home: Quick start guide and features overview
  - 📚 Document Upload: File management and processing
- **Document Processing**:
  - Support for PDF, TXT, DOCX, and MD files
  - Automatic chunking and vectorization
  - Semantic search for relevant context
- **Modern Tech Stack**:
  - LLaMA 3 70B via Groq for state-of-the-art responses
  - LangChain for RAG and memory management
  - ChromaDB for vector storage
  - Streamlit for clean, responsive UI

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Groq API key (get one at [console.groq.com](https://console.groq.com))

### Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Hams-Ollo/Dynamic-AI-Assistant-dev-base.git
   cd Dynamic-AI-Assistant-dev-base
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
   GROQ_API_KEY=your_api_key_here
   MODEL_NAME=llama-3-70b
   MODEL_TEMPERATURE=0.7
   ```

5. **Run the application:**

   ```bash
   streamlit run frontend/Chat.py
   ```

## 🎯 Use Cases

- **Documentation Assistant**: Upload technical docs for instant expert support
- **Knowledge Base**: Create a smart FAQ system from your content
- **Research Helper**: Process and query academic papers or research documents
- **Legal Assistant**: Analyze and query legal documents and contracts
- **Training Material**: Create interactive learning systems from training content

## 🔧 Customization

The template is designed for easy customization:

1. **Document Processing**: Adjust chunking and embedding in `document_processor.py`
2. **Chat Behavior**: Modify prompts and logic in `chat_agent.py`
3. **UI/UX**: Customize the interface in the frontend Streamlit files
4. **Vector Storage**: Configure or swap ChromaDB settings as needed

## 📚 Project Structure

```curl
├── app/
│   ├── agents/
│   │   └── chat_agent.py      # Core chat logic and RAG integration
│   └── utils/
│       └── document_processor.py  # Document handling and vectorization
├── frontend/
│   ├── Chat.py               # Main chat interface
│   └── pages/
│       ├── 0_🏠_Home.py      # Home page and documentation
│       └── 1_📚_Document_Upload.py  # Document management
└── requirements.txt          # Project dependencies
```

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Fork the repository
- Create a feature branch
- Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
