#-------------------------------------------------------------------------------------#
# File: base_agent.py
# Description: Base agent class providing core functionality for all agent types
# Author: @hams_ollo
# Version: 0.0.3
# Last Updated: [2024-11-21]
#-------------------------------------------------------------------------------------#

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class BaseAgent(ABC):
    """
    Abstract base class for all agents in the system.
    Provides a common interface that all agents must implement.
    """

    def __init__(self, agent_id: str, config: Dict[str, Any]):
        """
        Initialize the base agent.

        Args:
            agent_id (str): Unique identifier for the agent
            config (Dict[str, Any]): Configuration dictionary for the agent
        """
        self.agent_id = agent_id
        self.config = config
        self.memory = None  # Can be initialized with specific memory system
        self._initialize()

    def _initialize(self) -> None:
        """
        Initialize agent-specific components.
        Override this method to add custom initialization logic.
        """
        pass

    @abstractmethod
    async def process(self, input_data: Any) -> Any:
        """
        Process input data and return a response.
        Must be implemented by all agent classes.

        Args:
            input_data: The input data to process

        Returns:
            The processed result
        """
        pass

    @abstractmethod
    async def handle_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle incoming messages from other agents or the system.

        Args:
            message: The incoming message

        Returns:
            The response message
        """
        pass

    def update_config(self, new_config: Dict[str, Any]) -> None:
        """
        Update the agent's configuration.

        Args:
            new_config: New configuration parameters
        """
        self.config.update(new_config)

    @abstractmethod
    def save_state(self) -> Dict[str, Any]:
        """
        Save the current state of the agent.

        Returns:
            A dictionary containing the agent's state
        """
        pass

    @abstractmethod
    def load_state(self, state: Dict[str, Any]) -> None:
        """
        Load a previously saved state.

        Args:
            state: The state to load
        """
        pass

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.agent_id})"
