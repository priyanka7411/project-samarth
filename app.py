import streamlit as st
from ai_system import IntelligentQASystem
import time
from dotenv import load_dotenv

load_dotenv()

# Page config
st.set_page_config(
    page_title="Project Samarth - Agricultural Q&A",
    page_icon="🌾",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #2E7D32;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .source-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'qa_system' not in st.session_state:
    st.session_state.qa_system = IntelligentQASystem()
if 'history' not in st.session_state:
    st.session_state.history = []

# Header
st.markdown('<h1 class="main-header">🌾 Project Samarth</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Intelligent Q&A System for Indian Agricultural & Climate Data</p>', unsafe_allow_html=True)

# Sidebar with info
with st.sidebar:
    st.header("📊 About")
    st.write("""
    This system answers questions about Indian agriculture and climate by:
    - Analyzing your natural language question
    - Fetching relevant data from data.gov.in APIs
    - Providing AI-powered insights with source citations
    """)
    
    st.header("💡 Example Questions")
    examples = [
        "Compare rice production in Punjab and Tamil Nadu for 2014",
        "What is the wheat production trend in Haryana from 2010 to 2014?",
        "Show rainfall patterns in Kerala for 2020",
        "Which districts in Maharashtra have highest sugarcane production in 2013?"
    ]
    
    for example in examples:
        if st.button(example, key=example):
            st.session_state.current_question = example
    
    st.header("📚 Data Sources")
    st.write("""
    - **Crop Production**: District-wise, season-wise data (1997-2014)
    - **Rainfall**: Daily district-wise data (2018-present)
    - **Source**: data.gov.in APIs
    """)

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Ask Your Question")
    
    # Question input
    question = st.text_input(
        "Enter your question:",
        value=st.session_state.get('current_question', ''),
        placeholder="e.g., Compare rice production in Punjab and Kerala for 2013"
    )
    
    col_btn1, col_btn2 = st.columns([1, 4])
    with col_btn1:
        ask_button = st.button("🔍 Ask", type="primary")
    with col_btn2:
        clear_button = st.button("🗑️ Clear History")
    
    if clear_button:
        st.session_state.history = []
        st.rerun()
    
    # Process question
    if ask_button and question:
        with st.spinner("🤔 Analyzing question and fetching data..."):
            try:
                result = st.session_state.qa_system.answer_question(question)
                st.session_state.history.insert(0, result)
                
            except Exception as e:
                st.error(f"Error: {e}")

with col2:
    st.header("📈 Query Analysis")
    if st.session_state.history:
        latest = st.session_state.history[0]
        st.info(f"**Type:** {latest['analysis']['query_type'].title()}")
        if latest['analysis']['states']:
            st.success(f"**States:** {', '.join(latest['analysis']['states'])}")
        if latest['analysis']['crops']:
            st.success(f"**Crops:** {', '.join(latest['analysis']['crops'])}")
        if latest['analysis']['years']:
            st.success(f"**Years:** {', '.join(map(str, latest['analysis']['years']))}")

# Display results
if st.session_state.history:
    st.header("📝 Results")
    
    for idx, result in enumerate(st.session_state.history):
        with st.expander(f"Q: {result['question']}", expanded=(idx == 0)):
            # Answer
            st.markdown("### 💡 Answer")
            st.write(result['answer'])
            
            # Sources
            st.markdown("### 📚 Data Sources")
            for source in result['sources']:
                st.markdown(f"- ✅ {source}")
            
            st.markdown("---")
else:
    st.info("👆 Ask a question to get started!")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #888; padding: 2rem;'>
        <p>🚀 Built for data-driven agricultural insights | Powered by data.gov.in APIs</p>
    </div>
    """,
    unsafe_allow_html=True
)