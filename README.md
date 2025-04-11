# 📚 Learnova – Education Effectiveness Analysis

**Learnova** is a Streamlit-powered web app designed to help educators, students, and policymakers gain insights into student performance using data-driven methods and machine learning. Developed by **Team Hackos**, this app was built as part of an academic research project to improve learning outcomes.

---

## 🚀 Features

- 🔐 Secure user authentication using Firebase  
- 🧠 Predict student performance with machine learning models  
- 📊 Visual analytics for educational insights  
- 📁 Firebase Firestore integration for user and contact data  
- 📬 Contact form with backend message storage  
- 🔒 Session-based page protection (auth guard)  

---

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)  
- **Backend**: [Firebase Authentication](https://firebase.google.com/products/auth), [Firestore](https://firebase.google.com/products/firestore)  
- **Machine Learning**: scikit-learn, pandas, NumPy  
- **Deployment**: Streamlit Cloud / Local  
- **Version Control**: Git & GitHub  

---

## 📂 Project Structure

```
learnova/
│
├── home.py                  # App landing page
├── pages/
│   ├── 1_🔐_Account.py       # Sign Up / Login page
│   ├── 2_📊_Dashboard.py     # ML predictions or analytics
│   └── 3_🤝_About_Us.py      # About and Contact
│
├── auth_guard.py           # Auth check utility
├── firebase_config/
│   └── serviceAccountKey.json  # 🔒 Do NOT push this file to GitHub!
│
├── requirements.txt        # Required Python packages
└── README.md               # Project documentation
```

---

## ⚙️ Setup Instructions

1. **Clone the Repository**

```bash
git clone https://github.com/your-username/learnova.git
cd learnova
```

2. **Create Virtual Environment (Optional)**

```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

4. **Firebase Configuration**

Create a folder `firebase_config/` and place your Firebase Admin SDK JSON inside it.  
This file is typically named something like `serviceAccountKey.json`.

> 🔐 **Never push this JSON file to GitHub!** Add it to `.gitignore`.

5. **Run the App**

```bash
streamlit run home.py
```

---

## 📦 Example `.gitignore`

```
firebase_config/serviceAccountKey.json
__pycache__/
.venv/
*.pyc
```

---

## 💡 Future Improvements

- 📥 Allow users to upload CSV student data  
- 📈 Model accuracy tracking and comparison  
- 📅 Performance over time graphs  
- 🌐 Admin panel to manage users and view messages  

---

## 🤝 About Us

We are **Team Hackos**, a group of passionate students working on tech-driven solutions in education.

📬 Contact us via the **Contact Us** section of the app or through [Formspree](https://formspree.io).

---

## 📜 License

This project is for **academic and educational purposes** only.  
All rights reserved © Team Hackos.

---

> Built with ❤️ by **Team Hackos** – Empowering Education Through Data
