# Developer Quick Reference

A comprehensive guide for the Dynamic AI Assistant development workflow.

## 🚀 Initial Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Unix/MacOS:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Setup environment
cp .env.example .env

# Update dependencies
pip freeze > requirements.txt
```

## 💻 Development Workflow

### 1. Environment Management

```bash
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Unix/MacOS

# Dependencies
pip install -r requirements.txt  # Install
pip freeze > requirements.txt    # Update
pip install package==version    # Specific version
```

### 2. Git Workflow

```bash
# Basic workflow
git status                      # Check status
git pull origin main           # Get latest
git checkout -b feature/name   # New branch
git add .                      # Stage all
git commit -m "type: message"  # Commit
git push origin branch-name    # Push

# Fix common issues
git stash                     # Save changes
git stash pop                 # Restore changes
git reset --hard HEAD         # Undo all
git reset --soft HEAD^        # Undo commit
git clean -fd                 # Remove untracked
```

### 3. Code Quality

```bash
# Formatting
black .                       # Format code
isort .                      # Sort imports
flake8                       # Lint code
mypy .                       # Type check

# Testing
pytest                       # Run tests
pytest -v                    # Verbose
pytest -k "test_name"        # Specific test
pytest --cov=app tests/      # Coverage
```

### 4. Docker Operations

```bash
# Basic operations
docker build -t name .       # Build image
docker run -p 8501:8501 name # Run container
docker ps                    # List running
docker stop <container-id>   # Stop container
docker-compose up           # Start services
```

### 5. Database Management

```bash
# PostgreSQL
psql -U username -d dbname   # Connect
\l                          # List DBs
\dt                         # List tables
\q                          # Quit

# MongoDB
mongosh                     # Connect shell
show dbs                    # List DBs
use dbname                  # Switch DB
show collections            # List collections
```

### 6. API Testing

```bash
# cURL
curl -X GET url            # GET request
curl -X POST url -d data   # POST request

# HTTPie (more readable)
http GET url              # GET request
http POST url key=value   # POST request
```

### 7. Debugging

```bash
# Python debugger
breakpoint()              # Set breakpoint
n                        # Next line
s                        # Step into
c                        # Continue
p variable              # Print variable
q                       # Quit

# Logging
logger.debug("message")  # Debug level
logger.info("message")   # Info level
logger.error("message")  # Error level
```

### 8. Performance Monitoring

```bash
# Profiling
python -m cProfile script.py  # Profile script
memory_profiler              # Memory usage
line_profiler               # Line-by-line

# Monitoring
top                         # System usage
htop                       # Better top
df -h                      # Disk usage
```

### 9. Security

```bash
# Environment
cp .env.example .env       # Create env file
chmod 600 .env             # Secure perms

# SSH
ssh-keygen -t ed25519     # Generate key
ssh-copy-id user@host     # Copy key
```

## 🔧 Quick Fixes

### Port Conflicts

```bash
netstat -ano | findstr :8501  # Find process
taskkill /PID <PID> /F       # Kill process
```

### Virtual Environment Issues

```bash
deactivate                    # Exit venv
rm -rf venv                   # Remove venv
python -m venv venv           # Recreate
```

### Package Issues

```bash
pip install --no-cache-dir    # Clean install
pip install -U package        # Upgrade
```

## ⚡ Productivity Tips

### VSCode Shortcuts

- `Ctrl+Shift+P` - Command palette
- `Ctrl+P` - Quick open
- `Ctrl+`` - Terminal
- `Alt+Up/Down` - Move line
- `Ctrl+D` - Multi-select

### Terminal Shortcuts

- `Ctrl+R` - Search history
- `Ctrl+L` - Clear screen
- `!!` - Last command
- `cd -` - Previous dir

## 📝 Best Practices

### Commit Message Types

- `feat`: new feature
- `fix`: bug fix
- `docs`: documentation
- `style`: formatting
- `refactor`: code structure
- `test`: adding tests
- `chore`: maintenance

### Python Guidelines

- Use type hints
- Write docstrings
- Follow PEP 8
- Keep functions small
- Test edge cases

### Development Reminders

1. Always pull before starting work
2. Keep commits atomic and descriptive
3. Document significant changes
4. Test before pushing
5. Review your own code first

## 🚀 Streamlit Commands

### Development

```bash
streamlit run app.py                    # Run app
streamlit run app.py --server.port 8502 # Custom port
streamlit run app.py --logger.level=debug # Debug mode
streamlit cache clear                    # Clear cache
streamlit config show                    # Show config
streamlit create my_component            # New component
```

### Production

```bash
# Run in production
streamlit run app.py --server.address=0.0.0.0

# Set memory limit
streamlit run app.py --server.maxUploadSize=50

# Enable authentication
streamlit run app.py --server.enableCORS=false
```
