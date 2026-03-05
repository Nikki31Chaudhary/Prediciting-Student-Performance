from flask import Flask, render_template, request, redirect, session, send_file,jsonify
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

users = {
"admin":{"password":"123456","role":"Admin"},
"teacher":{"password":"123456","role":"Teacher"},
"student":{"password":"123456","role":"Student"}
}

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET","POST"])
def login():

    if request.method=="POST":

        username=request.form["username"]
        password=request.form["password"]

        if username in users and users[username]["password"]==password:

            session["user"]=username
            session["role"]=users[username]["role"]

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
            suggestion = "Immediate academic counseling recommended."
        elif predicted_grade < 15:
            risk = "Medium"
            suggestion = "Weekly monitoring and performance review advised."
        else:
            risk = "Low"
            suggestion = "No intervention required. Maintain consistency."

        students.append({
            "id": i,
            "G1": df.iloc[i]["G1"],
            "G2": df.iloc[i]["G2"],
            "absences": df.iloc[i]["absences"],
            "studytime": df.iloc[i]["studytime"],
            "failures": df.iloc[i]["failures"],
            "predicted_grade": predicted_grade,
            "risk": risk,
            "suggestion": suggestion,
            "importance": importance.tolist()
        })

        # Risk Summary Counts
        high_count = sum(1 for s in students if s["risk"] == "High")
        medium_count = sum(1 for s in students if s["risk"] == "Medium")
        low_count = sum(1 for s in students if s["risk"] == "Low")

    return render_template(
    "dashboard.html",
    students=students,
    high_count=high_count,
    medium_count=medium_count,
    low_count=low_count,
    role=session.get("role")

)

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
    max_index = importance.argmax()
    top_feature = features[max_index]

    interpretation_text = f"The model shows strong predictive performance. The most influential feature is {top_feature}, indicating it significantly impacts final grade prediction."

    

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
    feature_data=feature_data,
    interpretation_text=interpretation_text
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

@app.route("/upload-data")
def upload_page():
    if "user" not in session:
        return redirect("/")
    return render_template("upload.html")

@app.route("/analyze-data", methods=["POST"])
def analyze_data():

    file = request.files["file"]

    if file.filename == "":
        return "No file uploaded"

    df_uploaded = pd.read_csv(file)

    features = ["G1","G2","studytime","failures","absences"]

    X = df_uploaded[features]

    predictions = regression_model.predict(X)
    importance = regression_model.feature_importances_

    students = []

    for i in range(len(df_uploaded)):

        predicted_grade = round(predictions[i],2)

        if predicted_grade < 10:
            risk="High"
        elif predicted_grade < 15:
            risk="Medium"
        else:
            risk="Low"

        students.append({
            "id":i,
            "G1":df_uploaded.iloc[i]["G1"],
            "G2":df_uploaded.iloc[i]["G2"],
            "absences":df_uploaded.iloc[i]["absences"],
            "studytime":df_uploaded.iloc[i]["studytime"],
            "failures":df_uploaded.iloc[i]["failures"],
            "predicted_grade":predicted_grade,
            "risk":risk,
            "importance":importance.tolist()
        })

        # Risk Summary Counts
        high_count = sum(1 for s in students if s["risk"] == "High")
        medium_count = sum(1 for s in students if s["risk"] == "Medium")
        low_count = sum(1 for s in students if s["risk"] == "Low")

    return render_template(
    "dashboard.html",
    students=students,
    high_count=high_count,
    medium_count=medium_count,
    low_count=low_count
)

# ---------------- EXPORT ----------------
@app.route("/export")
def export():
    if session.get("role")!="Admin":
        return "Access Denied"

    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)

    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype="text/csv",
        as_attachment=True,
        download_name="student_report.csv"
    )

@app.route("/student/<int:student_id>")
def student_detail(student_id):

    if "user" not in session:
        return redirect("/")

    X = df[features]

    predictions = regression_model.predict(X)
    importance = regression_model.feature_importances_

    student = df.iloc[student_id]

    predicted_grade = round(predictions[student_id],2)

    if predicted_grade < 10:
        risk="High"
    elif predicted_grade < 15:
        risk="Medium"
    else:
        risk="Low"

    # Class averages
    avg_g1 = round(df["G1"].mean(),2)
    avg_g2 = round(df["G2"].mean(),2)
    avg_abs = round(df["absences"].mean(),2)
    avg_study = round(df["studytime"].mean(),2)
    avg_fail = round(df["failures"].mean(),2)

    return render_template(
        "student_detail.html",
        student=student,
        predicted_grade=predicted_grade,
        risk=risk,
        importance=importance.tolist(),

        avg_g1=avg_g1,
        avg_g2=avg_g2,
        avg_abs=avg_abs,
        avg_study=avg_study,
        avg_fail=avg_fail
)
    

@app.route("/admin-analytics")
def admin_analytics():

    if session.get("role")!="Admin":
        return "Access Denied"

    X=df[features]

    predictions=regression_model.predict(X)

    high=0
    medium=0
    low=0

    for p in predictions:

        if p<10:
            high+=1
        elif p<15:
            medium+=1
        else:
            low+=1

    importance=regression_model.feature_importances_

    total=len(df)

    return render_template(
        "admin_analytics.html",
        high=high,
        medium=medium,
        low=low,
        total=total,
        importance=importance.tolist()
    )

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

@app.route("/simulate", methods=["POST"])
def simulate():

    g1 = float(request.form["g1"])
    g2 = float(request.form["g2"])
    studytime = float(request.form["studytime"])
    failures = float(request.form["failures"])
    absences = float(request.form["absences"])

    input_data = [[g1, g2, studytime, failures, absences]]

    predicted_grade = round(regression_model.predict(input_data)[0], 2)

    prob = classifier_model.predict_proba(input_data)[0]
    max_prob = max(prob)

    risk_index = prob.argmax()

    if risk_index == 0:
        risk = "High"
    elif risk_index == 1:
        risk = "Medium"
    else:
        risk = "Low"

    return jsonify({
    "predicted_grade": predicted_grade,
    "risk": risk,
    "confidence": round(max_prob * 100, 1)
})

if __name__ == "__main__":
    app.run(debug=True)