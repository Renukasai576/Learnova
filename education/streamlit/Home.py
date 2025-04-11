import streamlit as st
import json
from streamlit_lottie import st_lottie
import requests

# Page configuration
st.set_page_config(page_title="Education Effectiveness Analysis", page_icon="📊", layout="wide")

# 🔄 Load Lottie animation
@st.cache_data
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

lottie_learning = load_lottiefile("assets/strawberry.json")

# Title
st.title("📊 Education Effectiveness Analysis")

# Login status display
if "user" in st.session_state:
    st.success(f"✅ Logged in as: {st.session_state['user']}")
else:
    st.info("🔐 Want to sign in or create an account? Go to the **Account** tab in the sidebar.")

# UI layout
col1, col2 = st.columns([1, 2])

with col1:
    if lottie_learning:
        st_lottie(lottie_learning, speed=1, loop=True, quality="high", height=300)
    else:
        st.warning("⚠️ Animation failed to load.")

with col2:
    st.subheader("Welcome to a Smart Prediction Platform for Student Improvement")
    st.markdown("""
    This platform helps you explore and predict student performance using learning data.

    **What you can do:**
    - 📁 Upload & explore your dataset  
    - 📊 Train and evaluate models  
    - 🧠 Predict new student outcomes  
    - 💡 Get insights and recommendations  
    """)

# Image display
st.image(
    "https://plus.unsplash.com/premium_photo-1683147742318-6c46879145fc?w=600&auto=format&fit=crop&q=60",
    use_container_width=True,
    caption="Educational Awareness for a Brighter Tomorrow"
)

# Call to action
st.markdown("### 🔍 Ready to explore?")
if st.button("🚀 Explore Now"):
    st.switch_page("pages/2_📁_Upload_and_Explore_Data.py")

st.markdown("---")
st.markdown("Made with ❤️ using Streamlit | Developed by *Hackos*")
