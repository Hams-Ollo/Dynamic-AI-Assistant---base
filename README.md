# 🤖 hams_ollo AI | A Dynamic AI Assistant development base

A sophisticated, production-ready AI assistant framework built with LLaMA 3 70B (via Groq), LangChain, and Streamlit. This project provides a robust foundation for developing advanced AI applications with RAG capabilities and multi-modal interactions.

## 🌟 Key Features

- **Document-Enhanced Conversations**: RAG capabilities for context-aware responses
- **Multi-Page Interface**:
  - 💬 AI Chat Agent: Main conversation interface with RAG capabilities
  - 🏠 Home: Quick start guide, setup instructions, and application overview
  - 📚 Document Upload: File management, processing, and search/filter functionality
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

4. **Environment setup:**

   ```bash
   cp .env.example .env
   # Add your Groq API key to .env
   ```

5. **Running the Application:**

   ```bash
   # Start the application
   python main.py
   # Or using Streamlit
   streamlit run frontend/Home.py
   ```

6. **Access the application:**

   Open your browser and go to `http://localhost:8501`

7. **Stopping the Application:**

   Use `Ctrl+C` in the terminal to stop the application.

8. **Deactivate virtual environment:**

   ```bash
   deactivate
   ```

### Development Commands

- **Update dependencies:**

  ```bash
  pip freeze > requirements.txt
  ```

- **Run with debug logging:**

  ```bash
  python main.py --log-level=debug
  ```

- **Clear Streamlit cache:**

  ```bash
  streamlit cache clear
  ```

### Git Quick Reference

- **Initialize repository:**

  ```bash
  git init
  ```

- **Add files to staging:**

  ```bash
  git add .
  ```

- **Commit changes:**

  ```bash
  git commit -m "your message"
  ```

- **Create new branch:**

  ```bash
  git checkout -b branch-name
  ```

- **Switch branches:**

  ```bash
  git checkout branch-name
  ```

- **Push to remote:**

  ```bash
  git push -u origin branch-name
  ```

- **Pull latest changes:**

  ```bash
  git pull origin branch-name
  ```

- **Check status:**

  ```bash
  git status
  ```

- **View commit history:**

  ```bash
  git log
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
