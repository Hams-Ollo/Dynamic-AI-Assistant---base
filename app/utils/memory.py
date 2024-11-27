"""
Memory management for chat agents.
"""
from typing import Dict, Any, Optional, List
from pathlib import Path
import logging
from langchain_core.memory import BaseMemory
from langchain_community.chat_message_histories import ChatMessageHistory, RedisChatMessageHistory
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import json
from datetime import datetime
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

class MemoryManager:
    """Manages different types of memory for chat agents."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize memory manager with configuration."""
        self.config = config
        self.memory_type = config.get('type', 'vector')
        self.memory_path = Path(config.get('path', './data/memory'))
        
        # Ensure memory directory exists
        self.memory_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize storage files
        self.feedback_path = self.memory_path / "feedback.json"
        self.query_history_path = self.memory_path / "query_history.json"
        self.source_relevance_path = self.memory_path / "source_relevance.json"
        
        # Initialize TF-IDF vectorizer for query similarity
        self.vectorizer = TfidfVectorizer()
        self.query_vectors = None
        
        # Initialize appropriate memory system
        if self.memory_type == 'vector':
            self._init_vector_memory()
        else:
            self._init_buffer_memory()
            
        self._init_storage()
        
        logging.info(f"Initialized {self.memory_type} memory system")
    
    async def initialize(self):
        """Initialize the memory system."""
        try:
            # Ensure directories exist
            self.data_dir = Path("./data/memory")
            self.data_dir.mkdir(parents=True, exist_ok=True)
            
            # Initialize vector store
            self.vector_store = self._setup_vector_store()
            
            # Load conversation history
            self.conversation_history = []
            self._load_history()
            
            logging.info("Memory system initialized successfully")
            
        except Exception as e:
            logging.error(f"Failed to initialize memory system: {str(e)}")
            raise

    async def cleanup(self):
        """Cleanup resources used by the memory system."""
        try:
            # Save conversation history
            self._save_history()
            
            # Clean up vector store
            if hasattr(self, 'vector_store') and self.vector_store is not None:
                try:
                    # Some vector stores might need special cleanup
                    if hasattr(self.vector_store, '_client'):
                        await self.vector_store._client.close()
                except:
                    pass
            
            # Clear resources
            self.conversation_history = []
            self.vector_store = None
            
            logging.info("Memory system cleanup completed successfully")
            
        except Exception as e:
            logging.error(f"Error during memory system cleanup: {str(e)}")
            raise

    def _load_history(self):
        """Load conversation history from disk."""
        try:
            history_file = self.data_dir / "conversation_history.json"
            if history_file.exists():
                with open(history_file, 'r') as f:
                    self.conversation_history = json.load(f)
        except Exception as e:
            logging.warning(f"Failed to load conversation history: {str(e)}")

    def _save_history(self):
        """Save conversation history to disk."""
        try:
            history_file = self.data_dir / "conversation_history.json"
            with open(history_file, 'w') as f:
                json.dump(self.conversation_history, f)
        except Exception as e:
            logging.warning(f"Failed to save conversation history: {str(e)}")

    def _init_vector_memory(self):
        """Initialize vector store memory."""
        try:
            # Initialize embeddings with a local model
            self.embeddings = HuggingFaceEmbeddings(
                model_name="all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
            
            # Initialize vector store with collection name
            self.vector_store = Chroma(
                persist_directory=str(self.memory_path),
                embedding_function=self.embeddings,
                collection_name="chat_memory"
            )
            
            # Initialize conversation memory
            self.memory = ChatMessageHistory()
            self.message_history = self.memory
            
        except Exception as e:
            logging.error(f"Failed to initialize vector memory: {str(e)}")
            raise
    
    def _init_buffer_memory(self):
        """Initialize conversation memory using newer LangChain interface."""
        self.message_history = ChatMessageHistory()
        self.memory = {
            'history': self.message_history,
            'messages': []
        }
    
    def _init_storage(self):
        """Initialize the memory storage system."""
        if self.memory_type == 'vector':
            self._init_vector_memory()
        else:
            self._init_buffer_memory()
                
    def _save_json(self, path: Path, data: Any):
        """Save data to JSON file with error handling."""
        try:
            with open(path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logging.error(f"Error saving to {path}: {str(e)}")
            
    def _load_json(self, path: Path) -> Any:
        """Load data from JSON file with error handling."""
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Error loading from {path}: {str(e)}")
            return None
            
    def add_documents(self, documents: list):
        """Add documents to vector store if using vector memory."""
        if self.memory_type == 'vector':
            try:
                self.vector_store.add_documents(documents)
                logging.info(f"Added {len(documents)} documents to vector store")
            except Exception as e:
                logging.error(f"Failed to add documents to vector store: {str(e)}")
                raise
    
    def get_relevant_context(self, query: str) -> Optional[str]:
        """Retrieve relevant context from vector store."""
        if self.memory_type == 'vector':
            try:
                docs = self.vector_store.similarity_search(query)
                return "\n".join(doc.page_content for doc in docs)
            except Exception as e:
                logging.error(f"Failed to retrieve context: {str(e)}")
                return None
        return None
    
    def store_feedback(self, interaction_id: str, feedback: Dict[str, Any]):
        """Store user feedback for an interaction."""
        try:
            feedbacks = self._load_json(self.feedback_path)
            if feedbacks is None:
                feedbacks = []
                
            feedback['timestamp'] = datetime.now().isoformat()
            feedback['interaction_id'] = interaction_id
            feedbacks.append(feedback)
            
            self._save_json(self.feedback_path, feedbacks)
            
            # Update source relevance if provided
            if 'source_ratings' in feedback:
                self._update_source_relevance(feedback['source_ratings'])
                
        except Exception as e:
            logging.error(f"Error storing feedback: {str(e)}")
            
    def store_query(self, query: str, intent: str, urls: List[str], response: str):
        """Store query and related information."""
        try:
            queries = self._load_json(self.query_history_path)
            if queries is None:
                queries = []
                
            query_data = {
                'query': query,
                'intent': intent,
                'urls': urls,
                'response': response,
                'timestamp': datetime.now().isoformat()
            }
            queries.append(query_data)
            
            self._save_json(self.query_history_path, queries)
            
            # Update query vectors
            self._update_query_vectors()
            
        except Exception as e:
            logging.error(f"Error storing query: {str(e)}")
            
    def get_similar_queries(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Retrieve similar historical queries using TF-IDF similarity."""
        try:
            queries = self._load_json(self.query_history_path)
            if not queries:
                return []
                
            # Transform new query
            query_vector = self.vectorizer.transform([query])
            
            if self.query_vectors is None:
                self._update_query_vectors()
                
            # Calculate similarities
            similarities = np.dot(self.query_vectors, query_vector.T).toarray().flatten()
            
            # Get top similar queries
            similar_indices = np.argsort(similarities)[-limit:][::-1]
            return [queries[i] for i in similar_indices if similarities[i] > 0]
            
        except Exception as e:
            logging.error(f"Error getting similar queries: {str(e)}")
            return []
            
    def _update_query_vectors(self):
        """Update TF-IDF vectors for all queries."""
        queries = self._load_json(self.query_history_path)
        if queries:
            query_texts = [q['query'] for q in queries]
            self.query_vectors = self.vectorizer.fit_transform(query_texts)
            
    def _update_source_relevance(self, source_ratings: Dict[str, float]):
        """Update source relevance scores."""
        try:
            relevance = self._load_json(self.source_relevance_path)
            if relevance is None:
                relevance = {}
                
            for source, rating in source_ratings.items():
                if source in relevance:
                    # Running average of ratings
                    relevance[source]['count'] += 1
                    relevance[source]['score'] = (
                        (relevance[source]['score'] * (relevance[source]['count'] - 1) + rating)
                        / relevance[source]['count']
                    )
                else:
                    relevance[source] = {'score': rating, 'count': 1}
                    
            self._save_json(self.source_relevance_path, relevance)
            
        except Exception as e:
            logging.error(f"Error updating source relevance: {str(e)}")
            
    def get_source_relevance(self, source: str) -> Optional[float]:
        """Get relevance score for a source."""
        try:
            relevance = self._load_json(self.source_relevance_path)
            if relevance and source in relevance:
                return relevance[source]['score']
            return None
        except Exception as e:
            logging.error(f"Error getting source relevance: {str(e)}")
            return None
            
    def get_feedback_stats(self) -> Dict[str, Any]:
        """Get statistics about feedback."""
        try:
            feedbacks = self._load_json(self.feedback_path)
            if not feedbacks:
                return {
                    'total_feedback': 0,
                    'positive_feedback': 0,
                    'negative_feedback': 0,
                    'average_rating': 0.0
                }
                
            total = len(feedbacks)
            ratings = [f.get('rating', 0) for f in feedbacks if 'rating' in f]
            
            return {
                'total_feedback': total,
                'positive_feedback': sum(1 for r in ratings if r > 3),
                'negative_feedback': sum(1 for r in ratings if r <= 3),
                'average_rating': sum(ratings) / len(ratings) if ratings else 0.0
            }
            
        except Exception as e:
            logging.error(f"Error getting feedback stats: {str(e)}")
            return {
                'total_feedback': 0,
                'positive_feedback': 0,
                'negative_feedback': 0,
                'average_rating': 0.0
            }
            
    def _setup_vector_store(self):
        """Set up the vector store for semantic search."""
        try:
            # Initialize embeddings
            self.embeddings = HuggingFaceEmbeddings(
                model_name="all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
            
            # Set up Chroma store
            persist_directory = str(self.data_dir / "vector_store")
            return Chroma(
                persist_directory=persist_directory,
                embedding_function=self.embeddings,
                collection_name="chat_memory"
            )
            
        except Exception as e:
            logging.error(f"Failed to setup vector store: {str(e)}")
            raise
