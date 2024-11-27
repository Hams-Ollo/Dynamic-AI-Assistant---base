#-------------------------------------------------------------------------------------#
# File: Chat.py
# Description: Main application entry point and process manager
# Author: @hams_ollo
# Version: 0.0.3
# Last Updated: [2024-11-21]
#-------------------------------------------------------------------------------------#
# SETUP GUIDE:  streamlit run .\frontend\Chat.py 
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

"""
Main Chat Interface with RAG capabilities
"""
import sys
import os
from pathlib import Path
import asyncio
from typing import Optional, Dict, Any

# Add parent directory to path to import app modules
sys.path.append(str(Path(__file__).parent.parent))

import streamlit as st
from app.agents.chat_agent import ChatAgent
from app.utils.memory import MemoryManager
from app.utils.document_processor import DocumentProcessor
from app.core.config import load_config

async def initialize_chat_system():
    """Initialize the chat system components."""
    try:
        print("Initializing AI Chat System...")
        config = load_config()
        
        print("Initializing Memory System...")
        memory_manager = MemoryManager(config.get('memory', {}))
        
        print("Initializing AI Agent...")
        agent = ChatAgent(config.get('agent', {}))
        await agent.initialize(memory_manager)
        
        print("Chat system initialized successfully!")
        return agent
    except Exception as e:
        st.error(f"Error initializing chat system: {str(e)}")
        return None

async def process_message(agent: ChatAgent, message: str, doc_processor: Optional[DocumentProcessor] = None) -> Optional[dict]:
    """Process a message using the chat agent with document context."""
    try:
        # Get relevant document chunks if available
        context = []
        if doc_processor:
            chunks = doc_processor.get_relevant_chunks(message)
            if chunks:
                context = [
                    f"Document: {chunk['metadata']['file_name']}\n{chunk['content']}"
                    for chunk in chunks
                ]
        
        # Process message with context
        response = await agent.process_message(
            message,
            additional_context=context if context else None
        )
        return response
    except Exception as e:
        st.error(f"Error processing message: {str(e)}")
        return None

def initialize_document_processor():
    """Initialize the document processor if not in session state."""
    if 'doc_processor' not in st.session_state:
        st.session_state.doc_processor = DocumentProcessor()

def display_chat_interface():
    """Display the main chat interface."""
    st.title("💬 Dynamic AI Chat Assistant")
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    if "chat_agent" not in st.session_state:
        st.session_state.chat_agent = asyncio.run(initialize_chat_system())
        if not st.session_state.chat_agent:
            st.error("Failed to initialize chat system. Please check your configuration and try again.")
            return
    
    # Initialize document processor
    initialize_document_processor()
    
    # Display uploaded documents info
    if hasattr(st.session_state, 'doc_processor'):
        docs = st.session_state.doc_processor.list_documents()
        if docs:
            with st.expander("📚 Available Documents"):
                for doc in docs:
                    st.write(f"- 📄 {doc['name']}")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What would you like to know?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("🤔 AI is thinking..."):
                try:
                    response = asyncio.run(process_message(
                        st.session_state.chat_agent,
                        prompt,
                        st.session_state.doc_processor
                    ))
                    if response:
                        ai_response = response.get("response", "I apologize, but I encountered an error processing your message.")
                        st.markdown(ai_response)
                        st.session_state.messages.append({"role": "assistant", "content": ai_response})
                        
                        # Display source documents if used
                        if response.get("sources"):
                            with st.expander("📚 Sources Used"):
                                for source in response["sources"]:
                                    st.markdown(f"- **{source['file_name']}**")
                                    st.markdown(f"  > {source['excerpt']}")
                except Exception as e:
                    error_message = f"Error generating response: {str(e)}"
                    st.error(error_message)
                    st.session_state.messages.append({"role": "assistant", "content": f"❌ {error_message}"})

def main():
    """Main Streamlit application."""
    # Page configuration
    st.set_page_config(
        page_title="AI Agent Graphical User Interface",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Set the app title in sidebar
    st.sidebar.markdown("# 💬 AI Chat Agent")
    
    # Display chat interface
    display_chat_interface()

if __name__ == "__main__":
    main()
