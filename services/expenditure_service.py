import joblib
import pandas as pd

class ExpenditureService:
    def __init__(self):
        self.model = joblib.load("models/expenditure_predictor.pkl")

    def predict(self, income, daily, screen, wlb, eat, gender, academic, accomodation, part_time):

        df = pd.DataFrame([{
            "monthly_income": income,
            "daily_study_hours": daily,
            "weekly_academic_hours": 0,
            "screen_time": screen,
            "wlb_rating": wlb,
            "eat_out_frequency": eat,
            "Gender": gender,
            "What is your current academic year?": academic,
            "Which of the following best describes your primary accommodation?": accomodation,
            "part_time_work": part_time
        }])

        return float(self.model.predict(df)[0])
