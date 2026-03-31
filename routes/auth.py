from flask import Blueprint, render_template, request, redirect, session
from models import db, User
from extensions import limiter
 
auth_bp = Blueprint("auth", __name__)
 
 
@auth_bp.route("/", methods=["GET", "POST"])
@limiter.limit("10 per minute", methods=["POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
 
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
 
 
@auth_bp.route("/signup", methods=["POST"])
@limiter.limit("5 per hour")
def signup():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
 
    if not username or not password:
        return redirect("/")
    if len(password) < 6:
        return "Password must be at least 6 characters.", 400
    if User.query.filter_by(username=username).first():
        return redirect("/")
 
    new_user = User(username=username, role="Student")
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return redirect("/")
 
 
@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")
 