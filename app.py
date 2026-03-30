from flask import Flask, render_template, request, redirect, session, send_file, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import pandas as pd
import joblib
import io
from sklearn.metrics import mean_squared_error, r2_score, confusion_matrix, accuracy_score, classification_report

# ─── App Setup ───────────────────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = "change-this-to-a-random-secret-in-production"

# Security: CORS — only allow your own origin
CORS(app, origins=["http://localhost:5000", "http://127.0.0.1:5000"])

# Security: Rate limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["300 per day", "60 per hour"]
)

# Database setup
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# ─── Database Models ──────────────────────────────────────────────────────────
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="Student")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class StudentRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    g1 = db.Column(db.Float)
    g2 = db.Column(db.Float)
    studytime = db.Column(db.Integer)
    failures = db.Column(db.Integer)
    absences = db.Column(db.Integer)
    predicted_grade = db.Column(db.Float)
    risk_level = db.Column(db.String(10))
    course = db.Column(db.String(50))
    semester = db.Column(db.String(20))


# ─── Load ML Models ───────────────────────────────────────────────────────────
regression_model = joblib.load("model.pkl")
classifier_model = joblib.load("classifier_model.pkl")
df = pd.read_csv("data/student-mat.csv", sep=";")
features = ["G1", "G2", "studytime", "failures", "absences"]
REQUIRED_CSV_COLUMNS = set(features)

# ─── Seed Default Users (run once) ────────────────────────────────────────────
def seed_users():
    """Creates default users with hashed passwords if they don't exist."""
    defaults = [
        ("admin", "123456", "Admin"),
        ("teacher", "123456", "Teacher"),
        ("student", "123456", "Student"),
    ]
    for username, password, role in defaults:
        if not User.query.filter_by(username=username).first():
            u = User(username=username, role=role)
            u.set_password(password)
            db.session.add(u)
    db.session.commit()


# ─── Auth Decorators ─────────────────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" not in session:
            return redirect("/")
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" not in session:
            return redirect("/")
        if session.get("role") != "Admin":
            return "Access Denied — Admins only.", 403
        return f(*args, **kwargs)
    return decorated


# ─── Helper: classify grade ──────────────────────────────────────────────────
def classify_risk(grade):
    if grade < 10:
        return "High", "Immediate academic counseling recommended."
    elif grade < 15:
        return "Medium", "Weekly monitoring advised."
    else:
        return "Low", "No intervention required."


# ─── Helper: build student list from dataframe ───────────────────────────────
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


# ─── LOGIN ────────────────────────────────────────────────────────────────────
@app.route("/", methods=["GET", "POST"])
@limiter.limit("10 per minute", methods=["POST"])  # brute-force protection
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        # Input validation
        if not username or not password:
            error = "Username and password are required."
        else:
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                session["user"] = username
                session["role"] = user.role
                return redirect("/dashboard")
            else:
                error = "Invalid username or password."

    return render_template("login.html", error=error)


@app.route("/signup", methods=["POST"])
@limiter.limit("5 per hour")
def signup():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    # Input validation
    if not username or not password:
        return redirect("/")
    if len(password) < 6:
        return "Password must be at least 6 characters.", 400

    if User.query.filter_by(username=username).first():
        return redirect("/")  # already exists, silently redirect

    new_user = User(username=username, role="Student")
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return redirect("/")


# ─── DASHBOARD ───────────────────────────────────────────────────────────────
@app.route("/dashboard")
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


# ─── MODEL INSIGHTS ──────────────────────────────────────────────────────────
@app.route("/model-insights")
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
        mse=mse,
        r2=r2,
        feature_data=feature_data,
        interpretation_text=interpretation_text
    )


# ─── FAIRNESS ANALYSIS ───────────────────────────────────────────────────────
@app.route("/fairness-analysis")
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


# ─── CLASSIFICATION INSIGHTS ─────────────────────────────────────────────────
@app.route("/classification-insights")
@login_required
def classification_insights():
    X = df[features]
    y = df["G3"].apply(lambda g: 0 if g < 10 else (1 if g < 15 else 2))
    predictions = classifier_model.predict(X)

    cm = confusion_matrix(y, predictions).tolist()
    acc = round(accuracy_score(y, predictions), 3)
    report = classification_report(y, predictions, output_dict=True)

    return render_template("classification_insights.html", cm=cm, acc=acc, report=report)


