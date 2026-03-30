"""
train_model.py — Trains and evaluates both the regression and classification models.
Run this once to generate model.pkl and classifier_model.pkl.
"""

import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import (
    mean_squared_error, r2_score,
    confusion_matrix, classification_report, accuracy_score
)
import joblib
import numpy as np

# ─── Load Data ────────────────────────────────────────────────────────────────
df = pd.read_csv("data/student-mat.csv", sep=";")

features = ["G1", "G2", "studytime", "failures", "absences"]
X = df[features]

# ─── Risk label for classification ───────────────────────────────────────────
def classify(g):
    if g < 10:
        return 0   # High risk
    elif g < 15:
        return 1   # Medium risk
    else:
        return 2   # Low risk

# ─── Train/Test Split ─────────────────────────────────────────────────────────
X_train, X_test, y_train_reg, y_test_reg = train_test_split(
    X, df["G3"], test_size=0.2, random_state=42
)

y_class = df["G3"].apply(classify)
X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(
    X, y_class, test_size=0.2, random_state=42
)

# ─── Regression Model ─────────────────────────────────────────────────────────
print("=" * 50)
print("Training Regression Model (RandomForestRegressor)...")
reg_model = RandomForestRegressor(n_estimators=100, random_state=42)
reg_model.fit(X_train, y_train_reg)

reg_preds = reg_model.predict(X_test)
mse = mean_squared_error(y_test_reg, reg_preds)
r2 = r2_score(y_test_reg, reg_preds)

print(f"  MSE  : {mse:.4f}")
print(f"  R²   : {r2:.4f}")

# Cross-validation score
cv_scores = cross_val_score(reg_model, X, df["G3"], cv=5, scoring="r2")
print(f"  5-Fold CV R² : {np.mean(cv_scores):.4f} ± {np.std(cv_scores):.4f}")

# Feature importance
print("\n  Feature Importances:")
for feat, imp in zip(features, reg_model.feature_importances_):
    print(f"    {feat:12s}: {imp:.4f}")

joblib.dump(reg_model, "model.pkl")
print("\n  Regression model saved → model.pkl")

# ─── Classification Model ─────────────────────────────────────────────────────
print("=" * 50)
print("Training Classification Model (RandomForestClassifier)...")
clf_model = RandomForestClassifier(n_estimators=100, random_state=42)
clf_model.fit(X_train_c, y_train_c)

clf_preds = clf_model.predict(X_test_c)
acc = accuracy_score(y_test_c, clf_preds)

print(f"  Accuracy : {acc:.4f}")
print("\n  Confusion Matrix:")
print(confusion_matrix(y_test_c, clf_preds))
print("\n  Classification Report:")
print(classification_report(y_test_c, clf_preds, target_names=["High", "Medium", "Low"]))

# Cross-validation
cv_clf = cross_val_score(clf_model, X, y_class, cv=5, scoring="accuracy")
print(f"  5-Fold CV Accuracy: {np.mean(cv_clf):.4f} ± {np.std(cv_clf):.4f}")

joblib.dump(clf_model, "classifier_model.pkl")
print("\n  Classifier model saved → classifier_model.pkl")
print("=" * 50)
print("Done! Both models saved successfully.")