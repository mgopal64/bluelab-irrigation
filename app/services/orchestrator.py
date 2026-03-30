import pandas as pd
import numpy as np
import weather as w

# function for predicting if we should water
def should_we_water():
  
    # makes api call to open_meteo
    w.api_call()
    
    # thresholds
    sm_threshold = 0.285
    et0_threshold = 5.0
    delta = 0.03
    
    # data
    et0_daily = pd.read_csv("app/data/running_et0_values.csv")["et0_fao_evapotranspiration"].iloc[-1]
    current_sm = pd.read_csv("app/data/running_soil_precipitation.csv")["soil_moisture(m^3/m^3)"].iloc[-1]
    future_sm = np.array(pd.read_csv("app/data/predictions.csv")["0"])

    # already too low
    if current_sm < sm_threshold:
        return True

    # will be too low in next 6h
    if future_sm.min() < sm_threshold:
        return True

    # high ET and near threshold
    if et0_daily > et0_threshold and current_sm < sm_threshold + delta:
        return True

    return False

print(should_we_water())
