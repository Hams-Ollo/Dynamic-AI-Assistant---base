#-------------------------------------------------------------------------------------#
# File: config_manager.py
# Description: Configuration management system for handling application settings
# Author: @hams_ollo
# Version: 0.0.3
# Last Updated: [2024-11-21]
#-------------------------------------------------------------------------------------#

import os
import json
from typing import Any, Dict, Optional
from pathlib import Path

class ConfigManager:
    """
    Manages configuration loading and validation for the multi-agent system.
    Supports hierarchical configuration with defaults and custom overrides.
    """

    def __init__(self, config_dir: str = "config"):
        """
        Initialize the configuration manager.

        Args:
            config_dir (str): Path to the configuration directory
        """
        self.config_dir = Path(config_dir)
        self.default_config = self._load_config_dir(self.config_dir / "default")
        self.custom_config = self._load_config_dir(self.config_dir / "custom")
        self.env_config = self._load_env_config()
        self.merged_config = self._merge_configs()

    def _load_config_dir(self, config_path: Path) -> Dict[str, Any]:
        """
        Load all JSON configuration files from a directory.

        Args:
            config_path (Path): Path to the configuration directory

        Returns:
            Dict containing merged configurations from all JSON files
        """
        if not config_path.exists():
            return {}

        config = {}
        for file_path in config_path.glob("*.json"):
            with open(file_path, 'r') as f:
                config.update(json.load(f))
        return config

    def _load_env_config(self) -> Dict[str, Any]:
        """
        Load configuration from environment variables.
        Environment variables should be prefixed with 'AGENT_'.

        Returns:
            Dict containing configuration from environment variables
        """
        config = {}
        for key, value in os.environ.items():
            if key.startswith("AGENT_"):
                config_key = key[6:].lower()  # Remove 'AGENT_' prefix
                try:
                    # Try to parse as JSON for complex values
                    config[config_key] = json.loads(value)
                except json.JSONDecodeError:
                    # Use as string if not valid JSON
                    config[config_key] = value
        return config

    def _merge_configs(self) -> Dict[str, Any]:
        """
        Merge configurations in order of precedence:
        1. Environment variables
        2. Custom config
        3. Default config

        Returns:
            Dict containing the merged configuration
        """
        config = self.default_config.copy()
        config.update(self.custom_config)
        config.update(self.env_config)
        return config

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.

        Args:
            key (str): Configuration key
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        return self.merged_config.get(key, default)

    def get_agent_config(self, agent_id: str) -> Dict[str, Any]:
        """
        Get configuration for a specific agent.

        Args:
            agent_id (str): ID of the agent

        Returns:
            Dict containing agent-specific configuration
        """
        agents_config = self.get("agents", {})
        return agents_config.get(agent_id, {})

    def save_custom_config(self, config: Dict[str, Any], filename: str = "custom.json") -> None:
        """
        Save a custom configuration to file.

        Args:
            config (Dict[str, Any]): Configuration to save
            filename (str): Name of the configuration file
        """
        custom_dir = self.config_dir / "custom"
        custom_dir.mkdir(exist_ok=True)
        
        with open(custom_dir / filename, 'w') as f:
            json.dump(config, f, indent=4)
        
        # Reload configurations
        self.custom_config = self._load_config_dir(self.config_dir / "custom")
        self.merged_config = self._merge_configs()
