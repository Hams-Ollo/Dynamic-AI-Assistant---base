"""
Document processing utilities for chat agents.
"""
from typing import List, Dict, Any, Optional
import logging
from pathlib import Path

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

class DocumentProcessor:
    """Processes and chunks documents for vector storage."""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """Initialize document processor.
        
        Args:
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            is_separator_regex=False
        )
    
    def process_text(self, text: str) -> List[Document]:
        """Process raw text into chunks.
        
        Args:
            text: Raw text to process
            
        Returns:
            List of Document objects
        """
        try:
            return self.text_splitter.create_documents([text])
        except Exception as e:
            logging.error(f"Error processing text: {str(e)}")
            return []
    
    def process_file(self, file_path: Path) -> List[Document]:
        """Process a file into chunks.
        
        Args:
            file_path: Path to file
            
        Returns:
            List of Document objects
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            return self.process_text(text)
        except Exception as e:
            logging.error(f"Error processing file {file_path}: {str(e)}")
            return []
    
    def process_documents(self, documents: List[Any]) -> List[Document]:
        """Process multiple documents into chunks.
        
        Args:
            documents: List of documents to process
            
        Returns:
            List of processed Document objects
        """
        processed_docs = []
        for doc in documents:
            if isinstance(doc, str):
                processed_docs.extend(self.process_text(doc))
            elif isinstance(doc, Path):
                processed_docs.extend(self.process_file(doc))
            elif isinstance(doc, Document):
                processed_docs.append(doc)
            else:
                logging.warning(f"Unsupported document type: {type(doc)}")
        return processed_docs
        
    def query_documents(self, query: str, documents: List[Document], top_k: int = 3) -> List[Document]:
        """Query documents for relevant context.
        
        Args:
            query: Search query
            documents: List of documents to search
            top_k: Number of most relevant documents to return
            
        Returns:
            List of most relevant documents
        """
        try:
            # Simple keyword matching for now
            # In a real implementation, you'd want to use embeddings and similarity search
            matched_docs = []
            query_terms = set(query.lower().split())
            
            for doc in documents:
                content = doc.page_content.lower()
                matches = sum(1 for term in query_terms if term in content)
                if matches > 0:
                    matched_docs.append((matches, doc))
            
            # Sort by number of matches and take top_k
            matched_docs.sort(key=lambda x: x[0], reverse=True)
            return [doc for _, doc in matched_docs[:top_k]]
            
        except Exception as e:
            logging.error(f"Error querying documents: {str(e)}")
            return []
