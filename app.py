from flask import Flask, render_template, request, redirect, session, send_file
import pandas as pd
import joblib
import io

app = Flask(__name__)
app.secret_key = "supersecretkey"

model = joblib.load("model.pkl")
df = pd.read_csv("data/student-mat.csv", sep=";")

features = ["G1", "G2", "studytime", "failures", "absences"]

USERNAME = "admin"
PASSWORD = "123456"   # UPDATED PASSWORD

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == USERNAME and request.form["password"] == PASSWORD:
            session["user"] = USERNAME
            return redirect("/dashboard")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    X = df[features]
    predictions = model.predict(X)

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
            "predicted_grade": predicted_grade,
            "risk": risk
        })

    return render_template("dashboard.html", students=students)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

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

if __name__ == "__main__":
    app.run(debug=True)