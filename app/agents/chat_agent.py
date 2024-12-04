"""
Chat agent with RAG capabilities.
"""
from typing import Optional, Dict, Any, List
import logging
import asyncio

from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_groq import ChatGroq
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

from app.utils.memory import MemoryManager

class ChatAgent:
    """Chat agent with document-aware conversation capabilities."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize chat agent with configuration."""
        self.config = config or {}
        self.memory_manager = None
        self.llm = None
        self.chain = None
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    async def initialize(self, memory_manager: Optional[MemoryManager] = None):
        """Initialize the chat agent with optional memory manager."""
        try:
            self.memory_manager = memory_manager
            
            # Initialize LLM
            self.llm = ChatGroq(
                temperature=0.7,
                model_name="mixtral-8x7b-32768",
                max_tokens=4096
            )
            
            # Initialize conversation chain
            self.chain = ConversationChain(
                llm=self.llm,
                memory=ConversationBufferMemory(),
                verbose=True
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
            context_str = ""
            if additional_context:
                context_str = "\n\nRelevant context from documents:\n" + "\n---\n".join(additional_context)
            
            enhanced_prompt = f"""Please help me with the following:

{message}

{context_str}

If you use information from the provided documents, please cite them in your response.
"""
            
            # Get response from LLM
            response = await asyncio.to_thread(
                self.chain.predict,
                input=enhanced_prompt
            )
            
            # Extract sources if context was used
            sources = []
            if additional_context:
                sources = [
                    {
                        "file_name": ctx.split("Document: ")[1].split("\n")[0],
                        "excerpt": ctx.split("\n", 1)[1]
                    }
                    for ctx in additional_context
                ]
            
            return {
                "response": response,
                "sources": sources if sources else None
            }
            
        except Exception as e:
            self.logger.error(f"Error processing message: {str(e)}")
            raise
    
    async def clear_context(self):
        """Clear conversation context."""
        if self.chain and hasattr(self.chain, 'memory'):
            self.chain.memory.clear()
            self.logger.info("Conversation context cleared")
