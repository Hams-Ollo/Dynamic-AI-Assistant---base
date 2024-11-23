# Environment Setup Guide

This guide provides detailed instructions for setting up your development environment for the Multi-Agent Chatbot Template.

## System Requirements

### Minimum Requirements

- Python 3.8 or higher
- 4GB RAM
- 2GB free disk space

### Recommended

- Python 3.10 or higher
- 8GB RAM
- 4GB free disk space
- SSD for storage

## Python Environment Setup

### 1. Python Installation

#### Windows

1. Download Python from [python.org](https://python.org)
2. Run the installer, ensuring you check "Add Python to PATH"
3. Verify installation:

   ```bash
   python --version
   pip --version
   ```

#### macOS

```bash
# Using Homebrew
brew install python

# Verify installation
python3 --version
pip3 --version
```

#### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

### 2. Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate on Windows
.\venv\Scripts\activate

# Activate on Unix/MacOS
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip
```

## Dependencies Installation

```bash
# Install required packages
pip install -r requirements.txt

# Optional: Install development dependencies
pip install -r requirements-dev.txt
```

## Environment Configuration

### 1. Environment Variables

Create a `.env` file in the project root:

```env
# Required
GROQ_API_KEY=your-groq-api-key

# Optional
LOG_LEVEL=INFO
MEMORY_TYPE=buffer
MEMORY_PATH=./data/memory
MAX_TOKENS=4096
TEMPERATURE=0.7
```

### 2. Configuration Options

#### Logging Configuration

```python
# In .env
LOG_LEVEL=DEBUG  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT=detailed  # Options: simple, detailed
LOG_FILE=app.log  # Default: None (console only)
```

#### Memory Configuration

```python
# In .env
MEMORY_TYPE=vector  # Options: buffer, vector
MEMORY_PATH=./data/memory
MEMORY_MAX_ITEMS=1000
MEMORY_CLEANUP_INTERVAL=3600  # In seconds
```

#### LLM Configuration

```python
# In .env
MODEL_NAME=llama3-groq-70b-8192-tool-use-preview
TEMPERATURE=0.7
MAX_TOKENS=4096
TOP_P=0.9
```

## Directory Structure Setup

```bash
# Create necessary directories
mkdir -p data/memory
mkdir -p logs
mkdir -p tests/fixtures
```

## Development Tools

### 1. Code Formatting

```bash
# Install formatters
pip install black isort

# Run formatters
black .
isort .
```

### 2. Type Checking

```bash
# Install mypy
pip install mypy

# Run type checking
mypy app/
```

### 3. Testing Tools

```bash
# Install testing tools
pip install pytest pytest-cov pytest-asyncio

# Run tests
pytest
```

## IDE Setup

### VSCode

1. Install Python extension
2. Configure settings.json:

   ```json
   {
     "python.defaultInterpreterPath": "./venv/bin/python",
     "python.formatting.provider": "black",
     "python.linting.enabled": true,
     "python.linting.mypyEnabled": true
   }
   ```

### PyCharm

1. Set project interpreter to venv
2. Enable Black formatter
3. Configure pytest as test runner

## Troubleshooting

### Common Issues

1. **Virtual Environment Not Activating**

   ```bash
   # Windows
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   
   # Unix
   chmod +x venv/bin/activate
   ```

2. **Package Installation Errors**

   ```bash
   pip install --upgrade pip setuptools wheel
   pip install -r requirements.txt --no-cache-dir
   ```

3. **Memory Path Issues**

   ```bash
   # Ensure directories exist
   mkdir -p data/memory
   chmod 755 data/memory
   ```

## Next Steps

1. Review the [Getting Started Guide](getting_started.md)
2. Check the [Development Guidelines](development_guidelines.md)
3. Explore [Agent Development](guides/agents.md)

## Additional Resources

- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [pip Documentation](https://pip.pypa.io/en/stable/)
- [Groq API Documentation](https://groq.com/docs)
