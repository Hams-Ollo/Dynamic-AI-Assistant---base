"""
Chat agent with RAG capabilities.
"""
from typing import Optional, Dict, Any, List, Callable
import logging
import asyncio
import time
from datetime import datetime, timedelta

from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, BaseMessage
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_groq import ChatGroq
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from app.utils.memory import MemoryManager
from app.utils.emoji_logger import EmojiLogger

class ChatMessageHistory(BaseChatMessageHistory):
    """Custom message history implementation."""
    
    def __init__(self):
        """Initialize an empty message store."""
        super().__init__()
        self.messages: List[BaseMessage] = []
    
    def add_message(self, message: BaseMessage) -> None:
        """Add a message to the store."""
        self.messages.append(message)
    
    def clear(self) -> None:
        """Clear all messages from the store."""
        self.messages = []

    async def aget_messages(self) -> List[BaseMessage]:
        """Get message history asynchronously.
        
        This is a required method from BaseChatMessageHistory.
        The 'a' prefix stands for 'async'.
        """
        return self.messages.copy()
        
    def get_messages(self) -> List[BaseMessage]:
        """Get message history synchronously."""
        return self.messages.copy()

class ChatAgent:
    """Chat agent with document-aware conversation capabilities."""
    
    def __init__(self):
        """Initialize chat agent."""
        self.logger = EmojiLogger
        self.chain = None
        self.llm = None
        self.memory_manager = None
        self.message_histories: Dict[str, ChatMessageHistory] = {}
        self.last_request_time = None
        self.request_count = 0
        self.max_requests_per_hour = 500  # Adjust based on your API tier
        self.cooldown_period = 3600  # 1 hour in seconds
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
    
    def get_message_history(self, session_id: str) -> ChatMessageHistory:
        """Get or create message history for a session."""
        if session_id not in self.message_histories:
            self.message_histories[session_id] = ChatMessageHistory()
        return self.message_histories[session_id]
    
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
            self.logger.startup("Chat agent initialized successfully")
        except Exception as e:
            self.logger.error(f"Error initializing chat agent: {str(e)}")

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
            
        # Initialize the chain using the newer RunnableWithMessageHistory approach
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a versatile AI assistant capable of both natural conversation and document analysis. Your role is to:

1. General Conversation:
   - Engage in natural, friendly dialogue on any topic
   - Draw from your broad knowledge base to provide helpful information
   - Share insights, examples, and explanations across various subjects
   - Maintain a conversational and approachable tone

2. Document-Specific Assistance:
   - When referencing uploaded documents, use simple numbered citations [¹], [²], etc.
   - Place citations immediately after the referenced information
   - At the end of responses using document data, add a "Sources:" section with brief document references
   - Format sources as: [1] Document_Name.pdf, [2] Document_Name.txt, etc.

3. Adaptive Interaction:
   - Seamlessly switch between general conversation and document-specific help
   - Combine both knowledge sources when beneficial
   - Ask for clarification when needed
   - Keep citations minimal and unobtrusive

Remember: Engage naturally in conversation while providing clear but subtle document citations when referencing uploaded materials. Citations should enhance, not interrupt, the conversation flow."""),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])

        chain = prompt | self.llm
            
        self.chain = RunnableWithMessageHistory(
            chain,
            lambda session_id: self.get_message_history(session_id),
            input_messages_key="input",
            history_messages_key="history"
        )
            
        self.logger.startup("Chat agent initialized successfully")
            
    def update_parameters(self, temperature: float = None, max_tokens: int = None):
        """Update the LLM parameters."""
        try:
            if temperature is not None:
                self.llm.temperature = temperature
            if max_tokens is not None:
                self.llm.max_tokens = max_tokens
            self.logger.success("Chat agent parameters updated.")
        except Exception as e:
            self.logger.error(f"Error updating parameters: {str(e)}")
    
    async def process_message(
        self,
        message: str,
        additional_context: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Process a message with optional document context.

        Args:
            message: The message to process
            additional_context: Additional context to consider
        """
        try:
            self.logger.info("Processing message with ChatAgent...")
            self.logger.info(f"User Message: {message}")

            # Check if user is asking for document info
            if "document" in message.lower():
                self.logger.info("User requested document information.")
                # Add logic to retrieve and include document context
                document_context = additional_context if additional_context else []
            else:
                self.logger.info("User did not request document information.")
                document_context = []

            self.logger.info("Sending request to ChatAgent...")
            # Process the message and get a response
            response = await self.get_response(message, document_context)
            
            if isinstance(response, str):
                response = {"response": response}
            
            self.logger.info(f"Response received ({len(str(response))} chars)")
            return response
            
        except Exception as e:
            self.logger.error(f"Error from ChatAgent: {str(e)}")
            return {"error": str(e)}

    async def get_response(self, message: str, document_context: List[str]) -> str:
        """
        Synchronously get a response from the chat agent.

        Args:
            message: The input message to process
            document_context: Document context to consider

        Returns:
            str: The agent's response

        Raises:
            ValueError: If chat agent is not initialized
            Exception: If rate limit is exceeded
        """
        try:
            if not self.chain:
                raise ValueError("Chat agent is not initialized.")

            self._check_rate_limit()

            # Prepare context-enhanced prompt
            if document_context:
                formatted_context = []
                for i, ctx in enumerate(document_context, 1):
                    formatted_context.append(f"[{i}] {ctx}")
                context_str = "\n\nSources:\n" + "\n".join(formatted_context)
                full_message = f"{message}\n\n{context_str}"
            else:
                full_message = message

            # Add user message to history before processing
            history = self.get_message_history("default")
            history.add_message(HumanMessage(content=full_message))

            try:
                # Get response from the chain
                response = await self.chain.ainvoke(
                    {"input": full_message},
                    {"configurable": {"session_id": "default"}}
                )

                # Extract response content
                if isinstance(response, str):
                    response_text = response
                else:
                    response_text = response.content if hasattr(response, 'content') else str(response)

                # Add AI response to history
                history.add_message(AIMessage(content=response_text))

                return response_text
            except Exception as chain_error:
                self.logger.error(f"Chain error: {str(chain_error)}")
                raise chain_error

        except Exception as e:
            self.logger.error(f"Error in get_response: {str(e)}")
            raise e
    
    async def clear_context(self):
        """Clear conversation context."""
        if self.chain and hasattr(self.chain, 'memory'):
            self.chain.memory.clear()
            self.logger.info("Conversation context cleared")
    
if __name__ == "__main__":
    pass
