import streamlit as st
import time
import requests
import pandas as pd
import numpy as np
import google.generativeai as genai
import PyPDF2 as pdf
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Global Scholar AI | Elite Edition",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. ASSETS & STYLING ---
def load_lottieurl(url):
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except:
        return None

st.markdown("""
<style>
    /* Premium Black & Neon Theme */
    .stApp { background: radial-gradient(circle at center, #020617 0%, #0f172a 100%); color: #e2e8f0; font-family: 'Inter', sans-serif; }
    
    /* Intro Animation */
    .intro-container { height: 85vh; display: flex; flex-direction: column; justify-content: center; align-items: center; background: #000; border: 1px solid #1e293b; box-shadow: 0 0 60px rgba(56, 189, 248, 0.15); }
    .neon-name { font-size: 80px; font-weight: 900; color: white; text-transform: uppercase; animation: neon-pulse 1.5s infinite alternate; text-align: center; letter-spacing: 2px; }
    .neon-uni { font-size: 30px; color: #38bdf8; letter-spacing: 8px; margin-top: 20px; border-bottom: 2px solid #38bdf8; padding-bottom: 10px; text-align: center; }
    @keyframes neon-pulse { from { text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #38bdf8; } to { text-shadow: 0 0 20px #fff, 0 0 30px #0ea5e9, 0 0 50px #0ea5e9; } }

    /* Glassmorphism Output Box */
    .report-box { background: rgba(15, 23, 42, 0.95); border-left: 5px solid #06b6d4; padding: 25px; margin-top: 20px; border-radius: 10px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
    
    /* Buttons */
    .stButton > button { background: linear-gradient(90deg, #2563eb, #06b6d4); color: white; border: none; padding: 16px 32px; font-weight: 800; border-radius: 8px; text-transform: uppercase; letter-spacing: 1.5px; width: 100%; transition: all 0.3s ease; }
    .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 10px 25px rgba(6, 182, 212, 0.6); }
</style>
""", unsafe_allow_html=True)

# --- 3. INTELLIGENT BACKEND (Fixes 404 & Parsing) ---
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
            
            # TRY-CATCH BLOCK FOR MODELS (Safety Net)
            try:
                # Priority 1: Latest Flash Model
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content([input_prompt, content] if content else input_prompt)
                return response.text
            except:
                try:
                    # Priority 2: Standard Pro
                    model = genai.GenerativeModel('gemini-pro')
                    response = model.generate_content([input_prompt, content] if content else input_prompt)
                    return response.text
                except Exception as e:
                    return f"⚠️ Model Error: {str(e)} (Please update requirements.txt)"
        else:
            return "⚠️ System Error: API Key Missing."
    except Exception as e:
        return f"⚠️ Connection Error: {str(e)}"

