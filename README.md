# 🚀 Project Template & Implementation

This repository serves dual purposes:

1. A working implementation of an AI-powered application (currently: Podcast & AI Assistant)
2. A template for quickly bootstrapping new Python projects with best practices

## 📋 Template Features

### 🏗️ Project Structure

```curl
project_root/
├── app/                    # Core application code
│   ├── agents/            # AI agents and processors
│   │   ├── __init__.py
│   │   └── chat_agent.py  # Example: Chat implementation
│   └── utils/             # Utility functions
│       ├── __init__.py
│       └── tools.py       # Common utilities
├── frontend/              # UI components
│   └── streamlit.py       # Streamlit interface
├── tests/                 # Test suite
│   └── test_sample.py     # Test examples
├── docs/                  # Documentation
│   ├── api.md            # API documentation
│   └── development.md    # Development guidelines
├── .env.example          # Environment variables template
├── .gitignore           # Git ignore rules
├── requirements.txt     # Production dependencies
├── CHANGELOG.txt       # Version history
└── README.md          # Project documentation
```

### 🎯 Key Features

- **Standardized File Headers**: Consistent documentation across Python files
- **Environment Management**: Ready-to-use virtual environment setup
- **Documentation Templates**: Pre-structured documentation files
- **Testing Framework**: Basic test setup with examples
- **Development Guidelines**: Best practices and coding standards
- **Version Control**: Git setup with .gitignore
- **Dependency Management**: Requirements file structure

## 🛠️ Getting Started

### Prerequisites

- Python 3.8+
- Git
- Virtual environment tool (venv)

### Quick Start

1. **Clone & Rename**

   ```bash
   git clone https://github.com/yourusername/project-template.git new-project
   cd new-project
   ```

2. **Environment Setup**

   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Unix/MacOS
   source venv/bin/activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**

   ```bash
   cp .env.example .env
   # Edit .env with your configurations
   ```

5. **Run Application**

   ```bash
   streamlit run frontend/streamlit.py
   ```

## 📦 Current Implementation: Podcast & AI Assistant

### Features

- **AI Chat Interface**: Groq-powered conversational AI
- **Document Processing**: Support for multiple formats
- **RAG System**: ChromaDB-based knowledge retrieval
- **Modern UI**: Streamlit-based interface

### Tech Stack

- **LLM**: Groq's Mixtral-8x7b-32768
- **Framework**: LangChain
- **Vector Store**: ChromaDB
- **Frontend**: Streamlit
- **Document Processing**: Unstructured, python-docx, pdfminer.six

## 🔧 Development

### File Structure

Each Python file follows a standardized header format:

```python
#-------------------------------------------------------------------------------------#
# File: filename.py
# Description: Brief description of the file's purpose
# Author: @username
#
# INITIAL SETUP:
# 1. Create virtual environment:    python -m venv venv
# 2. Activate virtual environment:
#    - Windows:                    .\venv\Scripts\activate
#    - Unix/MacOS:                 source venv/bin/activate
# 3. Install requirements:         pip install -r requirements.txt
# 4. Create .env file:            cp .env.example .env
# 5. Update dependencies:          pip freeze > requirements.txt
#
#-------------------------------------------------------------------------------------#
```

### Common Tasks

```bash
# Development
pip install -r requirements.txt    # Install dependencies
pytest                            # Run tests
black .                           # Format code
flake8                           # Lint code

# Git Operations
git checkout -b feature-name      # Create new branch
git commit -m "type: message"     # Commit changes
git push origin feature-name      # Push changes
```

## 📝 Documentation

- [API Documentation](docs/api.md)
- [Development Guidelines](docs/development.md)
- [Change Log](CHANGELOG.txt)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📫 Support

For support:

- Open an issue
- Review documentation
- Contact maintainers

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Groq](https://groq.com) - LLM API
- [LangChain](https://python.langchain.com) - AI framework
- [Streamlit](https://streamlit.io) - UI components
- [ChromaDB](https://www.trychroma.com) - Vector storage

---
*This README serves as both documentation for the current project and a template for future projects. Feel free to customize it based on your specific needs.*
