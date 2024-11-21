# Development Guidelines

## Code Organization

### Project Structure

```curl
project_root/
├── app/                        # Core application code
│   ├── agents/                # AI agent definitions and logic
│   │   ├── __init__.py
│   │   └── chat_agent.py     # Example: Chat implementation
│   ├── config/               # Configuration management
│   ├── models/               # Data models and schemas
│   ├── services/            # Business logic and services
│   └── utils/               # Utility functions and helpers
├── frontend/                 # UI components
│   └── streamlit.py         # Example: Streamlit interface
├── tests/                    # Test suite
│   ├── unit/               # Unit tests
│   └── integration/        # Integration tests
├── docs/                     # Documentation
└── scripts/                  # Utility scripts
```

## Development Workflow

### 1. Environment Setup

```bash
# Create virtual environment
python -m venv venv

# Activate environment
# Windows
.\venv\Scripts\activate
# Unix/MacOS
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Code Quality

```bash
# Format code
black .
isort .

# Run linting
flake8
pylint app/

# Type checking
mypy app/

# Run tests
pytest
pytest --cov=app tests/
```

### 3. Git Workflow

```bash
# Create feature branch
git checkout -b feature/name

# Make changes
git add .
git commit -m "feat: description"

# Push changes
git push origin feature/name
```

## Best Practices

### Python Coding Standards

1. **Follow PEP 8**
   - Use 4 spaces for indentation
   - Maximum line length of 88 characters (Black default)
   - Clear variable and function names

2. **Type Hints**

   ```python
   def process_data(input_data: List[str]) -> Dict[str, Any]:
       """Process input data and return results."""
       results: Dict[str, Any] = {}
       return results
   ```

3. **Docstrings**

   ```python
   def complex_function(param1: str, param2: int) -> bool:
       """
       Brief description of function.

       Args:
           param1 (str): Description of param1
           param2 (int): Description of param2

       Returns:
           bool: Description of return value

       Raises:
           ValueError: When param1 is empty
       """
       pass
   ```

4. **File Headers**

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

### Error Handling

1. **Use Specific Exceptions**

   ```python
   try:
       process_data()
   except ValueError as e:
       logging.error(f"Invalid data format: {e}")
   except IOError as e:
       logging.error(f"IO operation failed: {e}")
   ```

2. **Logging**

   ```python
   import logging

   logging.basicConfig(
       level=logging.INFO,
       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
   )
   ```

### Testing

1. **Unit Tests**

   ```python
   def test_process_data():
       input_data = ["test"]
       result = process_data(input_data)
       assert isinstance(result, dict)
       assert "status" in result
   ```

2. **Integration Tests**

   ```python
   @pytest.mark.integration
   def test_api_endpoint():
       response = client.get("/api/data")
       assert response.status_code == 200
   ```

### Documentation

1. **Keep README Updated**
   - Project overview
   - Setup instructions
   - Usage examples
   - Contributing guidelines

2. **API Documentation**
   - Endpoint descriptions
   - Request/response formats
   - Authentication details
   - Error codes

3. **Code Comments**
   - Complex logic explanation
   - Warning about edge cases
   - TODO items for future work

## Common Commands

```bash
# Development
make run          # Run application
make test         # Run tests
make lint         # Check code style
make format       # Format code
make clean        # Clean cache files

# Git
git fetch         # Update branches
git rebase main   # Rebase on main
git push -f       # Force push after rebase
```

## Troubleshooting

### Common Issues

1. **Port Conflicts**

   ```bash
   # Windows
   netstat -ano | findstr :<PORT>
   taskkill /PID <PID> /F
   ```

2. **Environment Issues**

   ```bash
   pip install -r requirements.txt --upgrade
   ```

3. **Git Conflicts**

   ```bash
   git stash
   git pull origin main
   git stash pop
   ```

## Additional Resources

- [Python Style Guide](https://peps.python.org/pep-0008/)
- [Type Hints Guide](https://mypy.readthedocs.io/)
- [Git Best Practices](https://git-scm.com/book/en/v2)

---
*These guidelines serve as both development standards for the current project and a template for future projects.*
