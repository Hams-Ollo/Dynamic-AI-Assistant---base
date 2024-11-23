#-------------------------------------------------------------------------------------#
# File: chat_agent.py
# Description: Custom chat agent implementation using Groq's Mixtral model for conversational AI
# Author: @hams_ollo
#
# INITIAL SETUP:
# 1. Create virtual environment:    python -m venv venv
# 2. Activate virtual environment:
#    - Windows:                    .\venv\Scripts\activate
#    - Unix/MacOS:                 source venv/bin/activate
# 3. Install requirements:         pip install -r requirements.txt
# 4. Create .env file:            cp .env.example .env
# 5. Update dependencies:          pip freeze > requirements.txt
#
#-------------------------------------------------------------------------------------#
#----------# IMPORTS  #----------#
from typing import List, Dict, Any, Optional
import logging

import groq
from langchain.schema import AIMessage, HumanMessage
from langchain.chat_models.base import BaseChatModel

from .document_processor import DocumentProcessor
from ..utils.memory import MemoryManager

class GroqChatModel(BaseChatModel):
    """Custom chat model class for Groq."""
    
    def __init__(self, api_key: str, model: str = "llama3-groq-70b-8192-tool-use-preview", temperature: float = 0.7):
        """Initialize the Groq chat model."""
        super().__init__()
        self._client = groq.Groq(api_key=api_key)
        self._model = model
        self._temperature = temperature
    
    @property
    def client(self):
        """Get the Groq client."""
        return self._client
    
    @property
    def model(self):
        """Get the model name."""
        return self._model
    
    @property
    def temperature(self):
        """Get the temperature value."""
        return self._temperature
    
    def generate_response(self, messages: list) -> Dict[str, Any]:
        """Generate a response using the Groq API.
        
        Args:
            messages: List of conversation messages
            
        Returns:
            Response from the model
        """
        try:
            # Convert messages to chat format
            chat_messages = []
            for msg in messages:
                if isinstance(msg, HumanMessage):
                    chat_messages.append({"role": "user", "content": msg.content})
                elif isinstance(msg, AIMessage):
                    chat_messages.append({"role": "assistant", "content": msg.content})
            
            # Call Groq API
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=chat_messages,
                temperature=self.temperature
            )
            
            return completion
            
        except Exception as e:
            logging.error(f"Error generating response: {str(e)}")
            raise

class ChatAgent:
    """Main chat agent implementation."""
    
    def __init__(self, api_key: str, model: str = "llama3-groq-70b-8192-tool-use-preview"):
        """Initialize the chat agent."""
        try:
            self.llm = GroqChatModel(
                api_key=api_key,
                model=model,
                temperature=0.7
            )
            logging.info("Successfully initialized Groq chat model")
        except Exception as e:
            logging.error(f"Failed to initialize Groq: {str(e)}")
            raise
            
        self.doc_processor = DocumentProcessor()
        self.memory = MemoryManager({
            'type': 'buffer',
            'path': './data/memory'
        })
        
        # Custom prompt template for the chatbot
        self.system_prompt = """
        You are a helpful AI assistant with access to a knowledge base of documents.
        Use the provided context to answer questions accurately and concisely.
        If you don't know the answer, just say that you don't know.
        If the question is not related to the context, respond based on your general knowledge.
        """
    
    def process_message(self, message: str) -> Dict[str, Any]:
        """Process a user message and return a response.
        
        Args:
            message: User's input message
            
        Returns:
            Dict containing response and any source documents
        """
        try:
            # Get relevant documents from memory
            relevant_docs = []
            if hasattr(self.memory, 'get_relevant_context'):
                context = self.memory.get_relevant_context(message)
                if context:
                    relevant_docs = self.doc_processor.process_text(context)
            
            # Prepare conversation history
            messages = [
                {"role": "system", "content": self.system_prompt},
            ]
            
            # Add context if available
            if relevant_docs:
                context = "\n".join(doc.page_content for doc in relevant_docs)
                messages.append({
                    "role": "system",
                    "content": f"Context:\n{context}"
                })
            
            # Add user message
            messages.append({"role": "user", "content": message})
            
            # Generate response
            completion = self.llm.generate_response(messages)
            
            return {
                "response": completion.choices[0].message.content,
                "source_documents": relevant_docs
            }
            
        except Exception as e:
            logging.error(f"Error processing message: {str(e)}")
            return {
                "response": "I apologize, but I encountered an error processing your message. "
                           "This might be due to API limits or connectivity issues. "
                           "Please try again later or contact support if the issue persists.",
                "source_documents": []
            }
