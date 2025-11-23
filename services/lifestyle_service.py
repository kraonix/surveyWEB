import joblib
import pandas as pd

MODEL_PATH = "models/lifestyle_predictor.pkl"

class LifestyleService:
    def __init__(self):
        self.model = joblib.load(MODEL_PATH)

    def predict(self, weekly_academic, daily_study, screen_time, part_time, age, academic_year, gender):
        """
        Predict work-life balance rating (1-5 scale)
        
        Args:
            weekly_academic: Weekly academic hours
            daily_study: Daily study hours
            screen_time: Screen time per day (hours)
            part_time: Part-time work (Yes/No)
            age: Age
            academic_year: Academic year (1st Year, 2nd Year, etc.)
            gender: Gender (Male/Female)
        """
        # Convert part_time to binary
        part_time_binary = 1 if str(part_time).strip().lower() in ["yes", "y", "1", "true"] else 0
        
        # Create base features
        weekly_academic_hours = float(weekly_academic)
        daily_study_hours = float(daily_study)
        screen_time_val = float(screen_time)
        
        # Feature engineering (matching the training script)
        total_study_hours = weekly_academic_hours + (daily_study_hours * 7)
        study_screen_ratio = daily_study_hours / (screen_time_val + 0.1)  # Add small value to avoid division by zero
        
        df = pd.DataFrame([{
            "weekly_academic_hours": weekly_academic_hours,
            "daily_study_hours": daily_study_hours,
            "screen_time": screen_time_val,
            "part_time_binary": part_time_binary,
            "Age": float(age),
            "What is your current academic year?": str(academic_year),
            "Gender": str(gender),
            "total_study_hours": total_study_hours,
            "study_screen_ratio": study_screen_ratio
        }])
        
        try:
            prediction = float(self.model.predict(df)[0])
            # Clamp prediction to 1-5 range
            prediction = max(1.0, min(5.0, prediction))
            return prediction
        except Exception as e:
            print(f"Prediction error: {e}")
            # Fallback: return a default value based on inputs
            return 3.0

