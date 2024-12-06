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
    if not hasattr(st.session_state, 'doc_processor'):
        try:
            config = {
                "vector_store_type": "chroma"
            }
            st.session_state.doc_processor = DocumentProcessor(config=config)
            
            # Store processed files in session state
            if 'processed_files' not in st.session_state:
                st.session_state.processed_files = set()
                
            return True
        except Exception as e:
            st.error(f"Failed to initialize document processor: {str(e)}")
            return False
    return True

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
    if not initialize_document_processor():
        return [], []
        
    successful_files = []
    failed_files = []
    
    for uploaded_file in files:
        try:
            # Save uploaded file temporarily
            temp_path = Path("temp") / uploaded_file.name
            temp_path.parent.mkdir(exist_ok=True)
            
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Process the document
            success = st.session_state.doc_processor.process_document(
                str(temp_path),
                uploaded_file.name
            )
            
            if success:
                successful_files.append(uploaded_file)
            else:
                failed_files.append((uploaded_file, "Processing failed"))
                
            # Clean up temp file
            temp_path.unlink()
            
        except Exception as e:
            failed_files.append((uploaded_file, str(e)))
            
    progress_bar = st.progress(0)
    status_text = st.empty()
    error_container = st.empty()
    success_container = st.empty()
    
    errors = []
    processed = 0

    try:
        for idx, file in enumerate(files):
            status_text.text(f"Processing {file.name}...")
            
            if file in successful_files:
                processed += 1
                
            # Update progress
            progress = (idx + 1) / len(files)
            progress_bar.progress(progress)
                
        # Show final status
        if failed_files:
            error_text = "\n".join([f"Failed to process {file[0].name}: {file[1]}" for file in failed_files])
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

def handle_document_deletion(doc_id: str, filename: str):
    """Handle the deletion of a document."""
    try:
        if st.session_state.doc_processor.delete_document(doc_id):
            st.toast(f"Document '{filename}' deleted successfully", icon="✅")
        else:
            st.error(f"Failed to delete document '{filename}'")
    except Exception as e:
        st.error(f"Error deleting document: {str(e)}")

def get_document_categories():
    """Get list of available document categories."""
    if not initialize_document_processor():
        return []
    
    # Get categories from document processor
    categories = st.session_state.doc_processor.get_available_categories()
    
    # Add "All Categories" as first option if there are any documents
    if categories:
        return ["All Categories"] + categories
    return []

def filter_documents(documents, search_query="", selected_category=""):
    """Filter documents based on search query and category."""
    filtered_docs = documents
    
    # Filter by category if selected
    if selected_category and selected_category != "All Categories":
        filtered_docs = [doc for doc in filtered_docs if doc.get('category') == selected_category]
    
    # Filter by search query if provided
    if search_query:
        search_lower = search_query.lower()
        filtered_docs = [
            doc for doc in filtered_docs 
            if search_lower in doc['filename'].lower()
        ]
    
    return filtered_docs

def display_file_content(doc):
    """Display the content of a document with syntax highlighting."""
    try:
        content = st.session_state.doc_processor.get_document_content(doc['filename'])
        if content:
            # Determine file type for syntax highlighting
            file_ext = Path(doc['filename']).suffix.lower()
            language = {
                '.py': 'python',
                '.js': 'javascript',
                '.html': 'html',
                '.css': 'css',
                '.md': 'markdown',
                '.json': 'json',
                '.txt': 'text',
                '.docx': 'text',
                '.pdf': 'text'
            }.get(file_ext, 'text')
            
            st.code(content, language=language)
        else:
            st.info("No content available for this document.")
    except Exception as e:
        st.error(f"Error displaying file content: {str(e)}")

