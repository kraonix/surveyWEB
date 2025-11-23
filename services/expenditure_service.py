import joblib
import pandas as pd

class ExpenditureService:
    def __init__(self):
        self.model = joblib.load("models/expenditure_predictor.pkl")

    def predict(self, income, eat, academic, accommodation, part_time):
        # Create DataFrame for prediction
        input_df = pd.DataFrame([{
            "monthly_income": income,
            "eat_out_frequency": eat,
            "academic_year": academic,
            "accommodation": accommodation,
            "part_time": part_time
        }])

        pred = float(self.model.predict(input_df)[0])
        
        # Advice Logic
        if pred > income:
            advice = "Spend less"
        else:
            advice = "Good budgeting"
            
        return pred, advice
