

# 🎓 AI-Based Student Performance Prediction & Early Academic Intervention System

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Random%20Forest-green)
![Frontend](https://img.shields.io/badge/Frontend-Bootstrap%205-purple)
![Status](https://img.shields.io/badge/Project-Academic%20AI%20System-orange)

An **AI-powered academic analytics platform** designed to predict student performance early in the semester and identify **at-risk students before academic failure occurs**.

The system integrates **Machine Learning, Explainable AI, interactive dashboards, and role-based authentication** to help educators take **early academic intervention decisions**.

---

# 📌 Project Overview

Traditional academic systems identify struggling students **only after final results**, when intervention is often too late.

This project introduces a **predictive academic monitoring system** that allows educators to:

* Predict final grades early
* Identify at-risk students
* Analyze academic patterns
* Provide explainable AI insights
* Visualize student risk distribution

The system transforms **reactive academic monitoring into predictive decision support**.

---

# 🎯 Problem Statement

Most educational institutions lack tools to detect academic risk early.

Common issues include:

* Late identification of struggling students
* No predictive analytics system
* Limited transparency in evaluation
* No automated risk classification

This system solves these problems through:

✔ Early **Machine Learning grade prediction**
✔ **Automated student risk classification**
✔ **Explainable AI insights**
✔ **Fairness and bias analysis**
✔ **Interactive educator dashboard**

---

# 🧠 Machine Learning Pipeline

The system uses **Random Forest algorithms** for both regression and classification.

### Models Used

| Model                    | Purpose                  |
| ------------------------ | ------------------------ |
| Random Forest Regressor  | Predict Final Grade (G3) |
| Random Forest Classifier | Predict Risk Category    |

---

### Input Features

| Feature       | Description                    |
| ------------- | ------------------------------ |
| G1            | First internal grade           |
| G2            | Second internal grade          |
| Study Time    | Weekly study hours             |
| Past Failures | Number of past failed subjects |
| Absences      | Total class absences           |

---

### Target Variable

**G3 → Final Grade (0–20 scale)**

---

# 📊 Risk Classification Logic

Students are classified into risk categories based on predicted grade.

| Risk Level     | Grade Range |
| -------------- | ----------- |
| 🔴 High Risk   | Grade < 10  |
| 🟡 Medium Risk | 10 – 14     |
| 🟢 Low Risk    | ≥ 15        |

This helps teachers **identify vulnerable students early**.

---

# 📈 Model Performance

| Metric                   | Score                        |
| ------------------------ | ---------------------------- |
| Mean Squared Error (MSE) | ~2.63                        |
| R² Score                 | Strong predictive capability |
| Classification Accuracy  | ~87%                         |

The dashboard also visualizes model performance using a **confusion matrix and analytics charts**.

---

# 💡 Key System Features

## 🔍 AI & Analytics

* Final grade prediction using Machine Learning
* Student risk classification
* AI confidence score
* Explainability engine (feature contribution analysis)
* SHAP-style approximation logic
* Bias detection (gender & age fairness analysis)
* Confusion matrix visualization

---

## 📊 Interactive Dashboard

The dashboard provides a **complete academic risk analytics interface** including:

* KPI summary cards
* Risk percentage indicators
* Risk distribution charts
* Student risk analytics table
* AI confidence scores
* Intervention recommendations

According to the dashboard analytics:

* **High Risk Students → 43%**
* **Medium Risk Students → 40%**
* **Low Risk Students → 17%**

with **395 students analyzed**. 

---

# 🔐 Authentication System

The application includes a **multi-user role-based login system**.

Features include:

* Glassmorphism login interface
* Sign In / Sign Up toggle
* Demo accounts
* Role-based access control
* Session tracking
* Conditional feature access

Supported roles:

* Admin
* Teacher
* Student

---

# 🌗 UI / UX Design

The application includes modern SaaS-style UI components:

* Glassmorphism login page
* Animated gradient background
* Light / Dark theme toggle
* Smooth hover effects
* Premium card-based layout
* Fully responsive design (Bootstrap 5)

---

# 🏗️ System Architecture

```
Dataset (CSV)
      ↓
Data Preprocessing
      ↓
Feature Selection
      ↓
Random Forest Model Training
      ↓
Risk Classification Layer
      ↓
Explainability Engine
      ↓
Flask Backend API
      ↓
Interactive Web Dashboard
```

---

# 📸 Application Screenshots

## 🔐 Login Page

![Login Interface](https://github.com/Nikki31Chaudhary/Prediciting-Student-Performance/blob/0b9f43504f0c04751043830eae32452d3471665c/Screenshot%202026-03-11%20112238.png)

Modern glassmorphism styled login page with role-based authentication.

---

## 📊 AI Academic Early Warning Dashboard

![Dashboard](screenshots/dashboard.png)

The dashboard provides a **complete academic risk monitoring system** including:

* Student risk percentage indicators
* Risk distribution charts
* Study-time risk heatmaps
* AI confidence scores
* Student intervention recommendations

The system highlights students who require:

* Immediate academic counseling
* Weekly monitoring
* No intervention

These insights help educators **take proactive academic actions**. 

---

# 🛠️ Tech Stack

### Backend

* Python
* Flask
* Pandas
* Scikit-learn
* Joblib

---

### Frontend

* HTML5
* CSS3
* Bootstrap 5
* Chart.js
* DataTables
* JavaScript

---

### Authentication

* Session-based authentication
* Role-based access control

---

### Version Control

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

# 🌐 Deployment (Future Scope)

Planned deployment platforms:

* Render
* Railway
* AWS

Production environment setup will include:

* Gunicorn server
* Environment variables
* Scalable cloud infrastructure

---

# 📈 Expected Impact

* Early detection of academically vulnerable students
* Improved student success rates
* Data-driven academic decision making
* Transparent AI-based evaluation

---

# 🔮 Future Enhancements

* Database authentication (SQLite / PostgreSQL)
* Secure password hashing
* AI-powered academic recommendations
* PDF analytics export
* Real-time model retraining
* Advanced bias auditing
* CI/CD deployment pipeline

---

# 👩‍💻 Developed By

**Shristi Upadhyay**
**Nikki Chaudhary**

---

# 📜 Academic Portfolio Project

This project demonstrates:

* Machine Learning deployment
* Explainable AI implementation
* Full-stack web development
* Role-based authentication systems
* Professional dashboard design


