import joblib
import pandas as pd
 
regression_model = joblib.load("model.pkl")
classifier_model = joblib.load("classifier_model.pkl")
 
df = pd.read_csv("data/student-mat.csv", sep=";")
 
features = ["G1", "G2", "studytime", "failures", "absences"]
REQUIRED_CSV_COLUMNS = set(features)