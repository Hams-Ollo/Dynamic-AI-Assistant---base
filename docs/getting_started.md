# Getting Started

## Quick Start Guide

This guide will help you get up and running with the Program_and_Chill project quickly.

## Prerequisites

Before you begin, ensure you have:

- Python 3.8 or higher
- Git
- A code editor (VSCode recommended)
- Basic knowledge of Python and AI concepts

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/YOUR_USERNAME/Program_and_Chill.git
   cd Program_and_Chill
   ```

2. **Set Up Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Unix/macOS
   .\venv\Scripts\activate   # Windows
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**

   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configurations
   ```

## First Steps

### 1. Run the Application

```bash
streamlit run frontend/streamlit.py
```

### 2. Create Your First Agent

```python
from app.agents import BaseAgent

class MyFirstAgent(BaseAgent):
    def __init__(self, config):
        super().__init__(config)
        self.capabilities = ["chat"]

    async def process_message(self, message: str) -> str:
        return f"Echo: {message}"
```

### 3. Test the Agent

```python
agent = MyFirstAgent({"name": "echo_agent"})
response = await agent.process_message("Hello, World!")
print(response)  # Output: Echo: Hello, World!
```

## Project Structure

```curl
├── requirements.txt
├── Makefile
├── app/                 # Core application code
├── frontend/           # Streamlit UI
├── tests/             # Test suite
└── docs/              # Documentation
```

## Key Features

1. **Multi-Agent System**
   - Create custom agents
   - Chain agents together
   - Manage agent communication

2. **Streamlit Frontend**
   - Interactive UI
   - Real-time updates
   - Visualization tools

3. **Development Tools**
   - Code formatting
   - Testing framework
   - Documentation

## Common Tasks

### Running Tests

```bash
pytest tests/
```

### Formatting Code

```bash
black .
isort .
```

### Checking Types

```bash
mypy app/
```

## Next Steps

1. Review the [Development Guidelines](./development_guidelines.md)
2. Explore the [API Documentation](./api.md)
3. Learn about [Agent Architecture](./agents.md)
4. Join our community:
   - GitHub Discussions
   - Discord Channel
   - Stack Overflow Tag

## Troubleshooting

### Common Issues

1. **Port Already in Use**

   ```bash
   netstat -ano | findstr :8501
   taskkill /PID <PID> /F
   ```

2. **Package Conflicts**

   ```bash
   pip install -r requirements.txt --upgrade
   ```

3. **Environment Issues**

   ```bash
   deactivate
   rm -rf venv
   python -m venv venv
   ```

## Best Practices

1. **Code Organization**
   - Follow project structure
   - Use meaningful names
   - Keep files focused

2. **Development Flow**
   - Write tests first
   - Document your code
   - Use type hints

3. **Git Workflow**
   - Create feature branches
   - Write clear commit messages
   - Keep PRs focused

## Resources

- [Python Documentation](https://docs.python.org/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Project Wiki](https://github.com/YOUR_USERNAME/Program_and_Chill/wiki)

## Support

Need help? Try these resources:

- Check the documentation
- Open an issue
- Join our community channels

## Contributing

Want to contribute? Great!

1. Check out [CONTRIBUTING.md](./contributing.md)
2. Pick an issue to work on
3. Submit a pull request

## License

This project is licensed under the MIT License. See [LICENSE](../LICENSE) for details.
