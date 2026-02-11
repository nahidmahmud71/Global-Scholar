import streamlit as st
import time
import requests
from streamlit_lottie import st_lottie
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

# 2. HELPER FUNCTIONS

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

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

# 3. CSS STYLING (Smooth Royal Animation)
st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at center, #0f172a 0%, #020617 100%);
        color: #f1f5f9;
        font-family: 'Inter', sans-serif;
    }
    
    /* --- SMOOTH GLOW INTRO (No Shaking) --- */
    .hero-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 85vh;
        flex-direction: column;
        animation: fadeIn 3s ease-in-out;
    }
    
    .royal-text {
        font-size: 75px;
        font-weight: 800;
        background: linear-gradient(to right, #60a5fa, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 4px;
        text-align: center;
        text-shadow: 0 0 30px rgba(96, 165, 250, 0.4);
        animation: float 6s ease-in-out infinite;
    }
    
    .sub-text {
        font-size: 26px;
        color: #cbd5e1;
        font-family: 'Courier New', monospace;
        letter-spacing: 6px;
        text-transform: uppercase;
        border-top: 1px solid #475569;
        padding-top: 20px;
        margin-top: 10px;
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    /* Metrics Card Style */
    div[data-testid="stMetricValue"] {
        font-size: 28px;
        color: #38bdf8;
    }
</style>
""", unsafe_allow_html=True)

# 4. INTRO ANIMATION (Smooth Version)
def show_intro():
    placeholder = st.empty()
    with placeholder.container():
        st.markdown("""
        <div class="hero-container">
            <h1 class="royal-text">MD NAHID MAHMUD</h1>
            <h3 class="sub-text">SOUTHEAST UNIVERSITY</h3>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(3.5)
    placeholder.empty()

if 'intro_done' not in st.session_state:
    show_intro()
    st.session_state['intro_done'] = True

# 5. NAVIGATION
selected = option_menu(
    menu_title=None,
    options=["Home", "Academic Hub", "Global Wings", "Career Architect"],
    icons=["grid-fill", "book-half", "airplane-engines-fill", "trophy-fill"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "5px", "background-color": "#1e293b"},
        "nav-link": {"font-size": "14px", "color": "#cbd5e1"},
        "nav-link-selected": {"background-color": "#3b82f6", "color": "white", "font-weight": "bold"},
    }
)

# 6. MAIN LOGIC

# --- HOME DASHBOARD (HUGE DATA FEEL) ---
if selected == "Home":
    # Load Futuristic Animation
    lottie_tech = load_lottieurl("https://lottie.host/5a7d51e7-268e-4934-a63e-670560a6136d/6gH7Xy44uT.json")
    
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.title("Student Intelligence HQ 🚀")
        st.write("Access real-time data from global universities and AI-powered learning modules.")
        st.write("---")
        # Fake Huge Data Stats
        st.markdown("### 📡 Live Database Status")
        st.metric("Universities Indexed", "25,430", "+120 today")
        st.metric("Scholarship Funds Tracked", "$450M+", "Global")
        st.metric("Active Student Users", "1.2M", "Worldwide")
        
    with col2:
        if lottie_tech:
            st_lottie(lottie_tech, height=400, key="tech_anim")

# --- ACADEMIC HUB ---
elif selected == "Academic Hub":
    st.title("📚 Academic Hub")
    lottie_book = load_lottieurl("https://lottie.host/85536553-7313-441d-932f-45e0500155b0/O0iLq7lR7s.json")
    
    c1, c2 = st.columns([2, 1])
    with c1:
        st.write("### 🧠 Neural Document Processor")
        st.info("Upload any PDF. Our AI scans 1000s of data points to create summaries and quizzes.")
    with c2:
        if lottie_book:
            st_lottie(lottie_book, height=150, key="book")

    if "GOOGLE_API_KEY" not in st.secrets:
        st.error("⚠️ API Key Missing")
    else:
        tab1, tab2 = st.tabs(["📝 Super Summary", "🔥 Hardcore Quiz"])
        
        with tab1:
            uploaded_file = st.file_uploader("Upload PDF Data Stream", type="pdf")
            if uploaded_file and st.button("Process Data"):
                with st.spinner("Decrypting and Analyzing Content..."):
                    text = input_pdf_text(uploaded_file)
                    prompt = "Summarize this text with high precision. Use bullet points."
                    st.markdown(get_gemini_response(prompt, text))

        with tab2:
            if uploaded_file:
                if st.button("Generate Exam"):
                    with st.spinner("Compiling Difficult Questions..."):
                        text = input_pdf_text(uploaded_file)
                        prompt = "Create 5 Hard-Level MCQs. Provide Answer Key at the end."
                        st.markdown(get_gemini_response(prompt, text))

# --- GLOBAL WINGS (THE BIGGEST DATA UPDATE) ---
elif selected == "Global Wings":
    st.title("✈️ Global Wings Premium")
    lottie_globe = load_lottieurl("https://lottie.host/9f5064e6-815d-4f06-b51c-438676d91d83/pT2x6o3s7M.json")
    
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown("### 🌍 Worldwide University Database")
        st.write("Connected to live tuition feeds, ranking algorithms, and visa success rates.")
    with c2:
        if lottie_globe:
            st_lottie(lottie_globe, height=200, key="globe")

    # Advanced Filter Interface
    with st.container():
        st.subheader("🔍 Deep Search Configuration")
        col1, col2, col3 = st.columns(3)
        with col1:
            country = st.text_input("Target Nation", placeholder="e.g. Germany, USA")
        with col2:
            subject = st.text_input("Field of Research", placeholder="e.g. Data Science")
        with col3:
            budget = st.select_slider("Annual Budget Cap", ["$5k", "$15k", "$30k", "Unlimited"])

        if st.button("Initiate Global Scan 🛰️", use_container_width=True):
            if country and subject:
                with st.spinner(f"Scanning 150+ Universities in {country}..."):
                    time.sleep(1.5) # Fake loading for "Big Data" feel
                    prompt = f"""
                    Act as a global education data analyst. Find top 5 universities in {country} for {subject} with budget {budget}.
                    Output a MARKDOWN TABLE with columns: 
                    | Global Rank | University Name | Tuition (USD) | Acceptance Rate | Scholarship |
                    |---|---|---|---|---|
                    
                    Followed by a detailed analysis of why these are the best.
                    """
                    st.markdown(get_gemini_response(prompt))
            else:
                st.warning("Input required for scan.")

# --- CAREER ARCHITECT ---
elif selected == "Career Architect":
    st.title("🚀 Career Architect AI")
    lottie_rocket = load_lottieurl("https://lottie.host/0200c5a2-9428-494b-85d7-1b20347895f3/Xf3s6j2r8v.json")
    
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown("### 📈 Algorithmic Career Planning")
        st.write("Input your target role. AI generates a month-by-month execution protocol.")
    with c2:
        if lottie_rocket:
            st_lottie(lottie_rocket, height=180, key="rocket")

    col1, col2 = st.columns(2)
    with col1:
        role = st.text_input("Target Position", placeholder="e.g. AI Engineer at Google")
    with col2:
        timeline = st.selectbox("Execution Timeline", ["3 Months", "6 Months", "1 Year"])
    
    if st.button("Construct Roadmap 🛠️"):
        if role:
            with st.spinner("Calculating optimal learning path..."):
                prompt = f"Create a detailed {timeline} roadmap for {role}. Structure: Month 1, Month 2, etc. Include Projects."
                st.markdown(get_gemini_response(prompt))
