# AI Resume Critiquer

An intelligent resume analysis tool powered by Google Gemini AI that provides personalized, constructive feedback on your resume to help you stand out to recruiters and hiring managers.

## 🎯 Features

- **AI-Powered Analysis**: Uses Google Gemini 1.5 Flash to analyze resumes with expert-level insights
- **Multi-Format Support**: Accepts both PDF and TXT resume formats
- **Job Role Targeting**: Customize feedback based on specific job roles you're targeting
- **Comprehensive Feedback**: Analyzes four key aspects:
  - Content clarity and impact
  - Skill presentation
  - Experience description
  - Role-specific improvements
- **User-Friendly Interface**: Built with Streamlit for an intuitive, interactive experience
- **Real-Time Feedback**: Get instant analysis results with loading indicators

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Google API Key (from [Google AI Studio](https://makersuite.google.com/app/apikey))
- `uv` package manager (or pip/conda as alternative)

### Installation

1. **Clone the repository** (or create a new project directory)
```bash
mkdir ai-resume-critiquer
cd ai-resume-critiquer
```

2. **Create a virtual environment using `uv`**
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
uv add streamlit google-generativeai PyPDF2 python-dotenv
```

Or using pip:
```bash
pip install streamlit google-generativeai PyPDF2 python-dotenv
```

4. **Create a `.env` file in the project root**
```bash
echo "GOOGLE_API_KEY=your_api_key_here" > .env
```

Replace `your_api_key_here` with your actual Google API key from [Google AI Studio](https://makersuite.google.com/app/apikey).

### Usage

1. **Run the Streamlit app**
```bash
streamlit run main.py
```

2. **Upload your resume**
   - Click "Upload your Resume (PDF or TXT)" button
   - Select your resume file

3. **Enter target job role (optional)**
   - Type the job role you're targeting for more tailored feedback
   - Leave blank for general job application feedback

4. **Click "Analyse Resume"**
   - Wait for the AI to analyze your resume
   - View detailed feedback and recommendations

## 📁 Project Structure

```
ai-resume-critiquer/
├── main.py                 # Main Streamlit application
├── .env                    # Environment variables (create this)
├── .gitignore             # Git ignore file
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## 💻 Code Overview

### Key Functions

**`extract_text_from_pdf(pdf_file)`**
- Extracts text content from PDF files
- Handles multi-page PDFs
- Returns combined text from all pages

**`extract_text_from_file(uploaded_file)`**
- Detects file type (PDF or TXT)
- Routes to appropriate extraction function
- Returns extracted text content

### Main Workflow

1. User uploads resume file
2. Application detects file type and extracts text
3. User enters target job role (optional)
4. AI analyzes resume with context of job role
5. Detailed feedback displayed to user

## 🛠️ Technologies Used

- **Streamlit**: Web app framework for interactive UI
- **Google Generative AI**: Gemini 1.5 Flash LLM for resume analysis
- **PyPDF2**: PDF text extraction
- **python-dotenv**: Environment variable management
- **Python 3.12+**: Core language

## 📋 Requirements

```
streamlit>=1.28.0
google-generativeai>=0.3.0
PyPDF2>=3.0.0
python-dotenv>=1.0.0
```

## 🔐 Environment Variables

Create a `.env` file with the following:

```env
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

**Note**: Never commit your `.env` file to version control. Add it to `.gitignore`.

## 🎨 UI/UX Features

- Clean, centered layout optimized for resume analysis
- Emoji indicators for better visual feedback
- Loading animations while AI processes
- Structured output with clear section headers
- Error handling with user-friendly messages
- Status updates during analysis

## 📝 Resume Analysis Criteria

The AI evaluates your resume on:

1. **Content Clarity & Impact**
   - How clearly your accomplishments are communicated
   - Strength and relevance of bullet points
   - Overall impact on potential employers

2. **Skill Presentation**
   - Organization of technical and soft skills
   - Relevance to target position
   - Use of industry keywords

3. **Experience Description**
   - Quality of job descriptions
   - Quantifiable achievements
   - Action verbs and professional language

4. **Role-Specific Improvements**
   - Tailored recommendations for your target job
   - Missing keywords or skills to highlight
   - Structural improvements for ATS compatibility

## 🐛 Troubleshooting

### ImportError: cannot import name 'genai'
Make sure you're using the correct import:
```python
import google.generativeai as genai  # Correct
# NOT: from google import genai
```

### UTF-8 Decoding Error
This typically happens with corrupted PDFs. The app now handles this gracefully with error handling.

### No response from API
- Verify your `GOOGLE_API_KEY` is correct
- Check your internet connection
- Ensure your API quota hasn't been exceeded

### File upload not working
- Ensure file is in PDF or TXT format
- Check file size (very large files may timeout)
- Try converting PDF with another tool if corrupted

## 🚀 Future Enhancements

- [ ] Support for DOCX format
- [ ] Batch resume analysis
- [ ] Custom evaluation criteria
- [ ] Resume score/rating system
- [ ] Download analysis as PDF
- [ ] Template suggestions
- [ ] ATS compatibility checker
- [ ] Multi-language support

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues, questions, or suggestions, please open an issue on the project repository.

## 🙏 Acknowledgments

- Google Gemini API for powerful AI capabilities
- Streamlit for making web app development easy
- PyPDF2 for reliable PDF processing

---

**Made with ❤️ for job seekers everywhere**
