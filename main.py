import streamlit as st
import time
import datetime
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

# 2. HELPER FUNCTIONS (Backend Logic - UNCHANGED)

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

# 3. ULTRA MODERN CSS (Restored Glitch Effect & New Home Design)
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background: radial-gradient(circle at center, #0f172a 0%, #020617 100%);
        color: #f1f5f9;
        font-family: 'Inter', sans-serif;
    }
    
    /* --- RESTORED GLITCH INTRO ANIMATION --- */
    .hero-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 85vh;
        flex-direction: column;
    }
    
    .neon-text {
        font-size: 80px;
        font-weight: 900;
        color: #fff;
        text-transform: uppercase;
        animation: flicker 1.5s infinite alternate;     
    }
    
    .sub-text {
        font-size: 28px;
        color: #94a3b8;
        font-family: 'Courier New', monospace;
        letter-spacing: 5px;
        text-transform: uppercase;
        border-top: 2px solid #38bdf8;
        padding-top: 15px;
        margin-top: 10px;
    }

    @keyframes flicker {
        0%, 18%, 22%, 25%, 53%, 57%, 100% {
            text-shadow:
            0 0 4px #fff,
            0 0 11px #fff,
            0 0 19px #fff,
            0 0 40px #0fa,
            0 0 80px #0fa,
            0 0 90px #0fa,
            0 0 100px #0fa,
            0 0 150px #0fa;
        }
        20%, 24%, 55% {       
            text-shadow: none;
        }
    }

    /* --- HOME PAGE DASHBOARD CARDS --- */
    div.css-1r6slb0.e1tzin5v2 {
        background-color: #1e293b;
        border: 1px solid #334155;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s;
    }
    div.css-1r6slb0.e1tzin5v2:hover {
        transform: scale(1.02);
        border-color: #38bdf8;
    }

    /* Button Styling */
    .stButton > button {
        background: linear-gradient(90deg, #3b82f6, #06b6d4);
        color: white;
        border: none;
        padding: 10px 24px;
        font-weight: 600;
        border-radius: 8px;
        width: 100%;
    }
    .stButton > button:hover {
        box-shadow: 0 0 15px #3b82f6;
    }
</style>
""", unsafe_allow_html=True)

# 4. INTRO ANIMATION (Restored Logic)
def show_intro():
    placeholder = st.empty()
    with placeholder.container():
        st.markdown("""
        <div class="hero-container">
            <h1 class="neon-text">MD NAHID MAHMUD</h1>
            <h3 class="sub-text">SOUTHEAST UNIVERSITY</h3>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(3.0)
    placeholder.empty()

if 'intro_done' not in st.session_state:
    show_intro()
    st.session_state['intro_done'] = True

# 5. NAVIGATION MENU
selected = option_menu(
    menu_title=None,
    options=["Home", "Academic Hub", "Global Wings", "Career Architect"],
    icons=["grid-fill", "book-half", "airplane-engines-fill", "trophy-fill"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "5px", "background-color": "#1e293b", "border-radius": "10px"},
        "nav-link": {"font-size": "14px", "color": "#cbd5e1", "margin": "0px 5px"},
        "nav-link-selected": {"background-color": "#3b82f6", "color": "white", "font-weight": "bold"},
    }
)

# 6. MAIN APP LOGIC

# --- HOME DASHBOARD (RE-DESIGNED FOR 2026) ---
if selected == "Home":
    # Header Section with Date
    today = datetime.date.today().strftime("%B %d, %Y")
    st.markdown(f"<p style='color: #94a3b8; font-size: 14px;'>📅 {today} | 📍 Dhaka, Bangladesh</p>", unsafe_allow_html=True)
    st.markdown("<h1 style='background: linear-gradient(to right, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>Student Command Center 🚀</h1>", unsafe_allow_html=True)
    
    # Quick Stats Row (Dashboard Feel)
    st.markdown("### 📊 Your Activity")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Focus Time", "4h 12m", "+15%")
    with c2:
        st.metric("Universities Tracked", "12", "Global Wings")
    with c3:
        st.metric("Quizzes Aced", "8", "Academic Hub")
    with c4:
        st.metric("Career Goals", "Software Eng.", "On Track")
    
    st.markdown("---")
    
    # Feature Cards (The "Best Options")
    st.markdown("### ⚡ Quick Access Modules")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container():
            st.image("https://cdn-icons-png.flaticon.com/512/2997/2997295.png", width=60)
            st.subheader("Academic Hub")
            st.write("AI-Powered Tutor. Upload notes, summarize lectures, and generate exam questions instantly.")
            if st.button("Open Study Mode"):
                st.toast("Go to 'Academic Hub' from the menu!")

    with col2:
        with st.container():
            st.image("https://cdn-icons-png.flaticon.com/512/201/201623.png", width=60)
            st.subheader("Global Wings")
            st.write("Worldwide University Database. Check tuition, scholarships, and ranking with AI precision.")
            if st.button("Explore World"):
                st.toast("Go to 'Global Wings' from the menu!")

    with col3:
        with st.container():
            st.image("https://cdn-icons-png.flaticon.com/512/1584/1584892.png", width=60)
            st.subheader("Career Architect")
            st.write("Future Roadmap Generator. Get a step-by-step monthly plan to land your dream job.")
            if st.button("Build Career"):
                st.toast("Go to 'Career Architect' from the menu!")

    # Footer Section (Futuristic Touch)
    st.markdown("---")
    st.markdown("<center><p style='color: #475569; font-size: 12px;'>Powered by Google Gemini Pro | Created for the Future of Education (2026-2030)</p></center>", unsafe_allow_html=True)


# --- ACADEMIC HUB (UNCHANGED LOGIC) ---
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
                    prompt = f"Create 5 {difficulty}-level multiple choice questions based on the text. Provide answers at the end."
                    st.markdown(get_gemini_response(prompt, text))

# --- GLOBAL WINGS (UNCHANGED LOGIC) ---
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

# --- CAREER ARCHITECT (UNCHANGED LOGIC) ---
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
                prompt = f"Create a detailed {timeline} learning roadmap for a {current_level} wanting to become a {role}. Structure it Month-by-Month."
                st.markdown(get_gemini_response(prompt))
        else:
            st.warning("Please specify a Target Job Role.")
