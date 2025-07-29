import streamlit as st
import requests
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI Research Analyzer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .upload-section {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 2px dashed #667eea;
        text-align: center;
        color: #333;
    }
    
    .upload-section h2 {
        color: #2c3e50;
        font-weight: bold;
    }
    
    .upload-section p {
        color: #34495e;
        font-size: 1.1rem;
    }
    
    .analysis-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
        color: #333;
    }
    
    .analysis-card h3 {
        color: #2c3e50;
        font-weight: bold;
    }
    
    .analysis-card p {
        color: #34495e;
    }
    
    .recommendation-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        transition: transform 0.3s ease;
    }
    
    .recommendation-card:hover {
        transform: translateY(-2px);
    }
    
    .success-message {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .success-message h3 {
        color: white;
        font-weight: bold;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
    }
    
    .success-message p {
        color: white;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        text-align: center;
        border: 1px solid #e0e0e0;
        color: #333;
    }
    
    .metric-card h4 {
        color: #2c3e50;
        font-weight: bold;
    }
    
    .metric-card p {
        color: #34495e;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

# FastAPI backend URL
API_URL = "http://localhost:8000"

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; color: white; padding: 1rem;">
        <h2>🧠 AI Research Analyzer</h2>
        <p>Advanced Research Paper Analysis & Recommendations</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 📊 Features")
    st.markdown("""
    - 📄 **PDF Upload & Processing**
    - 🔍 **AI-Powered Analysis**
    - 📝 **Smart Summarization**
    - 🎯 **Similar Paper Recommendations**
    - 🌐 **Internet Research Integration**
    """)
    
    st.markdown("---")
    
    st.markdown("### 🛠️ How it works")
    st.markdown("""
    1. Upload your research paper (PDF)
    2. Get AI-generated summary
    3. Find similar papers from database
    4. Discover related research online
    """)
    
    st.markdown("---")
    
    # Status indicator
    try:
        response = requests.get(f"{API_URL}/docs")
        if response.status_code == 200:
            st.success("✅ Backend Connected")
        else:
            st.error("❌ Backend Error")
    except:
        st.error("❌ Backend Offline")

# Main content
st.markdown("""
<div class="main-header">
    <h1>🧠 AI Research Paper Analyzer</h1>
    <p>Transform your research workflow with AI-powered analysis and intelligent recommendations</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'uploaded_paper' not in st.session_state:
    st.session_state.uploaded_paper = None
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False

# File Upload Section
st.markdown("""
<div class="upload-section">
    <h2>📄 Upload Your Research Paper</h2>
    <p>Drag and drop your PDF file or click to browse</p>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"], key="file_uploader")

if uploaded_file:
    # Show file info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📄 File Name", uploaded_file.name)
    with col2:
        st.metric("📏 File Size", f"{uploaded_file.size / 1024:.1f} KB")
    with col3:
        st.metric("📅 Upload Time", datetime.now().strftime("%H:%M:%S"))
    
    # Upload button
    if st.button("🚀 Upload & Process Paper", key="upload_btn"):
        with st.spinner("🔄 Uploading and processing your paper..."):
            files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
            response = requests.post(f"{API_URL}/api/upload/", files=files)
            
            if response.status_code == 200:
                paper_data = response.json()
                st.session_state.uploaded_paper = paper_data
                
                st.markdown(f"""
                <div class="success-message">
                    <h3>✅ Paper Uploaded Successfully!</h3>
                    <p><strong>Title:</strong> {paper_data['title']}</p>
                    <p><strong>Paper ID:</strong> {paper_data['paper_id']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Show paper details
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("""
                    <div class="metric-card">
                        <h4>📊 Paper Details</h4>
                        <p><strong>Title:</strong> {}</p>
                        <p><strong>ID:</strong> {}</p>
                    </div>
                    """.format(paper_data['title'], paper_data['paper_id']), unsafe_allow_html=True)
                
                with col2:
                    st.markdown("""
                    <div class="metric-card">
                        <h4>🎯 Next Steps</h4>
                        <p>• Analyze the paper</p>
                        <p>• Get AI summary</p>
                        <p>• Find similar papers</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.success("🎉 Ready for analysis!")
                
            else:
                st.error("❌ Failed to upload file. Please try again.")

# Analysis Section
if st.session_state.uploaded_paper:
    st.markdown("---")
    st.markdown("## 🔍 Paper Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🧠 Generate AI Summary", key="analyze_btn"):
            with st.spinner("🤖 AI is analyzing your paper..."):
                analysis_response = requests.get(f"{API_URL}/api/analyze/{st.session_state.uploaded_paper['paper_id']}")
                
                if analysis_response.status_code == 200:
                    summary_data = analysis_response.json()
                    st.session_state.analysis_done = True
                    st.session_state.summary = summary_data['summary']
                    
                    st.markdown("""
                    <div class="analysis-card">
                        <h3>📝 AI-Generated Summary</h3>
                        <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                            {}
                        </div>
                    </div>
                    """.format(summary_data['summary']), unsafe_allow_html=True)
                    
                    # Summary metrics
                    word_count = len(summary_data['summary'].split())
                    st.metric("📊 Summary Length", f"{word_count} words")
                    
                else:
                    st.error("❌ Error analyzing paper. Please try again.")
    
    with col2:
        if st.button("📊 View Analysis Stats", key="stats_btn"):
            if st.session_state.analysis_done:
                st.markdown("""
                <div class="metric-card">
                    <h4>📈 Analysis Statistics</h4>
                    <p>✅ Summary Generated</p>
                    <p>✅ Paper Processed</p>
                    <p>✅ Ready for Recommendations</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("⚠️ Please generate summary first")

# Recommendations Section
if st.session_state.uploaded_paper:
    st.markdown("---")
    st.markdown("## 🎯 Find Similar Papers")
    
    # Recommendation options
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔍 Search Options")
        search_type = st.radio(
            "Choose search source:",
            ["🏠 Local Database", "🌐 Internet Research"],
            key="search_type"
        )
    
    with col2:
        st.markdown("### 📊 Search Settings")
        top_k = st.slider("Number of recommendations", 3, 10, 5, key="top_k")
    
    if st.button("🔍 Find Similar Papers", key="recommend_btn"):
        with st.spinner("🔍 Searching for similar papers..."):
            source = "local" if search_type == "🏠 Local Database" else "internet"
            response = requests.get(
                f"{API_URL}/api/recommend/{st.session_state.uploaded_paper['paper_id']}", 
                params={"source": source}
            )
            
            if response.status_code == 200:
                data = response.json()
                recommendations = data["recommendations"]
                
                st.markdown(f"""
                <div class="success-message">
                    <h3>🎯 Found {len(recommendations)} Similar Papers</h3>
                    <p>Source: {search_type}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Display recommendations
                for i, rec in enumerate(recommendations, 1):
                    if source == "internet":
                        st.markdown(f"""
                        <div class="recommendation-card">
                            <h4>#{i} {rec['title']}</h4>
                            <p><a href="{rec['link']}" target="_blank" style="color: white;">🔗 View Paper</a></p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="recommendation-card">
                            <h4>#{i} {rec['title']}</h4>
                            <p>📄 Available in local database</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Recommendation metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("📊 Total Found", len(recommendations))
                with col2:
                    st.metric("🎯 Source", search_type.split()[1])
                with col3:
                    st.metric("⏱️ Search Time", "~2s")
                    
            else:
                st.error("❌ No recommendations found. Please try again.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🧠 Powered by AI Research Analyzer | Built with Streamlit & FastAPI</p>
    <p>Transform your research workflow with intelligent analysis</p>
</div>
""", unsafe_allow_html=True)
