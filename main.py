import streamlit as st
import time
from streamlit_option_menu import option_menu

# 1. PAGE CONFIGURATION (Must be the first line)
st.set_page_config(
    page_title="Global Scholar AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. CUSTOM CSS (Styling & Animations)
st.markdown("""
<style>
    /* মেইন ব্যাকগ্রাউন্ড এবং টেক্সট কালার */
    .stApp {
        background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
        color: white;
    }
    
    /* ইন্ট্রো অ্যানিমেশন স্টাইল */
    .intro-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 60vh;
        flex-direction: column;
    }
    
    .intro-text {
        font-size: 70px;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #00C9FF, #92FE9D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: glow 1.5s ease-in-out infinite alternate;
        text-align: center;
    }
    
    .sub-intro {
        font-size: 25px;
        color: #ddd;
        margin-top: 10px;
        font-family: 'Courier New', Courier, monospace;
    }

    @keyframes glow {
        from { text-shadow: 0 0 10px #00C9FF, 0 0 20px #00C9FF; }
        to { text-shadow: 0 0 20px #92FE9D, 0 0 30px #92FE9D; }
    }

    /* রিমুভ ডিফল্ট এলিমেন্টস */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)

# 3. INTRO ANIMATION FUNCTION
def run_intro_animation():
    placeholder = st.empty()
    
    with placeholder.container():
        st.markdown("""
        <div class="intro-container">
            <h1 class="intro-text">Created by Future World</h1>
            <p class="sub-intro">Loading AI Modules...</p>
        </div>
        """, unsafe_allow_html=True)
        
        # প্রোগ্রেস বার
        progress_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.01) # অ্যানিমেশন স্পিড
            progress_bar.progress(percent_complete + 1)
            
        time.sleep(0.5)
        
    placeholder.empty() # অ্যানিমেশন শেষ হলে স্ক্রিন ক্লিয়ার

# সেশন স্টেট চেক (যাতে অ্যানিমেশন একবারই হয়)
if 'animation_shown' not in st.session_state:
    run_intro_animation()
    st.session_state['animation_shown'] = True

# 4. TOP NAVIGATION MENU (Horizontal)
selected = option_menu(
    menu_title=None,
    options=["Home", "Universe Explorer", "Smart Study Buddy", "Budget Planner"],
    icons=["house-fill", "globe", "book-half", "wallet2"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "transparent"},
        "icon": {"color": "#00C9FF", "font-size": "20px"}, 
        "nav-link": {
            "font-size": "16px", 
            "text-align": "center", 
            "margin": "0px 10px", 
            "color": "white",
            "font-weight": "bold"
        },
        "nav-link-selected": {"background-color": "#00C9FF", "color": "white"},
    }
)

# 5. PAGE CONTENT LOGIC

# --- HOME PAGE ---
if selected == "Home":
    st.markdown("<h1 style='text-align: center; color: white;'>Welcome to Global Scholar AI 🎓</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #a8b2d1;'>আপনার স্বপ্নের উচ্চশিক্ষার পথে বিশ্বস্ত সঙ্গী</h3>", unsafe_allow_html=True)
    
    st.divider()
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("""
        ### 🚀 কেন এই অ্যাপ?
        এই AI-Powered অ্যাপটি স্টুডেন্টদের জন্য তৈরি, যা বিদেশে উচ্চশিক্ষার প্রতিটি ধাপ সহজ করে দেয়।
        
        **ফিচারসমূহ:**
        * 🌍 **Universe Explorer:** বিশ্বের সেরা ইউনিভার্সিটিগুলো খুঁজুন।
        * 📚 **Smart Study Buddy:** কঠিন পড়া সহজে বুঝুন AI-এর সাহায্যে।
        * 💰 **Budget Planner:** টিউশন ফি এবং লিভিং কস্টের হিসাব রাখুন।
        """)
        
        if st.button("Explore Now ->"):
            st.toast("উপরের মেনু থেকে Universe Explorer সিলেক্ট করুন!")

    with col2:
        # এখানে একটি ডামি ইমেজ বা Lottie অ্যানিমেশন দেওয়া হলো
        st.image("https://cdn.dribbble.com/users/466602/screenshots/14104085/media/3c2a6d71343729938d87635c10202682.png", use_container_width=True)

# --- UNIVERSE EXPLORER ---
elif selected == "Universe Explorer":
    st.title("🌍 Universe Explorer")
    st.info("AI দিয়ে বিশ্বের যেকোনো দেশের ইউনিভার্সিটি এবং স্কলারশিপ খুঁজুন।")
    
    search_query = st.text_input("কোন দেশে পড়তে যেতে চান?", placeholder="Example: Canada, Germany, USA...")
    if search_query:
        st.write(f"🔍 **{search_query}** এর জন্য সেরা ইউনিভার্সিটিগুলো খোঁজা হচ্ছে... (Backend Logic will be added soon)")

# --- SMART STUDY BUDDY ---
elif selected == "Smart Study Buddy":
    st.title("📚 Smart Study Buddy")
    st.warning("আপনার পিডিএফ আপলোড করুন, AI আপনাকে কুইজ এবং সামারি দেবে।")
    
    uploaded_file = st.file_uploader("Upload your Study Material (PDF)", type="pdf")
    if uploaded_file is not None:
        st.success("ফাইল আপলোড হয়েছে! AI এখন এটি বিশ্লেষণ করছে...")

# --- BUDGET PLANNER ---
elif selected == "Budget Planner":
    st.title("💰 Budget Planner")
    st.write("বিদেশে পড়ার এবং থাকার খরচের রিয়েল-টাইম হিসাব।")
    
    col1, col2 = st.columns(2)
    with col1:
        tuition = st.number_input("বার্ষিক টিউশন ফি ($)", min_value=0)
    with col2:
        living = st.number_input("মাসিক থাকা-খাওয়ার খরচ ($)", min_value=0)
        
    if st.button("Total Cost Calculate"):
        total = tuition + (living * 12)
        st.metric(label="এক বছরের মোট খরচ", value=f"${total}")