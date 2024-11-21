# Environment Setup Guide

## Prerequisites

- Python 3.8+
- Git
- Make (optional, but recommended)
- Code editor (VSCode recommended)

## Initial Setup

### 1. Repository Setup

```bash
# Clone template
git clone https://github.com/yourusername/project-template.git new-project
cd new-project

# Initialize git
git init
git remote add origin your-repo-url
```

### 2. Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate environment
# Windows
.\venv\Scripts\activate
# Unix/MacOS
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Variables

1. Create environment file:

   ```bash
   cp .env.example .env
   ```

2. Configure variables:

   ```bash
   # API Keys
   GROQ_API_KEY=your_key_here
   
   # Application Settings
   DEBUG=True
   LOG_LEVEL=INFO
   
   # Database Configuration (if needed)
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=your_db_name
   ```

## IDE Setup

### VSCode Configuration

1. Install Extensions:
   - Python
   - Pylance
   - Black Formatter
   - isort
   - GitLens

2. Workspace Settings:

   ```json
   {
     "python.formatting.provider": "black",
     "python.linting.enabled": true,
     "python.linting.flake8Enabled": true,
     "editor.formatOnSave": true,
     "python.analysis.typeCheckingMode": "basic",
     "files.trimTrailingWhitespace": true
   }
   ```

### PyCharm Setup

1. Enable:
   - Black formatter
   - Flake8 linting
   - Type checking
   - Git integration

## Development Tools

### Code Quality Tools

```bash
# Install development dependencies
pip install black flake8 mypy pytest pytest-cov

# Install pre-commit hooks
pre-commit install
```

### Git Configuration

```bash
# Configure git
git config --local user.name "Your Name"
git config --local user.email "your.email@example.com"

# Set up git hooks
cp scripts/pre-commit .git/hooks/
chmod +x .git/hooks/pre-commit
```

## Verification

Run these commands to verify your setup:

```bash
# Check Python version
python --version

# Verify packages
pip list

# Run tests
pytest

# Start application
streamlit run frontend/streamlit.py
```

## Common Issues

### Package Installation Errors

```bash
# Clean install
pip install --no-cache-dir -r requirements.txt

# If using pip-tools
pip-compile requirements.in
pip-sync
```

### Virtual Environment Issues

```bash
# Windows
deactivate
rm -rf venv
python -m venv venv
.\venv\Scripts\activate

# Unix/MacOS
deactivate
rm -rf venv
python -m venv venv
source venv/bin/activate
```

### Port Conflicts

```bash
# Windows
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# Unix/MacOS
lsof -i :8501
kill -9 <PID>
```

## Next Steps

1. Review the [Development Guidelines](./development_guidelines.md)
2. Check out the [API Documentation](./api.md)
3. Read the [Contributing Guide](./CONTRIBUTING.md)

## Docker Setup (Optional)

### Local Development

```bash
# Build image
docker build -t project-name .

# Run container
docker run -p 8501:8501 project-name

# Development with volume mount
docker run -v $(pwd):/app -p 8501:8501 project-name
```

### Production

```bash
# Build production image
docker build -t project-name:prod -f Dockerfile.prod .

# Run with environment file
docker run --env-file .env -p 8501:8501 project-name:prod
```

---
*This setup guide serves as both instructions for the current project and a template for future projects.*
