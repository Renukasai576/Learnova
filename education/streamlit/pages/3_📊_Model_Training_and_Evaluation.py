import streamlit as st

# Require login manually
if "user" not in st.session_state:
    st.warning("🔐 You must be logged in to access this page.")
    if st.button("Go to Login / Sign Up"):
        st.switch_page("pages/1_🔐_Account.py")
    st.stop()  # Stops rendering further until login is done

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Page config
st.set_page_config(page_title="Model Training & Evaluation", page_icon="📊", layout="wide")

st.title("📊 Train and Evaluate Models")

with st.expander("ℹ️ What happens here?"):
    st.markdown("""
    This section allows you to train and evaluate simple machine learning models on your dataset.
    
    - We clean and prepare your data.
    - We split it into training and testing parts.
    - We scale the values to make models work better.
    - You can pick a model to train and see how well it performs!
    """)

# Upload file
uploaded_file = st.file_uploader("Upload your dataset", type=["csv"])

# Fallback file path
fallback_path = "C:/Users/chava/Downloads/Enhanced_Education_Dataset (1).csv"

# Load data
def load_data(path_or_file):
    try:
        return pd.read_csv(path_or_file)
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

if uploaded_file is not None:
    df = load_data(uploaded_file)
    st.success("Using uploaded file.")
elif os.path.exists(fallback_path):
    df = load_data(fallback_path)
    st.info(f"Using fallback file: {fallback_path}")
else:
    df = None
    st.warning("Please upload a dataset to continue.")

if df is not None:
    st.write("### Raw Data Preview")
    st.dataframe(df.head())

    non_numeric = df.select_dtypes(exclude=[np.number]).columns
    df = df.drop(columns=non_numeric)

    if "Improvement_Percentage" not in df.columns:
        st.error("Dataset must contain 'Improvement_Percentage' column.")
        st.stop()

    X = df.drop("Improvement_Percentage", axis=1)
    y = df["Improvement_Percentage"]

    X.replace([np.inf, -np.inf], np.nan, inplace=True)
    X.fillna(X.mean(), inplace=True)
    y.replace([np.inf, -np.inf], np.nan, inplace=True)
    y.fillna(y.mean(), inplace=True)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest Regressor": RandomForestRegressor(random_state=42),
        "Decision Tree Regressor": DecisionTreeRegressor(random_state=42),
        "Support Vector Regressor": SVR()
    }

    selected_model = st.selectbox("Choose model to train", list(models.keys()))

    if st.button("Train and Evaluate"):
        with st.spinner("Training model..."):
            model = models[selected_model]
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)
        st.success("Model training and evaluation complete!")

        st.subheader("📈 Performance Metrics")
        st.write(f"- **MSE**: {mean_squared_error(y_test, y_pred):.2f}")
        st.write(f"- **RMSE**: {np.sqrt(mean_squared_error(y_test, y_pred)):.2f}")
        st.write(f"- **MAE**: {mean_absolute_error(y_test, y_pred):.2f}")
        st.write(f"- **R² Score**: {r2_score(y_test, y_pred):.2f}")

        st.markdown("""
        - **MSE (Mean Squared Error)**: Average of squared differences between actual and predicted.
        - **RMSE (Root MSE)**: Square root of MSE; gives error in original units.
        - **MAE (Mean Absolute Error)**: Average of absolute differences.
        - **R² Score**: How well model explains variation in target. Closer to 1 is better.
        """)

        fig, ax = plt.subplots()
        ax.scatter(y_test, y_pred, color='green', alpha=0.6)
        ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
        ax.set_xlabel("Actual")
        ax.set_ylabel("Predicted")
        ax.set_title("Actual vs Predicted")
        st.pyplot(fig)

        residuals = y_test - y_pred
        fig2, ax2 = plt.subplots()
        sns.scatterplot(x=y_pred, y=residuals, ax=ax2, color="orange")
        ax2.axhline(0, linestyle='--', color='red')
        ax2.set_title("Residuals vs Predicted")
        st.pyplot(fig2)

        if selected_model == "Random Forest Regressor":
            importances = model.feature_importances_
            feat_imp = pd.DataFrame({"Feature": X.columns, "Importance": importances}).sort_values(by="Importance", ascending=False)
            st.subheader("🔍 Feature Importances")
            st.dataframe(feat_imp)
            fig3, ax3 = plt.subplots()
            sns.barplot(data=feat_imp, x="Importance", y="Feature", palette="viridis", ax=ax3)
            st.pyplot(fig3)

        pred_df = pd.DataFrame({"Actual": y_test, "Predicted": y_pred})
        csv = pred_df.to_csv(index=False).encode("utf-8")
        st.download_button("📅 Download Predictions", data=csv, file_name="predictions.csv", mime="text/csv")

    if st.checkbox("Compare All Models"):
        results = []
        for name, model in models.items():
            model.fit(X_train_scaled, y_train)
            pred = model.predict(X_test_scaled)
            results.append({
                "Model": name,
                "MSE": mean_squared_error(y_test, pred),
                "RMSE": np.sqrt(mean_squared_error(y_test, pred)),
                "MAE": mean_absolute_error(y_test, pred),
                "R² Score": r2_score(y_test, pred)
            })
        st.subheader("🏋️ Model Comparison Table")
        st.dataframe(pd.DataFrame(results).sort_values(by="R² Score", ascending=False))
else:
    st.info("No data available. Please upload a file.")
