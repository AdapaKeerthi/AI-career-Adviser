import streamlit as st
from openai import OpenAI
import sqlite3
import hashlib
import datetime

# -----------------------------
# ✅ OpenAI Client (Admin key hidden)
# -----------------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# -----------------------------
# Database setup
# -----------------------------
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users
             (username TEXT PRIMARY KEY, email TEXT, password TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS reports
             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
              username TEXT, 
              report TEXT, 
              timestamp TEXT)''')
conn.commit()

# -----------------------------
# Helper functions
# -----------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, email, password):
    c.execute("INSERT OR REPLACE INTO users (username, email, password) VALUES (?, ?, ?)",
              (username, email, hash_password(password)))
    conn.commit()

def login_user(username, password):
    c.execute("SELECT * FROM users WHERE username=? AND password=?",
              (username, hash_password(password)))
    return c.fetchone()

def reset_password(username, new_password):
    c.execute("UPDATE users SET password=? WHERE username=?",
              (hash_password(new_password), username))
    conn.commit()

def save_report(username, report):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO reports (username, report, timestamp) VALUES (?, ?, ?)",
              (username, report, timestamp))
    conn.commit()

def get_user_reports(username):
    c.execute("SELECT id, report, timestamp FROM reports WHERE username=? ORDER BY id DESC", (username,))
    return c.fetchall()

def delete_report(report_id):
    c.execute("DELETE FROM reports WHERE id=?", (report_id,))
    conn.commit()

# -----------------------------
# App Config
# -----------------------------
st.set_page_config(page_title="AI Career Path Adviser", layout="wide")
st.title("💼 AI Career Path Adviser")

# -----------------------------
# Session state init
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# -----------------------------
# Authentication
# -----------------------------
if not st.session_state.logged_in:
    menu = ["Login", "Register", "Forgot Password"]
    choice = st.sidebar.selectbox("🔐 Authentication", menu)

    if choice == "Register":
        st.subheader("🧾 Create a New Account")
        new_user = st.text_input("Username")
        email = st.text_input("Email")
        new_pass = st.text_input("Password", type="password")
        if st.button("Register"):
            if new_user and new_pass:
                register_user(new_user, email, new_pass)
                st.success("✅ Registered successfully! You can now log in.")
            else:
                st.warning("Please fill all fields.")

    elif choice == "Login":
        st.subheader("🔐 Login to Your Account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user = login_user(username, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"🎉 Welcome back, {username}!")
            else:
                st.error("❌ Invalid username or password.")

    elif choice == "Forgot Password":
        st.subheader("🔑 Reset Your Password")
        username = st.text_input("Enter your username")
        new_pass = st.text_input("Enter new password", type="password")
        if st.button("Reset Password"):
            reset_password(username, new_pass)
            st.success("✅ Password updated successfully! Please log in.")

# -----------------------------
# Main Career Adviser
# -----------------------------
if st.session_state.logged_in:

    # Logout
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    # Past Reports
    with st.sidebar.expander("📂 My Past Reports"):
        reports = get_user_reports(st.session_state.username)
        if reports:
            for r in reports:
                st.markdown(f"**🗓 {r[2]}**")
                st.download_button(
                    label="⬇️ Download",
                    data=r[1],
                    file_name=f"career_report_{r[0]}.txt",
                    mime="text/plain",
                    key=f"download_{r[0]}"
                )
                st.text_area("Preview", r[1], height=150, key=f"preview_{r[0]}")
                if st.button("🗑️ Delete", key=f"delete_{r[0]}"):
                    delete_report(r[0])
                    st.warning(f"🗑️ Report {r[0]} deleted.")
                    st.rerun()
                st.markdown("---")
        else:
            st.info("No saved reports yet.")

    # User profile
    st.header("📝 Your Profile")
    name = st.text_input("Your Name", value=st.session_state.username)
    education = st.text_area("Educational Background")
    skills = st.text_area("List your current skills (comma separated)")
    interests = st.text_area("What fields/industries interest you?")
    goals = st.text_area("What are your career goals? (salary, remote work, growth, etc.)")

    if st.button("🚀 Get My Career Advice"):
        if not skills:
            st.warning("Please enter at least some skills.")
        else:
            with st.spinner("🤖 AI is analyzing your profile..."):
                prompt = f"""
                You are an expert career adviser AI.
                Based on this profile:
                - Name: {name}
                - Education: {education}
                - Skills: {skills}
                - Interests: {interests}
                - Goals: {goals}

                Provide:
                1. Top 3 suitable career paths with reasoning.
                2. Skills the user is missing for each path.
                3. Recommended resources to learn those skills.
                4. A step-by-step career roadmap.
                """

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful career adviser."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )

                advice = response.choices[0].message.content

                st.subheader("📊 Your AI-Powered Career Advice")
                st.write(advice)

                save_report(st.session_state.username, advice)

                st.download_button(
                    label="📥 Download Career Report",
                    data=advice,
                    file_name=f"{name}_career_advice.txt",
                    mime="text/plain"
                )
