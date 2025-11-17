import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

df = pd.read_csv("student_survey_data.csv")

# Clean money fields
def clean_money(v):
    if pd.isna(v):
        return None

    v = str(v).replace("₹", "").replace(",", "").strip()

    if "<" in v:
        return float(v.replace("<", "").strip())
    if ">" in v:
        return float(v.replace(">", "").strip())
    if "-" in v:
        a, b = v.split("-")
        return (float(a.strip()) + float(b.strip())) / 2

    return float(v)

df["exp_rent"]        = df.iloc[:,11].apply(clean_money)
df["exp_utilities"]   = df.iloc[:,12].apply(clean_money)
df["exp_food"]        = df.iloc[:,13].apply(clean_money)
df["exp_transport"]   = df.iloc[:,14].apply(clean_money)
df["exp_supplies"]    = df.iloc[:,15].apply(clean_money)
df["exp_entertainment"]=df.iloc[:,16].apply(clean_money)
df["exp_care"]        = df.iloc[:,17].apply(clean_money)
df["exp_other"]       = df.iloc[:,18].apply(clean_money)

df["total_exp"] = df[[
    "exp_rent","exp_utilities","exp_food","exp_transport",
    "exp_supplies","exp_entertainment","exp_care","exp_other"
]].sum(axis=1)

# Our simple model only uses 3 features:
X = df[["exp_rent", "exp_food", "exp_transport"]]
y = df["total_exp"]

# Remove rows with missing values
X = X.dropna()
y = y.loc[X.index]

# Train model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestRegressor(n_estimators=200)
model.fit(X_train, y_train)

# Accuracy
r2 = r2_score(y_test, model.predict(X_test))
print("Model R2:", r2)

# Save
joblib.dump(model, "models/expenditure_model.pkl")

with open("models/expenditure_accuracy.txt", "w") as f:
    f.write(str(r2))
