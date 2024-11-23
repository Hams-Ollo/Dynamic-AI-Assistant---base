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
        self.config = config
        print(f"{Fore.CYAN}📚 Initializing Memory System...{Style.RESET_ALL}")
        self.memory_manager = MemoryManager(config.get('memory', {}))
        print(f"{Fore.CYAN}🤖 Initializing AI Agent...{Style.RESET_ALL}")
        self.agent = ChatAgent(config.get('agent', {}))
    
    def start(self):
        """Start the chat system."""
        try:
            self.agent.initialize(self.memory_manager)
            print(f"{Fore.GREEN}✨ Chat system initialized successfully!{Style.RESET_ALL}")
        except Exception as e:
            logging.error(f"Failed to start chat system: {str(e)}")
            print(f"{Fore.RED}❌ Failed to start chat system: {str(e)}{Style.RESET_ALL}")
            sys.exit(1)
    
    def stop(self):
        """Gracefully stop the chat system."""
        try:
            print(f"\n{Fore.YELLOW}🔄 Cleaning up resources...{Style.RESET_ALL}")
            self.agent.cleanup()
            self.memory_manager.cleanup()
            print(f"{Fore.GREEN}👋 Chat system stopped successfully. Goodbye!{Style.RESET_ALL}")
        except Exception as e:
            logging.error(f"Error during system shutdown: {str(e)}")
            print(f"{Fore.RED}❌ Error during system shutdown: {str(e)}{Style.RESET_ALL}")

    def chat_loop(self):
        """Run the main chat loop."""
        print_welcome_message()
        
        while True:
            try:
                # Get user input with a cool prompt
                user_input = input(f"{Fore.CYAN}🧑‍💻 You: {Style.RESET_ALL}")
                
                # Handle commands
                if user_input.lower() == 'exit':
                    break
                elif user_input.lower() == 'help':
                    print_help()
                    continue
                elif user_input.lower() == 'clear':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print_welcome_message()
                    continue
                elif not user_input.strip():
                    continue
                
                # Process message and get response
                print(f"{Fore.YELLOW}🤔 AI is thinking...{Style.RESET_ALL}")
                result = self.agent.process_message(user_input)
                
                # Print AI response
                print(f"{Fore.GREEN}🤖 AI: {Style.RESET_ALL}{result['response']}\n")
                
                # If there are source documents, show them
                if result.get('source_documents'):
                    print(f"{Fore.BLUE}📚 Sources used:{Style.RESET_ALL}")
                    for doc in result['source_documents']:
                        print(f"  • {doc.page_content[:100]}...")
                    print()
                
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}⚠️  Detected Ctrl+C{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"{Fore.RED}❌ Error: {str(e)}{Style.RESET_ALL}")
                logging.error(f"Error in chat loop: {str(e)}")

def main():
    """Main entry point for the application."""
    config = initialize_app()
    
    system = ChatSystem(config)
    try:
        system.start()
        system.chat_loop()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⚠️  Shutting down...{Style.RESET_ALL}")
    finally:
        system.stop()

if __name__ == "__main__":
    main()
