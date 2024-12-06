"""
Document Upload and Management Interface
"""
import streamlit as st
import os
from pathlib import Path
import tempfile
from typing import List, Dict, Any
import logging
import pandas as pd
from datetime import datetime
import humanize
import time
import uuid

# Add parent directory to path to import app modules
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from app.utils.document_processor import DocumentProcessor
from app.utils.memory import MemoryManager

def initialize_document_processor():
    """Initialize the document processor if not already initialized."""
    if 'doc_processor' not in st.session_state:
        st.session_state.doc_processor = DocumentProcessor(
            config={"vector_store_type": "chroma"}
        )
    elif not hasattr(st.session_state.doc_processor, 'vector_store'):
        # Reinitialize if vector store is missing
        st.session_state.doc_processor.initialize_vector_store()

def clear_session_state():
    """Clear all document-related session state."""
    if 'doc_processor' in st.session_state:
        # Ensure proper cleanup of existing processor
        try:
            st.session_state.doc_processor._cleanup_vector_store()
        except Exception as e:
            logging.error(f"Error cleaning up vector store: {str(e)}")
    
    keys_to_clear = ['uploaded_files', 'messages', 'doc_processor']
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
    # Force reinitialization of document processor
    initialize_document_processor()

def process_uploaded_files(files: List[Any]):
    """Process uploaded files and store them in vector database."""
    progress_bar = st.progress(0)
    status_text = st.empty()
    error_container = st.empty()
    success_container = st.empty()
    
    errors = []
    processed = 0

    try:
        for idx, file in enumerate(files):
            status_text.text(f"Processing {file.name}...")
            
            try:
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.name).suffix) as tmp_file:
                    tmp_file.write(file.getvalue())
                    tmp_path = tmp_file.name

                # Process the document
                doc_id = st.session_state.doc_processor.process_document(tmp_path, file.name)
                
                if not doc_id:
                    errors.append(f"Failed to process {file.name}")
                else:
                    processed += 1
                
                # Update progress
                progress = (idx + 1) / len(files)
                progress_bar.progress(progress)
                
                # Clean up temporary file
                try:
                    os.unlink(tmp_path)
                except Exception as e:
                    logging.warning(f"Error cleaning up temporary file {tmp_path}: {str(e)}")

            except Exception as e:
                errors.append(f"Error processing {file.name}: {str(e)}")
                logging.error(f"Error processing {file.name}: {str(e)}")

        # Show final status
        if errors:
            error_text = "\n".join(errors)
            error_container.error(f"Failed to process some files:\n{error_text}")
        
        if processed > 0:
            success_container.success(f"Successfully processed {processed} file{'s' if processed > 1 else ''}!")
        
        # Clear progress indicators after a delay
        time.sleep(1)
        progress_bar.empty()
        status_text.empty()
            
    except Exception as e:
        st.error(f"Error processing files: {str(e)}")
        logging.error(f"Error processing files: {str(e)}")

def handle_file_upload():
    """Handle file upload and processing."""
    st.markdown("### 📤 Document Upload")
    
    # Create a unique key for the file uploader based on session state
    uploader_key = f"file_uploader_{st.session_state.get('uploader_reset_counter', 0)}"
    
    uploaded_files = st.file_uploader(
        "Choose files to upload",
        accept_multiple_files=True,
        type=["pdf", "txt", "docx", "md"],
        help="Limit 200MB per file • PDF, TXT, DOCX, MD",
        key=uploader_key
    )

    # Track uploaded files to prevent duplicates
    if 'processed_files' not in st.session_state:
        st.session_state.processed_files = set()

    if uploaded_files:
        # Filter out already processed files
        new_files = [f for f in uploaded_files if f.name not in st.session_state.processed_files]
        if new_files:
            process_uploaded_files(new_files)
            # Add processed files to tracking set
            st.session_state.processed_files.update(f.name for f in new_files)

def handle_document_deletion(doc_id: str, filename: str):
    """Handle deletion of a single document."""
    if not hasattr(st.session_state, 'doc_processor'):
        st.error("Document processor not initialized")
        return

    # Create columns for better message placement
    col1, col2 = st.columns([6, 1])
    with col1:
        with st.spinner(""):
            success = st.session_state.doc_processor.delete_document(doc_id)
            if success:
                # Remove the file from processed files tracking
                if 'processed_files' in st.session_state:
                    st.session_state.processed_files.discard(filename)
                
                # Increment the uploader reset counter
                if 'uploader_reset_counter' not in st.session_state:
                    st.session_state.uploader_reset_counter = 0
                st.session_state.uploader_reset_counter += 1
                
                # Use a more subtle success message with custom styling
                message_container = st.empty()
                message_container.markdown("""
                    <style>
                    .delete-success {
                        padding: 0.75rem;
                        border-radius: 0.5rem;
                        background-color: rgba(40, 167, 69, 0.1);
                        border: 1px solid rgba(40, 167, 69, 0.2);
                        color: rgb(40, 167, 69);
                        text-align: center;
                        margin: 1rem 0;
                        animation: fadeInOut 2s ease-in-out forwards;
                        position: relative;
                        z-index: 1000;
                    }
                    @keyframes fadeInOut {
                        0% { opacity: 0; transform: translateY(0); }
                        10% { opacity: 1; transform: translateY(0); }
                        90% { opacity: 1; transform: translateY(0); }
                        100% { opacity: 0; }
                    }
                    </style>
                    <div class="delete-success">Document deleted successfully</div>
                    """, unsafe_allow_html=True)
                time.sleep(2)
                message_container.empty()
                st.rerun()
            else:
                st.error("Failed to delete document")

