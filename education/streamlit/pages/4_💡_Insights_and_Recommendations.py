import streamlit as st

# Require login manually
if "user" not in st.session_state:
    st.warning("🔐 You must be logged in to access this page.")
    if st.button("Go to Login / Sign Up"):
        st.switch_page("pages/1_🔐_Account.py")
    st.stop()  # Stops rendering further until login is done

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Page configuration
st.set_page_config(page_title="📌 Insights & Recommendations", page_icon="📌", layout="wide")

st.title("📌 Insights & Recommendations")

st.markdown("""
Welcome! This section helps you **understand what factors are driving student improvement** and offers **practical suggestions** based on the model's learning.

---

### What You'll Find Here:
- 🎯 Which features are most important?
- 📊 A pie chart showing feature impact visually
- ✅ Easy-to-follow recommendations
- 📉 A heatmap to explore relationships between features

---
""")

# Fallback path
fallback_path = r"C:\Users\chava\Downloads\Enhanced_Education_Dataset (1).csv"

@st.cache_data
def load_data():
    if os.path.exists(fallback_path):
        df = pd.read_csv(fallback_path)
        df = df.select_dtypes(include=np.number)
        df = df.dropna()
        return df
    return None

df = load_data()

if df is not None and "Improvement_Percentage" in df.columns:
    X = df.drop(columns=["Improvement_Percentage"])
    y = df["Improvement_Percentage"]

    from sklearn.ensemble import RandomForestRegressor
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)

    # 🎯 Feature Importance
    st.subheader("🎯 Feature Importance: What Matters Most?")
    st.markdown("The model learned which features (columns) most affect the **Improvement_Percentage** of students. The bigger the slice, the more important the feature is.")

    feature_importance = model.feature_importances_
    feature_imp_df = pd.DataFrame({"Feature": X.columns, "Importance": feature_importance})
    feature_imp_df = feature_imp_df.sort_values(by="Importance", ascending=False)

    # Pie chart
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(feature_imp_df["Importance"], labels=feature_imp_df["Feature"],
           autopct='%1.1f%%', startangle=90, colors=sns.color_palette("Set3", len(feature_imp_df)))
    ax.axis('equal')
    st.pyplot(fig)

    # ✅ Friendly Recommendations
    st.subheader("✅ Simple Recommendations")
    st.markdown("Here’s where you should **focus your improvement efforts**:")

    for idx, row in feature_imp_df.iterrows():
        importance = row["Importance"]
        feature = row["Feature"]

        if importance > 0.1:
            st.success(f"🔹 **{feature}**: Crucial area! Focus here for big impact on student improvement.")
        elif importance > 0.05:
            st.info(f"🔸 **{feature}**: Useful area. Improving this will moderately help outcomes.")
        else:
            st.warning(f"🔻 **{feature}**: Low impact. You may not need to prioritize this, but keep it in check.")

    # 📉 Correlation Matrix
    st.subheader("📉 Correlation Matrix: How Features Relate")
    st.markdown("This chart shows how features relate to each other. It helps you see which ones grow or shrink together.")

    corr = df.corr()
    fig_corr, ax_corr = plt.subplots(figsize=(10, 6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax_corr)
    st.pyplot(fig_corr)

    st.markdown("_🧠 Tip: Focus on features strongly correlated with 'Improvement_Percentage' or other major factors._")

else:
    st.error("⚠️ Could not load the dataset or it does not contain 'Improvement_Percentage'.")
