import streamlit as st
import time
from streamlit_option_menu import option_menu
import json

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="Global Scholar AI 2.0",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. ULTRA MODERN CSS & ANIMATIONS
st.markdown("""
<style>
    /* Dark Theme Background */
    .stApp {
        background: radial-gradient(circle at center, #1b2735 0%, #090a0f 100%);
        color: white;
    }
    
    /* --- CINEMATIC INTRO ANIMATION --- */
    .hero-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 70vh;
        flex-direction: column;
    }
    
    .neon-text {
        font-size: 80px;
        font-weight: 900;
        color: #fff;
        text-transform: uppercase;
        animation: flicker 1.5s infinite alternate;
        text-shadow: 
            0 0 7px #fff,
            0 0 10px #fff,
            0 0 21px #fff,
            0 0 42px #0fa,
            0 0 82px #0fa,
            0 0 92px #0fa,
            0 0 102px #0fa,
            0 0 151px #0fa;
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

    /* --- TAB DESIGN --- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: #0e1117;
        padding: 10px;
        border-radius: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: transparent;
        border-radius: 5px;
        color: white;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        background-color: #00C9FF;
        color: black;
    }
    
</style>
""", unsafe_allow_html=True)

# 3. INTRO ANIMATION FUNCTION (Only once per session)
def show_intro():
    placeholder = st.empty()
    with placeholder.container():
        st.markdown('<div class="hero-container"><h1 class="neon-text">FUTURE WORLD</h1></div>', unsafe_allow_html=True)
        time.sleep(2.5) # অ্যানিমেশন ডিউরেশন
        
    placeholder.empty()

if 'intro_done' not in st.session_state:
    show_intro()
    st.session_state['intro_done'] = True

# 4. NAVIGATION MENU (Updated & Merged)
selected = option_menu(
    menu_title=None,
    options=["Home", "Academic Hub", "Global Wings", "Career Architect"],
    icons=["house", "journal-code", "airplane-engines", "diagram-3"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "5px", "background-color": "#161b22"},
        "nav-link": {"font-size": "14px", "text-align": "center", "margin": "0px", "color": "#ddd"},
        "nav-link-selected": {"background-color": "#00C9FF", "color": "black", "font-weight": "bold"},
    }
)

# 5. MAIN LOGIC

# --- HOME ---
if selected == "Home":
    st.markdown("<h1 style='text-align: center; color: #00C9FF;'>Welcome to Global Scholar AI 2.0 🎓</h1>", unsafe_allow_html=True)
    st.write("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("📚 **Academic Hub**")
        st.caption("আপনার পার্সোনাল টিউটর। নোটস আপলোড করুন, কুইজ দিন।")
    with col2:
        st.success("✈️ **Global Wings**")
        st.caption("বিদেশ যাত্রা ও বাজেট প্ল্যানিং এখন এক ছাতার নিচে।")
    with col3:
        st.warning("🚀 **Career Architect**")
        st.caption("AI আপনাকে বলে দেবে আপনার ক্যারিয়ারের রোডম্যাপ।")

# --- ACADEMIC HUB (Study Buddy + Quiz Merged) ---
elif selected == "Academic Hub":
    st.title("📚 Academic Hub")
    
    tab1, tab2 = st.tabs(["📄 Study Material Analyzer", "🧠 AI Quiz Master"])
    
    with tab1:
        st.subheader("Upload PDF & Understand Instantly")
        uploaded_file = st.file_uploader("নোটস বা বই আপলোড করুন", type="pdf")
        if uploaded_file:
            st.success("AI ফাইলটি পড়ছে... (Backend Integration Pending)")
            
    with tab2:
        st.subheader("Test Your Knowledge")
        topic = st.text_input("কোন টপিকের ওপর পরীক্ষা দিতে চান?")
        if st.button("Generate Quiz"):
            st.write(f"Generating quiz for: **{topic}**...")

# --- GLOBAL WINGS (Universe Explorer + Budget Merged) ---
elif selected == "Global Wings":
    st.title("✈️ Global Wings")
    
    tab1, tab2 = st.tabs(["🌍 Universe Explorer", "💰 Smart Budget"])
    
    with tab1:
        col1, col2 = st.columns([3, 1])
        with col1:
            country = st.text_input("Destination Country", placeholder="e.g. Germany")
        with col2:
            st.write("")
            st.write("")
            st.button("Search Unis 🔍")
            
    with tab2:
        st.write("### Expense Calculator")
        tuition = st.slider("Yearly Tuition ($)", 0, 50000, 10000)
        living = st.slider("Monthly Living Cost ($)", 0, 3000, 800)
        total = tuition + (living * 12)
        st.metric("Total Yearly Cost", f"${total}")
        st.progress(min(total/60000, 1.0))

# --- CAREER ARCHITECT (New AI Feature) ---
elif selected == "Career Architect":
    st.title("🚀 Career Architect AI")
    st.write("আপনার স্বপ্নের জব রোলের জন্য কমপ্লিট গাইডলাইন নিন।")
    
    target_role = st.selectbox("আপনার লক্ষ্য কী?", ["Software Engineer", "Data Scientist", "Product Manager", "Digital Marketer"])
    current_level = st.select_slider("আপনার বর্তমান অবস্থা:", options=["Beginner", "Intermediate", "Advanced"])
    
    if st.button("Generate Roadmap 🗺️"):
        with st.spinner("AI রোডম্যাপ তৈরি করছে..."):
            time.sleep(2)
            st.subheader(f"Roadmap for {target_role} ({current_level})")
            
            # Simulated AI Response
            st.markdown(f"""
            1. **Month 1-2:** Master the basics of {target_role}.
            2. **Month 3:** Build 2 real-world projects.
            3. **Month 4:** Focus on Networking & LinkedIn optimization.
            4. **Month 5:** Apply for Internships.
            """)
            st.balloons()
