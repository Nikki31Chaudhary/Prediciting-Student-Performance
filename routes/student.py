from flask import Blueprint, render_template, request, redirect, session, jsonify
from decorators import login_required
from extensions import limiter
from models import db, StudentRecord
from ml import regression_model, classifier_model, df, features, REQUIRED_CSV_COLUMNS
from sklearn.metrics import mean_squared_error, r2_score, confusion_matrix, accuracy_score, classification_report
import pandas as pd

student_bp = Blueprint("student", __name__)

def classify_risk(grade):
    if grade < 10:
        return "High", "Immediate academic counseling recommended."
    elif grade < 15:
        return "Medium", "Weekly monitoring advised."
    else:
        return "Low", "No intervention required."

def build_students(dataframe, predictions, importance):
    students = []
    for i in range(len(dataframe)):
        predicted_grade = round(float(predictions[i]), 2)
        risk, suggestion = classify_risk(predicted_grade)
        students.append({
            "id": i,
            "G1": dataframe.iloc[i]["G1"],
            "G2": dataframe.iloc[i]["G2"],
            "absences": dataframe.iloc[i]["absences"],
            "studytime": dataframe.iloc[i]["studytime"],
            "failures": dataframe.iloc[i]["failures"],
            "predicted_grade": predicted_grade,
            "risk": risk,
            "suggestion": suggestion,
            "importance": importance.tolist()
        })
    return students

@student_bp.route("/dashboard")
@login_required
def dashboard():
    X = df[features]
    predictions = regression_model.predict(X)
    importance = regression_model.feature_importances_
    students = build_students(df, predictions, importance)
    high_count = sum(1 for s in students if s["risk"] == "High")
    medium_count = sum(1 for s in students if s["risk"] == "Medium")
    low_count = sum(1 for s in students if s["risk"] == "Low")
    heatmap_data = [
        {"studytime": int(s["studytime"]), "absences": int(s["absences"]), "risk": str(s["risk"])}
        for s in students
    ]
    return render_template(
        "dashboard.html",
        students=students,
        high_count=high_count,
        medium_count=medium_count,
        low_count=low_count,
        heatmap_data=heatmap_data,
        role=session.get("role")
    )

@student_bp.route("/student/<int:student_id>")
@login_required
def student_detail(student_id):
    if student_id < 0 or student_id >= len(df):
        return "Student not found.", 404
    X = df[features]
    predictions = regression_model.predict(X)
    importance = regression_model.feature_importances_
    student = df.iloc[student_id]
    predicted_grade = round(float(predictions[student_id]), 2)
    risk, _ = classify_risk(predicted_grade)
    return render_template(
        "student_detail.html",
        student=student,
        predicted_grade=predicted_grade,
        risk=risk,
        importance=importance.tolist(),
        avg_g1=round(df["G1"].mean(), 2),
        avg_g2=round(df["G2"].mean(), 2),
        avg_abs=round(df["absences"].mean(), 2),
        avg_study=round(df["studytime"].mean(), 2),
        avg_fail=round(df["failures"].mean(), 2),
    )

@student_bp.route("/upload-data")
@login_required
def upload_page():
    return render_template("upload.html")

