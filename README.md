# 🎓 AI-Based Student Performance Prediction & Early Academic Intervention System

---

## 📌 Project Overview

This project is an AI-powered academic analytics dashboard designed to predict student performance early in the semester and identify students at risk of underperformance.

The system leverages Machine Learning to forecast final grades and classify students into risk categories (High / Medium / Low), enabling proactive academic intervention before final academic failure occurs.

---

## 🎯 Problem Statement

Traditional academic monitoring systems are reactive. Students are identified as at-risk only after significant grade decline.

This system provides:

- Early academic performance prediction
- Risk probability classification
- Visual analytics dashboard
- AI-supported intervention insights

---

## 🧠 Machine Learning Model

### 🔹 Model Used:
Random Forest Regressor

### 🔹 Input Features:
- G1 (First Internal Assessment Grade)
- G2 (Second Internal Assessment Grade)
- Study Time
- Failures
- Absences

### 🔹 Target:
- G3 (Final Grade)

---

## 📊 Risk Classification Logic

Based on predicted grade (0–20 scale):

- **High Risk** → Grade < 10  
- **Medium Risk** → 10 – 14  
- **Low Risk** → ≥ 15  

Grading Scale: 0–20

---

## 🚀 Key Features

- 📈 Risk Distribution Visualization (Pie / Bar Toggle)
- 📊 Animated KPI Cards
- 📉 Student Performance Progress Bars
- 🔍 Risk Filtering
- 🧠 AI Confidence Score
- 💡 Modal-based Risk Explanation
- 🌗 Theme Toggle (Light/Dark)
- 📁 CSV Report Export
- 🔐 Authentication System
- 📊 Interactive DataTables Integration

---

## 🛠️ Tech Stack

### Backend
- Python
- Flask
- Pandas
- Scikit-learn
- Joblib

### Frontend
- HTML5
- CSS3
- Bootstrap 5
- Chart.js
- DataTables
- JavaScript

### Version Control
- Git
- GitHub (Collaborative Development)

---

## 🏗️ System Architecture

1. Data Collection Layer  
2. Data Processing & Feature Engineering  
3. Machine Learning Model Training  
4. Risk Classification Layer  
5. Dashboard Visualization Layer  
6. Educator Decision Support Interface  

---

## ▶️ How to Run Locally

### 1️⃣ Clone Repository

```bash
git clone https://github.com/Nikki31Chaudhary/Prediciting-Student-Performance.git
cd Prediciting-Student-Performance
```

### 2️⃣ Install Dependencies

```bash
pip install flask pandas scikit-learn joblib
```

### 3️⃣ Run Application

```bash
python app.py
```

Open browser:

```
http://127.0.0.1:5000
```

### 🔐 Login Credentials

Username: `admin`  
Password: `123456`

---

## 🌐 Deployment (Upcoming Phase)

This project will be deployed using:

- Render / Railway / AWS (Flask backend hosting)
- Gunicorn (Production server)
- Environment variable configuration
- Public access dashboard

Deployment enhancements will include:

- Production-ready configuration
- Secure secret key management
- Scalable cloud infrastructure

---

## 📈 Expected Impact

- Early identification of at-risk students
- Improved retention rates
- Data-driven academic intervention
- Transparent and interpretable AI decision support

---

## 🔮 Future Enhancements

- OpenAI-powered personalized recommendations
- PDF analytics report export
- Role-based authentication (Teacher / Admin)
- Real-time model retraining
- Advanced fairness & bias evaluation


## 👩‍💻 Developed By

- **Shristi Upadhyay**
- **Nikki Chaudhary**
---

## 📜 Academic Project

This project is developed for AI/ML academic evaluation and portfolio development purposes.
