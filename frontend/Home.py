#-------------------------------------------------------------------------------------#
# File: Home.py
# Description: Main application entry point and process manager
# Author: @hams_ollo
# Version: 0.0.3
# Last Updated: [2024-11-21]
#-------------------------------------------------------------------------------------#
# SETUP GUIDE:  streamlit run frontend\Home.py
#
# Initial Setup:
# 1. Create virtual environment  -> python -m venv venv
# 2. Activate virtual environment:
#    - Windows                   -> .\venv\Scripts\activate
#    - Unix/MacOS               -> source venv/bin/activate
# 3. Install requirements       -> pip install -r requirements.txt
# 4. Copy environment file      -> cp .env.example .env
# 5. Add your Groq API key to .env
#
# Running the Application:
# 1. Start the application      -> python main.py     /     streamlit run main.py
# 2. Access the web interface   -> http://localhost:8501
# 3. Stop the application      -> Ctrl+C
# 4. Deactivate virtual env    -> deactivate
#
# Development Commands:
# 1. Update dependencies       -> pip freeze > requirements.txt
# 2. Run with debug logging   -> python main.py --log-level=debug
# 3. Clear Streamlit cache    -> streamlit cache clear
#
# Git Quick Reference:
# 1. Initialize repository    -> git init
# 2. Add files to staging    -> git add .
# 3. Commit changes         -> git commit -m "your message"
# 4. Create new branch      -> git checkout -b branch-name
# 5. Switch branches        -> git checkout branch-name
# 6. Push to remote         -> git push -u origin branch-name
# 7. Pull latest changes    -> git pull origin branch-name
# 8. Check status          -> git status
# 9. View commit history   -> git log
#
#-------------------------------------------------------------------------------------#

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
