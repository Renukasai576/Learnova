
import streamlit as st
# Require login manually
if "user" not in st.session_state:
    st.warning("🔐 You must be logged in to access this page.")
    if st.button("Go to Login / Sign Up"):
        st.switch_page("pages/1_🔐_Account.py")
    st.stop()  # Stops rendering further until login is done



import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Page configuration
st.set_page_config(page_title="📈 Predict New Data", page_icon="📈", layout="wide")

st.title("📈 Predict Improvement Percentages for Education Data")
st.markdown("""
This tool predicts how much students might improve based on their features.

---

### 📘 How to Use:
1. Upload a new CSV file (excluding the `Improvement_Percentage` column).
2. If not uploaded, a default fallback file will be used (if available).
3. Predictions will be shown below with visuals and option to download.

---
""")

# Paths (raw string to handle Windows slashes)
fallback_training_path = r"C:\Users\chava\Downloads\Enhanced_Education_Dataset (1).csv"
fallback_new_data_path = r"C:\Users\chava\Downloads\New_Education_Data.csv"

@st.cache_data
def load_training_data():
    if os.path.exists(fallback_training_path):
        df = pd.read_csv(fallback_training_path)
        df = df.select_dtypes(include=np.number)
        return df
    return None

training_df = load_training_data()

if training_df is None or "Improvement_Percentage" not in training_df.columns:
    st.error("❌ Could not find training data or it lacks the 'Improvement_Percentage' column.")
    st.stop()

# Prepare model
X = training_df.drop(columns=["Improvement_Percentage"])
y = training_df["Improvement_Percentage"]

X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Upload new data
st.subheader("📤 Upload New Data")
new_data_file = st.file_uploader("Upload your new dataset (CSV)", type=["csv"])

# Load new data
if new_data_file:
    new_data = pd.read_csv(new_data_file)
    st.success("✅ New data uploaded successfully!")
elif os.path.exists(fallback_new_data_path):
    new_data = pd.read_csv(fallback_new_data_path)
    st.info(f"ℹ️ Using fallback file: {fallback_new_data_path}")
else:
    new_data = None
    st.warning("⚠️ Please upload a new dataset or check fallback file location.")

if new_data is not None:
    st.subheader("👀 Preview of Uploaded Data")
    st.dataframe(new_data.head(), use_container_width=True)

    new_data_numeric = new_data.select_dtypes(include=np.number)
    new_data_numeric = new_data_numeric.replace([np.inf, -np.inf], np.nan).fillna(new_data_numeric.mean())

    missing_cols = set(X.columns) - set(new_data_numeric.columns)
    if missing_cols:
        st.error(f"❌ Missing columns in new data: {', '.join(missing_cols)}")
    else:
        try:
            new_data_scaled = scaler.transform(new_data_numeric[X.columns])
            predictions = model.predict(new_data_scaled)

            new_data["Predicted_Improvement"] = np.round(predictions, 2)

            st.subheader("📊 Prediction Results")
            st.dataframe(new_data.style.highlight_max(axis=0, subset=["Predicted_Improvement"]), use_container_width=True)

            # Visual 1: Histogram of Predictions
            st.markdown("### 📉 Prediction Distribution (Histogram)")
            fig1, ax1 = plt.subplots()
            sns.histplot(new_data["Predicted_Improvement"], kde=True, ax=ax1, color="skyblue")
            ax1.set_title("Distribution of Predicted Improvement")
            ax1.set_xlabel("Improvement Percentage")
            ax1.set_ylabel("Number of Students")
            st.pyplot(fig1)
            st.markdown("_This chart shows how most students are expected to improve — check for peaks and spread._")

            # Visual 2: Top 10 Predictions
            st.markdown("### 🏆 Top 10 Students with Highest Predicted Improvement")
            top10 = new_data.nlargest(10, "Predicted_Improvement")
            fig2, ax2 = plt.subplots()
            sns.barplot(data=top10, x="Predicted_Improvement", y=top10.index, ax=ax2, palette="viridis")
            ax2.set_xlabel("Predicted Improvement")
            ax2.set_ylabel("Student Index")
            st.pyplot(fig2)
            st.markdown("_This bar chart highlights the top 10 students who are expected to improve the most._")

            # Download button
            csv = new_data.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Predicted Data", data=csv, file_name="predicted_improvement.csv", mime="text/csv")

        except Exception as e:
            st.error(f"🚨 Prediction error: {e}")
