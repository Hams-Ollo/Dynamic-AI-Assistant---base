"""
Enhanced Home Page with Comprehensive Guide
"""
import streamlit as st
from pathlib import Path
import sys

# Add parent directory to path to import app modules
sys.path.append(str(Path(__file__).parent.parent.parent))

def display_quick_guide():
    """Display the comprehensive guide."""
    st.title("🌟 Welcome to hams_ollo_AI, Your Dynamic Multi-Agent AI Assistant")
    
    # Introduction with animated container
    with st.container():
        st.markdown("""
        ## 🎯 About This System
        
        Welcome to hams_ollo_AI, Your Dynamic Multi-Agent AI Assistant! This intelligent system leverages multiple specialized AI agents 
        working together to provide comprehensive assistance for your tasks. Each agent has specific expertise and 
        collaborates seamlessly to deliver the best possible results.
        """)

    # Key Features in an expander
    with st.expander("✨ Key Features", expanded=True):
        st.markdown("""
        - 🤖 **Multi-Agent Architecture**
          - Specialized agents for different tasks
          - Collaborative problem-solving
          - Dynamic task delegation
        
        - 🧠 **Advanced Capabilities**
          - Context-aware conversations
          - Document analysis and understanding
          - Complex task breakdown and execution
          
        - 🔄 **Real-time Processing**
          - Live agent interaction visualization
          - Step-by-step reasoning display
          - Transparent decision-making process
        """)

    # Navigation Guide
    st.markdown("## 🗺️ Navigation Guide")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📱 Core Pages
        
        1. **🏠 Home (Current)**
           - System overview
           - Feature guides
           - Best practices
        
        2. **💬 Chat**
           - Multi-agent interactions
           - Context-aware discussions
           - Real-time processing
        """)
    
    with col2:
        st.markdown("""
        3. **📚 Document Upload**
           - File management
           - Knowledge base enhancement
           - Supported formats
        
        4. **📊 System Monitor**
           - Agent status tracking
           - Performance metrics
           - System health
        """)

    # Usage Guidelines in an expander
    with st.expander("📖 Usage Guidelines", expanded=False):
        st.markdown("""
        ### 🎯 Getting the Best Results
        
        1. **Effective Communication**
           - Be specific in your requests
           - Provide relevant context
           - Use follow-up questions for clarification
        
        2. **Document Management**
           - Upload relevant documents (PDF, TXT, DOCX, MD)
           - Organize files by topic
           - Remove outdated materials
        
        3. **System Interaction**
           - Monitor agent activities
           - Review agent reasoning
           - Provide feedback when needed
        """)

    # Advanced Features in an expander
    with st.expander("🚀 Advanced Features", expanded=False):
        st.markdown("""
        ### 💫 Power User Features
        
        1. **Agent Collaboration**
           - Watch agents work together
           - Understand decision processes
           - Track task progression
        
        2. **Knowledge Integration**
           - Custom knowledge base
           - Document cross-referencing
           - Context preservation
        
        3. **System Optimization**
           - Performance monitoring
           - Resource management
           - Error handling
        """)

    # Privacy and Security
    st.markdown("""
    ## 🔒 Privacy & Security
    
    - **Local Processing**: All documents are processed locally
    - **Data Protection**: No information shared with external services
    - **User Control**: Full control over uploaded data
    - **Secure Storage**: Encrypted data storage
    """)

    # Help and Support with custom styling
    st.markdown("""
    ## 🆘 Need Assistance?
    
    - **Quick Help**: Use the chat interface for immediate assistance
    - **Documentation**: Access comprehensive guides in the system
    - **Feedback**: Share your experience to help us improve
    """)

    # Pro Tips in a success message
    st.success("""
    💡 **Pro Tips**:
    - Start with simple queries and gradually increase complexity
    - Monitor agent interactions to understand the system better
    - Use the document upload feature to enhance response accuracy
    """)

def main():
    """Main function for home page."""
    display_quick_guide()

if __name__ == "__main__":
    main()
