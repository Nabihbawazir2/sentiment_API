import streamlit as st
import openai

# Set your OpenAI API key
openai.api_key = st.secrets.get("openai_api_key", "sk-...")

st.title("🧠 Resume Analyzer with GPT")

# Upload CV and JD
cv_file = st.file_uploader("📄 Upload your Resume (PDF or TXT)", type=["txt", "pdf"])
jd_input = st.text_area("📝 Paste the Job Description Here")

# Helper to read uploaded file
def read_file(file):
    if file.name.endswith(".pdf"):
        import PyPDF2
        reader = PyPDF2.PdfReader(file)
        return "\n".join([page.extract_text() for page in reader.pages])
    else:
        return file.read().decode("utf-8")

# Analyze button
if st.button("🔍 Analyze Fit"):
    if cv_file and jd_input:
        cv_text = read_file(cv_file)
        
        # Prompt engineering
        prompt = f"""
You are an expert resume reviewer.

Compare the following resume and job description:
Resume:
{cv_text[:3000]}

Job Description:
{jd_input[:2000]}

Evaluate:
1. How well does the resume match the job?
2. What are the strengths?
3. What could be improved?

Give a final fit score (0-100).
Limit response to 400 tokens.
"""

        with st.spinner("Analyzing..."):
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.5
            )
            result = response['choices'][0]['message']['content']
            st.success("✅ Analysis Complete")
            st.markdown(result)
    else:
        st.warning("Please upload a resume and provide a job description.")
