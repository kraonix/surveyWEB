import pandas as pd
import os

def preprocess_eating_frequency(df):
    mapping = {
        "Never": 0,
        "1 time": 1,
        "1-2 times": 1.5,
        "2-3 times": 2.5,
        "3-4 times": 3.5,
        "4-5 times": 4.5,
        "5+ times": 5,
        "Often": 4,
        "Rarely": 1,
        "Sometimes": 2.5,
    }

    df["eat_out_frequency_numeric"] = df["eat_out_frequency"].map(mapping)
    df["exp_food"] = df["exp_food"].clip(lower=0, upper=20000)

    return df


def load_data(filepath="student_survey_data.csv"):
    # If filepath is relative, make it absolute based on current working directory or app root
    if not os.path.isabs(filepath):
        # Assuming the file is in the root of the project, same as app.py
        # This might need adjustment based on where the app is run from
        filepath = os.path.join(os.getcwd(), filepath)

    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        # Fallback or re-raise with clearer message
        raise FileNotFoundError(f"Data file not found at {filepath}")

    df.columns = df.columns.str.strip()

    # Rename columns for easier use
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

    # List of all money-related fields
    money_cols = [
        "monthly_income", "exp_rent", "exp_utilities", "exp_food",
        "exp_transport", "exp_supplies", "exp_entertainment",
        "exp_care", "exp_other"
    ]

    
    def clean_money(value):
        if pd.isna(value):
            return None

        value = str(value).strip()

        # Remove currency + commas
        value = value.replace("₹", "").replace(",", "").strip()

        # Patterns:
        # "< 5000" → 5000 (upper bound)
        # "> 30000" → 30000 (lower bound)
        # "5000 - 10000" → take AVERAGE
        if "<" in value:
            return float(value.replace("<", "").strip())

        if ">" in value:
            return float(value.replace(">", "").strip())

        if "-" in value:
            low, high = value.split("-")
            return (float(low.strip()) + float(high.strip())) / 2

        return float(value)

    # Apply cleaning to all money columns
    for col in money_cols:
        if col in df.columns:
             df[col] = df[col].apply(clean_money)

    # Convert screen time to numeric
    if "screen_time" in df.columns:
        df["screen_time"] = pd.to_numeric(df["screen_time"], errors="coerce")

    # Convert study hours to numeric
    if "daily_study_hours" in df.columns:
        df["daily_study_hours"] = pd.to_numeric(df["daily_study_hours"], errors="coerce")

    # Fix duplicates
    df = df.drop_duplicates()

    return df
