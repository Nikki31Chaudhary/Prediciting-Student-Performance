from flask import Flask
from extensions import limiter, cors
from models import db, User


def seed_users():
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


def create_app():
    app = Flask(__name__)
    app.secret_key = "change-this-to-a-random-secret-in-production"

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    limiter.init_app(app)
    cors.init_app(app, origins=["http://localhost:5000", "http://127.0.0.1:5000"])

    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.student import student_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(student_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
        seed_users()
    app.run(debug=False)