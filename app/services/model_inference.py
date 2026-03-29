# Seena's model .joblib service will be referenced here
import joblib
import numpy as np
import pandas as pd

model = joblib.load("app/models/soil_moisture_rf.pkl")
data = pd.read_csv("app/data/running_soil_precipitation.csv")

FEATURES_IN = model.feature_names_in_
  

# def get_input():
#     return {
#         'hour': int(input("Hour (0-23): ")),
#         'day': int(input("Day: ")),
#         'month': int(input("Month (1-12): ")),
#         'quarter': int(input("Quarter (1-4): ")),
#         'year': int(input("Year: ")),
#         'soil_moisture(m^3/m^3)': float(input("Current soil moisture (m^3/m^3): ")),
#         'precipitation(mm)': float(input("Precipitation (mm): ")),
#     }

# function for predicting 6 future hours of soil moisture
def predict_soil_moisture(features = data.tail(1)):
    X = features[FEATURES_IN]
    return model.predict(X)[0]

features = data.tail(1)
print(predict_soil_moisture())

df = pd.DataFrame(predict_soil_moisture())

df.to_csv("app/data/predictions.csv")