# --- 4. INTRO ANIMATION ---
def run_intro():
    placeholder = st.empty()
    with placeholder.container():
        st.markdown("""
        <div class="intro-container">
            <h1 class="neon-name">MD NAHID MAHMUD</h1>
            <h2 class="neon-uni">SOUTHEAST UNIVERSITY</h2>
            <br>
            <p style="color: #94a3b8; font-family: monospace;">ESTABLISHING SECURE CONNECTION...</p>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(3.5)
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
        "nav-link-selected": {"background-color": "#2563eb", "color": "white", "font-weight": "bold"},
    }
)

# --- 6. MAIN CONTENT ---

# === HOME DASHBOARD ===
if selected == "Home Dashboard":
    col_a, col_b = st.columns([3, 1])
    with col_a:
        st.markdown("# 🚀 Student Command Center")
        st.caption("System Status: **ONLINE** | AI Core: **ACTIVE**")
    with col_b:
        st.markdown(f"**Date:** {time.strftime('%Y-%m-%d')}")
    st.markdown("---")
    st.info("🔔 **LIVE INTEL:** 50+ New Universities Added for Bangladesh | Server Load: Normal")

    lottie_db = load_lottieurl("https://lottie.host/5a7d51e7-268e-4934-a63e-670560a6136d/6gH7Xy44uT.json")
    col1, col2 = st.columns([2, 1])
    with col1:
        c1, c2, c3 = st.columns(3)
        c1.metric("Universities", "25,000+", "Global")
        c2.metric("Scholarships", "$4.2B", "Active")
        c3.metric("AI Engine", "Gemini 1.5", "Turbo")
        st.markdown("### ⚡ Module Access")
        qc1, qc2, qc3 = st.columns(3)
        qc1.success("📚 Study Buddy")
        qc2.info("✈️ Global Wings")
        qc3.warning("🚀 Career AI")
    with col2:
        if lottie_db: st_lottie(lottie_db, height=280)

# === ACADEMIC HUB ===
elif selected == "Academic Hub":
    st.title("📚 Academic Hub Pro")
    lottie_study = load_lottieurl("https://lottie.host/9364951b-5262-4299-8d7b-402eb0656a81/w53e7XF0oN.json")
    col1, col2 = st.columns([2, 1])
    with col1: st.write("Upload PDF notes. AI will Summarize or Generate Exams."); 
    with col2: 
        if lottie_study: st_lottie(lottie_study, height=150)

    if "GOOGLE_API_KEY" not in st.secrets:
        st.error("⚠️ API Key Missing")
    else:
        tab1, tab2 = st.tabs(["📝 Summarizer", "🔥 Exam Generator"])
        with tab1:
            uploaded_file = st.file_uploader("Upload PDF", type="pdf")
            mode = st.radio("Mode:", ["Summary", "Detailed Notes"])
            if uploaded_file and st.button("Analyze"):
                with st.spinner("Processing..."):
                    text = input_pdf_text(uploaded_file)
                    st.markdown(get_gemini_response(f"Provide a {mode} of this text.", text))
        with tab2:
            if uploaded_file:
                if st.button("Create Exam"):
                    with st.spinner("Generating..."):
                        text = input_pdf_text(uploaded_file)
                        st.markdown(get_gemini_response("Create 5 Hard MCQs with answers.", text))

# === GLOBAL WINGS (50+ UNI FIX) ===
elif selected == "Global Wings":
    lottie_plane = load_lottieurl("https://lottie.host/9f5064e6-815d-4f06-b51c-438676d91d83/pT2x6o3s7M.json")
    col_head1, col_head2 = st.columns([3, 1])
    with col_head1:
        st.title("✈️ Global Wings | Elite")
        st.write("Access massive database of Public & Private Universities.")
    with col_head2:
        if lottie_plane: st_lottie(lottie_plane, height=180)
    st.markdown("---")

    # Step 1: Destination
    st.subheader("📍 Step 1: Scan Destination")
    country = st.text_input("Enter Country Name", placeholder="e.g. Bangladesh, USA")
    
    if 'uni_list' not in st.session_state:
        st.session_state.uni_list = []

    if st.button("🛰️ Initiate Satellite Scan"):
        if country:
            # Fake "Heavy Scanning" Animation
            progress_bar = st.progress(0)
            status_text = st.empty()
            for i in range(100):
                time.sleep(0.015) # Slower for effect
                progress_bar.progress(i + 1)
                if i < 40: status_text.text(f"Connecting to {country} Education Grid...")
                elif i < 80: status_text.text("Retrieving Public & Private University Data...")
                else: status_text.text("Finalizing List...")
            
            with st.spinner(f"Compiling Huge Database for {country}..."):
                # SUPER PROMPT FOR 50+ UNIVERSITIES
                prompt = f"""
                List at least 50 major universities in {country}. 
                Include Top Public Universities AND Private Universities.
                Output ONLY the names separated by a newline character (one per line). 
                Do not include numbers, bullets, or extra text. Just the names.
                """
                response = get_gemini_response(prompt)
                
                if "⚠️" in response:
                    st.error(response)
                else:
                    # ROBUST PARSING (Split by newlines for better accuracy)
                    uni_raw = response.strip().split("\n")
                    # Clean and Filter
                    clean_list = [u.strip().replace("*", "").replace("-", "") for u in uni_raw if len(u.strip()) > 3]
                    st.session_state.uni_list = sorted(list(set(clean_list)))
                    
                    st.success(f"✅ Data Acquired: {len(st.session_state.uni_list)} Universities Found in {country}!")
        else:
            st.warning("Enter a country.")

    # Step 2: Report
    if st.session_state.uni_list:
        st.divider()
        st.subheader("🏫 Step 2: Deep Analysis")
        col1, col2 = st.columns(2)
        selected_uni = col1.selectbox("Select University", st.session_state.uni_list)
        subject = col2.text_input("Enter Subject", placeholder="e.g. CSE")
        
        if st.button("📊 Generate Confidential Report"):
            if selected_uni and subject:
                with st.spinner("Retrieving Data..."):
                    prompt = f"""
                    Provide a detailed report for:
                    University: {selected_uni}
                    Subject: {subject}
                    Country: {country}
                    
                    Output in Markdown:
                    ### 🏛️ {selected_uni}
                    **1. Financials:** Tuition & Living Costs.
                    **2. Academics:** Rank, Acceptance Rate, Requirements.
                    **3. Why Study Here:** 3 Reasons.
                    """
                    st.markdown(f'<div class="report-box">{get_gemini_response(prompt)}</div>', unsafe_allow_html=True)
            else:
                st.warning("Select University & Subject.")

# === CAREER ARCHITECT ===
elif selected == "Career Architect":
    st.title("🚀 Career Architect AI")
    lottie_career = load_lottieurl("https://lottie.host/0200c5a2-9428-494b-85d7-1b20347895f3/Xf3s6j2r8v.json")
    c1, c2 = st.columns([2, 1])
    with c1: st.write("AI-Powered Roadmap Generator."); 
    with c2: 
        if lottie_career: st_lottie(lottie_career, height=180)
    st.divider()
    
    col1, col2 = st.columns(2)
    role = col1.text_input("Target Role")
    time_frame = col2.select_slider("Timeline", ["3 Months", "6 Months", "1 Year"])

    if st.button("🚀 Generate Blueprint"):
        if role:
            st.subheader("📊 Market Trends")
            st.line_chart(pd.DataFrame(np.random.randint(50, 150, size=(6, 1)), columns=["Salary"]))
            with st.spinner("Architecting..."):
                st.markdown(get_gemini_response(f"Create a {time_frame} roadmap for {role}."))
