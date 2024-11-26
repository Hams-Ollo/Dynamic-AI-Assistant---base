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
from typing import List, Dict, Any, Tuple
import logging
import re
from datetime import datetime
import uuid
from enum import Enum
import json
import asyncio
from typing import Optional

import groq
from langchain.schema import AIMessage, HumanMessage, SystemMessage, BaseMessage, ChatResult, ChatGeneration
from langchain.chat_models.base import BaseChatModel
from langchain.callbacks.manager import CallbackManagerForLLMRun

from .document_processor import DocumentProcessor
from ..utils.memory import MemoryManager
from scripts.text_scraper import TextScraper

class QueryIntent(Enum):
    GENERAL_CHAT = "general_chat"
    NEED_RESEARCH = "need_research"
    NEED_UPDATE = "need_update"

class GroqChatModel(BaseChatModel):
    """Custom chat model class for Groq."""
    
    def __init__(self, api_key: str, model: str = "mixtral-8x7b-32768", temperature: float = 0.7):
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

    async def _generate(self, messages: List[BaseMessage], stop: Optional[List[str]] = None, run_manager: Optional[CallbackManagerForLLMRun] = None, **kwargs: Any) -> ChatResult:
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
        self.config = config
        self.memory = MemoryManager(config.get('memory', {}))
        self.text_scraper = TextScraper()
        self._setup_llm()
        self._setup_intent_classifier()
        self.initialized = False
        logging.info("Chat agent created")

    async def initialize(self, memory_manager: Optional['MemoryManager'] = None):
        """Initialize the chat agent's components."""
        if memory_manager:
            self.memory = memory_manager
        try:
            # Initialize text scraper
            await self.text_scraper.initialize()
            
            # Initialize memory system
            await self.memory.initialize()
            
            # Set up any additional resources
            self.conversation_history = []
            self.last_interaction_time = None
            self.active_research_tasks = set()
            
            self.initialized = True
            logging.info("Chat agent initialized successfully")
            
        except Exception as e:
            logging.error(f"Failed to initialize chat agent: {str(e)}")
            raise

    async def cleanup(self):
        """Cleanup resources used by the chat agent."""
        try:
            # Clean up text scraper
            if hasattr(self, 'text_scraper'):
                await self.text_scraper.cleanup()
            
            # Clean up memory system
            if hasattr(self, 'memory'):
                await self.memory.cleanup()
            
            # Clear any active tasks or resources
            self.conversation_history = []
            self.active_research_tasks.clear()
            self.initialized = False
            
            logging.info("Chat agent cleanup completed successfully")
            
        except Exception as e:
            logging.error(f"Error during chat agent cleanup: {str(e)}")
            raise

    async def process_message(self, message: str) -> Dict[str, Any]:
        """Process a user message with enhanced capabilities."""
        if not self.initialized:
            raise RuntimeError("Chat agent not initialized. Call initialize() first.")

        interaction_id = str(uuid.uuid4())
        self.last_interaction_time = datetime.now()
        
        # Classify intent and get context
        intent, confidence = await self._classify_intent(message)
        
        response_data = {
            'interaction_id': interaction_id,
            'intent': intent.value,
            'confidence': confidence,
            'context': self._last_context if hasattr(self, '_last_context') else {},
            'sources': [],
            'response': None,
            'timestamp': self.last_interaction_time.isoformat()
        }
        
        try:
            # Determine if we need to perform research based on intent and confidence
            if intent == QueryIntent.NEED_RESEARCH and confidence > 0.6:
                sources = await self._perform_research(message)
                response_data['sources'] = sources
                
            # Generate response using all available context
            response = await self._generate_response(message, response_data)
            response_data['response'] = response
            
            # Store interaction data
            self.memory.store_query(
                query=message,
                intent=intent.value,
                urls=response_data['sources'],
                response=response
            )
            
            # Add to conversation history
            self.conversation_history.append({
                'role': 'user',
                'content': message,
                'timestamp': self.last_interaction_time.isoformat()
            })
            self.conversation_history.append({
                'role': 'assistant',
                'content': response,
                'timestamp': datetime.now().isoformat()
            })
            
            return response_data
            
        except Exception as e:
            logging.error(f"Error processing message: {str(e)}")
            error_response = {
                **response_data,
                'error': str(e),
                'response': "I apologize, but I encountered an error processing your message. Please try again or rephrase your question."
            }
            return error_response

    def _setup_llm(self):
        """Setup the language model."""
        if not self.config.get('api_key'):
            raise ValueError("API key is not configured")
        
        self.llm = GroqChatModel(
            api_key=self.config.get('api_key'),
            model=self.config.get('model', "mixtral-8x7b-32768"),
            temperature=self.config.get('temperature', 0.7)
        )
        
    def _setup_intent_classifier(self):
        """Setup the intent classification system."""
        # Initialize system prompts for different analysis tasks
        self.intent_analysis_prompt = """You are an expert AI intent classifier. Your task is to analyze user messages and determine:
1. The primary intent (GENERAL_CHAT, NEED_RESEARCH, NEED_UPDATE)
2. The confidence level in your classification (0.0 to 1.0)
3. The key context and entities that inform your decision

For each message, provide a structured analysis in JSON format with the following fields:
- intent: The primary intent category
- confidence: Your confidence score (0.0 to 1.0)
- context: Key contextual information and entities identified
- reasoning: Brief explanation of your classification

Intent Categories:
- GENERAL_CHAT: General conversation, greetings, or simple questions
- NEED_RESEARCH: Requires gathering or analyzing specific information
- NEED_UPDATE: Requests for updates or changes to existing information

Example Response:
{
    "intent": "NEED_RESEARCH",
    "confidence": 0.95,
    "context": {
        "topic": "quantum computing",
        "aspect": "recent developments",
        "time_frame": "current"
    },
    "reasoning": "Query specifically asks about latest developments, indicating need for current research"
}"""

    async def _classify_intent(self, message: str) -> Tuple[QueryIntent, float]:
        """Classify the intent of the user's message using advanced LLM reasoning."""
        try:
            # Prepare the analysis prompt
            analysis_prompt = f"""Analyze the following user message:
"{message}"

Provide your analysis in the specified JSON format."""

            messages = [
                SystemMessage(content=self.intent_analysis_prompt),
                HumanMessage(content=analysis_prompt)
            ]

            # Get LLM analysis
            response = await self.llm._generate(messages)
            response_text = response.generations[0].message.content

            # Parse JSON response
            try:
                analysis = json.loads(response_text)
                intent_str = analysis['intent']
                confidence = float(analysis['confidence'])

                # Store context for later use
                self._last_context = {
                    'context': analysis.get('context', {}),
                    'reasoning': analysis.get('reasoning', ''),
                    'timestamp': datetime.now().isoformat()
                }

                # Map string intent to enum
                intent_map = {
                    'GENERAL_CHAT': QueryIntent.GENERAL_CHAT,
                    'NEED_RESEARCH': QueryIntent.NEED_RESEARCH,
                    'NEED_UPDATE': QueryIntent.NEED_UPDATE
                }
                intent = intent_map.get(intent_str, QueryIntent.GENERAL_CHAT)

                logging.info(f"Intent Analysis - Intent: {intent_str}, Confidence: {confidence}")
                logging.debug(f"Context: {self._last_context}")

                return intent, confidence

            except json.JSONDecodeError:
                logging.error(f"Failed to parse LLM response: {response_text}")
                return QueryIntent.GENERAL_CHAT, 0.5

        except Exception as e:
            logging.error(f"Error in intent classification: {str(e)}")
            return QueryIntent.GENERAL_CHAT, 0.5

    async def _perform_research(self, query: str) -> List[str]:
        """Perform targeted research based on the query."""
        urls = await self.text_scraper.find_relevant_urls(query)
        processed_urls = []
        
        for url in urls:
            result = await self.text_scraper.process_url(url)
            if result and result['quality_score'] > 0.7:
                processed_urls.append(url)
                # Add content to vector store
                self.memory.add_documents([{
                    'content': chunk,
                    'metadata': {
                        'url': url,
                        'quality_score': result['quality_score'],
                        **result['metadata']
                    }
                } for chunk in result['content']])
                
        return processed_urls
        
    async def _generate_response(self, message: str, response_data: Dict[str, Any]) -> str:
        """Generate a response using all available context and LLM reasoning."""
        try:
            # Build comprehensive context
            context_parts = []
            
            # Add intent analysis context
            if 'context' in response_data:
                context_parts.append("Intent Analysis:")
                context_parts.append(f"- Intent: {response_data['intent']}")
                context_parts.append(f"- Confidence: {response_data['confidence']}")
                if 'reasoning' in response_data['context']:
                    context_parts.append(f"- Reasoning: {response_data['context']['reasoning']}")

            # Add relevant historical queries
            similar_queries = self.memory.get_similar_queries(message)
            if similar_queries:
                context_parts.append("\nRelevant Previous Interactions:")
                for query in similar_queries[:2]:
                    context_parts.append(f"Q: {query['query']}\nA: {query['response']}")

            # Add research sources
            if response_data['sources']:
                context_parts.append("\nRelevant Research Sources:")
                for url in response_data['sources']:
                    relevant_content = self.memory.get_relevant_context(message, url)
                    if relevant_content:
                        context_parts.append(f"From {url}:\n{relevant_content}")

            # Prepare comprehensive prompt
            system_prompt = """You are an intelligent AI assistant with access to:
1. Understanding of the user's intent and context
2. Relevant historical interactions
3. Fresh research from reliable sources
4. Domain expertise across various topics

Your task is to provide a comprehensive, accurate, and helpful response that:
- Directly addresses the user's query and intent
- Incorporates relevant context and information
- Cites sources when using researched information
- Maintains a natural, conversational tone"""

            prompt = f"""Context Information:
{chr(10).join(context_parts)}

User Question: {message}

Please provide a comprehensive response that addresses the user's query while incorporating the available context and information."""

            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=prompt)
            ]

            # Generate response
            response = await self.llm._generate(messages)
            return response.generations[0].message.content

        except Exception as e:
            logging.error(f"Error generating response: {str(e)}")
            return "I apologize, but I encountered an error while generating a response. Please try again or rephrase your question."

    async def process_feedback(self, interaction_id: str, feedback: Dict[str, Any]):
        """Process user feedback for continuous improvement."""
        self.memory.store_feedback(interaction_id, feedback)
        
        # Update source relevance scores
        if feedback.get('relevant_sources'):
            for url in feedback['relevant_sources']:
                await self.text_scraper.update_source_relevance(url, 1.0)
        
        # Handle negative feedback
        if feedback.get('rating', 5) <= 3:
            await self._handle_negative_feedback(feedback)
            
    async def _handle_negative_feedback(self, feedback: Dict[str, Any]):
        """Handle negative feedback for system improvement."""
        if feedback.get('missing_information'):
            # Adjust scraping patterns
            await self.text_scraper.adjust_scraping_patterns({
                'missing_content': True
            })
        
        if feedback.get('incorrect_metadata'):
            await self.text_scraper.adjust_scraping_patterns({
                'incorrect_metadata': True
            })
            
        # Log feedback for analysis
        logging.warning(f"Received negative feedback: {feedback}")
