# Program & Chill AI Assistant 🤖

A powerful multi-agent AI assistant with advanced document processing and Retrieval-Augmented Generation (RAG) capabilities. Built with Groq's Mixtral model, LangChain, and Streamlit.

## 🌟 Features

- **Intelligent Conversations**: Powered by Groq's Mixtral-8x7b-32768 model
- **Document Processing**: Support for multiple document formats (PDF, DOCX, TXT)
- **Knowledge Base**: Dynamic RAG system using ChromaDB vector store
- **User-Friendly Interface**: Clean, intuitive Streamlit UI
- **Multi-Agent Architecture**: Modular design for extensibility

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- [Groq API Key](https://console.groq.com)
- Virtual environment (recommended)

### Installation

Step 1. Clone the repository:

```bash
git clone https://github.com/yourusername/program_and_chill.git
cd program_and_chill
```

Step 2. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Step 3. Install dependencies:

```bash
pip install -r requirements.txt
```

Step 4. Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
MODEL_NAME=mixtral-8x7b-32768
DEBUG=False
LOG_LEVEL=INFO
```

### Running the Application

Start the application with:

```bash
streamlit run main.py
```

The app will be available at `http://localhost:8501`

## 💡 Usage

### Chat Interface

1. Navigate to the "Chat" tab
2. Type your message in the input field
3. Get AI-powered responses with context from your documents

### Document Management

1. Go to the "Document Upload" tab
2. Upload supported documents (PDF, DOCX, TXT)
3. Documents will be processed and added to the knowledge base
4. Chat with the AI about your documents' content

## 🛠 Technical Architecture

### Components

- **Chat Agent**: Custom implementation using Groq's API
- **Document Processor**: Handles document parsing and vectorization
- **Vector Store**: ChromaDB for efficient similarity search
- **UI Layer**: Streamlit for the web interface

### Key Technologies

- **LLM**: Groq's Mixtral-8x7b-32768
- **Framework**: LangChain
- **Embeddings**: Sentence Transformers
- **Vector DB**: ChromaDB
- **UI**: Streamlit
- **Document Processing**: Unstructured, python-docx, pdfminer.six

## 📦 Project Structure

```curl
program_and_chill/
├── app/
│   ├── agents/
│   │   ├── chat_agent.py
│   │   └── document_processor.py
│   └── utils/
├── static/
├── .env
├── main.py
├── requirements.txt
└── README.md
```

## 🔄 Version History

- **v0.3.0**: Migration to Groq API, improved error handling
- **v0.2.1**: Enhanced document processing, bug fixes
- **v0.2.0**: Added RAG capabilities
- **v0.1.0**: Initial release

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Groq](https://groq.com) for the LLM API
- [LangChain](https://python.langchain.com) for the framework
- [Streamlit](https://streamlit.io) for the UI components
- [ChromaDB](https://www.trychroma.com) for vector storage

## ⚠️ Known Limitations

- Async operations not yet supported
- File size limits apply to document processing
- Single model configuration

## 🔮 Future Enhancements

- Implement async processing
- Add support for more document types
- Enhance error recovery mechanisms
- Add model selection options
- Improve document preprocessing

## 📫 Support

For support, please open an issue in the GitHub repository or contact the maintainers.
