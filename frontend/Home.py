"""
Home page and main entry point for the Dynamic AI Assistant
"""
import streamlit as st
from pathlib import Path

def display_welcome():
    st.title("🤖 Welcome to Dynamic AI Assistant")
    
    st.markdown("""
    A sophisticated AI assistant powered by LLaMA 3 70B, featuring advanced RAG capabilities 
    and multi-modal interactions.
    
    ### 🌟 Key Features
    
    #### 💬 AI Chat
    - Context-aware conversations using RAG
    - Multi-document knowledge integration
    - Intelligent response generation
    - Chat history management
    
    #### 📚 Document Management
    - Support for multiple file formats (PDF, TXT, DOCX, MD)
    - Advanced document processing and vectorization
    - Document tagging and categorization
    - Semantic search capabilities
    
    #### ⚙️ Customization Options
    - Adjustable knowledge base settings
    - Configurable chat parameters
    - Document processing controls
    - Interface preferences
    """)

def display_quick_start():
    st.header("🚀 Quick Start Guide")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 Upload Documents")
        st.markdown("""
        1. Navigate to 'Document Upload' in the sidebar
        2. Upload your documents (PDF, TXT, DOCX, MD)
        3. Configure processing settings if needed
        4. View document statistics and manage uploads
        """)
        
        if st.button("Go to Document Upload"):
            st.switch_page("pages/Document_Upload.py")
    
    with col2:
        st.subheader("💭 Start Chatting")
        st.markdown("""
        1. Click on 'Chat' in the sidebar
        2. Type your question or prompt
        3. Get AI responses with document context
        4. Manage conversation history
        """)
        
        if st.button("Go to Chat"):
            st.switch_page("pages/Chat.py")

def display_system_status():
    st.header("🔧 System Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("System Status", "Online ✅")
    with col2:
        st.metric("Documents Loaded", "Ready 📚")
    with col3:
        st.metric("AI Model", "LLaMA 3 70B 🧠")

def main():
    st.set_page_config(
        page_title="Dynamic AI Assistant",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Display components
    display_welcome()
    display_quick_start()
    display_system_status()
    
    # Footer
    st.markdown("---")
    st.markdown("Made with ❤️ by hams_ollo")

if __name__ == "__main__":
    main()
