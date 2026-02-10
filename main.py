import streamlit as st
import time
from streamlit_option_menu import option_menu
import google.generativeai as genai
import PyPDF2 as pdf

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

def get_gemini_response(input_prompt, pdf_content):
    # API Key অটোমেটিক সিক্রেটস থেকে নেবে
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content([input_prompt, pdf_content])
        return response.text
    except Exception as e:
        return "⚠️ Error: API Key পাওয়া যায়নি। দয়া করে Streamlit Settings-এ Key টি যুক্ত করুন।"

# 3. CSS DESIGN (Ultra Modern)
st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at center, #1b2735 0%, #090a0f 100%);
        color: white;
    }
    .hero-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 80vh;
        flex-direction: column;
        animation: fadeIn 2.5s ease-in;
    }
    .neon-text {
        font-size: 70px;
        font-weight: 900;
        color: #fff;
        text-transform: uppercase;
        text-align: center;
        text-shadow: 0 0 20px #00C9FF;
        animation: glow 2s infinite alternate;
    }
    .sub-text {
        font-size: 30px;
        color: #b0c4de;
        margin-top: 10px;
        font-family: 'Courier New', monospace;
        font-weight: bold;
        text-align: center;
    }
    @keyframes glow {
        from { text-shadow: 0 0 10px #00C9FF; }
        to { text-shadow: 0 0 30px #92FE9D; }
    }
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
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
    icons=["house", "journal-code", "airplane-engines", "diagram-3"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "5px", "background-color": "#161b22"},
        "nav-link": {"font-size": "14px", "color": "#ddd"},
        "nav-link-selected": {"background-color": "#00C9FF", "color": "black", "font-weight": "bold"},
    }
)

# 6. MAIN APP LOGIC

if selected == "Home":
    st.markdown("<h1 style='text-align: center; color: #00C9FF;'>Global Scholar AI 2.0 🎓</h1>", unsafe_allow_html=True)
    st.write("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("📚 **Academic Hub**")
        st.caption("পিডিএফ আপলোড করুন, AI আপনাকে সামারি এবং কুইজ বানিয়ে দেবে।")
    with col2:
        st.success("✈️ **Global Wings**")
        st.caption("বিশ্বের যেকোনো ভার্সিটি খুঁজুন এবং বাজেট প্ল্যান করুন।")
    with col3:
        st.warning("🚀 **Career Architect**")
        st.caption("ফিউচার ক্যারিয়ারের জন্য কমপ্লিট রোডম্যাপ।")

elif selected == "Academic Hub":
    st.title("📚 Academic Hub")
    
    # Check if API Key exists in secrets
    if "GOOGLE_API_KEY" not in st.secrets:
        st.error("⚠️ API Key সেট করা হয়নি। Streamlit Cloud Settings এ গিয়ে 'Secrets' এ Key টি বসান।")
    else:
        tab1, tab2 = st.tabs(["📄 Summarizer", "🧠 Quiz Master"])
        
        with tab1:
            uploaded_file = st.file_uploader("নোটস বা বই আপলোড করুন (PDF)", type="pdf")
            if uploaded_file and st.button("Analyze PDF"):
                with st.spinner("AI ফাইলটি পড়ছে..."):
                    text = input_pdf_text(uploaded_file)
                    prompt = "Summarize this text in simple points:"
                    st.write(get_gemini_response(prompt, text))
                    
        with tab2:
            if uploaded_file:
                if st.button("Generate Quiz"):
                    with st.spinner("প্রশ্ন তৈরি হচ্ছে..."):
                        text = input_pdf_text(uploaded_file)
                        prompt = "Create 3 MCQs with answers based on this text."
                        st.write(get_gemini_response(prompt, text))
            else:
                st.warning("আগে একটি পিডিএফ আপলোড করুন।")

elif selected == "Global Wings":
    st.title("✈️ Global Wings")
    st.info("Features coming soon...")

elif selected == "Career Architect":
    st.title("🚀 Career Architect")
    st.info("Features coming soon...")
