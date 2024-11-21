"""Sample test file demonstrating testing patterns."""
import pytest
from typing import Dict, Any

def test_sample() -> None:
    """Sample test to demonstrate basic testing pattern."""
    assert True

@pytest.fixture
def sample_config() -> Dict[str, Any]:
    """Fixture providing sample configuration."""
    return {
        "api_key": "test_key",
        "base_url": "https://api.example.com",
        "timeout": 30
    }

class TestSampleClass:
    """Sample test class demonstrating class-based testing."""
    
    def test_with_fixture(self, sample_config: Dict[str, Any]) -> None:
        """Test using a fixture."""
        assert sample_config["api_key"] == "test_key"
        assert sample_config["timeout"] == 30
    
    @pytest.mark.parametrize("input_value,expected", [
        (1, 2),
        (2, 4),
        (3, 6)
    ])
    def test_parametrized(self, input_value: int, expected: int) -> None:
        """Demonstrate parametrized testing."""
        assert input_value * 2 == expected

    @pytest.mark.asyncio
    async def test_async_operation(self) -> None:
        """Demonstrate async testing."""
        result = await self._async_operation()
        assert result == "success"
    
    async def _async_operation(self) -> str:
        """Sample async operation."""
        return "success"
