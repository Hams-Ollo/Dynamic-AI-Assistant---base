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

# Add parent directory to path to import app modules
sys.path.append(str(Path(__file__).parent.parent.parent))

from app.agents.chat_agent import ChatAgent
from app.utils.document_processor import DocumentProcessor

def process_message(agent: ChatAgent, message: str, doc_processor: Optional[DocumentProcessor] = None):
    """Process a message using the chat agent with document context."""
    print("\n=== Processing New Message ===")
    print(f"User Message: {message[:100]}...")  # Print first 100 chars of message
    
    try:
        # Ensure agent is initialized
        if not agent.chain:
            raise ValueError("Chat agent not initialized")
            
        # Get relevant document context if available
        context = []
        if doc_processor:
            try:
                print("Retrieving document context...")
                relevant_docs = doc_processor.get_relevant_chunks(message)
                if relevant_docs:
                    print(f"Found {len(relevant_docs)} relevant document chunks")
                    context = [
                        f"Document: {doc['metadata']['file_name']}\n{doc['content']}"
                        for doc in relevant_docs
                    ]
            except Exception as e:
                print(f"Error retrieving document context: {str(e)}")
                st.warning(f"Could not retrieve document context: {str(e)}")
        
        # Process message with context
        print("Sending request to ChatAgent...")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            response = loop.run_until_complete(agent.process_message(message, context))
            return response.get('response', 'I encountered an error while processing your request. Please try again.')
        finally:
            loop.close()
        
    except Exception as e:
        print(f"\nError from ChatAgent: {str(e)}")
        return f"I encountered an error while processing your request. Please try again.\n\nError: {str(e)}"

def initialize_document_processor():
    """Initialize the document processor if not in session state."""
    if 'doc_processor' not in st.session_state:
        st.session_state.doc_processor = DocumentProcessor()

def initialize_chat_system():
    """Initialize the chat system components."""
    if 'chat_agent' not in st.session_state:
        print("Initializing AI Chat System...")
        chat_agent = ChatAgent()
        # Run async initialization in a new event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(chat_agent.initialize())
            st.session_state.chat_agent = chat_agent
            print("Chat system initialized successfully!")
        finally:
            loop.close()

def display_chat_interface():
    """Display the main chat interface."""
    print("\n=== Chat Interface Initialized ===")
    
    st.title("💬 Dynamic AI Chat Assistant")
    
    # Initialize chat history if not exists
    if "messages" not in st.session_state:
        st.session_state.messages = []
        print("Initialized new chat history")
    
    # Initialize rate limit counter if not exists
    if "rate_limit_count" not in st.session_state:
        st.session_state.rate_limit_count = 0
        print("Initialized rate limit counter")

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("What would you like to know?", disabled=st.session_state.get("rate_limit_count", 0) > 3):
        print(f"\n=== New Chat Input ===\nUser: {prompt[:100]}...")  # Print first 100 chars
        
        # Rate limit warning
        if st.session_state.get("rate_limit_count", 0) > 2:
            print("Rate limit threshold exceeded - adding delay")
            st.warning("⚠️ Multiple rate limits detected. Please wait a few minutes before continuing.")
            time.sleep(2)  # Add a small delay
            st.session_state.rate_limit_count = max(0, st.session_state.rate_limit_count - 1)
            print(f"Updated rate limit count: {st.session_state.rate_limit_count}")
            return

        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get AI response
        with st.chat_message("assistant"):
            print("\nProcessing message with ChatAgent...")
            if not hasattr(st.session_state, 'chat_agent') or not st.session_state.chat_agent.chain:
                initialize_chat_system()
            response = process_message(
                st.session_state.chat_agent,
                prompt,
                st.session_state.doc_processor if hasattr(st.session_state, 'doc_processor') else None
            )
            if response:
                print(f"Response received ({len(response)} chars)")
                if "rate limit" in response.lower():
                    st.session_state.rate_limit_count += 1
                    print(f"Rate limit count increased to {st.session_state.rate_limit_count}")
                else:
                    st.session_state.rate_limit_count = max(0, st.session_state.rate_limit_count - 1)
                    print(f"Rate limit count decreased to {st.session_state.rate_limit_count}")
                
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                print("Chat history updated with new response")

def main():
    """Main Streamlit application."""
    try:
        # Initialize systems
        initialize_chat_system()
        initialize_document_processor()
        
        # Display interface
        display_chat_interface()
        
        # Update parameters periodically
        print("\nUpdating ChatAgent parameters...")
        if hasattr(st.session_state, 'chat_agent'):
            st.session_state.chat_agent.update_parameters(temperature=0.7)
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        print(f"Error in main: {str(e)}")

if __name__ == "__main__":
    main()
