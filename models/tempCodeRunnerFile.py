import pandas as pd

df = pd.read_csv("student_survey_data.csv")
df.columns = df.columns.str.strip()

for i, col in enumerate(df.columns):
    print(i, "->", repr(col))