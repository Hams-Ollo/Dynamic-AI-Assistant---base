"""
Chat agent with RAG capabilities.
"""
from typing import Optional, Dict, Any, List
import logging
import asyncio
import time
from datetime import datetime, timedelta

from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_groq import ChatGroq
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from app.utils.memory import MemoryManager

class ChatAgent:
    """Chat agent with document-aware conversation capabilities."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize chat agent with configuration."""
        self.config = config or {}
        self.memory_manager = None
        self.llm = None
        self.chain = None
        self.message_history = []
        
        # Rate limiting parameters
        self.last_request_time = None
        self.request_count = 0
        self.max_requests_per_hour = 100  # Adjust based on your API tier
        self.cooldown_period = 3600  # 1 hour in seconds
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def _check_rate_limit(self):
        """Check if we're within rate limits."""
        current_time = datetime.now()
        
        # Reset counter if cooldown period has passed
        if self.last_request_time and (current_time - self.last_request_time) > timedelta(seconds=self.cooldown_period):
            self.request_count = 0
            self.last_request_time = None
            return True
            
        # If we're in cooldown, calculate remaining time
        if self.request_count >= self.max_requests_per_hour:
            if not self.last_request_time:
                self.last_request_time = current_time
            wait_time = self.cooldown_period - (current_time - self.last_request_time).seconds
            minutes = wait_time // 60
            seconds = wait_time % 60
            raise Exception(f"Rate limit exceeded. Please try again in {minutes} minutes and {seconds} seconds.")
        
        # Update request count and time
        self.request_count += 1
        if not self.last_request_time:
            self.last_request_time = current_time
        
        return True
    
    async def initialize(self, memory_manager: Optional[MemoryManager] = None):
        """Initialize the chat agent with optional memory manager."""
        try:
            self.memory_manager = memory_manager
            
            # Reset rate limiting on initialization
            self.last_request_time = None
            self.request_count = 0
            
            # Initialize LLM with error handling
            try:
                self.llm = ChatGroq(
                    temperature=0.7,
                    model_name="mixtral-8x7b-32768",
                    max_tokens=4096
                )
            except Exception as llm_error:
                self.logger.error(f"Failed to initialize LLM: {str(llm_error)}")
                raise Exception("Failed to initialize language model. Please check your API key and try again.") from llm_error
            
            # Initialize message history
            self.message_history = []
            
            # Initialize the chain using the newer RunnableWithMessageHistory approach
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a helpful AI assistant."),
                MessagesPlaceholder(variable_name="history"),
                ("human", "{input}")
            ])
            
            self.chain = RunnableWithMessageHistory(
                prompt | self.llm,
                lambda session_id: self.message_history,
                input_messages_key="input",
                history_messages_key="history"
            )
            
            self.logger.info("Chat agent initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Error initializing chat agent: {str(e)}")
            raise
    
    def update_parameters(self, temperature: float = None, max_tokens: int = None):
        """Update the LLM parameters.
        
        Args:
            temperature: New temperature value for text generation
            max_tokens: New maximum tokens for response generation
        """
        if not self.llm:
            self.logger.warning("Cannot update parameters: LLM not initialized")
            return
            
        if temperature is not None:
            self.llm.temperature = temperature
            
        if max_tokens is not None:
            self.llm.max_tokens = max_tokens
            
        self.logger.info(f"Updated LLM parameters: temperature={temperature}, max_tokens={max_tokens}")
    
    async def process_message(
        self,
        message: str,
        additional_context: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Process a message with optional document context."""
        try:
            if not self.chain:
                raise ValueError("Chat agent not initialized")
            
            # Prepare context-enhanced prompt
            if additional_context:
                context_str = "\n\nRelevant context from documents:\n" + "\n---\n".join(additional_context)
                full_message = f"{message}\n\n{context_str}"
            else:
                full_message = message
            
            # Get response using the newer approach
            response = await self.chain.ainvoke(
                {"input": full_message},
                config={"configurable": {"session_id": "default"}}
            )
            
            return {
                "response": response.content if hasattr(response, 'content') else str(response),
                "sources": [{"content": ctx} for ctx in additional_context] if additional_context else None
            }
            
        except Exception as e:
            self.logger.error(f"Error processing message: {str(e)}")
            raise
    
    async def clear_context(self):
        """Clear conversation context."""
        if self.chain and hasattr(self.chain, 'memory'):
            self.chain.memory.clear()
            self.logger.info("Conversation context cleared")

    def get_response(self, message: str) -> str:
        """Synchronously get a response from the chat agent.
        
        Args:
            message: The input message to process
            
        Returns:
            str: The agent's response
            
        Raises:
            ValueError: If chat agent is not initialized
            Exception: If rate limit is exceeded
        """
        if not self.chain:
            raise ValueError("Chat agent not initialized")
            
        # Check rate limits
        self._check_rate_limit()
        
        try:
            # Use the chain to get response
            response = self.chain.predict(input=message)
            return response
        except Exception as e:
            if "rate limit exceeded" in str(e).lower():
                self.request_count = self.max_requests_per_hour  # Force cooldown
                raise Exception("Rate limit exceeded. Please try again in about an hour.")
            raise e

if __name__ == "__main__":
    pass
