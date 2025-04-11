import streamlit as st

def require_login():
    if "user" not in st.session_state:
        st.warning("🔒 You must be logged in to access this page.")
        st.info("👉 Please go to the **Account** page to log in.")
        st.stop()
