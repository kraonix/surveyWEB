import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split

# ---------------- SYNTHETIC DATA GENERATION ----------------
# We need to generate data where expenditure is roughly +/- 10% of income.
# We will use the requested features to create slight variations.

n_samples = 1000
np.random.seed(42)

# 1. Income (5k to 50k)
incomes = np.random.randint(5000, 50000, n_samples)

# 2. Categorical Features
eat_freqs = np.random.choice(["Never", "1 time", "1-2 times", "2-3 times", "3-4 times", "4-5 times", "5+ times", "Rarely", "Sometimes", "Often"], n_samples)
years = np.random.choice(["1st Year", "2nd Year", "3rd Year", "4th Year"], n_samples)
accommodations = np.random.choice(["Hostel", "PG", "Flat/Apartment", "With Family"], n_samples)
part_times = np.random.choice(["Yes", "No"], n_samples)

# 3. Calculate Base Expenditure (Target = Income)
# We start with expenditure = income
expenditures = incomes.astype(float).copy()

# 4. Apply Modifiers based on features (to create variance within +/- 10%)
# This logic creates the "ground truth" for our synthetic model.

for i in range(n_samples):
    modifier = 0.0
    
    # Eating Out: More freq = higher exp
    if eat_freqs[i] in ["4-5 times", "5+ times", "Often"]: modifier += 0.05
    elif eat_freqs[i] in ["Never", "Rarely"]: modifier -= 0.03
    
    # Accommodation: Flat > PG > Hostel > Family
    if accommodations[i] == "Flat/Apartment": modifier += 0.05
    elif accommodations[i] == "With Family": modifier -= 0.05
    
    # Part Time: Might mean more spending power or more expenses
    if part_times[i] == "Yes": modifier += 0.02
    
    # Random noise (+/- 2%)
    noise = np.random.uniform(-0.02, 0.02)
    
    # Apply modifier (clamped to +/- 10%)
    total_modifier = np.clip(modifier + noise, -0.10, 0.10)
    
    expenditures[i] = incomes[i] * (1 + total_modifier)

# ---------------- DATAFRAME ----------------
df = pd.DataFrame({
    "monthly_income": incomes,
    "eat_out_frequency": eat_freqs,
    "academic_year": years,
    "accommodation": accommodations,
    "part_time": part_times,
    "total_exp": expenditures
})

print("Synthetic Data Sample:")
print(df.head())

# ---------------- TRAINING ----------------
X = df[["monthly_income", "eat_out_frequency", "academic_year", "accommodation", "part_time"]]
y = df["total_exp"]

# Pipeline
categorical_features = ["eat_out_frequency", "academic_year", "accommodation", "part_time"]

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ],
    remainder='passthrough'
)

pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
pipeline.fit(X_train, y_train)

score = pipeline.score(X_test, y_test)
print(f"Model R2 Score: {score}")

# Save
joblib.dump(pipeline, "models/expenditure_predictor.pkl")
print("Model saved to models/expenditure_predictor.pkl")
