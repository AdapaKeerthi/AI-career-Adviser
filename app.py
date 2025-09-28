import streamlit as st
from openai import OpenAI

# OpenAI client using Streamlit Cloud secret
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("💼 AI Career Path Adviser")
st.write("This is your AI Career Adviser app. Replace this placeholder with your full app code.")
