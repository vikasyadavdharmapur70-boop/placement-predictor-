"""
Placement prediction model train karne ka simple script.

Chalane ka tareeka:  python train_model.py

Ye script:
1. Ek sample dataset banata hai (placement_data.csv)
2. Random Forest model train karta hai
3. Model ko model.pkl me save karta hai
"""

import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# ---------------------------------------------------------
# Step 1: Sample dataset banao (2000 students ka data)
# ---------------------------------------------------------
rng = np.random.default_rng(42)
n = 2000

tenth = np.clip(rng.normal(78, 9, n), 40, 100)          # 10th percentage
twelfth = np.clip(rng.normal(75, 10, n), 40, 100)       # 12th percentage
cgpa = np.clip(rng.normal(7.5, 0.9, n), 4, 10)          # college CGPA
internships = rng.integers(0, 4, n)                     # 0-3 internships
projects = rng.integers(0, 7, n)                        # 0-6 projects
aptitude = np.clip(rng.normal(65, 15, n), 0, 100)       # aptitude score
communication = np.clip(rng.normal(68, 14, n), 0, 100)  # communication score
work_exp = rng.integers(0, 2, n)                        # 0 = No, 1 = Yes

# Placement chance nikalo (0-100 ka score) aur usi se result decide karo
chance = (
    (cgpa / 10) * 30
    + (tenth / 100) * 15
    + (twelfth / 100) * 15
    + internships * 8
    + projects * 2
    + aptitude * 0.15
    + communication * 0.15
    + work_exp * 5
)
placed = (chance + rng.normal(0, 8, n) > 75).astype(int)  # thoda randomness

df = pd.DataFrame(
    {
        "tenth_percent": np.round(tenth, 1),
        "twelfth_percent": np.round(twelfth, 1),
        "cgpa": np.round(cgpa, 2),
        "internships": internships,
        "projects": projects,
        "aptitude_score": np.round(aptitude, 1),
        "communication_score": np.round(communication, 1),
        "work_experience": work_exp,
        "placed": placed,
    }
)
df.to_csv("placement_data.csv", index=False)
print(f"Dataset ban gaya: placement_data.csv ({n} students)")
print(f"Placed students: {df['placed'].mean() * 100:.0f}%")

# ---------------------------------------------------------
# Step 2: Model train karo
# ---------------------------------------------------------
FEATURES = [
    "tenth_percent", "twelfth_percent", "cgpa", "internships",
    "projects", "aptitude_score", "communication_score", "work_experience",
]

X = df[FEATURES]           # input (student details)
y = df["placed"]           # output (0 = Not Placed, 1 = Placed)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# ---------------------------------------------------------
# Step 3: Accuracy check karo aur model save karo
# ---------------------------------------------------------
accuracy = model.score(X_test, y_test)
print(f"Model accuracy: {accuracy * 100:.1f}%")

joblib.dump(model, "model.pkl")
print("Model save ho gaya: model.pkl")
print("\nAb website chalao:  python app.py")
