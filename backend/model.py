# import pandas as pd
# from sklearn.linear_model import LinearRegression
# import pickle

# # Load dataset
# data = pd.read_csv("../data/estate_data.csv")

# # Select features (modify according to your dataset)
# X = data[['area', 'bedrooms', 'bathrooms']]
# y = data['price']

# # Train model
# model = LinearRegression()
# model.fit(X, y)

# # Save model
# pickle.dump(model, open("estate_model.pkl", "wb"))

# print("Model trained and saved successfully!")

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
import pickle

# Load dataset
data = pd.read_csv("../data/estate_data.csv")

# Binary encoding (yes/no → 1/0)
binary_cols = [
    "mainroad", "guestroom", "basement",
    "hotwaterheating", "airconditioning", "prefarea"
]

for col in binary_cols:
    data[col] = data[col].map({"yes": 1, "no": 0})

# Encode furnishing status
furnish_encoder = LabelEncoder()
data["furnishingstatus"] = furnish_encoder.fit_transform(
    data["furnishingstatus"]
)

# Encode location
location_encoder = LabelEncoder()
data["location"] = location_encoder.fit_transform(
    data["location"]
)

# Feature set (ALL INPUT FEATURES)
X = data[
    [
        "area", "bedrooms", "bathrooms", "stories",
        "mainroad", "guestroom", "basement",
        "hotwaterheating", "airconditioning",
        "parking", "prefarea", "furnishingstatus",
        "location"
    ]
]

# Target
y = data["price"]

# Train model
model = LinearRegression()
model.fit(X, y)

# Save model & encoders
pickle.dump(model, open("estate_model.pkl", "wb"))
pickle.dump(furnish_encoder, open("furnishing_encoder.pkl", "wb"))
pickle.dump(location_encoder, open("location_encoder.pkl", "wb"))

print("Model trained successfully using estate_data.csv")
