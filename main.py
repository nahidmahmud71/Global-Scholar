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
            
            # Using the latest model
            model = genai.GenerativeModel('gemini-1.5-flash') 
            
            if content:
                response = model.generate_content([input_prompt, content])
            else:
                response = model.generate_content(input_prompt)
            return response.text
        else:
            return "⚠️ System Error: API Key Missing in Secrets."
    except Exception as e:
        return f"⚠️ AI Error: {str(e)} (Check requirements.txt)"

# --- 3. PREMIUM CSS STYLING ---
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(to bottom, #0f172a, #020617);
        color: #e2e8f0;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* Neon Pulse Intro */
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

    /* Buttons */
    .stButton > button {
        background: linear-gradient(45deg, #2563eb, #06b6d4);
        color: white;
        border: none;
        padding: 12px 25px;
        font-weight: bold;
        border-radius: 8px;
        width: 100%;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
    }
    .stButton > button:hover {
        box-shadow: 0 6px 20px rgba(6, 182, 212, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# --- 4. INTRO ANIMATION ---
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

# --- 5. NAVIGATION MENU ---
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

# --- 6. MAIN CONTENT ---

# ================= HOME DASHBOARD =================
if selected == "Home Dashboard":
    col_a, col_b = st.columns([3, 1])
    with col_a:
        st.markdown("# 🚀 Student Command Center")
        st.markdown("### System Status: **ONLINE**")
    with col_b:
        st.markdown(f"**Date:** {time.strftime('%Y-%m-%d')}")

    st.markdown("---")
    st.info("🔔 **LIVE:** 25 New Scholarships Added | Harvard Acceptance Rate Update | Visa Policies Changed for UK")

    lottie_db = load_lottieurl("https://lottie.host/5a7d51e7-268e-4934-a63e-670560a6136d/6gH7Xy44uT.json")
    col1, col2 = st.columns([2, 1])
    with col1:
        c1, c2, c3 = st.columns(3)
        c1.metric("Universities Indexed", "25,432", "+15")
        c2.metric("Total Scholarships", "$4.2B", "Active")
        c3.metric("AI Engine", "Gemini 1.5 Flash", "Online")
    with col2:
        if lottie_db: st_lottie(lottie_db, height=250)

# ================= ACADEMIC HUB =================
elif selected == "Academic Hub":
    st.title("📚 Academic Hub Pro")
    lottie_study = load_lottieurl("https://lottie.host/9364951b-5262-4299-8d7b-402eb0656a81/w53e7XF0oN.json")
    
    c1, c2 = st.columns([2, 1])
    with c1:
        st.write("Upload lecture slides or books. AI will Summarize or Generate Exams.")
    with c2:
        if lottie_study: st_lottie(lottie_study, height=150)

    if "GOOGLE_API_KEY" not in st.secrets:
        st.error("⚠️ API Key Missing")
    else:
        tab1, tab2 = st.tabs(["📝 Smart Summarizer", "🔥 Exam Generator"])
        with tab1:
            uploaded_file = st.file_uploader("Upload PDF", type="pdf")
            mode = st.radio("Mode:", ["Quick Overview", "Detailed Notes", "Explain Like I'm 5"])
            if uploaded_file and st.button("Analyze"):
                with st.spinner("Processing..."):
                    text = input_pdf_text(uploaded_file)
                    st.markdown(get_gemini_response(f"Provide a {mode} of this text.", text))
        with tab2:
            if uploaded_file:
                diff = st.select_slider("Difficulty", ["Easy", "Medium", "Hard"])
                if st.button("Create Exam"):
                    with st.spinner("Generating..."):
                        text = input_pdf_text(uploaded_file)
                        st.markdown(get_gemini_response(f"Create 5 {diff} MCQs with answers.", text))

# ================= GLOBAL WINGS (SUPER UPDATE) =================
elif selected == "Global Wings":
    st.title("✈️ Global Wings Premium")
    lottie_plane = load_lottieurl("https://lottie.host/9f5064e6-815d-4f06-b51c-438676d91d83/pT2x6o3s7M.json")
    
    col_head1, col_head2 = st.columns([3, 1])
    with col_head1:
        st.markdown("### 🌍 The Ultimate University Database")
        st.write("First select a country to load universities, then get detailed analysis.")
    with col_head2:
        if lottie_plane: st_lottie(lottie_plane, height=150)

    st.markdown("---")

    # STEP 1: SELECT COUNTRY
    st.subheader("📍 Step 1: Select Destination")
    country = st.text_input("Enter Country Name", placeholder="e.g. USA, Canada, Germany")
    
    # Session state to store universities list
    if 'uni_list' not in st.session_state:
        st.session_state.uni_list = []

    if st.button("🔍 Load Universities"):
        if country:
            with st.spinner(f"Connecting to {country} Education Database..."):
                # AI Generates the list of universities
                prompt = f"List top 25 most popular universities in {country}. Just give me the names separated by commas."
                response = get_gemini_response(prompt)
                # Cleaning the list
                uni_raw = response.replace("*", "").split(",")
                st.session_state.uni_list = [u.strip() for u in uni_raw if u.strip()]
                st.success(f"✅ Loaded {len(st.session_state.uni_list)} Universities from {country}")
        else:
            st.warning("Please enter a country name first.")

    # STEP 2: SELECT UNIVERSITY & SUBJECT
    if st.session_state.uni_list:
        st.divider()
        st.subheader("🏫 Step 2: Choose University & Subject")
        
        col1, col2 = st.columns(2)
        selected_uni = col1.selectbox("Select University", st.session_state.uni_list)
        subject = col2.text_input("Enter Your Subject", placeholder="e.g. Computer Science")
        
        if st.button("📊 Get Full University Report"):
            if selected_uni and subject:
                with st.spinner(f"Retrieving confidential data for {selected_uni}..."):
                    prompt = f"""
                    Act as a senior admission consultant. Provide a detailed report for:
                    University: {selected_uni}
                    Subject: {subject}
                    Country: {country}

                    Please provide the output in this EXACT format:
                    
                    ### 🏛️ {selected_uni} Analysis
                    
                    **1. Financial Overview:**
                    * **Tuition Fee (Approx):** [Amount in USD/Local Currency]
                    * **Living Cost:** [Amount per month]
                    * **Scholarship Opportunities:** [List 2-3 specific scholarships]

                    **2. Academic Details:**
                    * **Global Ranking:** [Approx Rank]
                    * **Acceptance Rate:** [Percentage]
                    * **IELTS/TOEFL Requirement:** [Score]

                    **3. Why Study Here?**
                    [Provide 3 strong reasons]

                    **4. Important Warning/Tip:**
                    [One crucial piece of advice for international students]
                    """
                    st.markdown(get_gemini_response(prompt))
            else:
                st.warning("Please select a university and enter a subject.")

# ================= CAREER ARCHITECT =================
elif selected == "Career Architect":
    st.title("🚀 Career Architect AI")
    lottie_career = load_lottieurl("https://lottie.host/0200c5a2-9428-494b-85d7-1b20347895f3/Xf3s6j2r8v.json")
    
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown("### 📈 Strategic Career Planning")
        st.write("AI-Powered Roadmap Generator & Market Analysis.")
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
