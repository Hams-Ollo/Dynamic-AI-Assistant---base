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
from langchain.schema import AIMessage, HumanMessage, SystemMessage, BaseMessage, ChatResult, ChatGeneration
from langchain.chat_models.base import BaseChatModel
from langchain.callbacks.manager import CallbackManagerForLLMRun

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

    @property
    def _llm_type(self) -> str:
        """Return identifier of llm."""
        return "groq"

    def _generate(self, messages: List[BaseMessage], stop: Optional[List[str]] = None, run_manager: Optional[CallbackManagerForLLMRun] = None, **kwargs: Any) -> ChatResult:
        """Generate chat response."""
        try:
            # Convert messages to chat format
            chat_messages = []
            for msg in messages:
                if isinstance(msg, HumanMessage):
                    chat_messages.append({"role": "user", "content": msg.content})
                elif isinstance(msg, AIMessage):
                    chat_messages.append({"role": "assistant", "content": msg.content})
                elif isinstance(msg, SystemMessage):
                    chat_messages.append({"role": "system", "content": msg.content})
            
            # Call Groq API
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=chat_messages,
                temperature=self.temperature,
                stop=stop,
                **kwargs
            )
            
            message = AIMessage(content=completion.choices[0].message.content)
            return ChatResult(generations=[ChatGeneration(message=message)])
            
        except Exception as e:
            logging.error(f"Error generating response: {str(e)}")
            raise

class ChatAgent:
    """Main chat agent implementation."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the chat agent with configuration."""
        try:
            self.llm = GroqChatModel(
                api_key=config.get('api_key'),
                model=config.get('model', "llama3-groq-70b-8192-tool-use-preview"),
                temperature=config.get('temperature', 0.7)
            )
            logging.info("Successfully initialized Groq chat model")
        except Exception as e:
            logging.error(f"Failed to initialize Groq: {str(e)}")
            raise
            
        self.doc_processor = DocumentProcessor()
        self.memory = None  # Will be set in initialize()
        
        # Custom prompt template for the chatbot
        self.system_prompt = config.get('system_prompt', """
        You are a helpful AI assistant with access to a knowledge base of documents.
        Use the provided context to answer questions accurately and concisely.
        If you don't know the answer, just say that you don't know.
        If the question is not related to the context, respond based on your general knowledge.
        """)

    def initialize(self, memory_manager: MemoryManager):
        """Initialize the chat agent with memory manager.
        
        Args:
            memory_manager: Memory manager instance to use for conversation history
        """
        self.memory = memory_manager
        logging.info("Chat agent initialized with memory manager")

    def cleanup(self):
        """Cleanup resources used by the chat agent."""
        self.memory = None
        logging.info("Chat agent cleanup completed")

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
            if self.memory and hasattr(self.memory, 'get_relevant_context'):
                context = self.memory.get_relevant_context(message)
                if context:
                    relevant_docs = self.doc_processor.process_text(context)
            
            # Convert messages to LangChain format
            messages = [
                SystemMessage(content=self.system_prompt),
            ]
            
            # Add context if available
            if relevant_docs:
                context = "\n".join(doc.page_content for doc in relevant_docs)
                messages.append(SystemMessage(content=f"Context:\n{context}"))
            
            # Add user message
            messages.append(HumanMessage(content=message))
            
            # Generate response
            response = self.llm._generate(messages)
            
            return {
                "response": response.generations[0].message.content,
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
