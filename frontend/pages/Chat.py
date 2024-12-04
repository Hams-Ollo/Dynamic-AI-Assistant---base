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

def initialize_chat_system():
    """Initialize the chat system components."""
    if 'chat_agent' not in st.session_state:
        print("Initializing AI Chat System...")
        st.session_state.chat_agent = ChatAgent()
        print("Chat system initialized successfully!")

def process_message(agent: ChatAgent, message: str, doc_processor: Optional[DocumentProcessor] = None):
    """Process a message using the chat agent with document context."""
    print("\n=== Processing New Message ===")
    print(f"User Message: {message[:100]}...")  # Print first 100 chars of message
    
    try:
        # Get relevant document context if available
        context = ""
        if doc_processor:
            try:
                print("Retrieving document context...")
                relevant_docs = doc_processor.get_relevant_chunks(message)
                if relevant_docs:
                    print(f"Found {len(relevant_docs)} relevant document chunks")
                    context = "\n\nRelevant context from documents:\n" + "\n---\n".join(
                        f"Document: {doc['metadata']['file_name']}\n{doc['content']}" for doc in relevant_docs
                    )
            except Exception as e:
                print(f"Error retrieving document context: {str(e)}")
                st.warning(f"Could not retrieve document context: {str(e)}")
        
        # Get response from agent
        try:
            with st.spinner("Thinking... This might take a moment."):
                print("\nSending request to ChatAgent...")
                response = agent.get_response(message + context if context else message)
                if response:
                    print("Successfully received response from ChatAgent")
                    return response
                print("Warning: Empty response received from ChatAgent")
                return "I apologize, but I couldn't generate a response. Please try again."
            
        except Exception as e:
            error_msg = str(e).lower()
            print(f"\nError from ChatAgent: {error_msg}")
            
            if any(phrase in error_msg for phrase in ["rate limit", "resource exhausted"]):
                error_container = st.error("⚠️ The AI service is currently at capacity.")
                suggestion = st.info("""
                    Suggestions:
                    1. Wait a moment before trying again
                    2. Try shorter messages
                    3. Reduce the response length in settings
                """)
                return "I apologize, but I'm receiving too many requests right now. Please try again in a moment."
            else:
                st.error(f"Error: {str(e)}")
                return "I encountered an error while processing your request. Please try again."
        
    except Exception as e:
        print(f"\nUnexpected error in process_message: {str(e)}")
        st.error(f"Error processing message: {str(e)}")
        return None

def initialize_document_processor():
    """Initialize the document processor if not in session state."""
    if 'doc_processor' not in st.session_state:
        st.session_state.doc_processor = DocumentProcessor()

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
            response = process_message(
                st.session_state.chat_agent,
                prompt,
                st.session_state.doc_processor if hasattr(st.session_state, 'doc_processor') else None
            )
            if response:
                print(f"Response received ({len(response)} chars)")
                if "rate limit" in response.lower():
                    st.session_state.rate_limit_count += 1
                    print(f"Rate limit detected - count increased to {st.session_state.rate_limit_count}")
                else:
                    st.session_state.rate_limit_count = max(0, st.session_state.rate_limit_count - 1)
                    print(f"Rate limit count decreased to {st.session_state.rate_limit_count}")
                
                st.markdown(response)
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
                print("Chat history updated with new response")

    # Sidebar controls
    with st.sidebar:
        st.subheader("Chat Controls")
        
        if st.button("Clear Chat History"):
            print("\n=== Clearing Chat History ===")
            st.session_state.messages = []
            st.session_state.rate_limit_count = 0
            print("Chat history and rate limit counter reset")
            st.rerun()
        
        st.markdown("---")
        
        st.subheader("Chat Settings")
        temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1, 
                              help="Higher values make the output more random, lower values make it more focused")
        max_tokens = st.slider("Max Response Length", 100, 8192, 1000, 100,
                             help="Maximum number of tokens in the response")
        
        # Update chat parameters when sliders change
        if "chat_agent" in st.session_state:
            print("\nUpdating ChatAgent parameters...")
            st.session_state.chat_agent.update_parameters(
                temperature=temperature,
                max_tokens=max_tokens
            )
            
        # Display rate limit status
        if st.session_state.get("rate_limit_count", 0) > 0:
            st.markdown("---")
            st.subheader("System Status")
            st.warning(f"Rate Limit Status: {st.session_state.rate_limit_count}/4")

def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="DynamicAI Chat Assistant",
        page_icon="💬",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize components
    initialize_chat_system()
    initialize_document_processor()
    
    # Display interface
    display_chat_interface()

if __name__ == "__main__":
    main()
