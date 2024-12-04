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

# Add parent directory to path to import app modules
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from app.utils.document_processor import DocumentProcessor
from app.utils.memory import MemoryManager

def initialize_document_processor():
    """Initialize the document processor if not in session state."""
    if 'doc_processor' not in st.session_state:
        st.session_state.doc_processor = DocumentProcessor()

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

def get_document_stats(docs_dir: str) -> Dict:
    """Calculate document statistics from the documents directory"""
    stats = {
        "total_docs": 0,
        "total_size": 0,
        "file_types": {},
        "recent_uploads": []
    }
    
    for file in Path(docs_dir).glob("**/*"):
        if file.is_file():
            stats["total_docs"] += 1
            size = file.stat().st_size
            stats["total_size"] += size
            file_type = file.suffix
            stats["file_types"][file_type] = stats["file_types"].get(file_type, 0) + 1
            stats["recent_uploads"].append({
                "name": file.name,
                "size": size,
                "modified": datetime.fromtimestamp(file.stat().st_mtime)
            })
    
    # Sort recent uploads by date
    stats["recent_uploads"] = sorted(
        stats["recent_uploads"], 
        key=lambda x: x["modified"], 
        reverse=True
    )[:5]
    
    return stats

def document_management_ui():
    st.title("Document Management")
    
    # Sidebar Configuration
    st.sidebar.header("Document Processing Settings")
    
    # Knowledge Base Configuration
    st.sidebar.subheader("Knowledge Base Settings")
    chunk_size = st.sidebar.slider("Chunk Size", 100, 1000, 500, 50)
    embedding_model = st.sidebar.selectbox(
        "Embedding Model",
        ["OpenAI", "HuggingFace", "Custom"]
    )
    temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
    context_window = st.sidebar.slider("Context Window Size", 1000, 4000, 2000, 100)
    vector_store = st.sidebar.selectbox(
        "Vector Store",
        ["Pinecone", "Faiss", "Chroma"]
    )
    
    # Initialize session state for tags if not exists
    if 'document_tags' not in st.session_state:
        st.session_state.document_tags = {}
    
    # Document Statistics Section
    st.header("📊 Document Statistics")
    docs_dir = "documents"  # Update this path as needed
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)
    
    stats = get_document_stats(docs_dir)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Documents", stats["total_docs"])
    with col2:
        st.metric("Total Size", humanize.naturalsize(stats["total_size"]))
    with col3:
        st.metric("File Types", len(stats["file_types"]))
    
    # Document Upload Section
    st.header("📤 Document Upload")
    uploaded_files = st.file_uploader(
        "Choose files to upload",
        accept_multiple_files=True,
        type=['pdf', 'txt', 'docx', 'md']
    )

    if uploaded_files:
        process_uploaded_files(uploaded_files)

    # Document Management Section
    st.header("📑 Document Management")
    
    # Search and Filter
    col1, col2 = st.columns(2)
    with col1:
        search_term = st.text_input("Search documents", "")
    with col2:
        filter_category = st.multiselect(
            "Filter by Category",
            ["General", "Technical", "Legal", "Financial", "Other"]
        )
    
    # Document List with Actions
    st.subheader("Document List")
    if stats["recent_uploads"]:
        for doc in stats["recent_uploads"]:
            if (not search_term or search_term.lower() in doc["name"].lower()) and \
               (not filter_category or st.session_state.document_tags.get(doc["name"], {}).get("category") in filter_category):
                
                col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 1])
                
                with col1:
                    st.write(doc["name"])
                with col2:
                    st.write(humanize.naturalsize(doc["size"]))
                with col3:
                    st.write(doc["modified"].strftime("%Y-%m-%d %H:%M"))
                with col4:
                    if doc["name"] in st.session_state.document_tags:
                        st.write(", ".join(st.session_state.document_tags[doc["name"]]["tags"]))
                with col5:
                    if st.button("Delete", key=f"del_{doc['name']}"):
                        try:
                            os.remove(os.path.join(docs_dir, doc["name"]))
                            if doc["name"] in st.session_state.document_tags:
                                del st.session_state.document_tags[doc["name"]]
                            st.success(f"Deleted {doc['name']}")
                            st.experimental_rerun()
                        except Exception as e:
                            st.error(f"Error deleting file: {str(e)}")
    else:
        st.info("No documents uploaded yet")
    
    # File Type Distribution
    if stats["file_types"]:
        st.subheader("File Type Distribution")
        file_type_df = pd.DataFrame(
            list(stats["file_types"].items()),
            columns=["File Type", "Count"]
        )
        st.bar_chart(file_type_df.set_index("File Type"))

def main():
    """Main function for document upload page."""
    # Initialize components
    initialize_document_processor()
    
    # Display interface
    document_management_ui()

if __name__ == "__main__":
    main()
