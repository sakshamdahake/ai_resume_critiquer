import google.generativeai as genai
import streamlit as st
import PyPDF2
import io
import os
from dotenv import load_dotenv


load_dotenv()


st.set_page_config(page_title="AI Resume Critiquer", page_icon="📜", layout="centered")


st.title("AI Resume Critiquer")
st.markdown("Upload your resume and get AI-powered feedback tailored to your needs!")


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)


uploaded_file = st.file_uploader("Upload your Resume (PDF or TXT)", type=["pdf", "txt"])
job_role = st.text_input("Enter the job role you are targeting (optional)")


analyse = st.button("Analyse Resume")


def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    
    return text  # Fixed: moved return outside the loop


def extract_text_from_file(uploaded_file):
    # Fixed: check the file type using the name attribute
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    
    return uploaded_file.read().decode("utf-8", errors="ignore")  # Added error handling for encoding


if analyse and uploaded_file:
    try:
        file_content = extract_text_from_file(uploaded_file)
        if not file_content.strip():
            st.error("File does not have any content...")
            st.stop()

        prompt = f"""Please analyse this resume and provide constructive feedback.
                    Focus on the following aspects:
                    1. Content clarity and impact.
                    2. Skill Presentation.
                    3. Experience description.
                    4. Specific improvements for {job_role if job_role else 'general job applications'}
                    
                    Resume Content:
                    {file_content}

                    Please provide your analysis in clear, structured format with specific recommendations."""
        
        with st.spinner("Analyzing your resume..."):
            model = genai.GenerativeModel(
                model_name="gemini-2.5-flash",
                system_instruction="You are an expert Resume Analyst and reviewer with years of experience in HR and recruitment."
            )
            
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7
                )
            )
        
        st.markdown("### Analysis Results")
        st.markdown(response.text)
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
