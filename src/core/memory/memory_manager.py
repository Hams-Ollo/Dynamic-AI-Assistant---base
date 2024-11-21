#-------------------------------------------------------------------------------------#
# File: memory_manager.py
# Description: Memory management system for storing and retrieving agent data
# Author: @hams_ollo
# Version: 0.0.3
# Last Updated: [2024-11-21]
#-------------------------------------------------------------------------------------#

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import json
from pathlib import Path

class BaseMemory(ABC):
    """
    Abstract base class for memory systems.
    Implement this class to create different types of memory (e.g., simple, vector, etc.).
    """

    @abstractmethod
    def add(self, key: str, value: Any) -> None:
        """Add an item to memory."""
        pass

    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """Retrieve an item from memory."""
        pass

    @abstractmethod
    def search(self, query: str) -> List[Any]:
        """Search memory for relevant items."""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Clear all items from memory."""
        pass

class SimpleMemory(BaseMemory):
    """
    Simple key-value memory implementation.
    Useful for basic agent memory needs.
    """

    def __init__(self, max_items: int = 1000):
        self.max_items = max_items
        self.memory: Dict[str, Any] = {}

    def add(self, key: str, value: Any) -> None:
        if len(self.memory) >= self.max_items:
            # Remove oldest item if at capacity
            oldest_key = next(iter(self.memory))
            del self.memory[oldest_key]
        self.memory[key] = value

    def get(self, key: str) -> Optional[Any]:
        return self.memory.get(key)

    def search(self, query: str) -> List[Any]:
        # Simple string matching search
        results = []
        for value in self.memory.values():
            if isinstance(value, (str, dict)) and query.lower() in str(value).lower():
                results.append(value)
        return results

    def clear(self) -> None:
        self.memory.clear()

class MemoryManager:
    """
    Manages different types of memory systems for agents.
    Supports multiple memory backends and persistence.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the memory manager.

        Args:
            config: Configuration dictionary for memory systems
        """
        self.config = config
        self.memories: Dict[str, BaseMemory] = {}
        self._initialize_memories()

    def _initialize_memories(self) -> None:
        """Initialize configured memory systems."""
        memory_configs = self.config.get("stores", {})
        
        for memory_id, memory_config in memory_configs.items():
            memory_type = memory_config.get("type", "simple")
            
            if memory_type == "simple":
                self.memories[memory_id] = SimpleMemory(
                    max_items=memory_config.get("max_items", 1000)
                )
            # Add other memory type initializations here
            # elif memory_type == "vector":
            #     self.memories[memory_id] = VectorMemory(**memory_config)

    def get_memory(self, memory_id: str) -> Optional[BaseMemory]:
        """
        Get a memory system by ID.

        Args:
            memory_id: ID of the memory system

        Returns:
            Memory system instance or None if not found
        """
        return self.memories.get(memory_id)

    def create_memory(self, memory_id: str, memory_type: str = "simple", **kwargs) -> BaseMemory:
        """
        Create a new memory system.

        Args:
            memory_id: ID for the new memory system
            memory_type: Type of memory system to create
            **kwargs: Additional configuration for the memory system

        Returns:
            Created memory system instance
        """
        if memory_type == "simple":
            memory = SimpleMemory(**kwargs)
        # Add other memory type creation here
        else:
            raise ValueError(f"Unsupported memory type: {memory_type}")

        self.memories[memory_id] = memory
        return memory

    def remove_memory(self, memory_id: str) -> None:
        """
        Remove a memory system.

        Args:
            memory_id: ID of the memory system to remove
        """
        if memory_id in self.memories:
            self.memories[memory_id].clear()
            del self.memories[memory_id]
