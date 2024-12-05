#-------------------------------------------------------------------------------------#
# File: Chat.py
# Description: Chat interface with RAG capabilities
# Author: @hams_ollo
# Version: 0.0.3
#-------------------------------------------------------------------------------------#

"""
Chat Interface with RAG capabilities
"""
import sys
import os
from pathlib import Path
import asyncio
from typing import Optional, Dict, Any
import streamlit as st
import time
from app.utils.emoji_logger import EmojiLogger

# Add parent directory to path to import app modules
sys.path.append(str(Path(__file__).parent.parent.parent))

from app.agents.chat_agent import ChatAgent
from app.utils.document_processor import DocumentProcessor

def get_or_create_event_loop():
    """Get the current event loop or create a new one."""
    try:
        return asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop

def process_message(agent: ChatAgent, message: str, doc_processor: Optional[DocumentProcessor] = None):
    """Process a message using the chat agent with document context."""
    EmojiLogger.log("info", f"User Message: {message[:100]}...")  # Log first 100 chars of message
    
    try:
        # Ensure agent is initialized
        if not agent.chain:
            raise ValueError("Chat agent not initialized")
            
        # Get relevant document context if available
        context = []
        if doc_processor:
            try:
                EmojiLogger.log("info", "Retrieving document context...")
                relevant_docs = doc_processor.get_relevant_chunks(message)
                if relevant_docs:
                    EmojiLogger.log("info", f"Found {len(relevant_docs)} relevant document chunks")
                    context = [
                        f"Document: {doc['metadata']['file_name']}\n{doc['content']}"
                        for doc in relevant_docs
                    ]
            except Exception as e:
                EmojiLogger.log("error", f"Error retrieving document context: {str(e)}")
                st.warning(f"Could not retrieve document context: {str(e)}")
        
        # Process message with context
        EmojiLogger.log("info", "Sending request to ChatAgent...")
        loop = get_or_create_event_loop()
        response = loop.run_until_complete(agent.process_message(message, context))
        if isinstance(response, str):
            return response
        return response.get('response', 'I encountered an error while processing your request. Please try again.')
        
    except Exception as e:
        EmojiLogger.log("error", f"Error from ChatAgent: {str(e)}")
        return f"I encountered an error while processing your request. Please try again.\n\nError: {str(e)}"

def initialize_document_processor():
    """Initialize the document processor if not in session state."""
    if 'doc_processor' not in st.session_state:
        st.session_state.doc_processor = DocumentProcessor()

def initialize_chat_system():
    """Initialize the chat system components."""
    if 'chat_agent' not in st.session_state:
        EmojiLogger.log("info", "Initializing AI Chat System...")
        chat_agent = ChatAgent()
        loop = get_or_create_event_loop()
        loop.run_until_complete(chat_agent.initialize())
        st.session_state.chat_agent = chat_agent
        EmojiLogger.log("info", "Chat system initialized successfully!")

def display_chat_interface():
    """Display the main chat interface."""
    EmojiLogger.log("info", "Chat Interface Initialized")
    
    st.title("💬 Dynamic AI Chat Assistant")
    
    # Initialize chat history if not exists
    if "messages" not in st.session_state:
        st.session_state.messages = []
        EmojiLogger.log("info", "Initialized new chat history")
    
    # Initialize rate limit counter if not exists
    if "rate_limit_count" not in st.session_state:
        st.session_state.rate_limit_count = 0
        st.session_state.last_rate_limit = None
        EmojiLogger.log("info", "Initialized rate limit counter")

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Reset rate limit if enough time has passed
    if st.session_state.get("last_rate_limit"):
        time_since_limit = time.time() - st.session_state.last_rate_limit
        if time_since_limit > 60:  # Reset after 1 minute
            st.session_state.rate_limit_count = 0
            st.session_state.last_rate_limit = None
            EmojiLogger.log("info", "Rate limit counter reset")

    # Chat input
    if prompt := st.chat_input("What would you like to know?", disabled=st.session_state.get("rate_limit_count", 0) > 3):
        EmojiLogger.log("info", f"\n=== New Chat Input ===\nUser: {prompt[:100]}...")
        
        # Rate limit handling
        if st.session_state.get("rate_limit_count", 0) > 2:
            st.warning("⚠️ Rate limit reached. Please wait a minute before continuing.")
            st.session_state.last_rate_limit = time.time()
            return

        # Add user message to chat history 🏹🪶🦚📿🌺🐝🪶🍯 🪬 🔱 🤖 💡🤓🙈🌕🐍🥰🤯😭🔥🪴🍑🌊💧🦢🪈
        st.session_state.messages.append({"role": "🪬", "content": prompt})
        with st.chat_message("🪬"):
            st.markdown(prompt)

        # Get AI response 🏹🪶🦚📿🌺🐝🪶🍯🪬🔱🤖💡🤓🙈🌕🐍🥰🤯😭🔥🪴🍑🌊💧🦢🪈
        with st.chat_message("🤖"):
            EmojiLogger.log("info", "\nProcessing message with ChatAgent...")
            message_placeholder = st.empty()
            message_placeholder.markdown("🤖 Thinking...")
            
            try:
                if not hasattr(st.session_state, 'chat_agent') or not st.session_state.chat_agent.chain:
                    initialize_chat_system()
                
                response = process_message(
                    st.session_state.chat_agent,
                    prompt,
                    st.session_state.doc_processor if hasattr(st.session_state, 'doc_processor') else None
                )
                
                if response:
                    EmojiLogger.log("info", f"Response received ({len(response)} chars)")
                    if "rate limit" in response.lower():
                        st.session_state.rate_limit_count += 1
                        st.session_state.last_rate_limit = time.time()
                        EmojiLogger.log("info", f"Rate limit count increased to {st.session_state.rate_limit_count}")
                    else:
                        st.session_state.rate_limit_count = max(0, st.session_state.rate_limit_count - 1)
                        EmojiLogger.log("info", f"Rate limit count decreased to {st.session_state.rate_limit_count}")
                    
                    message_placeholder.markdown(response)
                    st.session_state.messages.append({"role": "🤖", "content": response})
                    EmojiLogger.log("info", "Chat history updated with new response")
                    
            except Exception as e:
                message_placeholder.markdown(f"❌ Error: {str(e)}")
                EmojiLogger.log("error", f"Error processing message: {str(e)}")

def main():
    """Main Streamlit application."""
    try:
        # Initialize systems
        initialize_chat_system()
        initialize_document_processor()
        
        # Display interface
        display_chat_interface()
        
        # Update parameters periodically
        EmojiLogger.log("info", "\nUpdating ChatAgent parameters...")
        if hasattr(st.session_state, 'chat_agent'):
            st.session_state.chat_agent.update_parameters(temperature=0.7)
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        EmojiLogger.log("error", f"Error in main: {str(e)}")

if __name__ == "__main__":
    main()
