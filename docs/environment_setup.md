# Environment Setup Guide

## Prerequisites

- Python 3.8+
- Git
- Make (optional, but recommended)

## Initial Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/YOUR_USERNAME/Program_and_Chill.git
   cd Program_and_Chill
   ```

2. **Create Virtual Environment**

   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Unix/macOS
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Environment Variables

1. **Create Environment File**

   ```bash
   cp .env.example .env
   ```

2. **Required Environment Variables**

   ```bash
   # API Keys
   OPENAI_API_KEY=your_key_here
   GROQ_API_KEY=your_key_here
   LEONARDO_API_KEY=your_key_here

   # Application Settings
   DEBUG=True
   LOG_LEVEL=INFO

   # Database Configuration
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=your_db_name
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   ```

## Development Tools

1. **Code Quality Tools**

   ```bash
   pip install black flake8 mypy pytest
   ```

2. **Git Hooks (Optional)**

   ```bash
   pre-commit install
   ```

## IDE Setup

### VSCode

1. Install Extensions:
   - Python
   - Pylance
   - Git Lens
   - Black Formatter
   - Docker

2. Recommended Settings:

   ```json
   {
     "python.formatting.provider": "black",
     "python.linting.enabled": true,
     "python.linting.flake8Enabled": true,
     "editor.formatOnSave": true,
     "python.analysis.typeCheckingMode": "basic"
   }
   ```

### PyCharm

1. Enable:
   - Black formatter
   - Flake8 linting
   - Type checking
   - Git integration

## Docker Setup (Optional)

1. **Install Docker**
   - [Docker Desktop](https://www.docker.com/products/docker-desktop)

2. **Build Image**

   ```bash
   docker build -t program-and-chill .
   ```

3. **Run Container**

   ```bash
   docker run -p 8501:8501 program-and-chill
   ```

## Troubleshooting

### Common Issues

1. **Package Installation Errors**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt --no-cache-dir
   ```

2. **Virtual Environment Issues**

   ```bash
   deactivate
   rm -rf venv
   python -m venv venv
   ```

3. **Port Conflicts**

   ```bash
   # Windows
   netstat -ano | findstr :8501
   taskkill /PID <PID> /F

   # Unix/macOS
   lsof -i :8501
   kill -9 <PID>
   ```

## Verification

Run these commands to verify your setup:

```bash
# Activate virtual environment
source venv/bin/activate  # Unix/macOS
.\venv\Scripts\activate   # Windows

# Verify Python version
python --version

# Verify package installation
pip list

# Run tests
pytest

# Start application
streamlit run frontend/streamlit.py
```

## Next Steps

- Review the [Development Guidelines](./development_guidelines.md)
- Check out the [Contributing Guide](./contributing.md)
- Explore the [API Documentation](./api.md)
