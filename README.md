# 🌍 AI Career Agent

A Python and Streamlit application that helps job seekers explore job opportunities and compare job descriptions with their CV skills.

## 🚀 Features

- Search for job opportunities by role and country.
- Explore remote and on-site opportunities.
- Upload a CV in PDF or DOCX format.
- Extract skills from your CV and compare them with job descriptions.
- View matched skills and skills to improve.
- Identify job listings that mention visa sponsorship.
- Filter opportunities by experience and work arrangement.

## 🛠️ Tech Stack

- Python
- Streamlit
- Pandas / data processing tools, as used in the project
- REST APIs
- PyPDF
- Python-docx

## ▶️ Run Locally

1. Clone this repository:

   `git clone https://github.com/datasneha/ai-career-agent.git`

2. Open the project folder:

   `cd ai-career-agent`

3. Install dependencies:

   `pip install -r requirements.txt`

4. Create a `.env` file in the project folder and add your OpenAI API key if your current app configuration requires it:

   `OPENAI_API_KEY=your_api_key_here`

5. Run the application:

   `streamlit run app.py`

## ⚠️ Current Limitations

- Job results depend on the external job sources used by the application.
- Skill matching is based on keywords and is not a complete measure of candidate suitability.
- Visa sponsorship indicators are based on job-description text and are not independently verified.
- Remote jobs may have country-specific eligibility restrictions.

## 🔮 Future Improvements

- Improve job-title and skill matching.
- Expand job sources and country coverage.
- Improve sponsorship and work-location verification.
- Add more detailed job-match explanations.
- Deploy a live version of the application.

## 👩‍💻 About This Project

This is a portfolio project developed to practise Python, data processing, API integration, and building practical tools for job seekers.

**Project status:** Working prototype; further testing and improvements are planned.