def handle_clear_all_documents():
    """Handle clearing all documents."""
    if not hasattr(st.session_state, 'doc_processor'):
        st.warning("No documents to clear")
        return
    
    if not st.session_state.doc_processor.list_documents():
        st.warning("No documents to clear")
        return

    with st.spinner("Clearing all documents..."):
        try:
            # First cleanup vector store
            st.session_state.doc_processor._cleanup_vector_store()
            # Reinitialize vector store
            st.session_state.doc_processor.initialize_vector_store()
            # Clear documents
            success = st.session_state.doc_processor.clear_all_documents()
            
            if success:
                # Clear processed files tracking
                if 'processed_files' in st.session_state:
                    st.session_state.processed_files.clear()
                
                # Increment the uploader reset counter
                if 'uploader_reset_counter' not in st.session_state:
                    st.session_state.uploader_reset_counter = 0
                st.session_state.uploader_reset_counter += 1
                
                # Create a custom success message container
                message = st.empty()
                message.success("All documents cleared successfully")
                # Auto-dismiss after 2 seconds
                time.sleep(2)
                message.empty()
                st.rerun()
            else:
                st.error("Failed to clear documents")
        except Exception as e:
            st.error(f"Error clearing documents: {str(e)}")
            logging.error(f"Error clearing documents: {str(e)}")

def display_uploaded_documents():
    """Display the list of uploaded documents with delete buttons."""
    if not hasattr(st.session_state, 'doc_processor'):
        st.info("No documents uploaded yet")
        return
        
    docs = st.session_state.doc_processor.list_documents()
    if not docs:
        st.info("No documents uploaded yet")
        return

    st.markdown("#### 📄 Uploaded Documents")
    
    for doc in docs:
        col1, col2, col3 = st.columns([6, 2, 1])
        with col1:
            st.text(doc['name'])
        with col2:
            st.text(f"Added: {doc['timestamp'].split('T')[0]}")
        with col3:
            if st.button("🗑️", key=f"delete_{doc['id']}", help="Delete document"):
                handle_document_deletion(doc['id'], doc['name'])

def document_management_ui():
    """Document management interface."""
    st.title("Document Management")
    
    # Document Manager Section
    st.markdown("### 📑 Document Manager")
    
    # Search and filter
    col1, col2 = st.columns([3, 2])
    with col1:
        st.text_input("Search documents", key="search_docs")
    with col2:
        st.selectbox("Filter by Category", ["Choose an option"], key="filter_category")
    
    # Document stats
    total_docs = len(st.session_state.doc_processor.list_documents()) if hasattr(st.session_state, 'doc_processor') else 0
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Documents", total_docs)
    with col2:
        st.metric("Total Size", "0 Bytes")  # You can calculate actual size if needed
    with col3:
        st.metric("File Types", "1")  # You can calculate actual types if needed
    
    # Document Upload Section
    handle_file_upload()
    
    # Display uploaded documents
    display_uploaded_documents()
    
    # Settings Section
    with st.sidebar:
        st.subheader("Document Processing Settings")
        
        # Knowledge Base Settings
        st.subheader("Knowledge Base Settings")
        chunk_size = st.slider("Chunk Size", 100, 1000, 500)
        st.selectbox("Embedding Model", ["HuggingFace"], key="embedding_model")
        temperature = st.slider("Temperature", 0.00, 1.00, 0.70)
        context_size = st.slider("Context Window Size", 1000, 8192, 2000)
        
        # Vector Store Settings
        st.subheader("Vector Store Settings")
        st.selectbox("Vector Store", ["Chroma"], key="vector_store")
        
        # Clear All Documents Button
        if st.button("🗑️ Clear All Documents", type="primary", use_container_width=True):
            if hasattr(st.session_state, 'doc_processor'):
                handle_clear_all_documents()

def main():
    """Main function for document upload page."""
    initialize_document_processor()
    document_management_ui()

if __name__ == "__main__":
    main()
