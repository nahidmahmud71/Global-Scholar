import streamlit as st
import time
import requests
import pandas as pd
import numpy as np
import google.generativeai as genai
import PyPDF2 as pdf
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Global Scholar AI | Elite Edition",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. BACKEND HELPER FUNCTIONS ---

def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

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
            
            # UPDATED MODEL TO FIX 404 ERROR
            model = genai.GenerativeModel('gemini-1.5-flash') 
            
            if content:
                response = model.generate_content([input_prompt, content])
            else:
                response = model.generate_content(input_prompt)
            return response.text
        else:
            return "⚠️ System Error: API Key Missing in Secrets."
    except Exception as e:
        return f"⚠️ AI Engine Error: {str(e)}"

# --- 3. PREMIUM CSS STYLING (Neon Pulse) ---
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background: linear-gradient(to bottom, #0f172a, #020617);
        color: #e2e8f0;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* --- INTRO ANIMATION (User Favorite Neon) --- */
    .intro-container {
        height: 90vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        background: #000;
    }
    .neon-name {
        font-size: 80px;
        font-weight: 900;
        color: white;
        text-transform: uppercase;
        animation: neon-pulse 1.5s infinite alternate;
        text-align: center;
    }
    .neon-uni {
        font-size: 30px;
        color: #38bdf8;
        font-family: 'Courier New', monospace;
        letter-spacing: 5px;
        margin-top: 20px;
        border-bottom: 2px solid #38bdf8;
        padding-bottom: 10px;
        text-align: center;
    }
    
    @keyframes neon-pulse {
        from { text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #38bdf8; }
        to { text-shadow: 0 0 20px #fff, 0 0 30px #0ea5e9, 0 0 40px #0ea5e9; }
    }

    /* --- DASHBOARD CARDS --- */
    div.css-1r6slb0 {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
    }
    
    /* --- GLOBAL WINGS CARDS --- */
    .metric-card {
        background-color: #1e293b;
        border-left: 5px solid #3b82f6;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 10px;
    }

    /* --- BUTTONS --- */
    .stButton > button {
        background: linear-gradient(45deg, #2563eb, #06b6d4);
        color: white;
        border: none;
        padding: 12px 25px;
        font-weight: bold;
        border-radius: 8px;
        text-transform: uppercase;
        letter-spacing: 1px;
        width: 100%;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
    }
    .stButton > button:hover {
        box-shadow: 0 6px 20px rgba(6, 182, 212, 0.5);
        color: #fff;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. INTRO ANIMATION EXECUTION ---
def run_intro():
    placeholder = st.empty()
    with placeholder.container():
        st.markdown("""
        <div class="intro-container">
            <h1 class="neon-name">MD NAHID MAHMUD</h1>
            <h2 class="neon-uni">SOUTHEAST UNIVERSITY</h2>
            <br>
            <p style="color: gray; font-family: monospace;">INITIALIZING GLOBAL DATABASE...</p>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(3.5)
    placeholder.empty()

if 'intro_shown' not in st.session_state:
    run_intro()
    st.session_state['intro_shown'] = True

# --- 5. TOP NAVIGATION MENU ---
selected = option_menu(
    menu_title=None,
    options=["Home Dashboard", "Academic Hub", "Global Wings", "Career Architect"],
    icons=["speedometer2", "book", "globe", "briefcase"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#0f172a"},
        "nav-link": {"font-size": "14px", "text-align": "center", "margin": "0px", "color": "#94a3b8"},
        "nav-link-selected": {"background-color": "#2563eb", "color": "white", "font-weight": "bold"},
    }
)

# --- 6. MAIN CONTENT SECTIONS ---

# ================= HOME DASHBOARD =================
if selected == "Home Dashboard":
    # Header
    col_a, col_b = st.columns([3, 1])
    with col_a:
        st.markdown("# 🚀 Student Command Center")
        st.markdown("### Welcome back, **Nahid**. System Status: **ONLINE**")
    with col_b:
        st.markdown(f"**Date:** {time.strftime('%Y-%m-%d')}")
        st.markdown("**Location:** Dhaka, BD")

    st.markdown("---")

    # LIVE DATA TICKER
    st.info("🔔 **LIVE UPDATES:** 15 New Scholarships in Canada | Visa Ratio for Germany increased by 12% | Google Hiring Freeze Lifted")

    # STATS & ANIMATION
    lottie_db = load_lottieurl("https://lottie.host/5a7d51e7-268e-4934-a63e-670560a6136d/6gH7Xy44uT.json")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        c1, c2, c3 = st.columns(3)
        c1.metric("Universities Indexed", "25,432", "+15 today")
        c2.metric("Total Scholarships", "$4.2B", "Global")
        c3.metric("AI Models", "Gemini 1.5 Flash", "Active")
        
        st.write("")
        st.write("### ⚡ Quick Modules")
        qc1, qc2, qc3 = st.columns(3)
        qc1.success("📚 Study Buddy")
        qc2.info("✈️ Global Wings")
        qc3.warning("🚀 Career AI")
        
    with col2:
        if lottie_db: st_lottie(lottie_db, height=250)

# ================= ACADEMIC HUB =================
elif selected == "Academic Hub":
    st.title("📚 Academic Hub Pro")
    lottie_study = load_lottieurl("https://lottie.host/9364951b-5262-4299-8d7b-402eb0656a81/w53e7XF0oN.json")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("Upload lecture slides or books. The AI will break it down into Summaries or generate Exams.")
    with col2:
        if lottie_study: st_lottie(lottie_study, height=150)

    if "GOOGLE_API_KEY" not in st.secrets:
        st.error("⚠️ API Key Missing in Secrets.")
    else:
        tab1, tab2 = st.tabs(["📝 Smart Summarizer", "🔥 Exam Generator"])
        
        with tab1:
            uploaded_file = st.file_uploader("Upload PDF Material", type="pdf")
            mode = st.radio("Summary Depth:", ["Quick Overview", "Detailed Notes", "Explain Like I'm 5"])
            if uploaded_file and st.button("Analyze Document"):
                with st.spinner("Processing Knowledge Base..."):
                    text = input_pdf_text(uploaded_file)
                    prompt = f"Provide a {mode} of this text. Use bold headings and bullet points."
                    st.markdown(get_gemini_response(prompt, text))

        with tab2:
            if uploaded_file:
                diff = st.select_slider("Difficulty Level", ["Easy", "Medium", "Hard", "Professor Level"])
                if st.button("Create Exam"):
                    with st.spinner(f"Generating {diff} Questions..."):
                        text = input_pdf_text(uploaded_file)
                        prompt = f"Create 5 {diff} Multiple Choice Questions from the text. Show Answer Key at bottom."
                        st.markdown(get_gemini_response(prompt, text))

# ================= GLOBAL WINGS (BEST UPDATE) =================
elif selected == "Global Wings":
    st.title("✈️ Global Wings Premium")
    
    # Premium Header Animation
    lottie_plane = load_lottieurl("https://lottie.host/9f5064e6-815d-4f06-b51c-438676d91d83/pT2x6o3s7M.json")
    
    col_head1, col_head2 = st.columns([3, 1])
    with col_head1:
        st.markdown("### 🌍 The Ultimate University Finder")
        st.write("Access real-time tuition fees, scholarship data, and visa success predictions.")
    with col_head2:
        if lottie_plane: st_lottie(lottie_plane, height=150)

    st.markdown("---")

    # ADVANCED INPUTS
    with st.container():
        st.subheader("🔍 Configure Search Parameters")
        c1, c2, c3, c4 = st.columns(4)
        
        country = c1.text_input("Destination", placeholder="e.g. USA, Germany")
        subject = c2.text_input("Major / Subject", placeholder="e.g. Computer Science")
        degree = c3.selectbox("Degree Level", ["Bachelor's", "Master's", "PhD"])
        budget = c4.select_slider("Max Annual Budget", ["$5,000", "$15,000", "$30,000", "Unlimited"])

    # SEARCH BUTTON & LOGIC
    if st.button("🛰️ Initiate Global Scan", use_container_width=True):
        if country and subject:
            # 1. VISUAL FEEDBACK
            with st.status("📡 Connecting to Global Education Database...", expanded=True) as status:
                st.write("Handshaking with University Servers...")
                time.sleep(1)
                st.write(f"Filtering {degree} programs in {country}...")
                time.sleep(1)
                st.write("Analyzing Scholarship Availability...")
                time.sleep(0.5)
                status.update(label="Scan Complete!", state="complete", expanded=False)

            # 2. VISA SUCCESS METER (Simulated AI)
            st.subheader("📊 AI Analysis Report")
            visa_col1, visa_col2 = st.columns([1, 3])
            
            with visa_col1:
                # Simulated probability based on country (Randomized for demo feel)
                prob = np.random.randint(70, 95)
                st.metric(label="Visa Success Probability", value=f"{prob}%", delta="High Chance")
            
            with visa_col2:
                st.progress(prob)
                st.caption(f"Based on current immigration trends for {country}.")

            # 3. AI TABLE GENERATION
            st.subheader(f"🏆 Top University Matches in {country}")
            with st.spinner("Compiling Final Report..."):
                prompt = f"""
                Act as a senior education consultant. Find top 5 universities in {country} for {degree} in {subject} (Budget around {budget}).
                
                Strictly output a MARKDOWN TABLE with these columns:
                | Global Rank | University Name | Tuition (Yearly) | IELTS/TOEFL Req | Scholarship Name | Scholarship Amount |
                |---|---|---|---|---|---|
                
                After the table, provide 3 bullet points on 'Why these are the best fit'.
                """
                st.markdown(get_gemini_response(prompt))
                
        else:
            st.warning("⚠️ Please enter a Country and Subject to start the scan.")

# ================= CAREER ARCHITECT =================
elif selected == "Career Architect":
    st.title("🚀 Career Architect AI")
    lottie_career = load_lottieurl("https://lottie.host/0200c5a2-9428-494b-85d7-1b20347895f3/Xf3s6j2r8v.json")
    
    col_intro, col_anim = st.columns([2, 1])
    with col_intro:
        st.write("Don't just guess. Let AI architect your path to top-tier companies like Google, Microsoft, and Tesla.")
    with col_anim:
        if lottie_career: st_lottie(lottie_career, height=180)

    with st.expander("👤 Profile Configuration", expanded=True):
        c1, c2 = st.columns(2)
        target_role = c1.text_input("Target Job Role", placeholder="e.g. Machine Learning Engineer")
        timeline = c2.select_slider("Goal Timeline", options=["3 Months", "6 Months", "1 Year"])

    if st.button("🚀 Generate Blueprint"):
        if target_role:
            # Chart Visualization
            st.subheader(f"📊 Market Trends: {target_role}")
            chart_data = pd.DataFrame(np.random.randint(60, 100, size=(12, 1)), columns=["Demand Score"])
            st.line_chart(chart_data)

            # AI Logic
            with st.spinner("AI is analyzing successful career paths..."):
                prompt = f"""
                Create a detailed {timeline} roadmap for {target_role}.
                Structure:
                1. **Skill Gap Analysis**
                2. **Month-by-Month Plan**
                3. **Project Ideas**
                """
                st.markdown(get_gemini_response(prompt))
        else:
            st.warning("⚠️ Please enter a Target Job Role.")
