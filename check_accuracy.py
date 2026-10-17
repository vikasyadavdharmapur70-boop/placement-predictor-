"""
Model ki accuracy check karne ka script (model.pkl ko chhedta nahi,
kuch train ya save nahi karta — sirf test karta hai).

Chalane ka tareeka:  python check_accuracy.py
"""

import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

FEATURES = [
    "tenth_percent", "twelfth_percent", "cgpa", "internships",
    "projects", "aptitude_score", "communication_score", "work_experience",
]

# ---------------------------------------------------------
# Step 1: Data load karo aur wahi split lo jo training me tha
# ---------------------------------------------------------
df = pd.read_csv("placement_data.csv")
X = df[FEATURES]
y = df["placed"]

# Same split jo train_model.py me use hua tha (random_state=42)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ---------------------------------------------------------
# Step 2: Saved model load karo aur score nikalo
# ---------------------------------------------------------
model = joblib.load("model.pkl")

train_acc = model.score(X_train, y_train)
test_acc = model.score(X_test, y_test)

print(f"Dataset: {len(df)} students")
print(f"Training accuracy: {train_acc * 100:.1f}%")
print(f"Test accuracy:     {test_acc * 100:.1f}%")

# ---------------------------------------------------------
# Step 3: Thoda detail — confusion matrix + report
# ---------------------------------------------------------
y_pred = model.predict(X_test)

print("\nConfusion Matrix (test set):")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))
