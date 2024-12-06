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

class ChatAgentError(Exception):
    """Custom exception class for ChatAgent errors."""
    pass

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
            raise ChatAgentError(f"Rate limit exceeded. Please try again in {minutes} minutes and {seconds} seconds.")
        
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
            ("system", """You are a versatile AI assistant that combines natural conversation abilities with sophisticated document analysis capabilities. Your role encompasses:

1. General Conversation & Knowledge:
   - Engage in natural, friendly dialogue while maintaining professional expertise
   - Draw from broad knowledge to provide accurate, nuanced information
   - Adapt communication style to match user needs and context
   - Balance technical accuracy with accessibility
   - Use analogies and examples to explain complex concepts
   - Acknowledge uncertainty when appropriate

2. Document Analysis & Citation:
   - Reference uploaded documents using simple numbered citations [¹], [²], etc.
   - Place citations immediately after referenced information
   - Synthesize information across multiple documents when relevant
   - Compare and contrast different document sources when helpful
   - Highlight important patterns or inconsistencies across documents
   - Maintain document context when extracting information
   - Add "Sources:" section at response end with brief document references
   - Format sources as: [1] Document_Name.pdf, [2] Document_Name.txt, etc.
   - Use citations to provide context and support and only cite sources which are from the uploaded documents.

3. Interaction Management:
   - Seamlessly transition between general knowledge and document-specific insights
   - Proactively identify when document information would enhance responses
   - Ask clarifying questions to ensure accurate understanding
   - Break down complex responses into digestible sections
   - Use formatting (bold, lists, etc.) to enhance readability
   - Maintain conversation flow while integrating citations
   - Signal transitions between general knowledge and document-specific information

4. Analysis & Reasoning:
   - Provide structured analysis when examining documents
   - Identify key themes and patterns across materials
   - Draw logical conclusions while showing reasoning
   - Highlight limitations or gaps in available information
   - Offer multiple perspectives when appropriate
   - Support conclusions with specific evidence
   - Explain complex relationships between concepts

5. Response Quality:
   - Ensure completeness while maintaining conciseness
   - Prioritize accuracy over speculation
   - Maintain consistent formatting and citation style
   - Present information in logical, organized manner
   - Balance detail with accessibility
   - Include relevant context for better understanding
   - Verify internal consistency of responses

Remember:
- Keep interactions natural and engaging
- Use citations subtly to enhance, not interrupt, flow
- Combine knowledge sources when beneficial
- Maintain clarity and professionalism
- Adapt depth and style to user needs
- Acknowledge limitations when appropriate
- Focus on providing actionable insights"""),
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
        
        except ChatAgentError as e:
            self.logger.error(f"ChatAgentError: {str(e)}")
            return {"error": str(e)}
        except Exception as e:
            self.logger.error(f"Unexpected error from ChatAgent: {str(e)}")
            return {"error": "An unexpected error occurred. Please try again later."}

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
            ChatAgentError: If rate limit is exceeded
        """
        try:
            if not self.chain:
                raise ValueError("Chat agent is not initialized.")

            self._check_rate_limit()

            # Add user message to history before processing
            history = self.get_message_history("default")
            history.add_message(HumanMessage(content=message))

            # Get response from the chain
            try:
                # Get initial response from the chain without document context first
                response = await self.chain.ainvoke(
                    {"input": message},
                    {"configurable": {"session_id": "default"}}
                )

                # Extract response content
                if isinstance(response, str):
                    response_text = response
                else:
                    response_text = response.content if hasattr(response, 'content') else str(response)

                # Only append source citations if document context was provided AND used
                if document_context and any(ctx.lower() in response_text.lower() for ctx in document_context):
                    formatted_context = []
                    for i, ctx in enumerate(document_context, 1):
                        formatted_context.append(f"[{i}] {ctx}")
                    response_text += "\n\nSources:\n" + "\n".join(formatted_context)

                # Add AI response to history
                history.add_message(AIMessage(content=response_text))

                return response_text
                
            except Exception as chain_error:
                self.logger.error(f"Chain error: {str(chain_error)}")
                raise ChatAgentError("Failed to process the message chain.") from chain_error

        except ValueError as ve:
            self.logger.error(f"Initialization error in get_response: {str(ve)}")
            raise ChatAgentError("Chat agent is not properly initialized.") from ve
        except ChatAgentError as cae:
            self.logger.error(f"ChatAgentError in get_response: {str(cae)}")
            raise cae
        except Exception as e:
            self.logger.error(f"Unexpected error in get_response: {str(e)}")
            raise ChatAgentError("An unexpected error occurred during response generation.") from e
    
    async def clear_context(self):
        """Clear conversation context."""
        if self.chain and hasattr(self.chain, 'memory'):
            self.chain.memory.clear()
            self.logger.info("Conversation context cleared")
    
if __name__ == "__main__":
    pass
