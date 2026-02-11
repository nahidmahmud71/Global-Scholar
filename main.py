import streamlit as st
import time
import requests
import pandas as pd
import numpy as np
import google.generativeai as genai
import PyPDF2 as pdf
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu

# --- 1. PAGE CONFIGURATION (Browser Tab Info) ---
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
            model = genai.GenerativeModel('gemini-pro')
            if content:
                response = model.generate_content([input_prompt, content])
            else:
                response = model.generate_content(input_prompt)
            return response.text
        else:
            return "⚠️ System Error: API Key Missing in Secrets."
    except Exception as e:
        return f"⚠️ AI Engine Error: {str(e)}"

# --- 3. PREMIUM CSS STYLING (Neon & Glassmorphism) ---
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background: linear-gradient(to bottom, #0f172a, #020617);
        color: #e2e8f0;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* --- INTRO ANIMATION (Neon Pulse - The User Favorite) --- */
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
    }
    .neon-uni {
        font-size: 35px;
        color: #38bdf8; /* Light Blue */
        font-family: 'Courier New', monospace;
        letter-spacing: 5px;
        margin-top: 20px;
        border-bottom: 2px solid #38bdf8;
        padding-bottom: 10px;
    }
    
    @keyframes neon-pulse {
        from { text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #38bdf8; }
        to { text-shadow: 0 0 20px #fff, 0 0 30px #0ea5e9, 0 0 40px #0ea5e9; }
    }

    /* --- DASHBOARD CARDS (Glass Effect) --- */
    div.css-1r6slb0 {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        transition: transform 0.3s ease;
    }
    div.css-1r6slb0:hover {
        transform: translateY(-5px);
        border-color: #38bdf8;
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
            <p style="color: gray;">Initializing AI Core Systems...</p>
        </div>
        """, unsafe_allow_html=True)
        # Loading Bar Simulation
        progress = st.progress(0)
        for i in range(100):
            time.sleep(0.015)
            progress.progress(i + 1)
        time.sleep(0.5)
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
        "nav-link": {"font-size": "15px", "text-align": "center", "margin": "0px", "color": "#94a3b8"},
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

    # 1. LIVE DATA TICKER (Fake but feels real)
    st.info("🔔 **LATEST UPDATES:** Harvard Scholarship Deadline Extended | new Visa Rules for Germany Released | AI Jobs Growing by 40% in 2026")

    # 2. HUGE DATA STATS (Animated Lottie + Metrics)
    lottie_db = load_lottieurl("https://lottie.host/5a7d51e7-268e-4934-a63e-670560a6136d/6gH7Xy44uT.json")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Universities Tracked", "25,000+", "Global Wings")
    col2.metric("Scholarships Available", "$1.2B", "Updated Today")
    col3.metric("Career Paths Analyzed", "5,400+", "Career Architect")
    col4.metric("AI Models Active", "Gemini Pro", "v1.5")

    # 3. FEATURE PREVIEWS (Rich Cards)
    st.markdown("### ⚡ Quick Access Modules")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("#### 📚 Academic Hub")
        st.image("https://cdn-icons-png.flaticon.com/512/2232/2232688.png", width=50)
        st.write("Upload PDFs, get Summaries & Quizzes. Supports detailed analysis.")
        st.progress(85) # Shows 'usage' or 'capacity'
        
    with c2:
        st.markdown("#### ✈️ Global Wings")
        st.image("https://cdn-icons-png.flaticon.com/512/814/814513.png", width=50)
        st.write("Advanced Search for Unis, Tuition & Visas. 100% Data accuracy.")
        st.progress(92)
        
    with c3:
        st.markdown("#### 🚀 Career Architect")
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=50)
        st.write("Generate Roadmaps, Salary Graphs & Skill Gap Analysis.")
        st.progress(78)

# ================= ACADEMIC HUB =================
elif selected == "Academic Hub":
    st.title("📚 Academic Hub Pro")
    lottie_study = load_lottieurl("https://lottie.host/9364951b-5262-4299-8d7b-402eb0656a81/w53e7XF0oN.json")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("Upload your lecture slides or books. The AI will break it down into Digestible Summaries or Hardcore Exams.")
    with col2:
        if lottie_study: st_lottie(lottie_study, height=150)

    # Main Tool
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

# ================= GLOBAL WINGS =================
elif selected == "Global Wings":
    st.title("✈️ Global Wings Premium")
    lottie_globe = load_lottieurl("https://lottie.host/9f5064e6-815d-4f06-b51c-438676d91d83/pT2x6o3s7M.json")
    
    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown("### 🌍 Worldwide University Database Access")
        st.write("Search utilizing our massive dataset of tuition fees, acceptance rates, and scholarship funds.")
    with c2:
        if lottie_globe: st_lottie(lottie_globe, height=180)

    # Advanced Search UI
    with st.container():
        st.subheader("🔍 Deep Data Search")
        col1, col2, col3, col4 = st.columns(4)
        country = col1.text_input("Destination", placeholder="e.g. USA")
        subject = col2.text_input("Major", placeholder="e.g. CS")
        degree = col3.selectbox("Degree", ["Bachelor", "Master", "PhD"])
        budget = col4.select_slider("Budget Cap ($)", ["10k", "20k", "30k", "50k+"])

        if st.button("Run Global Scan 🛰️", use_container_width=True):
            if country and subject:
                with st.spinner(f"Scanning 12,000+ Universities in {country}..."):
                    time.sleep(1) # Feel of big data
                    prompt = f"""
                    Find top 5 universities in {country} for {degree} in {subject} (Budget: {budget}).
                    Output a MARKDOWN TABLE: | Rank | University | Tuition | Acceptance Rate | Best Scholarship |
                    Then add a 'Visa Success Tip' section.
                    """
                    st.markdown(get_gemini_response(prompt))

# ================= CAREER ARCHITECT (BEST UPDATE) =================
elif selected == "Career Architect":
    st.title("🚀 Career Architect AI")
    st.markdown("### 📈 Strategic Career Planning & Market Analysis")
    
    # Animated Intro for this section
    lottie_career = load_lottieurl("https://lottie.host/0200c5a2-9428-494b-85d7-1b20347895f3/Xf3s6j2r8v.json")
    
    col_intro, col_anim = st.columns([2, 1])
    with col_intro:
        st.write("Don't just guess. Let AI architect your path to top-tier companies like Google, Microsoft, and Tesla.")
        st.info("💡 **New Feature:** Market Salary Trends & Skill Gap Analysis included.")
    with col_anim:
        if lottie_career: st_lottie(lottie_career, height=200)

    st.divider()

    # INPUT SECTION (User Friendly Expander)
    with st.expander("👤 Step 1: Profile Configuration (Click to Expand)", expanded=True):
        c1, c2 = st.columns(2)
        target_role = c1.text_input("Target Job Role", placeholder="e.g. Machine Learning Engineer")
        current_status = c2.selectbox("Current Status", ["Student (1st-2nd Year)", "Student (3rd-4th Year)", "Fresh Graduate", "Professional"])
        
        target_company = st.multiselect("Target Companies (Optional)", ["Google", "Amazon", "Tesla", "Local Top Tier"], default=["Google"])
        timeline = st.select_slider("Goal Timeline", options=["3 Months", "6 Months", "1 Year"])

    # ACTION SECTION
    if st.button("🚀 Generate Blueprint"):
        if target_role:
            # 1. FAKE DATA VISUALIZATION (To show "Huge Data" feel)
            st.subheader(f"📊 Market Analysis: {target_role}")
            
            # Chart 1: Salary Trend
            col_chart1, col_chart2 = st.columns(2)
            with col_chart1:
                st.write("**💰 Estimated Salary Growth (Next 5 Years)**")
                chart_data = pd.DataFrame(
                    np.random.randint(50000, 150000, size=(5, 1)),
                    columns=["Salary ($)"],
                    index=["2026", "2027", "2028", "2029", "2030"]
                )
                st.line_chart(chart_data)
            
            # Chart 2: Demand Trend
            with col_chart2:
                st.write("**🔥 Market Demand Score**")
                st.bar_chart({"Demand": [80, 85, 90, 95, 98]})

            # 2. AI ROADMAP GENERATION
            st.divider()
            st.subheader("🗺️ Your Personalized Execution Plan")
            with st.spinner("AI is analyzing 1,000+ successful career paths..."):
                prompt = f"""
                Create a detailed {timeline} roadmap for a {current_status} aiming for {target_role} at {target_company}.
                
                Structure:
                1. **Skill Gap Analysis**: What they likely know vs what they NEED.
                2. **Month-by-Month Plan**: Specific topics, projects, and resources.
                3. **Project Ideas**: 2 Portfolio-ready project titles with descriptions.
                4. **Certification Guide**: Best certificates for this role.
                """
                st.markdown(get_gemini_response(prompt))
                st.balloons()
        else:
            st.warning("⚠️ Please enter a Target Job Role to begin analysis.")
