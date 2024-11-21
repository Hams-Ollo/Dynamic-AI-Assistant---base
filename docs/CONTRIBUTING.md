# Contributing to Program_and_Chill

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/Program_and_Chill.git`
3. Create your feature branch: `git checkout -b feature/amazing-feature`
4. Install dependencies: `make install`

## Development Workflow

1. Make your changes
2. Run tests: `make test`
3. Run linting: `make lint`
4. Format code: `make format`
5. Commit your changes: `git commit -m "feat: add amazing feature"`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

## Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```bash
<type>(<scope>): <description>

[optional body]

[optional footer]
```

Types:

- feat: New feature
- fix: Bug fix
- docs: Documentation
- style: Formatting
- refactor: Code restructuring
- test: Adding tests
- chore: Maintenance

Example:

```curl
feat(auth): implement JWT authentication

- Add JWT token generation
- Implement token validation middleware
- Add refresh token functionality

Closes #123
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for functions and classes
- Keep functions focused and small
- Write meaningful variable names

## Testing

- Write unit tests for new features
- Maintain test coverage above 80%
- Test edge cases
- Write integration tests for API endpoints

## Documentation

- Update README.md if needed
- Document new features
- Add docstrings to new functions/classes
- Update API documentation

## Questions?

Feel free to open an issue or contact the maintainers.
