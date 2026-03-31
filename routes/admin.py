from flask import Blueprint, render_template, session, send_file
from decorators import admin_required
from ml import regression_model, df, features
import io
 
admin_bp = Blueprint("admin", __name__)
 
 
@admin_bp.route("/admin-analytics")
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
 
 
@admin_bp.route("/export")
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