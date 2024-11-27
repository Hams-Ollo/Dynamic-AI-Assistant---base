# Changelog

All notable changes to the Dynamic AI Assistant will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.4.0] - 2024-03-20

### Changed

- Upgraded to LLaMA 3 70B model with 8K context window
- Enhanced configuration system with robust env variable handling
- Added comprehensive system workflow documentation
- Improved error handling and logging
- Project renamed to Dynamic AI Assistant

### Added

- Detailed system workflow documentation
- Comprehensive system prompt
- Robust environment variable parsing
- Enhanced model initialization logging
- Support for LLaMA 3 70B model
- ChromaDB integration improvements

### Fixed

- ChromaDB dependency and import issues
- Streamlit frontend compatibility
- Environment variable parsing
- Documentation consistency

## [0.3.0] - 2024-03-19

### Changed (0.3.0)

- Migrated from OpenAI to Groq for LLM functionality
- Updated chat agent to use Mixtral-8x7b-32768 model
- Modified API key handling to use GROQ_API_KEY
- Removed OpenAI dependencies
- Enhanced error handling for Groq API integration

### Added (0.3.0)

- Support for Groq's Mixtral model
- Improved token handling with 4096 token limit
- Better error messages for API initialization

### Removed

- OpenAI integration and dependencies
- GPT model configurations

## [0.2.1] - 2024-03-19

### Changed (0.2.1)

- Updated dependencies to use newer package versions
- Migrated to langchain-specific packages (openai, huggingface, chroma)
- Improved error handling for API quota limits
- Enhanced logging for better debugging
- Updated document processing validation

### Fixed (0.2.1)

- Deprecation warnings from LangChain packages
- OpenAI API quota handling
- Vector store initialization issues
- Document processing error handling

## [0.2.0] - 2024-03-19

### Added (0.2.0)

- Enhanced Word document processing using UnstructuredWordDocumentLoader
- Automatic creation of vector store directory
- Source metadata tracking for uploaded documents
- Comprehensive logging throughout document processing pipeline

### Changed (0.2.0)

- Replaced Docx2txtLoader with more robust UnstructuredWordDocumentLoader
- Improved error handling with detailed stack traces
- Enhanced logging messages for better debugging
- Added validation for vector store existence before querying

### Fixed (0.2.0)

- Word document processing issues
- Vector store initialization errors
- Missing directory creation for persistence

## [0.1.0] - 2024-03-19

### Added (0.1.0)

- Initial release of Program & Chill AI Assistant
- Document upload functionality with PDF, TXT, DOC, DOCX support
- RAG integration with ChromaDB
- Multi-agent architecture with DocumentProcessor and ChatAgent
- Streamlit-based user interface
