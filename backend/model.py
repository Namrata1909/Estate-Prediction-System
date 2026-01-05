import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

# Load dataset
data = pd.read_csv("../data/estate_data.csv")

# Select features (modify according to your dataset)
X = data[['area', 'bedrooms', 'bathrooms']]
y = data['price']

# Train model
model = LinearRegression()
model.fit(X, y)

# Save model
pickle.dump(model, open("estate_model.pkl", "wb"))

print("Model trained and saved successfully!")
