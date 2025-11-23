import os

class Config:
    DEBUG = os.environ.get("DEBUG", "True") == "True"
    DATA_PATH = os.environ.get("DATA_PATH", "student_survey_data.csv")
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key-please-change")
