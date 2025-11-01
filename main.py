import google.generativeai as genai
import streamlit as st
import PyPDF2
import io
import os
from dotenv import load_dotenv


load_dotenv()


# Configure page and theme
st.set_page_config(
    page_title="AI Resume Critiquer",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Custom CSS for styling
def load_custom_css():
    st.markdown("""
        <style>
        /* Main container styling */
        .main {
            padding: 2rem;
        }
        
        /* Header styling */
        .header-container {
            text-align: center;
            padding: 2rem 0;
            margin-bottom: 2rem;
            border-bottom: 3px solid #FF6B6B;
        }
        
        .header-container h1 {
            font-size: 3rem;
            margin-bottom: 0.5rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .header-container p {
            font-size: 1.1rem;
            color: #888;
        }
        
        /* Input section styling */
        .input-section {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .input-section h3 {
            color: #333;
            margin-top: 0;
        }
        
        /* Analysis result styling */
        .analysis-results {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            padding: 2rem;
            border-radius: 15px;
            margin-top: 2rem;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        }
        
        .analysis-results h2 {
            color: white;
            margin-top: 0;
            font-size: 2rem;
        }
        
        .result-content {
            background: white;
            padding: 2rem;
            border-radius: 10px;
            color: #333;
            line-height: 1.8;
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border: none !important;
            padding: 12px 30px !important;
            border-radius: 8px !important;
            font-size: 1rem !important;
            font-weight: bold !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6) !important;
        }
        
        .stButton > button:disabled {
            background: #ccc !important;
            box-shadow: none !important;
            cursor: not-allowed !important;
        }
        
        /* Info box styling */
        .info-box {
            background: #e3f2fd;
            border-left: 4px solid #2196F3;
            padding: 1.5rem;
            border-radius: 8px;
            margin: 1rem 0;
        }
        
        /* Success message */
        .success-box {
            background: #e8f5e9;
            border-left: 4px solid #4CAF50;
            padding: 1.5rem;
            border-radius: 8px;
            margin: 1rem 0;
        }
        
        /* Sidebar styling */
        .sidebar-content {
            padding: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)


load_custom_css()


# Sidebar for info
with st.sidebar:
    st.markdown("### About")
    st.info(
        """
        **AI Resume Critiquer** helps you optimize your resume with AI-powered insights.
        
        Features:
        - PDF & TXT support
        - Job role customization
        - Comprehensive analysis
        - Real-time feedback
        """
    )
    
    st.markdown("---")
    
    st.markdown("### 🔧 How to use")
    st.markdown(
        """
        1. Upload your resume (PDF or TXT)
        2. Enter target job role (optional)
        3. Click "Analyse Resume"
        4. Get instant AI feedback
        """
    )


# Main header
st.markdown("""
    <div class="header-container">
        <h1>📜 AI Resume Critiquer</h1>
        <p>Get AI-powered feedback to make your resume stand out</p>
    </div>
""", unsafe_allow_html=True)


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)


# Initialize session state variables
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False
    st.session_state.analysis_result = None
    st.session_state.current_file = None
    st.session_state.current_job_role = None


# Input section
st.markdown('<div class="input-section">', unsafe_allow_html=True)
st.markdown("### 📁 Upload & Configure")

col1, col2 = st.columns([1, 1])

with col1:
    uploaded_file = st.file_uploader(
        "Upload your Resume",
        type=["pdf", "txt"],
        help="Supported formats: PDF, TXT"
    )

with col2:
    job_role = st.text_input(
        "Target Job Role",
        placeholder="e.g., Senior Software Engineer",
        help="Leave blank for general feedback"
    )

st.markdown('</div>', unsafe_allow_html=True)


# Button row
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    analyse = st.button(
        "Analyse Resume",
        use_container_width=True,
        disabled=st.session_state.analysis_done and uploaded_file is not None
    )

with col2:
    if st.button("Clear Analysis", use_container_width=True):
        st.session_state.analysis_done = False
        st.session_state.analysis_result = None
        st.session_state.current_file = None
        st.session_state.current_job_role = None
        st.rerun()


def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    
    return text


def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    
    return uploaded_file.read().decode("utf-8", errors="ignore")


if analyse and uploaded_file:
    # Check if this is a new file or job role
    file_changed = (st.session_state.current_file != uploaded_file.name)
    job_role_changed = (st.session_state.current_job_role != job_role)
    
    if file_changed or job_role_changed or not st.session_state.analysis_done:
        try:
            file_content = extract_text_from_file(uploaded_file)
            if not file_content.strip():
                st.error("File does not have any content...")
                st.stop()

            prompt = f"""Please analyse this resume and provide constructive feedback.
                        Focus on the following aspects:
                        
                        1. **Content Clarity & Impact**
                           - How well accomplishments are communicated
                           - Strength and relevance of bullet points
                        
                        2. **Skill Presentation**
                           - Organization of technical and soft skills
                           - Industry keyword usage
                        
                        3. **Experience Description**
                           - Quality of job descriptions
                           - Quantifiable achievements
                           - Action verbs used
                        
                        4. **Specific Improvements for {job_role if job_role else 'General Job Applications'}**
                           - Targeted recommendations
                           - Missing keywords
                           - Structural improvements
                        
                        Resume Content:
                        {file_content}

                        Please provide your analysis in a clear, well-structured format with specific, actionable recommendations."""
            
            # Store current state
            st.session_state.current_file = uploaded_file.name
            st.session_state.current_job_role = job_role
            
            with st.status("Analyzing your resume...", expanded=True) as status:
                st.write("Extracting resume content...")
                
                st.write("Initializing AI model...")
                model = genai.GenerativeModel(
                    model_name="gemini-2.5-flash",
                    system_instruction="You are an expert Resume Analyst and reviewer with years of experience in HR and recruitment. Provide detailed, constructive, and actionable feedback."
                )
                
                st.write("Generating analysis...")
                response = model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.7
                    )
                )
                
                st.session_state.analysis_result = response.text
                st.session_state.analysis_done = True
                status.update(label="Analysis Complete!", state="complete")
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.session_state.analysis_done = False
    else:
        st.markdown("""
            <div class="success-box">
            <strong>Analysis already completed!</strong><br>
            Upload a new file or change the job role to analyze again.
            </div>
        """, unsafe_allow_html=True)


# Display the stored analysis result
if st.session_state.analysis_done and st.session_state.analysis_result:
    st.markdown("""
        <div class="analysis-results">
            <h2>Analysis Results</h2>
            <div class="result-content">
    """, unsafe_allow_html=True)
    
    st.markdown(st.session_state.analysis_result)
    
    st.markdown("""
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Download analysis as text
    st.download_button(
        label="Download Analysis",
        data=st.session_state.analysis_result,
        file_name="resume_analysis.txt",
        mime="text/plain",
        use_container_width=True
    )


# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #888; padding: 1rem;'>
        <p>Made with ❤️ for job seekers | Powered by Google Gemini</p>
    </div>
""", unsafe_allow_html=True)