def display_uploaded_documents():
    """Display the list of uploaded documents with expandable content view."""
    if not hasattr(st.session_state, 'doc_processor'):
        return

    documents = st.session_state.doc_processor.list_documents()
    search_query = st.session_state.get("doc_search", "")
    selected_category = st.session_state.get("category_filter", "")
    filtered_docs = filter_documents(documents, search_query, selected_category)
    
    if not filtered_docs:
        st.write("No documents uploaded yet.")
        return

    st.markdown("#### 📄 Uploaded Documents")
    
    # Initialize session state for expanded docs if not exists
    if 'expanded_docs' not in st.session_state:
        st.session_state.expanded_docs = set()
    
    # Custom CSS for document list and viewer
    st.markdown("""
        <style>
        .document-item {
            background-color: #1E1E1E;
            border: 1px solid #333;
            border-radius: 4px;
            padding: 8px 12px;
            margin: 4px 0;
        }
        .document-item:hover {
            background-color: #2D2D2D;
        }
        .document-name {
            color: #E0E0E0;
            font-size: 14px;
            font-weight: 500;
        }
        .document-meta {
            color: #A0A0A0;
            font-size: 12px;
        }
        .document-category {
            background-color: #2D2D2D;
            color: #E0E0E0;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 12px;
        }
        .file-viewer {
            background-color: #1E1E1E;
            border: 1px solid #333;
            border-radius: 4px;
            padding: 16px;
            margin: 8px 0;
        }
        .file-viewer-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }
        .close-button {
            background-color: #333;
            color: #E0E0E0;
            border: none;
            border-radius: 4px;
            padding: 4px 12px;
            cursor: pointer;
        }
        .close-button:hover {
            background-color: #444;
        }
        /* Hide the default Streamlit expander arrow */
        .streamlit-expanderHeader {
            display: none;
        }
        /* Style for delete button */
        .delete-button {
            background-color: transparent;
            border: 1px solid #FF4B4B;
            color: #FF4B4B;
            padding: 4px 8px;
            border-radius: 4px;
        }
        .delete-button:hover {
            background-color: #FF4B4B;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)
    
    for doc in filtered_docs:
        doc_id = doc['id']
        
        # Create a container for each document
        doc_container = st.container()
        
        with doc_container:
            # Document row with improved layout
            cols = st.columns([4, 2, 1.5, 1.5, 0.5])
            
            with cols[0]:
                doc_name = doc.get('filename', 'Unknown')
                if st.button(
                    f"📄 {doc_name}",
                    key=f"toggle_{doc_id}",
                    help="Click to view content",
                    use_container_width=True,
                ):
                    if doc_id in st.session_state.expanded_docs:
                        st.session_state.expanded_docs.remove(doc_id)
                    else:
                        st.session_state.expanded_docs.add(doc_id)
                        st.session_state.current_doc = doc_id
            
            with cols[1]:
                st.markdown(f"<div class='document-meta'>{doc.get('added_date', 'Unknown').split('T')[0]}</div>", unsafe_allow_html=True)
            
            with cols[2]:
                st.markdown(f"<div class='document-meta'>{humanize.naturalsize(doc.get('file_size', 0))}</div>", unsafe_allow_html=True)
            
            with cols[3]:
                st.markdown(f"<div class='document-category'>{doc.get('category', 'Unknown')}</div>", unsafe_allow_html=True)
            
            with cols[4]:
                if st.button("🗑️", key=f"delete_{doc_id}", help="Delete document", use_container_width=True):
                    handle_document_deletion(doc_id, doc_name)
                    if doc_id in st.session_state.expanded_docs:
                        st.session_state.expanded_docs.remove(doc_id)
                    st.rerun()
            
            # File viewer with improved styling
            if doc_id in st.session_state.expanded_docs:
                with st.container():
                    st.markdown("<div class='file-viewer'>", unsafe_allow_html=True)
                    st.markdown("<div class='file-viewer-header'>", unsafe_allow_html=True)
                    st.markdown(f"<h4>File Content: {doc_name}</h4>", unsafe_allow_html=True)
                    
                    # Close button
                    col1, col2 = st.columns([6, 1])
                    with col2:
                        if st.button("Close", key=f"close_{doc_id}", use_container_width=True):
                            st.session_state.expanded_docs.remove(doc_id)
                            st.rerun()
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Display file content
                    try:
                        content = st.session_state.doc_processor.get_document_content(doc_name)
                        if content:
                            file_ext = Path(doc_name).suffix.lower()
                            language = {
                                '.py': 'python',
                                '.js': 'javascript',
                                '.html': 'html',
                                '.css': 'css',
                                '.md': 'markdown',
                                '.json': 'json',
                                '.txt': 'text',
                                '.docx': 'text',
                                '.pdf': 'text'
                            }.get(file_ext, 'text')
                            
                            st.code(content, language=language)
                        else:
                            st.info("No content available for this document.")
                    except Exception as e:
                        st.error(f"Error displaying file content: {str(e)}")
                    
                    st.markdown("</div>", unsafe_allow_html=True)

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
            # Clear all documents using the processor method
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

def reprocess_documents():
    """Reprocess all documents to update categories."""
    if not hasattr(st.session_state, 'doc_processor'):
        return
    
    try:
        # Get list of current documents
        current_docs = st.session_state.doc_processor.list_documents()
        
        if not current_docs:
            st.warning("No documents to reprocess")
            return
        
        # Clear the vector store
        st.session_state.doc_processor.clear_all_documents()
        
        # Reprocess each document
        with st.spinner("Updating document categories..."):
            for doc in current_docs:
                filename = doc.get('filename')
                if filename:
                    # Get the original content
                    content = st.session_state.doc_processor.get_document_content(filename)
                    if content:
                        temp_path = Path("temp") / filename
                        temp_path.parent.mkdir(exist_ok=True)
                        
                        # Create temporary file with original content
                        with open(temp_path, "w", encoding="utf-8") as f:
                            f.write(content)
                        
                        # Reprocess the document
                        st.session_state.doc_processor.process_document(
                            str(temp_path),
                            filename
                        )
                        
                        # Clean up temp file
                        if temp_path.exists():
                            temp_path.unlink()
        
        st.success("Document categories updated!")
        time.sleep(1)
        st.rerun()
        
    except Exception as e:
        st.error(f"Error reprocessing documents: {str(e)}")

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
            st.rerun()

def document_management_ui():
    """Document management interface."""
    st.title("Document Management")
    
    # Initialize document processor
    if not initialize_document_processor():
        st.error("Failed to initialize document processor")
        return
    
    # Search and Category Filter
    col1, col2 = st.columns([3, 2])
    
    with col1:
        search_query = st.text_input("🔍 Search documents", key="doc_search")
    
    with col2:
        # Get available categories
        categories = get_document_categories()
        
        # If no documents uploaded yet, show placeholder
        if not categories:
            st.selectbox(
                "Filter by Category",
                ["No documents uploaded"],
                disabled=True,
                key="category_filter"
            )
        else:
            selected_category = st.selectbox(
                "Filter by Category",
                ["All Categories"] + categories,
                key="category_filter"
            )
    
    # Document statistics
    documents = st.session_state.doc_processor.list_documents()
    filtered_docs = filter_documents(documents, search_query, st.session_state.get("category_filter", ""))
    
    total_size = sum(doc.get('file_size', 0) for doc in filtered_docs)
    unique_types = len(set(doc.get('file_type', '') for doc in filtered_docs))
    
    stats_col1, stats_col2, stats_col3 = st.columns(3)
    with stats_col1:
        st.metric("Total Documents", len(filtered_docs))
    with stats_col2:
        st.metric("Total Size", humanize.naturalsize(total_size))
    with stats_col3:
        st.metric("File Types", unique_types)
    
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
        
        # Add some space before the buttons
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Document Management Actions
        st.subheader("Document Actions")
        
        # Custom CSS for buttons
        st.markdown("""
            <style>
            .stButton > button {
                width: 100%;
                border-radius: 4px;
                height: 42px;
                margin-top: 4px;
                margin-bottom: 4px;
            }
            .secondary-button > button {
                background-color: #262730;
                color: #fff;
                border: 1px solid #4B4B4B;
            }
            .secondary-button > button:hover {
                background-color: #3B3B3B;
                color: #fff;
                border: 1px solid #4B4B4B;
            }
            .danger-button > button {
                background-color: #262730;
                color: #FF4B4B;
                border: 1px solid #FF4B4B;
            }
            .danger-button > button:hover {
                background-color: #FF4B4B;
                color: #fff;
                border: 1px solid #FF4B4B;
            }
            </style>
            """, unsafe_allow_html=True)
        
        # Update Categories button with secondary styling
        st.markdown('<div class="secondary-button">', unsafe_allow_html=True)
        if st.button("🔄 Update Categories", use_container_width=True):
            reprocess_documents()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Small space between buttons
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        
        # Clear All button with danger styling
        st.markdown('<div class="danger-button">', unsafe_allow_html=True)
        if st.button("🗑️ Clear All Documents", use_container_width=True):
            if hasattr(st.session_state, 'doc_processor'):
                handle_clear_all_documents()
        st.markdown('</div>', unsafe_allow_html=True)

def main():
    """Main function for document upload page."""
    initialize_document_processor()
    document_management_ui()

if __name__ == "__main__":
    main()