@student_bp.route("/analyze-data", methods=["POST"])
@login_required
@limiter.limit("20 per hour")
def analyze_data():
    file = request.files.get("file")
    if not file or file.filename == "":
        return jsonify({"error": "No file uploaded."}), 400
    if not file.filename.endswith(".csv"):
        return jsonify({"error": "Only CSV files are accepted."}), 400
    try:
        df_uploaded = pd.read_csv(file)
    except Exception:
        return jsonify({"error": "Could not read CSV file."}), 400
    missing_cols = REQUIRED_CSV_COLUMNS - set(df_uploaded.columns)
    if missing_cols:
        return jsonify({"error": f"Missing columns: {', '.join(sorted(missing_cols))}"}), 400
    if df_uploaded[list(REQUIRED_CSV_COLUMNS)].isnull().any().any():
        return jsonify({"error": "Dataset contains empty values."}), 400
    for col in REQUIRED_CSV_COLUMNS:
        if not pd.api.types.is_numeric_dtype(df_uploaded[col]):
            return jsonify({"error": f"Column '{col}' must be numeric."}), 400
    X = df_uploaded[features]
    predictions = regression_model.predict(X)
    importance = regression_model.feature_importances_
    students = build_students(df_uploaded, predictions, importance)
    high_count = sum(1 for s in students if s["risk"] == "High")
    medium_count = sum(1 for s in students if s["risk"] == "Medium")
    low_count = sum(1 for s in students if s["risk"] == "Low")
    course = request.form.get("course", "Unknown")
    semester = request.form.get("semester", "Unknown")
    for s in students:
        record = StudentRecord(
            g1=s["G1"], g2=s["G2"], studytime=s["studytime"],
            failures=s["failures"], absences=s["absences"],
            predicted_grade=s["predicted_grade"], risk_level=s["risk"],
            course=course, semester=semester
        )
        db.session.add(record)
    db.session.commit()
    return render_template(
        "dashboard.html",
        students=students,
        high_count=high_count,
        medium_count=medium_count,
        low_count=low_count,
        heatmap_data=[],
        role=session.get("role")
    )

@student_bp.route("/model-insights")
@login_required
def model_insights():
    X = df[features]
    y = df["G3"]
    predictions = regression_model.predict(X)
    mse = round(mean_squared_error(y, predictions), 3)
    r2 = round(r2_score(y, predictions), 3)
    importance = regression_model.feature_importances_
    top_feature = features[importance.argmax()]
    interpretation_text = (
        f"The model shows strong predictive performance. "
        f"The most influential feature is {top_feature}, indicating it significantly impacts final grade prediction."
    )
    feature_data = [
        {"name": features[i], "importance": round(float(importance[i]), 4)}
        for i in range(len(features))
    ]
    return render_template(
        "model_insights.html",
        mse=mse, r2=r2,
        feature_data=feature_data,
        interpretation_text=interpretation_text
    )

@student_bp.route("/fairness-analysis")
@login_required
def fairness_analysis():
    X = df[features]
    predictions = regression_model.predict(X)
    df_copy = df.copy()
    df_copy["predicted"] = predictions
    df_copy["risk"] = df_copy["predicted"].apply(
        lambda g: "High" if g < 10 else ("Medium" if g < 15 else "Low")
    )
    df_copy["age_group"] = pd.cut(
        df_copy["age"], bins=[14, 16, 18, 22], labels=["15-16", "17-18", "19+"]
    )
    gender_risk = df_copy.groupby(["sex", "risk"]).size().unstack(fill_value=0).to_dict(orient="index")
    age_risk = df_copy.groupby(["age_group", "risk"]).size().unstack(fill_value=0).to_dict(orient="index")
    return render_template("fairness.html", gender_risk=gender_risk, age_risk=age_risk)

@student_bp.route("/classification-insights")
@login_required
def classification_insights():
    X = df[features]
    y = df["G3"].apply(lambda g: 0 if g < 10 else (1 if g < 15 else 2))
    predictions = classifier_model.predict(X)
    cm = confusion_matrix(y, predictions).tolist()
    acc = round(accuracy_score(y, predictions), 3)
    report = classification_report(y, predictions, output_dict=True)
    return render_template("classification_insights.html", cm=cm, acc=acc, report=report)

@student_bp.route("/simulate", methods=["POST"])
@login_required
@limiter.limit("30 per minute")
def simulate():
    try:
        g1 = float(request.form["g1"])
        g2 = float(request.form["g2"])
        studytime = float(request.form["studytime"])
        failures = float(request.form["failures"])
        absences = float(request.form["absences"])
    except (KeyError, ValueError):
        return jsonify({"error": "Invalid input values."}), 400
    if not (0 <= g1 <= 20):
        return jsonify({"error": "G1 must be between 0 and 20."}), 40