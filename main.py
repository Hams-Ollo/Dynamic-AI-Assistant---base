#-------------------------------------------------------------------------------------#
# File: main.py
# Description: Main application entry point and process manager
# Author: @hams_ollo
# Version: 0.0.3
# Last Updated: [2024-11-21]
#-------------------------------------------------------------------------------------#
# SETUP GUIDE:
#
# Initial Setup:
# 1. Create virtual environment  -> python -m venv venv
# 2. Activate virtual environment:
#    - Windows                   -> .\venv\Scripts\activate
#    - Unix/MacOS               -> source venv/bin/activate
# 3. Install requirements       -> pip install -r requirements.txt
# 4. Copy environment file      -> cp .env.example .env
# 5. Add your Groq API key to .env
#
# Running the Application:
# 1. Start the application      -> python main.py     /     streamlit run main.py
# 2. Access the web interface   -> http://localhost:8501
# 3. Stop the application      -> Ctrl+C
# 4. Deactivate virtual env    -> deactivate
#
# Development Commands:
# 1. Update dependencies       -> pip freeze > requirements.txt
# 2. Run with debug logging   -> python main.py --log-level=debug
# 3. Clear Streamlit cache    -> streamlit cache clear
#
# Git Quick Reference:
# 1. Initialize repository    -> git init
# 2. Add files to staging    -> git add .
# 3. Commit changes         -> git commit -m "your message"
# 4. Create new branch      -> git checkout -b branch-name
# 5. Switch branches        -> git checkout branch-name
# 6. Push to remote         -> git push -u origin branch-name
# 7. Pull latest changes    -> git pull origin branch-name
# 8. Check status          -> git status
# 9. View commit history   -> git log
#
#-------------------------------------------------------------------------------------#

#----------# IMPORTS #----------#
import os
import sys
import logging
from pathlib import Path
from typing import Optional, Dict, Any

from app.core.config import load_config
from app.core.logging import setup_logging
from app.agents.chat_agent import ChatAgent
from app.utils.memory import MemoryManager

#----------# CONFIGURATION #----------#
def initialize_app(config_path: Optional[str] = None) -> Dict[str, Any]:
    """Initialize the application with configuration and logging."""
    config = load_config(config_path)
    setup_logging(config.get('log_level', 'INFO'))
    return config

#----------# MAIN APPLICATION #----------#
class ChatSystem:
    """Main application class for the chat system."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.memory_manager = MemoryManager(config.get('memory', {}))
        self.agent = ChatAgent(config.get('agent', {}))
    
    def start(self):
        """Start the chat system."""
        try:
            self.agent.initialize(self.memory_manager)
            logging.info("Chat system started successfully")
        except Exception as e:
            logging.error(f"Failed to start chat system: {str(e)}")
            sys.exit(1)
    
    def stop(self):
        """Gracefully stop the chat system."""
        try:
            self.agent.cleanup()
            self.memory_manager.cleanup()
            logging.info("Chat system stopped successfully")
        except Exception as e:
            logging.error(f"Error during system shutdown: {str(e)}")

def main():
    """Main entry point for the application."""
    config = initialize_app()
    
    system = ChatSystem(config)
    try:
        system.start()
        # Main application loop would go here
        # For now, we'll just keep it running until interrupted
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Shutting down...")
    finally:
        system.stop()

if __name__ == "__main__":
    main()
