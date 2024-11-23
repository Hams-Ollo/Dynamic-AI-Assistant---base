"""
Test suite for the chat agent implementation.
"""
import os
import pytest
from unittest.mock import Mock, patch
from app.agents.chat_agent import ChatAgent, GroqChatModel
from app.utils.memory import MemoryManager

@pytest.fixture
def mock_config():
    """Fixture for test configuration."""
    return {
        'api_key': 'test_key',
        'model': 'test-model',
    }

@pytest.fixture
def mock_memory_config():
    """Fixture for memory configuration."""
    return {
        'type': 'buffer',
        'path': './data/test_memory'
    }

def test_groq_chat_model_initialization():
    """Test GroqChatModel initialization."""
    model = GroqChatModel(api_key='test_key')
    assert model.model == "llama3-groq-70b-8192-tool-use-preview"
    assert model.temperature == 0.7

@patch('app.agents.chat_agent.GroqChatModel')
def test_chat_agent_initialization(mock_groq):
    """Test ChatAgent initialization."""
    # Setup
    mock_llm = Mock()
    mock_groq.return_value = mock_llm
    
    # Execute
    agent = ChatAgent(api_key='test_key')
    
    # Verify
    assert agent.llm == mock_llm
    assert isinstance(agent.memory, MemoryManager)
    
@patch('app.agents.chat_agent.GroqChatModel')
def test_chat_agent_process_message(mock_groq):
    """Test message processing."""
    # Setup
    mock_llm = Mock()
    mock_llm.generate.return_value = "Test response"
    mock_groq.return_value = mock_llm
    
    # Execute
    agent = ChatAgent(api_key='test_key')
    response = agent.process_message("Hello!")
    
    # Verify
    assert isinstance(response, str)
    assert len(response) > 0
