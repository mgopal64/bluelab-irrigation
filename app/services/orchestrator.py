import pandas as pd
import numpy as np

et0_data = pd.read_csv("app/data/running_et0_values.csv")["et0_fao_evapotranspiration"].iloc[-1]

sm_data = pd.read_csv("app/data/running_soil_precipitation.csv")["soil_moisture(m^3/m^3)"].iloc[-1]

future_sm_data = np.array(pd.read_csv("app/data/predictions.csv")["0"])


# function for predicting if we should water
def should_we_water(current_sm = sm_data, future_sm = future_sm_data, et0_daily = et0_data):
    sm_threshold = 0.285
    et0_threshold = 5.0
    delta = 0.03

    # Condition 1: already too low
    if current_sm < sm_threshold:
        return True

    # Condition 2: will be too low in next 6h
    if future_sm.min() < sm_threshold:
        return True

    # high ET  and near threshold
    if et0_daily > et0_threshold and current_sm < sm_threshold + delta:
        return True

    return False

print(should_we_water())
