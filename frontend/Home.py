"""
Home page and main entry point for the Dynamic AI Assistant
"""
import streamlit as st
from pathlib import Path

def set_custom_style():
    # Set dark theme
    st.markdown("""
        <style>
        /* Dark theme colors */
        :root {
            --bg-color: #1a1a1a;
            --card-bg: #2d2d2d;
            --text-color: #e0e0e0;
            --border-color: #4b6cb7;
            --hover-color: #3d3d3d;
        }
        
        .main-header {
            background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
            padding: 2rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .feature-card {
            background-color: var(--card-bg);
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 4px solid var(--border-color);
            margin-bottom: 1rem;
            color: var(--text-color);
        }
        
        .feature-card:hover {
            background-color: var(--hover-color);
            transition: background-color 0.3s ease;
        }
        
        .metric-card {
            background: var(--card-bg);
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            text-align: center;
            color: var(--text-color);
        }
        
        .metric-value {
            font-size: 2rem;
            font-weight: bold;
            color: #4b6cb7;
        }
        
        .quick-start-card {
            background: var(--card-bg);
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            margin-bottom: 1rem;
            color: var(--text-color);
        }
        
        .quick-start-card:hover {
            background-color: var(--hover-color);
            transition: background-color 0.3s ease;
        }
        
        /* Override Streamlit's default text colors */
        .stMarkdown, p, h1, h2, h3, h4, li {
            color: var(--text-color) !important;
        }
        
        /* Style for buttons */
        .stButton button {
            background-color: #4b6cb7;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            transition: all 0.3s ease;
        }
        
        .stButton button:hover {
            background-color: #3b5998;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        
        /* Dark scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
            background: var(--bg-color);
        }
        
        ::-webkit-scrollbar-thumb {
            background: #4b6cb7;
            border-radius: 5px;
        }
        
        ::-webkit-scrollbar-track {
            background: var(--card-bg);
        }
        </style>
    """, unsafe_allow_html=True)

def display_welcome():
    st.markdown("""
        <div class="main-header">
            <h1>🤖 Dynamic AI Assistant</h1>
            <p style='font-size: 1.2rem;'>Your intelligent companion for document analysis and natural conversation</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Key Metrics Row
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">Groq</div>
                <p>Powered by Mixtral-8x7B</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">ChromaDB</div>
                <p>Vector Store</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">RAG</div>
                <p>Enhanced Responses</p>
            </div>
        """, unsafe_allow_html=True)

    # Features Section
    st.markdown("### 🌟 Core Capabilities")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="feature-card">
                <h4>💬 Intelligent Chat</h4>
                <ul>
                    <li>Natural conversation with context awareness</li>
                    <li>Wikipedia-style document citations</li>
                    <li>Multi-document knowledge integration</li>
                    <li>Seamless context switching</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="feature-card">
                <h4>🔍 Smart Search</h4>
                <ul>
                    <li>Semantic search capabilities</li>
                    <li>Cross-document references</li>
                    <li>Relevant snippet extraction</li>
                    <li>Context-aware responses</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="feature-card">
                <h4>📚 Document Processing</h4>
                <ul>
                    <li>Support for PDF, TXT, DOCX, MD</li>
                    <li>Advanced text extraction</li>
                    <li>Efficient vectorization</li>
                    <li>Document management tools</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="feature-card">
                <h4>⚙️ Customization</h4>
                <ul>
                    <li>Adjustable chat parameters</li>
                    <li>Processing controls</li>
                    <li>Vector store management</li>
                    <li>Interface preferences</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

def display_quick_start():
    st.markdown("### 🚀 Quick Start")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="quick-start-card">
                <h4>📝 Document Upload</h4>
                <ol>
                    <li>Click 'Document Upload' in sidebar</li>
                    <li>Drop your files or browse</li>
                    <li>Supported: PDF, TXT, DOCX, MD</li>
                    <li>View processing status</li>
                </ol>
                </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Document Upload", type="primary"):
            st.switch_page("pages/Document_Upload.py")
    
    with col2:
        st.markdown("""
            <div class="quick-start-card">
                <h4>💭 Start Chatting</h4>
                <ol>
                    <li>Select 'Chat' in sidebar</li>
                    <li>Type your message</li>
                    <li>Get AI responses with citations</li>
                    <li>View document references</li>
                </ol>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Chat", type="primary"):
            st.switch_page("pages/Chat.py")

def main():
    st.set_page_config(
        page_title="Dynamic AI Assistant",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': None,
            'Report a bug': None,
            'About': None
        }
    )
    
    # Configure dark theme
    st.markdown("""
        <style>
        .stApp {
            background-color: #1a1a1a;
        }
        </style>
    """, unsafe_allow_html=True)
    
    set_custom_style()
    display_welcome()
    display_quick_start()

if __name__ == "__main__":
    main()
