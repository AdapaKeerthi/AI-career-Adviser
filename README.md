# AI Career Path Adviser (Streamlit + OpenAI + SQLite)

An interactive AI-powered web app built with **Streamlit**, **OpenAI GPT-4o-mini**, and **SQLite**, designed to provide **personalized career guidance** based on a user’s profile (education, skills, interests, and goals).

The app features:
-  **User Authentication** (Login / Register / Forgot Password)
-  **AI-Powered Career Advice** using OpenAI GPT
-  **Personalized Report Saving** in SQLite database
-  **View, Download, and Delete Past Reports**
-  **Hidden API Key** stored securely in `.streamlit/secrets.toml`

##  Features

 **Login / Register / Forgot Password**  
 **Secure password hashing** using SHA-256  
 **AI-generated career suggestions** with roadmap and resources  
 **SQLite database** for user accounts and reports  
 **Downloadable AI reports** as `.txt`  
 **Admin key is hidden**, so users don’t need to know the API key  

## Tech Stack

- [Streamlit](https://streamlit.io/) – Web UI  
- [OpenAI GPT-4o-mini](https://platform.openai.com/) – AI model  
- [SQLite3](https://www.sqlite.org/) – Local database  
- [Python 3.10+](https://www.python.org/)  

## Setup Instructions

1️
Clone Repository  
```bash
git clone https://github.com/yourusername/ai-career-adviser.git
cd ai-career-adviser
```

2️
Create Virtual Environment (optional)  
```bash
python -m venv venv
venv\Scripts\activate     # Windows
source venv/bin/activate  # Mac/Linux
```

3️ 
Install Dependencies  
```bash
pip install -r requirements.txt
```

4️ 
Add OpenAI API Key  
Create a folder named `.streamlit` and add **secrets.toml**:

```toml
OPENAI_API_KEY = "your_openai_api_key_here"
```

5️
Run the App  
```bash
streamlit run app.py
```

App opens at: http://localhost:8501