# ─── UPLOAD DATA ─────────────────────────────────────────────────────────────
@app.route("/upload-data")
@login_required
def upload_page():
    return render_template("upload.html")


@app.route("/analyze-data", methods=["POST"])
@login_required
@limiter.limit("20 per hour")
def analyze_data():
    file = request.files.get("file")
    if not file or file.filename == "":
        return jsonify({"error": "No file uploaded."}), 400

    # Validate file extension
    if not file.filename.endswith(".csv"):
        return jsonify({"error": "Only CSV files are accepted."}), 400

    try:
        df_uploaded = pd.read_csv(file)
    except Exception:
        return jsonify({"error": "Could not read CSV. Make sure it is a valid CSV file."}), 400

    # Validate required columns
    missing_cols = REQUIRED_CSV_COLUMNS - set(df_uploaded.columns)
    if missing_cols:
        return jsonify({"error": f"Missing required columns: {', '.join(sorted(missing_cols))}"}), 400

    # Validate no empty values in required columns
    if df_uploaded[list(REQUIRED_CSV_COLUMNS)].isnull().any().any():
        return jsonify({"error": "Dataset contains empty/null values in required columns."}), 400

    # Validate numeric types
    for col in REQUIRED_CSV_COLUMNS:
        if not pd.api.types.is_numeric_dtype(df_uploaded[col]):
            return jsonify({"error": f"Column '{col}' must contain numeric values."}), 400

    X = df_uploaded[features]
    predictions = regression_model.predict(X)
    importance = regression_model.feature_importances_
    students = build_students(df_uploaded, predictions, importance)

    high_count = sum(1 for s in students if s["risk"] == "High")
    medium_count = sum(1 for s in students if s["risk"] == "Medium")
    low_count = sum(1 for s in students if s["risk"] == "Low")

    # Save to database for persistence
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


# ─── EXPORT ──────────────────────────────────────────────────────────────────
@app.route("/export")
@admin_required
def export():
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype="text/csv",
        as_attachment=True,
        download_name="student_report.csv"
    )


# ─── STUDENT DETAIL ──────────────────────────────────────────────────────────
@app.route("/student/<int:student_id>")
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


# ─── ADMIN ANALYTICS ─────────────────────────────────────────────────────────
@app.route("/admin-analytics")
@admin_required
def admin_analytics():
    X = df[features]
    predictions = regression_model.predict(X)

    high = sum(1 for p in predictions if p < 10)
    medium = sum(1 for p in predictions if 10 <= p < 15)
    low = sum(1 for p in predictions if p >= 15)

    importance = regression_model.feature_importances_

    return render_template(
        "admin_analytics.html",
        high=high,
        medium=medium,
        low=low,
        total=len(df),
        importance=importance.tolist()
    )


# ─── SIMULATE ────────────────────────────────────────────────────────────────
@app.route("/simulate", methods=["POST"])
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

    # Range validation
    for name, val in [("G1", g1), ("G2", g2)]:
        if not (0 <= val <= 20):
            return jsonify({"error": f"{name} must be between 0 and 20."}), 400
    if not (1 <= studytime <= 4):
        return jsonify({"error": "studytime must be between 1 and 4."}), 400
    if not (0 <= failures <= 4):
        return jsonify({"error": "failures must be between 0 and 4."}), 400
    if not (0 <= absences <= 100):
        return jsonify({"error": "absences must be between 0 and 100."}), 400

    input_data = [[g1, g2, studytime, failures, absences]]
    predicted_grade = round(float(regression_model.predict(input_data)[0]), 2)

    prob = classifier_model.predict_proba(input_data)[0]
    risk_index = prob.argmax()
    risk_map = {0: "High", 1: "Medium", 2: "Low"}

    return jsonify({
        "predicted_grade": predicted_grade,
        "risk": risk_map[risk_index],
        "confidence": round(float(max(prob)) * 100, 1)
    })


# ─── LOGOUT ──────────────────────────────────────────────────────────────────
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ─── Run ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_users()
    app.run(debug=False)  # debug=False in production!