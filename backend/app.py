from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import pickle
import numpy as np

app = Flask(__name__)
CORS(app)   # ⭐⭐ VERY IMPORTANT ⭐⭐

model = pickle.load(open("estate_model.pkl", "rb"))

def db_connection():
    return sqlite3.connect("database.db")

@app.route("/")
def home():
    return "Real Estate Price Prediction Backend is Running"

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users VALUES (?, ?)",
        (data["username"], data["password"])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "User Registered Successfully"})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (data["username"], data["password"])
    )
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"message": "Login Success"})
    else:
        return jsonify({"message": "Invalid Credentials"})
    
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json

        area = float(data["area"])
        bedrooms = float(data["bedrooms"])
        bathrooms = float(data["bathrooms"])

        features = np.array([[area, bedrooms, bathrooms]])
        prediction = model.predict(features)[0]

        return jsonify({
            "predicted_price": round(float(prediction), 2)
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
