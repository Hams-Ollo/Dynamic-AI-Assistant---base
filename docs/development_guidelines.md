# Development Guidelines

## Code Organization

### Project Structure

```curl
├── app/                        # Core application code
│   ├── agents/                # AI agent definitions and logic
│   ├── config/               # Configuration management
│   ├── models/               # AI/ML model implementations
│   ├── services/            # Business logic and services
│   └── utils/               # Utility functions and helpers
├── frontend/                 # Streamlit UI components
├── tests/                    # Test suite
├── docs/                     # Documentation
└── scripts/                  # Utility scripts
```

## Development Workflow

1. **Environment Setup**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Unix/macOS
   .\venv\Scripts\activate   # Windows
   pip install -r requirements.txt
   ```

2. **Code Quality**

   ```bash
   make lint     # Run linting
   make format   # Format code
   make test     # Run tests
   ```

3. **Git Workflow**

   ```bash
   git checkout -b feature/name
   # Make changes
   git add .
   git commit -m "feat: description"
   git push origin feature/name
   ```

## Best Practices

### Python Coding Standards

- Follow PEP 8
- Use type hints
- Write docstrings
- Keep functions small and focused

### AI Agent Development

- Document agent capabilities
- Include example conversations
- Handle edge cases
- Log important events

### Testing

- Write unit tests
- Include integration tests
- Test edge cases
- Maintain test coverage

### Documentation

- Update docs with changes
- Include code examples
- Document API changes
- Keep README updated

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

1. Port conflicts

   ```bash
   netstat -ano | findstr :<PORT>
   taskkill /PID <PID> /F
   ```

2. Environment issues

   ```bash
   pip install -r requirements.txt --upgrade
   ```

3. Git conflicts

   ```bash
   git stash
   git pull origin main
   git stash pop
   ```

## Additional Resources

- [Python Style Guide](https://peps.python.org/pep-0008/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Git Best Practices](https://git-scm.com/book/en/v2)
