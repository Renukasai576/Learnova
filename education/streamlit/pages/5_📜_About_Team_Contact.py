import streamlit as st
from firebase_admin import firestore
from datetime import datetime

# Require login manually
if "user" not in st.session_state:
    st.warning("🔐 You must be logged in to access this page.")
    if st.button("Go to Login / Sign Up"):
        st.switch_page("pages/1_🔐_Account.py")
    st.stop()

# Firestore client (reuse if initialized)
db = firestore.client()

st.set_page_config(page_title="🤝 About Us", page_icon="🤝", layout="wide")
st.title("🤝 About Us")

st.markdown("""
### 👥 Team Hackos  
We are a passionate team of students and developers working to create data-driven solutions for real-world problems in the education sector.

This app is part of our academic project focused on **predicting student improvement** using **machine learning**.  
It aims to assist educators, institutions, and policymakers by providing insights from educational data to help drive better outcomes.
""")

st.divider()
st.subheader("📬 Contact Us")

st.markdown("""
We’d love to hear from you — whether it's feedback, questions, or collaboration ideas!
""")

# Contact Form UI
with st.form("contact_form", clear_on_submit=True):
    name = st.text_input("👤 Your Name")
    email = st.text_input("📧 Your Email")
    message = st.text_area("💬 Your Message", height=150)
    send = st.form_submit_button("📩 Send Message")

    if send:
        if name and email and message:
            try:
                db.collection("contact_messages").add({
                    "name": name,
                    "email": email,
                    "message": message,
                    "from_user": st.session_state["user"],
                    "timestamp": datetime.utcnow()
                })
                st.success("✅ Your message has been submitted successfully!")
            except Exception as e:
                st.error(f"❌ Failed to send message: {e}")
        else:
            st.warning("⚠️ Please fill out all fields before submitting.")

st.divider()
st.info("🔍 This platform was built by **Team Hackos** as a research-based academic project to improve education using ML.")
