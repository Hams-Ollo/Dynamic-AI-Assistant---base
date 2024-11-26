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
import time
from colorama import init, Fore, Style
import asyncio

from app.core.config import load_config
from app.core.logging import setup_logging
from app.agents.chat_agent import ChatAgent
from app.utils.memory import MemoryManager

# Initialize colorama for Windows support
init()

#----------# CONFIGURATION #----------#
def initialize_app(config_path: Optional[str] = None) -> Dict[str, Any]:
    """Initialize the application with configuration and logging."""
    print(f"\n{Fore.CYAN}🚀 Initializing AI Chat System...{Style.RESET_ALL}")
    config = load_config(config_path)
    setup_logging(config.get('log_level', 'INFO'))
    return config

def print_welcome_message():
    """Print a stylish welcome message."""
    print(f"\n{Fore.GREEN}{'='*60}")
    print(f"🤖 Welcome to the Neural Chat Interface v1.0")
    print(f"🧠 Powered by Groq LLM & LangChain")
    print(f"⚡ Ready to assist you with lightning-fast responses")
    print(f"❓ Type 'help' for commands or 'exit' to quit")
    print(f"{'='*60}{Style.RESET_ALL}\n")

def print_help():
    """Print available commands."""
    print(f"\n{Fore.YELLOW}Available Commands:")
    print("🔹 help  - Show this help message")
    print("🔹 clear - Clear the screen")
    print("🔹 exit  - Exit the chat")
    print(f"Just type your message to chat with the AI!{Style.RESET_ALL}\n")

#----------# MAIN APPLICATION #----------#
class ChatSystem:
    """Main application class for the chat system."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the chat system."""
        self.config = config
        self.memory_manager = MemoryManager(config.get('memory', {}))
        self.agent = ChatAgent(config.get('agent', {}))
        
    async def initialize(self):
        """Initialize all system components."""
        try:
            # Initialize memory system
            await self.memory_manager.initialize()
            logging.info("Memory system initialized")
            
            # Initialize chat agent
            await self.agent.initialize()
            logging.info("Chat agent initialized")
            
        except Exception as e:
            logging.error(f"Failed to start chat system: {str(e)}")
            await self.cleanup()
            raise
            
    async def cleanup(self):
        """Cleanup system resources."""
        try:
            logging.info("Starting system cleanup...")
            
            # Cleanup components in parallel
            cleanup_tasks = []
            
            if hasattr(self, 'agent') and self.agent:
                cleanup_tasks.append(self.agent.cleanup())
                
            if hasattr(self, 'memory_manager') and self.memory_manager:
                cleanup_tasks.append(self.memory_manager.cleanup())
                
            if cleanup_tasks:
                # Wait for all cleanup tasks with timeout
                await asyncio.wait_for(
                    asyncio.gather(*cleanup_tasks, return_exceptions=True),
                    timeout=5.0
                )
            
            logging.info("System cleanup completed")
            
        except asyncio.TimeoutError:
            logging.error("System cleanup timed out")
        except Exception as e:
            logging.error(f"Error during system cleanup: {str(e)}")
            
async def main():
    """Main entry point for the chat system."""
    system = None
    try:
        print("\n🚀 Initializing AI Chat System...")
        
        # Load configuration and setup logging
        config = load_config()
        setup_logging(config)
        
        # Initialize chat system
        system = ChatSystem(config)
        await system.initialize()
        
        # Start the chat loop
        while True:
            try:
                message = input("\nYou: ").strip()
                if not message:
                    continue
                    
                if message.lower() in ['exit', 'quit', 'bye']:
                    print("\n👋 Goodbye!")
                    break
                    
                response = await system.agent.process_message(message)
                print(f"\nAI: {response['response']}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Gracefully shutting down...")
                break
            except Exception as e:
                logging.error(f"Error processing message: {str(e)}")
                print("\n❌ Sorry, I encountered an error. Please try again.")
                
    except KeyboardInterrupt:
        print("\n\n👋 Gracefully shutting down...")
    except Exception as e:
        print(f"\n❌ Failed to start chat system: {str(e)}")
    finally:
        if system:
            print("\n🔄 Cleaning up resources...")
            try:
                await asyncio.wait_for(system.cleanup(), timeout=5.0)
            except asyncio.TimeoutError:
                print("⚠️  Cleanup timed out, forcing exit...")
            except Exception as e:
                logging.error(f"Error during cleanup: {str(e)}")
                print("⚠️  Error during cleanup")

def run_chat_system():
    """Run the chat system with proper signal handling."""
    try:
        if sys.platform == 'win32':
            loop = asyncio.ProactorEventLoop()
            asyncio.set_event_loop(loop)
        else:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    finally:
        loop.close()

if __name__ == "__main__":
    run_chat_system()
