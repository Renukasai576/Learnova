import streamlit as st

# Require login manually
if "user" not in st.session_state:
    st.warning("🔐 You must be logged in to access this page.")
    if st.button("Go to Login / Sign Up"):
        st.switch_page("pages/1_🔐_Account.py")
    st.stop()  # Stops rendering further until login is done

import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import io
import os

# Page configuration
st.set_page_config(page_title="Upload & Explore Data", page_icon="📁", layout="wide")

st.title("📁 Upload and Explore Your Dataset")
st.markdown("""
This section allows you to upload your CSV dataset and get a detailed overview.
Ideal for beginners to understand and visualize their data.
""")

# Upload file
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"], help="Upload a .csv file from your computer.")

# Define fallback path
fallback_path = "C:/Users/chava/Downloads/Enhanced_Education_Dataset (1).csv"

# Load and display dataset
def load_data(file):
    try:
        df = pd.read_csv(file)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

if uploaded_file is not None:
    df = load_data(uploaded_file)
    st.success("File successfully uploaded and data loaded!")
elif os.path.exists(fallback_path):
    df = load_data(fallback_path)
    st.info(f"Using fallback file: {fallback_path}")
else:
    df = None
    st.warning("Please upload a CSV file to proceed.")

if df is not None:
    st.subheader("🔍 Data Preview")
    st.dataframe(df.head(), use_container_width=True)

    st.subheader("📊 Data Summary")
    st.write(df.describe())

    st.subheader("🧩 Column Types")
    st.write(df.dtypes)

    st.subheader("❓ Missing Values")
    st.write(df.isnull().sum())

    st.subheader("📌 Duplicate Rows")
    st.write(df.duplicated().sum())

    st.subheader("📌 Constant Columns")
    constant_cols = [col for col in df.columns if df[col].nunique() == 1]
    st.write(constant_cols if constant_cols else "No constant columns found.")

    # Download option
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Processed Data", data=csv, file_name="processed_data.csv", mime='text/csv')

    # Data visualizations
    st.subheader("📈 Data Visualizations")

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    if numeric_cols:
        selected_col = st.selectbox("Select a column for histogram", numeric_cols)
        fig, ax = plt.subplots()
        sns.histplot(df[selected_col], kde=True, ax=ax)
        ax.set_title(f"Distribution of {selected_col}")
        st.pyplot(fig)
        st.markdown("_Histogram: Shows how the data for this column is distributed. Useful to spot skewness, outliers, or normal distribution._")

        selected_x = st.selectbox("X-axis for scatter plot", numeric_cols)
        selected_y = st.selectbox("Y-axis for scatter plot", numeric_cols, index=1 if len(numeric_cols) > 1 else 0)
        fig2, ax2 = plt.subplots()
        sns.scatterplot(data=df, x=selected_x, y=selected_y, ax=ax2)
        ax2.set_title(f"{selected_y} vs {selected_x}")
        st.pyplot(fig2)
        st.markdown("_Scatter Plot: Helps identify correlation or pattern between two numeric variables._")

        st.subheader("📦 Box Plot")
        selected_box_col = st.selectbox("Select column for box plot", numeric_cols)
        fig3, ax3 = plt.subplots()
        sns.boxplot(data=df[selected_box_col], ax=ax3)
        ax3.set_title(f"Box Plot of {selected_box_col}")
        st.pyplot(fig3)
        st.markdown("_Box Plot: Visualizes the spread of data, median, and outliers._")

        st.subheader("🔥 Correlation Heatmap")
        fig4, ax4 = plt.subplots(figsize=(10, 6))
        sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm', ax=ax4)
        ax4.set_title("Correlation Matrix")
        st.pyplot(fig4)
        st.markdown("_Heatmap: Shows relationships between numeric columns. Values close to 1 or -1 mean strong correlation._")

    else:
        st.info("No numeric columns found for visualization.")
