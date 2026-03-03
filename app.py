from flask import Flask, render_template, request, redirect, session, send_file
import pandas as pd
import joblib
import io
from datetime import datetime
from sklearn.metrics import mean_squared_error, r2_score, confusion_matrix, accuracy_score, classification_report

app = Flask(__name__)
app.secret_key = "supersecretkey"

USERS = {
    "admin": "123456",
    "teacher": "123456",
    "student": "123456"
}

# Load models
regression_model = joblib.load("model.pkl")
classifier_model = joblib.load("classifier_model.pkl")

df = pd.read_csv("data/student-mat.csv", sep=";")

features = ["G1", "G2", "studytime", "failures", "absences"]

USERNAME = "admin"
PASSWORD = "123456"

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        if username in USERS and USERS[username] == password:
            session["user"] = username
            session["role"] = role
            session["login_time"] = datetime.now().strftime("%d %b %Y, %I:%M %p")
            return redirect("/dashboard")

    return render_template("login.html")

@app.route("/signup", methods=["POST"])
def signup():
    username = request.form["username"]
    password = request.form["password"]

    if username in USERS:
        return redirect("/")  # already exists

    USERS[username] = password
    return redirect("/")

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    X = df[features]
    predictions = regression_model.predict(X)
    importance = regression_model.feature_importances_

    students = []

    for i in range(len(df)):
        predicted_grade = round(predictions[i], 2)

        if predicted_grade < 10:
            risk = "High"
        elif predicted_grade < 15:
            risk = "Medium"
        else:
            risk = "Low"

        students.append({
            "id": i,
            "G1": df.iloc[i]["G1"],
            "G2": df.iloc[i]["G2"],
            "absences": df.iloc[i]["absences"],
            "studytime": df.iloc[i]["studytime"],
            "failures": df.iloc[i]["failures"],
            "predicted_grade": predicted_grade,
            "risk": risk,
            "importance": importance.tolist()
        })

    return render_template("dashboard.html", students=students)

# ---------------- MODEL INSIGHTS ----------------
@app.route("/model-insights")
def model_insights():
    if "user" not in session:
        return redirect("/")

    X = df[features]
    y = df["G3"]

    predictions = regression_model.predict(X)

    mse = round(mean_squared_error(y, predictions), 3)
    r2 = round(r2_score(y, predictions), 3)

    importance = regression_model.feature_importances_

    feature_data = []
    for i in range(len(features)):
        feature_data.append({
            "name": features[i],
            "importance": round(float(importance[i]), 4)
        })

    return render_template(
        "model_insights.html",
        mse=mse,
        r2=r2,
        feature_data=feature_data
    )

# ---------------- FAIRNESS ANALYSIS ----------------
@app.route("/fairness-analysis")
def fairness_analysis():
    if "user" not in session:
        return redirect("/")

    X = df[features]
    predictions = regression_model.predict(X)

    df_copy = df.copy()
    df_copy["predicted"] = predictions

    def classify(grade):
        if grade < 10:
            return "High"
        elif grade < 15:
            return "Medium"
        else:
            return "Low"

    df_copy["risk"] = df_copy["predicted"].apply(classify)

    gender_risk_df = df_copy.groupby(["sex", "risk"]).size().unstack(fill_value=0)

    df_copy["age_group"] = pd.cut(
        df_copy["age"],
        bins=[14,16,18,22],
        labels=["15-16","17-18","19+"]
    )

    age_risk_df = df_copy.groupby(["age_group", "risk"]).size().unstack(fill_value=0)

    gender_risk = gender_risk_df.to_dict(orient="index")
    age_risk = age_risk_df.to_dict(orient="index")

    return render_template(
        "fairness.html",
        gender_risk=gender_risk,
        age_risk=age_risk
    )

# ---------------- CLASSIFICATION INSIGHTS ----------------
@app.route("/classification-insights")
def classification_insights():
    if "user" not in session:
        return redirect("/")

    X = df[features]

    def classify(g):
        if g < 10:
            return 0
        elif g < 15:
            return 1
        else:
            return 2

    y = df["G3"].apply(classify)

    predictions = classifier_model.predict(X)

    cm = confusion_matrix(y, predictions).tolist()
    acc = round(accuracy_score(y, predictions), 3)
    report = classification_report(y, predictions, output_dict=True)

    return render_template(
        "classification_insights.html",
        cm=cm,
        acc=acc,
        report=report
    )

# ---------------- EXPORT ----------------
@app.route("/export")
def export():
    if "user" not in session:
        return redirect("/")

    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)

    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype="text/csv",
        as_attachment=True,
        download_name="student_report.csv"
    )

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)