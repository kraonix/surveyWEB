import joblib
import pandas as pd

MODEL_PATH = "models/income_predictor.pkl"

class IncomePredictorService:

    def __init__(self):
        self.model = joblib.load(MODEL_PATH)

    def predict(self, age, study, year):

        df = pd.DataFrame([{
            "Age": age,
            "daily_study_hours": study,
            "What is your current academic year?": year
        }])

        return float(self.model.predict(df)[0])



