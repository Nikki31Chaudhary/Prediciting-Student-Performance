import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report
import joblib

df = pd.read_csv("data/student-mat.csv", sep=";")

features = ["G1", "G2", "studytime", "failures", "absences"]

# Create risk label
def classify(g):
    if g < 10:
        return 0   # High
    elif g < 15:
        return 1   # Medium
    else:
        return 2   # Low

df["risk_label"] = df["G3"].apply(classify)

X = df[features]
y = df["risk_label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier()
model.fit(X_train, y_train)

pred = model.predict(X_test)

print("Confusion Matrix:")
print(confusion_matrix(y_test, pred))

print("\nClassification Report:")
print(classification_report(y_test, pred))

joblib.dump(model, "classifier_model.pkl")
print("Classifier model saved!")