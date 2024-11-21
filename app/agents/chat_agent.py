from typing import List, Dict, Any, Optional
import logging
import groq
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.schema import AIMessage, HumanMessage
from langchain.chat_models.base import BaseChatModel
from .document_processor import DocumentProcessor

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
        
    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        """Generate a response from the model."""
        prompt = " ".join([m.content for m in messages])
        try:
            completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                temperature=self.temperature,
                max_tokens=8192
            )
            message = AIMessage(content=completion.choices[0].message.content)
            return {"generations": [{"message": message}]}
        except Exception as e:
            logging.error(f"Error generating response: {str(e)}")
            raise

    async def _agenerate(self, messages, stop=None, run_manager=None, **kwargs):
        """Async generation is not implemented."""
        raise NotImplementedError("Async generation not implemented")

    @property
    def _llm_type(self):
        """Get the LLM type."""
        return "groq"

class ChatAgent:
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
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Custom prompt template for the chatbot
        self.qa_template = """
        You are a helpful AI assistant with access to a knowledge base of documents.
        Use the following pieces of context to answer the question at the end.
        If you don't know the answer, just say that you don't know. DO NOT try to make up an answer.
        If the question is not related to the context, just respond based on your general knowledge.
        
        Context: {context}
        
        Chat History: {chat_history}
        
        Question: {question}
        
        Answer: """
        
        self.qa_prompt = PromptTemplate(
            template=self.qa_template,
            input_variables=["context", "chat_history", "question"]
        )
        
        # Initialize the conversation chain
        self.conversation = None
        self._initialize_chain()
    
    def _initialize_chain(self):
        """Initialize the conversation chain with the vector store."""
        try:
            vectorstore = self.doc_processor.query_documents("", k=1)
            if vectorstore and len(vectorstore) > 0:  # Only initialize if we have documents
                self.conversation = ConversationalRetrievalChain.from_llm(
                    llm=self.llm,
                    retriever=vectorstore.as_retriever(),
                    memory=self.memory,
                    combine_docs_chain_kwargs={"prompt": self.qa_prompt}
                )
                logging.info("Successfully initialized conversation chain with vector store")
            else:
                logging.info("No documents loaded yet")
                self.conversation = None
        except Exception as e:
            logging.warning(f"Error initializing conversation chain: {str(e)}")
            self.conversation = None
    
    def process_message(self, message: str) -> Dict[str, Any]:
        """Process a user message and return a response."""
        try:
            # If we have documents loaded, use RAG
            if self.conversation:
                response = self.conversation({"question": message})
                return {
                    "response": response["answer"],
                    "source_documents": response.get("source_documents", [])
                }
            
            # Otherwise, just use the base LLM
            completion = self.llm.client.chat.completions.create(
                messages=[{"role": "user", "content": message}],
                model=self.llm.model,
                temperature=self.llm.temperature,
                max_tokens=4096
            )
            return {
                "response": completion.choices[0].message.content,
                "source_documents": []
            }
        except Exception as e:
            logging.error(f"Error processing message: {str(e)}", exc_info=True)
            return {
                "response": "I apologize, but I encountered an error processing your message. This might be due to API limits or connectivity issues. Please try again later or contact support if the issue persists.",
                "source_documents": []
            }
    
    def add_documents(self, documents: List[Any]):
        """Add new documents to the knowledge base."""
        try:
            vectorstore = self.doc_processor.process_documents(documents)
            self.conversation = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=vectorstore.as_retriever(),
                memory=self.memory,
                combine_docs_chain_kwargs={"prompt": self.qa_prompt}
            )
            logging.info("Successfully added documents to knowledge base")
        except Exception as e:
            logging.error(f"Error adding documents: {str(e)}")
            raise
