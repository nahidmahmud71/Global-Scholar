import streamlit as st
import time
from streamlit_option_menu import option_menu
import google.generativeai as genai
import PyPDF2 as pdf
import pandas as pd

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="Global Scholar AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. HELPER FUNCTIONS (Backend Logic)

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

def get_gemini_response(input_prompt, content=""):
    try:
        if "GOOGLE_API_KEY" in st.secrets:
            api_key = st.secrets["GOOGLE_API_KEY"]
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            if content:
                response = model.generate_content([input_prompt, content])
            else:
                response = model.generate_content(input_prompt)
            return response.text
        else:
            return "⚠️ Error: API Key not found in Secrets."
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# 3. ULTRA MODERN CSS (Premium Look)
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background: radial-gradient(circle at center, #0f172a 0%, #020617 100%);
        color: #f1f5f9;
        font-family: 'Inter', sans-serif;
    }
    
    /* Intro Animation */
    .hero-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 85vh;
        flex-direction: column;
        animation: fadeIn 2s ease-in-out;
    }
    .neon-text {
        font-size: 65px;
        font-weight: 800;
        background: linear-gradient(to right, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-align: center;
        margin-bottom: 10px;
    }
    .sub-text {
        font-size: 24px;
        color: #94a3b8;
        font-family: 'Courier New', monospace;
        letter-spacing: 3px;
        text-transform: uppercase;
        border-top: 1px solid #334155;
        padding-top: 10px;
    }

    /* Custom Input Fields */
    .stTextInput > div > div > input {
        background-color: #1e293b;
        color: white;
        border: 1px solid #334155;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(90deg, #3b82f6, #2563eb);
        color: white;
        border: none;
        padding: 10px 24px;
        font-weight: 600;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.5);
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# 4. INTRO ANIMATION
def show_intro():
    placeholder = st.empty()
    with placeholder.container():
        st.markdown("""
        <div class="hero-container">
            <h1 class="neon-text">MD NAHID MAHMUD</h1>
            <h3 class="sub-text">SOUTHEAST UNIVERSITY</h3>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(3.5)
    placeholder.empty()

if 'intro_done' not in st.session_state:
    show_intro()
    st.session_state['intro_done'] = True

# 5. NAVIGATION MENU
selected = option_menu(
    menu_title=None,
    options=["Home", "Academic Hub", "Global Wings", "Career Architect"],
    icons=["house-door-fill", "book-half", "airplane-engines-fill", "trophy-fill"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "5px", "background-color": "#1e293b", "border-radius": "10px"},
        "nav-link": {"font-size": "14px", "color": "#cbd5e1", "margin": "0px 5px"},
        "nav-link-selected": {"background-color": "#3b82f6", "color": "white", "font-weight": "bold"},
    }
)

# 6. MAIN APP LOGIC

# --- HOME ---
if selected == "Home":
    st.markdown("<h1 style='text-align: center; color: #38bdf8;'>Global Scholar AI 2.0 🎓</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 18px;'>Your All-in-One AI Companion for Education & Career</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/3079/3079350.png", width=80)
        st.subheader("Academic Hub")
        st.write("Upload PDFs, get detailed summaries, and generate exam-style quizzes with adjustable difficulty.")
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/826/826070.png", width=80)
        st.subheader("Global Wings")
        st.write("Find universities with tuition data, rankings, and acceptance rates using advanced AI search.")
    with col3:
        st.image("https://cdn-icons-png.flaticon.com/512/1063/1063376.png", width=80)
        st.subheader("Career Architect")
        st.write("Get a month-by-month roadmap, project ideas, and skill checklists for your dream job.")

# --- ACADEMIC HUB (UPDATED) ---
elif selected == "Academic Hub":
    st.title("📚 Academic Hub")
    st.caption("AI-Powered Study Assistant")
    
    if "GOOGLE_API_KEY" not in st.secrets:
        st.error("⚠️ Please configure your API Key in Streamlit Secrets.")
    else:
        tab1, tab2 = st.tabs(["📝 Smart Summarizer", "🧠 Exam Mode (Quiz)"])
        
        # Summarizer
        with tab1:
            col1, col2 = st.columns([2, 1])
            with col1:
                uploaded_file = st.file_uploader("Upload Study Material (PDF)", type="pdf")
            with col2:
                summary_type = st.selectbox("Summary Type", ["Brief Overview", "Detailed Explanation", "Bullet Points"])
            
            if uploaded_file and st.button("Generate Summary"):
                with st.spinner("Analyzing document structure..."):
                    text = input_pdf_text(uploaded_file)
                    prompt = f"You are a professor. Provide a {summary_type} of the following text. Focus on key concepts and definitions."
                    st.markdown(get_gemini_response(prompt, text))

        # Quiz Generator
        with tab2:
            col1, col2 = st.columns([2, 1])
            with col1:
                if uploaded_file:
                    st.success("✅ File Loaded from previous tab")
                else:
                    uploaded_file_quiz = st.file_uploader("Upload PDF for Quiz", type="pdf", key="quiz_uploader")
                    uploaded_file = uploaded_file_quiz
            with col2:
                difficulty = st.selectbox("Quiz Difficulty", ["Easy", "Medium", "Hard"])
            
            if uploaded_file and st.button("Start Quiz"):
                with st.spinner(f"Creating {difficulty} level questions..."):
                    text = input_pdf_text(uploaded_file)
                    prompt = f"""
                    Create 5 {difficulty}-level multiple choice questions based on the text.
                    Format:
                    Question 1: ...
                    A) ...
                    B) ...
                    C) ...
                    D) ...
                    
                    (Provide correct answers at the very bottom hidden in a 'Answer Key' section)
                    """
                    st.markdown(get_gemini_response(prompt, text))

# --- GLOBAL WINGS (UPDATED - HUGE DATA) ---
elif selected == "Global Wings":
    st.title("✈️ Global Wings Premium")
    st.caption("Advanced University Finder & Data Engine")
    
    with st.expander("🔍 Advanced Search Filters", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            country = st.text_input("Country", placeholder="USA, Canada...")
        with col2:
            subject = st.text_input("Major", placeholder="CS, Business...")
        with col3:
            degree = st.selectbox("Degree", ["Bachelor's", "Master's", "PhD"])
        with col4:
            budget = st.select_slider("Max Tuition Budget", ["$10k", "$20k", "$30k", "$50k", "Unlimited"])
            
        if st.button("Find Universities 🚀", use_container_width=True):
            if country and subject:
                with st.spinner("Scanning global database for best matches..."):
                    prompt = f"""
                    Act as a top-tier education consultant. Find top 5 universities in {country} for {degree} in {subject} with a budget around {budget}.
                    
                    Present the data in a Markdown Table with these exact columns:
                    | Rank | University Name | Approx. Tuition (Yearly) | Acceptance Rate | Best Scholarship |
                    |---|---|---|---|---|
                    
                    After the table, write a brief 'Pro Tip' for applying to these specific universities.
                    """
                    st.markdown(get_gemini_response(prompt))
            else:
                st.warning("Please enter Country and Subject.")

    # Budget Calculator
    st.divider()
    st.subheader("💰 Cost Estimator")
    c1, c2, c3 = st.columns(3)
    with c1:
        t_fee = st.number_input("Annual Tuition ($)", value=12000)
    with c2:
        l_cost = st.number_input("Monthly Living ($)", value=800)
    with c3:
        total_yr = t_fee + (l_cost * 12) + 1500 # Flight
        st.metric("Total 1st Year Expense", f"${total_yr:,.2f}", delta="Includes Flight & Visa")

# --- CAREER ARCHITECT (UPDATED) ---
elif selected == "Career Architect":
    st.title("🚀 Career Architect AI")
    st.caption("Strategic Career Planning System")
    
    col1, col2 = st.columns(2)
    with col1:
        role = st.text_input("Target Job Role", placeholder="e.g. Full Stack Developer")
    with col2:
        timeline = st.selectbox("Timeline to Goal", ["3 Months (Fast Track)", "6 Months (Standard)", "1 Year (Deep Dive)"])
    
    current_level = st.select_slider("Current Skill Level", options=["Beginner", "Intermediate", "Advanced"])
    
    if st.button("Generate Roadmap 🗺️"):
        if role:
            with st.spinner("Architecting your personalized roadmap..."):
                prompt = f"""
                Create a detailed {timeline} learning roadmap for a {current_level} wanting to become a {role}.
                
                Structure it Month-by-Month.
                For each month include:
                - 🎯 **Goal**
                - 🛠️ **Topics to Learn** (be specific)
                - 💻 **Project Idea** (Real-world application)
                """
                st.markdown(get_gemini_response(prompt))
        else:
            st.warning("Please specify a Target Job Role.")
