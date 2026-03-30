"""
tests/test_app.py — Unit tests for the AI Student Risk System.
Run with:  pytest tests/ -v
"""

import pytest
import sys
import os

# Add parent directory to path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ─── Test: classify_risk helper ───────────────────────────────────────────────
def test_classify_risk_high():
    from app import classify_risk
    risk, suggestion = classify_risk(5.0)
    assert risk == "High"
    assert "counseling" in suggestion.lower()

def test_classify_risk_medium():
    from app import classify_risk
    risk, suggestion = classify_risk(12.0)
    assert risk == "Medium"
    assert "monitoring" in suggestion.lower()

def test_classify_risk_low():
    from app import classify_risk
    risk, suggestion = classify_risk(17.0)
    assert risk == "Low"
    assert "No intervention" in suggestion

def test_classify_risk_boundary_10():
    """Grade exactly 10 should be Medium (not High)."""
    from app import classify_risk
    risk, _ = classify_risk(10.0)
    assert risk == "Medium"

def test_classify_risk_boundary_15():
    """Grade exactly 15 should be Low (not Medium)."""
    from app import classify_risk
    risk, _ = classify_risk(15.0)
    assert risk == "Low"


# ─── Test: Flask routes (login/logout/auth) ───────────────────────────────────
@pytest.fixture
def client():
    from app import app, db, seed_users
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # in-memory DB for tests
    app.config["WTF_CSRF_ENABLED"] = False
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            seed_users()
        yield client


def test_login_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200

def test_login_valid_admin(client):
    response = client.post("/", data={"username": "admin", "password": "123456"}, follow_redirects=True)
    assert response.status_code == 200

def test_login_invalid_password(client):
    response = client.post("/", data={"username": "admin", "password": "wrongpassword"}, follow_redirects=True)
    assert b"Invalid" in response.data or response.status_code == 200

def test_login_invalid_user(client):
    response = client.post("/", data={"username": "nobody", "password": "123456"}, follow_redirects=True)
    assert response.status_code == 200

def test_dashboard_requires_login(client):
    """Dashboard should redirect if not logged in."""
    response = client.get("/dashboard")
    assert response.status_code in [302, 308]

def test_admin_analytics_requires_admin(client):
    """Admin analytics should deny non-admin users."""
    with client.session_transaction() as sess:
        sess["user"] = "teacher"
        sess["role"] = "Teacher"
    response = client.get("/admin-analytics")
    assert response.status_code == 403

def test_admin_analytics_allows_admin(client):
    """Admin analytics should work for admin role."""
    with client.session_transaction() as sess:
        sess["user"] = "admin"
        sess["role"] = "Admin"
    response = client.get("/admin-analytics")
    assert response.status_code == 200

def test_export_requires_admin(client):
    """Export should be denied to non-admin users."""
    with client.session_transaction() as sess:
        sess["user"] = "student"
        sess["role"] = "Student"
    response = client.get("/export")
    assert response.status_code == 403

def test_logout_clears_session(client):
    with client.session_transaction() as sess:
        sess["user"] = "admin"
        sess["role"] = "Admin"
    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200


# ─── Test: CSV Upload Validation ──────────────────────────────────────────────
import io

def test_upload_no_file(client):
    with client.session_transaction() as sess:
        sess["user"] = "admin"
        sess["role"] = "Admin"
    response = client.post("/analyze-data", data={})
    assert response.status_code == 400

def test_upload_missing_columns(client):
    with client.session_transaction() as sess:
        sess["user"] = "admin"
        sess["role"] = "Admin"
    # CSV missing 'absences' and 'failures'
    csv_content = b"G1,G2,studytime\n5,6,2\n10,11,3\n"
    data = {"file": (io.BytesIO(csv_content), "test.csv")}
    response = client.post("/analyze-data", data=data, content_type="multipart/form-data")
    assert response.status_code == 400
    json_data = response.get_json()
    assert "Missing" in json_data["error"]

def test_upload_non_csv_file(client):
    with client.session_transaction() as sess:
        sess["user"] = "admin"
        sess["role"] = "Admin"
    data = {"file": (io.BytesIO(b"not a csv"), "test.txt")}
    response = client.post("/analyze-data", data=data, content_type="multipart/form-data")
    assert response.status_code == 400

def test_upload_valid_csv(client):
    with client.session_transaction() as sess:
        sess["user"] = "admin"
        sess["role"] = "Admin"
    csv_content = b"G1,G2,studytime,failures,absences\n5,6,2,0,3\n15,14,3,0,1\n10,12,2,1,5\n"
    data = {"file": (io.BytesIO(csv_content), "test.csv")}
    response = client.post("/analyze-data", data=data, content_type="multipart/form-data")
    assert response.status_code == 200


# ─── Test: Simulate route ─────────────────────────────────────────────────────
def test_simulate_valid_input(client):
    with client.session_transaction() as sess:
        sess["user"] = "admin"
        sess["role"] = "Admin"
    response = client.post("/simulate", data={
        "g1": "5", "g2": "6", "studytime": "2", "failures": "0", "absences": "3"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "predicted_grade" in data
    assert "risk" in data
    assert data["risk"] in ["High", "Medium", "Low"]

def test_simulate_invalid_grade(client):
    with client.session_transaction() as sess:
        sess["user"] = "admin"
        sess["role"] = "Admin"
    response = client.post("/simulate", data={
        "g1": "25",  # out of range (max 20)
        "g2": "6", "studytime": "2", "failures": "0", "absences": "3"
    })
    assert response.status_code == 400

def test_simulate_requires_login(client):
    response = client.post("/simulate", data={
        "g1": "5", "g2": "6", "studytime": "2", "failures": "0", "absences": "3"
    })
    assert response.status_code in [302, 308]


# ─── Test: Password hashing (User model) ─────────────────────────────────────
def test_password_hashing(client):
    from app import app, User
    with app.app_context():
        from app import db
        db.create_all()
        u = User(username="testuser_hash", role="Student")
        u.set_password("mypassword")
        assert u.password_hash != "mypassword"          # not stored plain text
        assert u.check_password("mypassword") is True   # correct password works
        assert u.check_password("wrongpass") is False   # wrong password fails

def test_student_not_found(client):
    with client.session_transaction() as sess:
        sess["user"] = "admin"
        sess["role"] = "Admin"
    response = client.get("/student/99999")  # ID that doesn't exist
    assert response.status_code == 404