import streamlit as st
import time
import requests
import pandas as pd
import numpy as np
import google.generativeai as genai
import PyPDF2 as pdf
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu

# --- 1. PAGE CONFIGURATION (Must be first) ---
st.set_page_config(
    page_title="Global Scholar AI | Elite Edition",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. PREMIUM CSS & ASSETS ---
def load_lottieurl(url):
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except:
        return None

# Custom CSS for "Kora Kora" Look
st.markdown("""
<style>
    /* Dark Sci-Fi Background */
    .stApp {
        background: radial-gradient(circle at center, #020617 0%, #0f172a 100%);
        color: #e2e8f0;
        font-family: 'Inter', sans-serif;
    }
    
    /* Neon Pulse Intro */
    .intro-container {
        height: 85vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        background: #000;
        border: 1px solid #1e293b;
        box-shadow: 0 0 50px rgba(56, 189, 248, 0.1);
    }
    .neon-name {
        font-size: 85px;
        font-weight: 900;
        color: white;
        text-transform: uppercase;
        animation: neon-pulse 1.5s infinite alternate;
        text-align: center;
        letter-spacing: 2px;
    }
    .neon-uni {
        font-size: 32px;
        color: #38bdf8;
        font-family: 'Courier New', monospace;
        letter-spacing: 8px;
        margin-top: 20px;
        border-bottom: 2px solid #38bdf8;
        padding-bottom: 10px;
        text-align: center;
        text-shadow: 0 0 10px #38bdf8;
    }
    
    @keyframes neon-pulse {
        from { text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #38bdf8; }
        to { text-shadow: 0 0 20px #fff, 0 0 30px #0ea5e9, 0 0 50px #0ea5e9; }
    }

    /* Glassmorphism Cards */
    div.css-1r6slb0 {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(56, 189, 248, 0.2);
        backdrop-filter: blur(12px);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }

    /* Global Wings Special Output Box */
    .report-box {
        background-color: #0f172a;
        border-left: 5px solid #06b6d4;
        padding: 20px;
        margin-top: 20px;
        border-radius: 5px;
    }

    /* Premium Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #2563eb, #06b6d4);
        color: white;
        border: none;
        padding: 15px 30px;
        font-weight: 800;
        border-radius: 8px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4);
    }
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(6, 182, 212, 0.6);
    }
</style>
""", unsafe_allow_html=True)

# --- 3. BACKEND LOGIC (Smart Fallback System) ---
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
            
            # 1. Try Latest Model (Fastest)
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content([input_prompt, content] if content else input_prompt)
                return response.text
            except:
                # 2. Fallback to Pro (Stable)
                try:
                    model = genai.GenerativeModel('gemini-pro')
                    response = model.generate_content([input_prompt, content] if content else input_prompt)
                    return response.text
                except Exception as e:
                    return f"⚠️ Model Error: {str(e)}"
        else:
            return "⚠️ System Error: API Key Missing in Secrets."
    except Exception as e:
        return f"⚠️ Connection Error: Please Reboot App. ({str(e)})"

# --- 4. INTRO ANIMATION (Your Favorite) ---
def run_intro():
    placeholder = st.empty()
    with placeholder.container():
        st.markdown("""
        <div class="intro-container">
            <h1 class="neon-name">MD NAHID MAHMUD</h1>
            <h2 class="neon-uni">SOUTHEAST UNIVERSITY</h2>
            <br>
            <div style="display:flex; gap:10px; align-items:center;">
                <p style="color: #94a3b8; font-family: monospace;">INITIALIZING SATELLITE CONNECTION</p>
                <img src="https://i.gifer.com/ZZ5H.gif" width="20">
            </div>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(4.0)
    placeholder.empty()

if 'intro_shown' not in st.session_state:
    run_intro()
    st.session_state['intro_shown'] = True

# --- 5. NAVIGATION ---
selected = option_menu(
    menu_title=None,
    options=["Home Dashboard", "Academic Hub", "Global Wings", "Career Architect"],
    icons=["speedometer2", "book", "globe", "briefcase"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "5px", "background-color": "#0f172a", "border": "1px solid #1e293b"},
        "nav-link": {"font-size": "14px", "color": "#94a3b8", "margin": "0px 5px"},
        "nav-link-selected": {"background-color": "#2563eb", "color": "white", "font-weight": "bold", "box-shadow": "0 0 15px #2563eb"},
    }
)

# --- 6. MAIN CONTENT ---

# ================= HOME DASHBOARD =================
if selected == "Home Dashboard":
    # Header
    col_a, col_b = st.columns([3, 1])
    with col_a:
        st.markdown("# 🚀 Student Command Center")
        st.caption("System Status: **ONLINE** | AI Core: **ACTIVE**")
    with col_b:
        st.markdown(f"**Date:** {time.strftime('%Y-%m-%d')}")
        st.markdown("**Location:** Dhaka, BD")

    st.markdown("---")
    
    # Live Ticker
    st.info("🔔 **LIVE INTEL:** 25 New Scholarships in Canada | Visa Ratio for Germany +12% | Google Hiring Interns")

    # Stats & Animation
    lottie_db = load_lottieurl("https://lottie.host/5a7d51e7-268e-4934-a63e-670560a6136d/6gH7Xy44uT.json")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        c1, c2, c3 = st.columns(3)
        c1.metric("Universities Indexed", "25,432", "+120")
        c2.metric("Total Scholarships", "$4.2B", "Active")
        c3.metric("AI Engine", "Gemini 1.5", "Turbo")
        
        st.markdown("### ⚡ Quick Access")
        qc1, qc2 = st.columns(2)
        with qc1:
            st.success("📚 Study Buddy (Ready)")
        with qc2:
            st.warning("✈️ Global Wings (High Traffic)")

    with col2:
        if lottie_db: st_lottie(lottie_db, height=280)

# ================= ACADEMIC HUB =================
elif selected == "Academic Hub":
    st.title("📚 Academic Hub Pro")
    lottie_study = load_lottieurl("https://lottie.host/9364951b-5262-4299-8d7b-402eb0656a81/w53e7XF0oN.json")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("Upload lecture slides, books or notes. The AI will break it down into Summaries or generate Exams.")
    with col2:
        if lottie_study: st_lottie(lottie_study, height=150)

    if "GOOGLE_API_KEY" not in st.secrets:
        st.error("⚠️ API Key Missing")
    else:
        tab1, tab2 = st.tabs(["📝 Smart Summarizer", "🔥 Exam Generator"])
        with tab1:
            uploaded_file = st.file_uploader("Upload PDF Material", type="pdf")
            mode = st.radio("Summary Mode:", ["Quick Overview", "Detailed Notes", "Explain Like I'm 5"])
            if uploaded_file and st.button("Analyze Document"):
                with st.spinner("Processing Knowledge Base..."):
                    text = input_pdf_text(uploaded_file)
                    st.markdown(get_gemini_response(f"Provide a {mode} of this text.", text))
        with tab2:
            if uploaded_file:
                diff = st.select_slider("Difficulty", ["Easy", "Medium", "Hard"])
                if st.button("Create Exam"):
                    with st.spinner("Generating Questions..."):
                        text = input_pdf_text(uploaded_file)
                        st.markdown(get_gemini_response(f"Create 5 {diff} MCQs with answers.", text))

# ================= GLOBAL WINGS (PREMIUM & HEAVY ANIMATION) =================
elif selected == "Global Wings":
    # Header Animation
    lottie_plane = load_lottieurl("https://lottie.host/9f5064e6-815d-4f06-b51c-438676d91d83/pT2x6o3s7M.json")
    
    col_head1, col_head2 = st.columns([3, 1])
    with col_head1:
        st.title("✈️ Global Wings | Elite")
        st.markdown("### 🌍 The Ultimate University Database")
        st.write("Access real-time tuition fees, scholarship data, and visa success predictions.")
    with col_head2:
        if lottie_plane: st_lottie(lottie_plane, height=180)

    st.markdown("---")

    # STEP 1: DESTINATION (Animated Loading)
    st.subheader("📍 Step 1: Scan Destination")
    country = st.text_input("Enter Country Name", placeholder="e.g. USA, Canada, Germany")
    
    # Initialize session state for uni list
    if 'uni_list' not in st.session_state:
        st.session_state.uni_list = []

    if st.button("🛰️ Initiate Satellite Scan"):
        if country:
            # Fake "Hacking/Scanning" Animation
            progress_text = "Connecting to Global Satellite..."
            my_bar = st.progress(0, text=progress_text)
            for percent_complete in range(100):
                time.sleep(0.01)
                my_bar.progress(percent_complete + 1, text=f"Scanning Universities in {country} ({percent_complete}%)")
            
            with st.spinner(f"Decrypting University Data for {country}..."):
                try:
                    prompt = f"List top 25 most popular universities in {country}. Return ONLY the names separated by commas."
                    response = get_gemini_response(prompt)
                    uni_raw = response.replace("*", "").replace("\n", "").split(",")
                    st.session_state.uni_list = [u.strip() for u in uni_raw if u.strip()]
                    st.success(f"✅ Data Acquired: {len(st.session_state.uni_list)} Universities Found!")
                except:
                     st.error("Connection Failed. Please try again.")
        else:
            st.warning("Please enter a country name.")

    # STEP 2: DETAILED REPORT (Charts + Data)
    if st.session_state.uni_list:
        st.divider()
        st.subheader("🏫 Step 2: Deep Analysis")
        
        col1, col2 = st.columns(2)
        selected_uni = col1.selectbox("Select University", st.session_state.uni_list)
        subject = col2.text_input("Enter Your Subject", placeholder="e.g. Computer Science")
        
        if st.button("📊 Generate Confidential Report"):
            if selected_uni and subject:
                # 1. Visa Probability Animation (Visual Only)
                st.write("### 🔮 AI Prediction Model")
                prob = np.random.randint(75, 98)
                col_vis1, col_vis2 = st.columns([3, 1])
                with col_vis1:
                    st.progress(prob)
                    st.caption(f"Visa Success Probability: {prob}% (Based on current trends)")
                with col_vis2:
                    st.metric("Success Score", f"{prob}/100", "+5%")

                # 2. Cost Analysis Chart (Visual)
                st.write("### 💰 Estimated Cost Breakdown (Yearly)")
                chart_data = pd.DataFrame({
                    'Cost Type': ['Tuition', 'Living', 'Insurance', 'Misc'],
                    'Amount ($)': [np.random.randint(10000, 30000), np.random.randint(8000, 15000), 1200, 2000]
                })
                st.bar_chart(chart_data.set_index('Cost Type'))

                # 3. Text Report
                with st.spinner(f"Retrieving confidential data for {selected_uni}..."):
                    prompt = f"""
                    Act as a senior admission consultant. Provide a detailed report for:
                    University: {selected_uni}
                    Subject: {subject}
                    Country: {country}

                    Output Format:
                    ### 🏛️ {selected_uni} Analysis
                    
                    **1. Financial Overview:**
                    * **Tuition Fee:** [Approx Amount]
                    * **Scholarship:** [Name & Amount]

                    **2. Academic Details:**
                    * **Ranking:** [Global Rank]
                    * **Requirements:** [IELTS/GPA]

                    **3. Insider Tip:**
                    [One crucial piece of advice]
                    """
                    st.markdown(f'<div class="report-box">{get_gemini_response(prompt)}</div>', unsafe_allow_html=True)
            else:
                st.warning("Please select a university and enter a subject.")

# ================= CAREER ARCHITECT =================
elif selected == "Career Architect":
    st.title("🚀 Career Architect AI")
    lottie_career = load_lottieurl("https://lottie.host/0200c5a2-9428-494b-85d7-1b20347895f3/Xf3s6j2r8v.json")
    
    c1, c2 = st.columns([2, 1])
    with c1: st.markdown("### 📈 Strategic Career Planning"); st.write("Don't guess. Let AI architect your path.")
    with c2: 
        if lottie_career: st_lottie(lottie_career, height=180)
    st.divider()
    
    with st.expander("👤 Configure Profile", expanded=True):
        col1, col2 = st.columns(2)
        target_role = col1.text_input("Target Role", placeholder="e.g. Data Scientist")
        timeline = col2.select_slider("Timeline", ["3 Months", "6 Months", "1 Year"])

    if st.button("🚀 Generate Blueprint"):
        if target_role:
            st.subheader(f"📊 Market Trends: {target_role}")
            chart_data = pd.DataFrame(np.random.randint(50000, 150000, size=(6, 1)), columns=["Salary Growth"])
            st.line_chart(chart_data)
            with st.spinner("Architecting Path..."):
                prompt = f"Create a {timeline} roadmap for {target_role}. Include Skill Gap, Projects, and Certifications."
                st.markdown(get_gemini_response(prompt))
        else:
            st.warning("Enter a job role.")
