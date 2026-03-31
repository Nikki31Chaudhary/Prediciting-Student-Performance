from flask import session, redirect
from functools import wraps


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