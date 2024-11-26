"""
Home Page with Quick Start Guide
"""
import streamlit as st
from pathlib import Path
import sys

# Add parent directory to path to import app modules
sys.path.append(str(Path(__file__).parent.parent.parent))

def display_quick_guide():
    """Display the quick start guide."""
    st.title("🏠 Welcome to AI Chat Assistant")
    
    st.markdown("""
    ## 🚀 Quick Start Guide
    
    Welcome to our advanced AI Chat Assistant! This guide will help you get started with all the features.
    
    ### 📱 Available Pages
    
    1. **🏠 Home (Current Page)**
       - Overview and quick start guide
       - Tips for best results
    
    2. **💬 Chat**
       - Main chat interface
       - Context-aware conversations
       - Access to uploaded knowledge
    
    3. **📚 Document Upload**
       - Upload your documents
       - Manage uploaded files
       - Enhance chatbot knowledge
    
    ### 💡 Tips for Best Results
    
    1. **Document Upload**
       - Upload relevant documents for more informed responses
       - Supported formats: PDF, TXT, DOCX, MD
       - Files are processed and securely stored
    
    2. **Chat Interface**
       - Be specific in your questions
       - Reference uploaded documents when needed
       - Use follow-up questions for clarification
    
    3. **Context Management**
       - The chat maintains conversation history
       - Previous context is considered in responses
       - Clear chat for fresh conversations
    
    ### 🔒 Privacy & Security
    
    - Documents are processed locally
    - No data is shared with external services
    - Uploaded files can be deleted anytime
    
    ### 🆘 Need Help?
    
    - Use clear, specific questions
    - Check uploaded documents status
    - Review conversation history
    """)

def main():
    """Main function for home page."""
    display_quick_guide()

if __name__ == "__main__":
    main()
