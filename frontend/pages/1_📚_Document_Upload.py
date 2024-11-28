"""
Document Upload and Management Interface
"""
import streamlit as st
import os
from pathlib import Path
import tempfile
from typing import List, Dict, Any
import logging

# Add parent directory to path to import app modules
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from app.utils.document_processor import DocumentProcessor
from app.utils.memory import MemoryManager

def initialize_document_processor():
    """Initialize the document processor if not in session state."""
    if 'doc_processor' not in st.session_state:
        st.session_state.doc_processor = DocumentProcessor()

def display_upload_interface():
    """Display the document upload interface."""
    st.title("📚 Document Upload")
    st.markdown("""
    Upload your documents to enhance the chatbot's knowledge. Supported formats:
    - PDF (.pdf)
    - Text (.txt)
    - Word (.doc, .docx)
    - Markdown (.md)
    - PowerPoint (.ppt, .pptx)
    - Excel (.xls, .xlsx)
    """)

    # File uploader
    uploaded_files = st.file_uploader(
        "Choose files to upload",
        accept_multiple_files=True,
        type=['pdf', 'txt', 'doc', 'docx', 'md', 'ppt', 'pptx', 'xls', 'xlsx']
    )

    if uploaded_files:
        process_uploaded_files(uploaded_files)

def process_uploaded_files(files: List[Any]):
    """Process uploaded files and store them in vector database."""
    progress_bar = st.progress(0)
    status_text = st.empty()

    try:
        for idx, file in enumerate(files):
            status_text.text(f"Processing {file.name}...")
            
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.name).suffix) as tmp_file:
                tmp_file.write(file.getvalue())
                tmp_path = tmp_file.name

            try:
                # Process and vectorize the document
                doc_id = st.session_state.doc_processor.process_document(
                    file_path=tmp_path,
                    file_name=file.name
                )
                
                if doc_id:
                    st.success(f"Successfully processed {file.name}")
                
            finally:
                # Clean up temporary file
                os.unlink(tmp_path)
            
            # Update progress
            progress_bar.progress((idx + 1) / len(files))

        status_text.text("All files processed successfully!")
        
        # Show uploaded documents
        display_uploaded_documents()

    except Exception as e:
        st.error(f"Error processing files: {str(e)}")
        logging.error(f"Document processing error: {str(e)}")

def display_uploaded_documents():
    """Display the list of uploaded documents."""
    if hasattr(st.session_state, 'doc_processor'):
        docs = st.session_state.doc_processor.list_documents()
        if docs:
            st.subheader("📑 Uploaded Documents")
            for doc in docs:
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.write(f"📄 {doc['name']}")
                with col2:
                    st.write(f"Added: {doc['timestamp']}")
                with col3:
                    if st.button("🗑️", key=f"delete_{doc['id']}"):
                        st.session_state.doc_processor.delete_document(doc['id'])
                        st.rerun()

def main():
    """Main function for document upload page."""
    # Initialize components
    initialize_document_processor()
    
    # Display interface
    display_upload_interface()

if __name__ == "__main__":
    main()
