import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
import joblib
import os


# ---------------- MONEY CLEANING ----------------
def clean_money(value):
    if pd.isna(value):
        return None

    value = str(value).replace("₹", "").replace(",", "").strip()

    if "<" in value:
        return float(value.replace("<", "").strip())

    if ">" in value:
        return float(value.replace(">", "").strip())

    if "-" in value:
        low, high = value.split("-")
        return (float(low.strip()) + float(high.strip())) / 2

    return float(value)


# ---------------- LOAD DATA ----------------
df = pd.read_csv("student_survey_data.csv")
df.columns = df.columns.str.strip()

# Rename columns (match app.py)
df = df.rename(columns={
    "How many hours do you study daily (outside classes)?": "daily_study_hours",
    "Average monthly allowance / income (₹)": "monthly_income"
})


# Clean income
df["monthly_income"] = df["monthly_income"].apply(clean_money)

# Drop missing values
df = df.dropna(subset=["Age", "daily_study_hours", "What is your current academic year?", "monthly_income"])


# ---------------- FEATURES ----------------
X = df[["Age", "daily_study_hours", "What is your current academic year?"]]
y = df["monthly_income"]

# One-hot encode academic year
preprocess = ColumnTransformer(
    transformers=[
        ("year_enc", OneHotEncoder(handle_unknown="ignore"), ["What is your current academic year?"])
    ],
    remainder="passthrough"
)

# ---------------- MODEL ----------------
model = Pipeline([
    ("prep", preprocess),
    ("rf", RandomForestRegressor(
        n_estimators=200,
        random_state=42
    ))
])

print("Training simple model...")
model.fit(X, y)

r2 = model.score(X, y)
print("\nModel R²:", r2)


# ---------------- SAVE ----------------
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/income_predictor.pkl")

print("\nSaved → models/income_predictor.pkl")
