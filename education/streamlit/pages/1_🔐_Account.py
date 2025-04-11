import streamlit as st
import requests
import firebase_admin
from firebase_admin import credentials, auth, firestore

FIREBASE_WEB_API_KEY = "AIzaSyAvfi66aMC7KvM3DX9fW74G706CDaUZRWk"

# 🔐 Initialize Firebase Admin
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_config/serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def app():
    st.set_page_config(page_title="Account", page_icon="🔐", layout="centered")
    st.title("🌐 Welcome to Learnova 🧠")
    st.markdown("Your smart assistant for learning insights and student performance.")

    st.divider()

    # ✅ Already logged in
    if "user" in st.session_state:
        user_doc = db.collection("users").document(st.session_state["user"]).get()
        if user_doc.exists:
            user_info = user_doc.to_dict()
            username = user_info.get("username")
            email = user_info.get("email")

            col1, col2 = st.columns([1, 3])
            with col1:
                avatar_url = f"https://ui-avatars.com/api/?name={username}&background=0D8ABC&color=fff&bold=true&size=256"
                st.image(avatar_url, width=120, caption="Your Avatar")
            with col2:
                st.markdown(f"### 👋 Welcome, **{username}**")
                st.markdown(f"📧 **Email:** {email}")
                st.success("You're successfully logged into **Learnova**!")

            st.divider()
            if st.button("🚪 Sign out"):
                del st.session_state["user"]
                st.success("You have been signed out.")
                st.rerun()
        return

    # --- Login or Signup ---
    st.subheader("🔐 Account Access")
    choice = st.radio("Choose an option:", ["Login", "Sign Up"], horizontal=True)
    st.markdown("")

    if choice == "Sign Up":
        email = st.text_input("📧 Email Address")
        password = st.text_input("🔑 Password", type="password")
        username = st.text_input("👤 Unique Username")

        if st.button("Create Account"):
            try:
                user = auth.create_user(email=email, password=password, uid=username)
                db.collection("users").document(username).set({
                    "email": email,
                    "username": username
                })
                st.session_state["user"] = username
                st.success("🎉 Account created and logged in successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ {e}")

    elif choice == "Login":
        email = st.text_input("📧 Email")
        password = st.text_input("🔑 Password", type="password")

        if st.button("Login"):
            try:
                url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"
                payload = {"email": email, "password": password, "returnSecureToken": True}
                res = requests.post(url, json=payload).json()

                if "error" in res:
                    st.error(f"❌ {res['error']['message']}")
                else:
                    local_id = res["localId"]
                    user_doc = db.collection("users").document(local_id).get()
                    if user_doc.exists:
                        st.session_state["user"] = local_id
                        st.success("✅ Login successful!")
                        st.rerun()
                    else:
                        st.error("❌ User not found in Firestore.")
            except Exception as e:
                st.error(f"❌ {e}")

        # Forgot password
        if st.button("Forgot Password?"):
            if email:
                try:
                    reset_url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={FIREBASE_WEB_API_KEY}"
                    reset_payload = {"requestType": "PASSWORD_RESET", "email": email}
                    reset_res = requests.post(reset_url, json=reset_payload).json()
                    if "error" in reset_res:
                        st.error(f"❌ {reset_res['error']['message']}")
                    else:
                        st.success("📩 Password reset email sent. Check your inbox.")
                except Exception as e:
                    st.error(f"❌ {e}")
            else:
                st.warning("⚠️ Please enter your email first.")

# Run the app
if __name__ == "__main__" or True:
    app()
