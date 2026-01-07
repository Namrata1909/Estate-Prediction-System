# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import sqlite3
# import pickle
# import numpy as np

# app = Flask(__name__)
# CORS(app)

# # ---------------- LOAD MODEL & ENCODERS ----------------
# model = pickle.load(open("estate_model.pkl", "rb"))
# furnish_encoder = pickle.load(open("furnishing_encoder.pkl", "rb"))
# location_encoder = pickle.load(open("location_encoder.pkl", "rb"))

# # ---------------- DATABASE CONNECTION ----------------
# def db_connection():
#     return sqlite3.connect("database.db")

# # ---------------- HOME ROUTE ----------------
# @app.route("/")
# def home():
#     return "Real Estate Price Prediction Backend is Running"

# # ---------------- REGISTER ROUTE ----------------
# @app.route("/register", methods=["POST"])
# def register():
#     data = request.json
#     username = data["username"]
#     password = data["password"]

#     conn = db_connection()
#     cursor = conn.cursor()

#     cursor.execute(
#         "CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)"
#     )

#     cursor.execute(
#         "INSERT INTO users VALUES (?, ?)",
#         (username, password)
#     )

#     conn.commit()
#     conn.close()

#     return jsonify({"message": "User Registered Successfully"})

# # ---------------- LOGIN ROUTE ----------------
# @app.route("/login", methods=["POST"])
# def login():
#     data = request.json
#     username = data["username"]
#     password = data["password"]

#     conn = db_connection()
#     cursor = conn.cursor()

#     cursor.execute(
#         "SELECT * FROM users WHERE username=? AND password=?",
#         (username, password)
#     )

#     user = cursor.fetchone()
#     conn.close()

#     if user:
#         return jsonify({"message": "Login Success"})
#     else:
#         return jsonify({"message": "Invalid Credentials"})

# # ---------------- PREDICTION ROUTE ----------------
# @app.route("/predict", methods=["POST"])
# def predict():
#     try:
#         data = request.json

#         # Numerical inputs
#         area = float(data["area"])
#         bedrooms = int(data["bedrooms"])
#         bathrooms = int(data["bathrooms"])
#         stories = int(data["stories"])
#         parking = int(data["parking"])

#         # Binary inputs (already 1/0 from frontend)
#         mainroad = int(data["mainroad"])
#         guestroom = int(data["guestroom"])
#         basement = int(data["basement"])
#         hotwaterheating = int(data["hotwaterheating"])
#         airconditioning = int(data["airconditioning"])
#         prefarea = int(data["prefarea"])

#         # Categorical inputs
#         furnishingstatus = data["furnishingstatus"]
#         location = data["location"]

#         furnishing_encoded = furnish_encoder.transform(
#             [furnishingstatus]
#         )[0]

#         location_encoded = location_encoder.transform(
#             [location]
#         )[0]

#         # Feature array (ORDER MUST MATCH model.py)
#         features = np.array([[
#             area, bedrooms, bathrooms, stories,
#             mainroad, guestroom, basement,
#             hotwaterheating, airconditioning,
#             parking, prefarea,
#             furnishing_encoded, location_encoded
#         ]])

#         prediction = model.predict(features)[0]

#         return jsonify({
#             "predicted_price": round(float(prediction), 2)
#         })

#     except Exception as e:
#         return jsonify({
#             "error": str(e)
#         }), 500

# # ---------------- RUN SERVER ----------------
# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)
CORS(app)

# ---------------- LOAD MODEL & ENCODERS ----------------
model = pickle.load(open("estate_model.pkl", "rb"))
furnish_encoder = pickle.load(open("furnishing_encoder.pkl", "rb"))
location_encoder = pickle.load(open("location_encoder.pkl", "rb"))

# ---------------- DATABASE CONNECTION ----------------
def db_connection():
    return sqlite3.connect("database.db")

# ---------------- HOME ROUTE ----------------
@app.route("/")
def home():
    return "Real Estate Price Prediction Backend is Running"

# ---------------- REGISTER ROUTE ----------------
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data["username"]
    password = data["password"]

    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT,
            password TEXT
        )
    """)

    cursor.execute(
        "INSERT INTO users VALUES (?, ?)",
        (username, password)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "User Registered Successfully"})

# ---------------- LOGIN ROUTE ----------------
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data["username"]
    password = data["password"]

    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"message": "Login Success"})
    else:
        return jsonify({"message": "Invalid Credentials"})

# ---------------- PRICE PREDICTION ROUTE ----------------
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json

        # Numerical inputs
        area = float(data["area"])
        bedrooms = int(data["bedrooms"])
        bathrooms = int(data["bathrooms"])
        stories = int(data["stories"])
        parking = int(data["parking"])

        # Binary inputs (1/0)
        mainroad = int(data["mainroad"])
        guestroom = int(data["guestroom"])
        basement = int(data["basement"])
        hotwaterheating = int(data["hotwaterheating"])
        airconditioning = int(data["airconditioning"])
        prefarea = int(data["prefarea"])

        # Categorical inputs
        furnishingstatus = data["furnishingstatus"]
        location = data["location"]

        furnishing_encoded = furnish_encoder.transform(
            [furnishingstatus]
        )[0]

        location_encoded = location_encoder.transform(
            [location]
        )[0]

        # Feature array (ORDER MUST MATCH model.py)
        features = np.array([[
            area, bedrooms, bathrooms, stories,
            mainroad, guestroom, basement,
            hotwaterheating, airconditioning,
            parking, prefarea,
            furnishing_encoded, location_encoded
        ]])

        prediction = model.predict(features)[0]

        return jsonify({
            "predicted_price": round(float(prediction), 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------- REAL-TIME MARKET TRENDS ROUTE ----------------
@app.route("/trends", methods=["GET"])
def market_trends():
    try:
        data = pd.read_csv("../data/estate_data.csv")

        # Average price per location
        trend_data = data.groupby("location")["price"].mean()

        return jsonify({
            "labels": list(trend_data.index),
            "values": list(trend_data.values)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    app.run(debug=True)
