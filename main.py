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
        # Fetch API Key from Streamlit Secrets
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
            return "⚠️ Error: API Key not found. Please set it in Streamlit Secrets."
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# 3. ULTRA MODERN CSS
st.markdown("""
<style>
    /* Global Background */
    .stApp {
        background: radial-gradient(circle at center, #1b2735 0%, #090a0f 100%);
        color: white;
    }
    
    /* Intro Animation Styles */
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
        margin-top: 15px;
        font-family: 'Courier New', monospace;
        letter-spacing: 2px;
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
    
    /* Custom Card Styling */
    div.stButton > button {
        background: linear-gradient(45deg, #00C9FF, #92FE9D);
        color: black;
        border: none;
        font-weight: bold;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 15px #00C9FF;
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
        "nav-link": {"font-size": "14px", "color": "#ddd", "margin": "0px 5px"},
        "nav-link-selected": {"background-color": "#00C9FF", "color": "black", "font-weight": "bold"},
    }
)

# 6. MAIN APP LOGIC

# --- HOME PAGE ---
if selected == "Home":
    st.markdown("<h1 style='text-align: center; color: #00C9FF;'>Welcome to Global Scholar AI 2.0 🎓</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #a8b2d1;'>Your Ultimate AI Companion for Higher Education & Career Growth</h4>", unsafe_allow_html=True)
    st.write("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("📚 **Academic Hub**")
        st.caption("Upload study materials (PDF), get instant summaries, and generate AI-powered quizzes.")
    with col2:
        st.success("✈️ **Global Wings**")
        st.caption("Find top universities worldwide, check scholarships, and calculate your budget.")
    with col3:
        st.warning("🚀 **Career Architect**")
        st.caption("Get a personalized learning roadmap to land your dream job at top tech giants.")

# --- ACADEMIC HUB ---
elif selected == "Academic Hub":
    st.title("📚 Academic Hub")
    
    if "GOOGLE_API_KEY" not in st.secrets:
        st.error("⚠️ API Key missing. Please add it to Streamlit Secrets.")
    else:
        tab1, tab2 = st.tabs(["📄 Smart Summarizer", "🧠 AI Quiz Master"])
        
        # Summarizer Tab
        with tab1:
            st.subheader("Analyze & Summarize Documents")
            uploaded_file = st.file_uploader("Upload your lecture notes or book (PDF)", type="pdf")
            if uploaded_file and st.button("Analyze PDF"):
                with st.spinner("AI is analyzing your document..."):
                    text = input_pdf_text(uploaded_file)
                    prompt = "You are an expert tutor. Summarize the key concepts of this text in clear bullet points. Explain complex terms simply."
                    st.write(get_gemini_response(prompt, text))
                    
        # Quiz Tab
        with tab2:
            st.subheader("Test Your Knowledge")
            if uploaded_file:
                if st.button("Generate Quiz"):
                    with st.spinner("Creating questions..."):
                        text = input_pdf_text(uploaded_file)
                        prompt = "Create 5 multiple-choice questions (MCQs) based on this text. Provide the correct answers at the end."
                        st.markdown(get_gemini_response(prompt, text))
            else:
                st.warning("Please upload a PDF in the 'Smart Summarizer' tab first.")

# --- GLOBAL WINGS ---
elif selected == "Global Wings":
    st.title("✈️ Global Wings")
    st.markdown("### Your AI Study Abroad Consultant")

    tab1, tab2 = st.tabs(["🌍 University Finder", "💰 Budget Calculator"])
    
    with tab1:
        col1, col2 = st.columns([3, 1])
        with col1:
            country = st.text_input("Destination Country", placeholder="e.g. Canada, Germany, USA, Australia")
            subject = st.text_input("Field of Study", placeholder="e.g. Computer Science, Data Science, MBA")
        with col2:
            st.write("") # Spacing
            st.write("")
            search_btn = st.button("Find Universities 🔍")
            
        if search_btn and country and subject:
            with st.spinner(f"Searching for top universities in {country} for {subject}..."):
                prompt = f"""
                Act as a senior study abroad consultant. Suggest the top 5 universities in {country} for {subject}.
                Output the data in a clean Markdown Table with these columns:
                | University Name | Approx. Tuition Fee (Yearly) | Acceptance Rate | Why it's good |
                """
                response = get_gemini_response(prompt)
                st.markdown(response)

    with tab2:
        st.write("### Expense Estimator")
        tuition = st.slider("Yearly Tuition Fee ($)", 0, 60000, 15000)
        living = st.slider("Monthly Living Cost ($)", 0, 4000, 1200)
        flight = st.number_input("One-time Flight & Visa Cost ($)", value=1500)
        
        if st.button("Calculate Total Cost"):
            yearly_living = living * 12
            total_first_year = tuition + yearly_living + flight
            
            st.success(f"Estimated Total Cost for 1st Year: **${total_first_year:,.2f}**")
            
            # Data Visualization
            data = {
                "Category": ["Tuition Fee", "Living Expenses (1 Year)", "Flight & Visa"],
                "Cost ($)": [tuition, yearly_living, flight]
            }
            df = pd.DataFrame(data)
            st.bar_chart(df.set_index("Category"))

# --- CAREER ARCHITECT ---
elif selected == "Career Architect":
    st.title("🚀 Career Architect AI")
    st.markdown("### Build Your Path to Success")
    
    col1, col2 = st.columns(2)
    with col1:
        target_role = st.text_input("Dream Job Role", placeholder="e.g. Google Software Engineer, AI Researcher")
    with col2:
        current_status = st.selectbox("Current Status", ["Freshman (1st Year)", "Sophomore (2nd Year)", "Junior (3rd Year)", "Senior (4th Year)", "Fresh Graduate"])
    
    if st.button("Generate Roadmap 🗺️"):
        if target_role:
            with st.spinner("AI is architecting your career path..."):
                prompt = f"""
                Create a detailed, month-by-month learning roadmap for a {current_status} student who wants to become a {target_role}.
                Format it clearly with bold headings for each month.
                Include:
                1. Technical Skills to Master
                2. Project Ideas (Beginner to Advanced)
                3. Soft Skills & Networking Tips
                4. Certification Recommendations
                """
                response = get_gemini_response(prompt)
                st.markdown(response)
        else:
            st.warning("Please enter your dream job role.")
