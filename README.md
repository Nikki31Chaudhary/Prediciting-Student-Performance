



# 🎓 AI-Based Student Performance Prediction & Early Academic Intervention System

An **AI-powered academic analytics platform** designed to predict student performance early in the semester and identify **at-risk students before academic failure occurs**.

The system combines **Machine Learning, Explainable AI, interactive dashboards, and role-based authentication** to help educators take **proactive academic interventions**.

Instead of waiting for final exam results, this system enables **data-driven early warning signals** for educators.

---

# 📌 Project Overview

Traditional academic evaluation systems often detect struggling students **too late**, after performance has already declined.

This project introduces a **predictive academic monitoring system** that can:

• Predict final grades early in the semester
• Identify at-risk students
• Provide explainable AI insights
• Detect bias in predictions
• Visualize academic trends using an interactive dashboard

The system transforms traditional **reactive monitoring → predictive decision support**.

---

# 🎯 Problem Statement

In most education systems:

* Students are evaluated only after final exams.
* Teachers lack early indicators of academic decline.
* No predictive or analytical tools exist to support intervention.

This project solves the problem by introducing:

✔ Early **grade prediction using Machine Learning**
✔ Automated **risk classification**
✔ **Explainable AI** insights for transparency
✔ **Fairness analysis** to detect model bias
✔ Interactive **analytics dashboard**

---

# 🧠 Machine Learning Pipeline

The platform uses **Random Forest algorithms** for both prediction and classification tasks.

### Models Used

**Random Forest Regressor**
Predicts the student's **final grade (G3)**.

**Random Forest Classifier**
Classifies students into **risk categories**.

---

### Input Features

The model uses the following academic indicators:

| Feature       | Description                    |
| ------------- | ------------------------------ |
| G1            | First Internal Grade           |
| G2            | Second Internal Grade          |
| Study Time    | Weekly study duration          |
| Past Failures | Number of past failed subjects |
| Absences      | Total class absences           |

---

### Target Variable

**G3 → Final Grade (0-20 scale)**

---

# 📊 Risk Classification Logic

Students are categorized based on predicted final grades.

| Risk Level     | Grade Range |
| -------------- | ----------- |
| 🔴 High Risk   | Grade < 10  |
| 🟡 Medium Risk | 10 – 14     |
| 🟢 Low Risk    | ≥ 15        |

This allows educators to **identify struggling students early**.

---

# 📈 Model Performance

| Metric                   | Value                        |
| ------------------------ | ---------------------------- |
| Mean Squared Error (MSE) | ~2.63                        |
| R² Score                 | Strong predictive capability |
| Classification Accuracy  | ~87%                         |

The dashboard also integrates a **confusion matrix visualization** to analyze model predictions.

---

# 💡 Key System Features

## 🔍 AI & Analytics

• Final grade prediction using ML
• Student risk classification
• AI confidence score
• Explainability engine (feature contribution analysis)
• SHAP-style approximation logic
• Bias detection (gender & age group fairness analysis)
• Confusion matrix visualization

---

## 📊 Interactive Dashboard

The educator dashboard includes:

• Animated KPI cards
• Risk distribution charts (Pie / Bar toggle)
• DataTables filtering & search
• Student progress visualization
• Premium gradient table styling
• CSV report export (Admin only)

---

## 🔐 Authentication System

The platform includes a **multi-role login system**.

Features include:

• Glassmorphism login interface
• Sign-in / Sign-up toggle
• Multi-user demo accounts
• Role-based access control
• Session tracking with login timestamp
• Conditional feature visibility

Roles supported:

* Admin
* Teacher
* Student

---

# 🌗 UI / UX Design

The application includes modern UI enhancements such as:

• SaaS-style glassmorphism login
• Animated gradient background
• Light / Dark theme toggle
• Smooth hover animations
• Premium shadow & card components
• Fully responsive layout using Bootstrap 5

---

# 🏗️ System Architecture

The system follows a **full-stack ML architecture pipeline**:

1️⃣ Data Collection (CSV dataset)
2️⃣ Feature preprocessing & selection
3️⃣ Model training (Random Forest)
4️⃣ Risk classification layer
5️⃣ Explainability engine
6️⃣ Flask backend API
7️⃣ Interactive frontend dashboard

---

# 🛠️ Tech Stack

## Backend

* Python
* Flask
* Pandas
* Scikit-learn
* Joblib

---

## Frontend

* HTML5
* CSS3
* Bootstrap 5
* Chart.js
* DataTables
* JavaScript

---

## Authentication

* Session-based authentication
* Role-based access control

---

## Version Control

* Git
* GitHub

---

# ▶️ How to Run Locally

### 1️⃣ Clone Repository

```bash
git clone https://github.com/Nikki31Chaudhary/Prediciting-Student-Performance.git
cd Prediciting-Student-Performance
```

---

### 2️⃣ Install Dependencies

```bash
pip install flask pandas scikit-learn joblib
```

---

### 3️⃣ Run Application

```bash
python app.py
```

---

### Open Browser

```
http://127.0.0.1:5000
```

---

# 🔐 Demo Login Credentials

| Username | Password |
| -------- | -------- |
| admin    | 123456   |
| teacher  | 123456   |
| student  | 123456   |

---

# 🌐 Deployment (Planned Phase)

The system is structured for deployment using:

• Render / Railway / AWS
• Gunicorn (Production Server)
• Environment variables for secret keys
• Scalable cloud infrastructure

---

# 📈 Expected Impact

• Early identification of academically vulnerable students
• Improved student retention rates
• Transparent AI-based academic evaluation
• Data-driven decision support for educators

---

# 🔮 Future Enhancements

Planned improvements include:

• Database-based authentication (SQLite / PostgreSQL)
• Secure password hashing
• OpenAI-powered academic recommendations
• PDF analytics export
• Real-time model retraining
• Advanced bias auditing
• CI/CD deployment pipeline

---

# 👩‍💻 Developed By

**Shristi Upadhyay**
**Nikki Chaudhary**

---

# 📜 Academic Portfolio Project

This project demonstrates expertise in:

✔ Machine Learning model deployment
✔ Explainable AI integration
✔ Full-stack dashboard development
✔ Role-based authentication systems
✔ Professional UI/UX implementation


