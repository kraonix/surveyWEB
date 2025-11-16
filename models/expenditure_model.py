import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
import joblib, os


# ------------ CLEAN MONEY -------------
def clean_money(x):
    if pd.isna(x):
        return None
    x = str(x).replace("₹", "").replace(",", "").strip()
    if "-" in x:
        a, b = x.split("-")
        return (float(a.strip()) + float(b.strip())) / 2
    if x.startswith("<"):
        return float(x.replace("<", "").strip())
    if x.startswith(">"):
        return float(x.replace(">", "").strip())
    try:
        return float(x)
    except:
        return None


# ------------ LOAD DATA -------------
df = pd.read_csv("student_survey_data.csv")
df.columns = df.columns.str.strip()


# ------------ RENAME COLUMNS LIKE app.py -------------
df = df.rename(columns={
    "On average, how many hours do you spend on academic activities (classes, studying, assignments) per week?": "weekly_academic_hours",
    "How many hours do you study daily (outside classes)?": "daily_study_hours",
    "How would you rate your overall satisfaction with your current work-life balance?": "wlb_rating",
    "What is your primary source of income (if any)?": "income_source",
    "Average monthly allowance / income (₹)": "monthly_income",

    "Approximately, what is your monthly expenditure on the following categories? [Rent/Accommodation]": "exp_rent",
    "Approximately, what is your monthly expenditure on the following categories? [Utilities (electricity, internet, etc.)]": "exp_utilities",
    "Approximately, what is your monthly expenditure on the following categories? [Groceries/Food]": "exp_food",
    "Approximately, what is your monthly expenditure on the following categories? [Transportation]": "exp_transport",
    "Approximately, what is your monthly expenditure on the following categories? [Academic Supplies (books, stationery)]": "exp_supplies",
    "Approximately, what is your monthly expenditure on the following categories? [Social/Entertainment]": "exp_entertainment",
    "Approximately, what is your monthly expenditure on the following categories? [Personal Care]": "exp_care",
    "Approximately, what is your monthly expenditure on the following categories? [Other]": "exp_other",

    "How often do you eat out or order takeout per week?": "eat_out_frequency",
    "What’s your average screen time per day (hrs)?": "screen_time",
    "Do you participate in any part-time work / freelancing?": "part_time_work"
})


# ------------ CLEAN EXPENDITURE COLUMNS -------------
expense_cols = [
    "exp_rent", "exp_utilities", "exp_food", "exp_transport",
    "exp_supplies", "exp_entertainment", "exp_care", "exp_other"
]

for col in expense_cols:
    df[col] = df[col].apply(clean_money)

# CLEAN monthly income also
df["monthly_income"] = df["monthly_income"].apply(clean_money)

df["total_exp"] = df[expense_cols].sum(axis=1)



# ------------ MANUAL CATEGORY TO NUMERIC -------------

# Gender
df["Gender"] = df["Gender"].map({"Male": 0, "Female": 1})

# Part-time
df["part_time_work"] = df["part_time_work"].map({"Yes": 1, "No": 0})

# Academic year
df["What is your current academic year?"] = df["What is your current academic year?"].map({
    "1st Year": 1,
    "2nd Year": 2,
    "3rd Year": 3,
    "4th Year": 4
})

# Accommodation
df["Which of the following best describes your primary accommodation?"] = df["Which of the following best describes your primary accommodation?"].astype("category").cat.codes

# Eat-out frequency
eat_map = {
    "Never": 0,
    "1 time": 1,
    "1-2 times": 1.5,
    "2-3 times": 2.5,
    "3-4 times": 3.5,
    "4-5 times": 4.5,
    "5+ times": 5,
    "Often": 4,
    "Rarely": 1,
    "Sometimes": 2.5
}
df["eat_out_frequency"] = df["eat_out_frequency"].map(eat_map)


# ------------ DROP NA -------------
features = [
    "monthly_income",
    "daily_study_hours",
    "weekly_academic_hours",
    "screen_time",
    "wlb_rating",
    "eat_out_frequency",
    "Gender",
    "What is your current academic year?",
    "Which of the following best describes your primary accommodation?",
    "part_time_work"
]

df = df.dropna(subset=features + ["total_exp"])


# ------------ MODEL TRAINING -------------
X = df[features]
y = df["total_exp"]

model = RandomForestRegressor(
    n_estimators=350,
    max_depth=15,
    random_state=42
)

model.fit(X, y)

r2 = r2_score(y, model.predict(X))

print("\nEXPENDITURE MODEL R²:", r2)


os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/expenditure_predictor.pkl")

print("Model saved → models/expenditure_predictor.pkl")
