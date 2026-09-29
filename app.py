"""
Placement Predictor website ka Flask app.

Chalane ka tareeka:  python app.py
Phir browser me kholo:  http://127.0.0.1:5000
"""

import os

import joblib
import numpy as np
from flask import Flask, jsonify, render_template, request

# Pehle check karo ki model train hua hai ya nahi
if not os.path.exists("model.pkl"):
    print("Model nahi mila! Pehle ye command chalao: python train_model.py")
    input("(Band karne ke liye Enter dabao...)")
    exit()

app = Flask(__name__)
model = joblib.load("model.pkl")

# Form se aane wale fields (same order me model ko bhejte hain)
FEATURES = [
    "tenth_percent", "twelfth_percent", "cgpa", "internships",
    "projects", "aptitude_score", "communication_score", "work_experience",
]


@app.route("/")
def home():
    # Website ka main page dikhao
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    # JavaScript se student ka data aata hai (JSON format me)
    data = request.get_json()

    # Form ki values ko number me badlo aur model ko do
    values = [float(data[f]) for f in FEATURES]
    prob = model.predict_proba([values])[0][1]  # placed hone ka chance (0 to 1)

    placed = prob >= 0.5
    percent = round(prob * 100, 1)

    return jsonify(
        {
            "prediction": "Placed 🎉" if placed else "Not Placed 😕",
            "probability": percent,
            "message": (
                "Great! Aapka profile placement ke liye strong hai."
                if placed
                else "Abhi chances kam hain — skills improve karo, ho jayega!"
            ),
        }
    )


if __name__ == "__main__":
    print("=" * 50)
    print("Website chalu ho gayi!")
    print("Apne computer me kholo: http://127.0.0.1:5000")

    # Dusre computer/phone se kholne ke liye is computer ka IP address dikhao
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        print(f"Dusre system/phone me kholo: http://{ip}:5000")
        print("(Dono devices ka SAME WiFi/hotspot hona zaroori hai)")
    except Exception:
        print("(IP nahi dikha par website chal rahi hai)")
    print("(Note: Ye terminal band mat karna, website isi se chalti hai)")
    print("=" * 50)
    # host="0.0.0.0" => dusre devices bhi is website ko khol sakte hain
    app.run(debug=True, host="0.0.0.0")
