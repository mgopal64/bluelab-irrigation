# Calls Open-Meteo API to get weather forecasts and ET_0.

import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
def api_call():
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
      "latitude": 42.27075250858827,
      "longitude": -83.58226485882234,
      "daily": "et0_fao_evapotranspiration",
      "hourly": ["soil_moisture_0_to_1cm", "soil_moisture_1_to_3cm", "precipitation", "soil_moisture_3_to_9cm", "soil_moisture_9_to_27cm"],
      "timezone": "America/New_York",
      "forecast_days": 1,
    }
    responses = openmeteo.weather_api(url, params = params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_soil_moisture_0_to_1cm = hourly.Variables(0).ValuesAsNumpy()
    hourly_soil_moisture_1_to_3cm = hourly.Variables(1).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(2).ValuesAsNumpy()
    hourly_soil_moisture_3_to_9cm = hourly.Variables(3).ValuesAsNumpy()
    hourly_soil_moisture_9_to_27cm = hourly.Variables(4).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
      start = pd.to_datetime(hourly.Time() + response.UtcOffsetSeconds(), unit = "s", utc = True),
      end =  pd.to_datetime(hourly.TimeEnd() + response.UtcOffsetSeconds(), unit = "s", utc = True),
      freq = pd.Timedelta(seconds = hourly.Interval()),
      inclusive = "left"
    )}

    hourly_data["soil_moisture(m^3/m^3)"] = (hourly_soil_moisture_0_to_1cm + hourly_soil_moisture_1_to_3cm + hourly_soil_moisture_3_to_9cm + hourly_soil_moisture_9_to_27cm) / 4
    hourly_data["precipitation(mm)"] = hourly_precipitation

    hourly_dataframe = pd.DataFrame(data = hourly_data)

    # Process daily data. The order of variables needs to be the same as requested.
    daily = response.Daily()
    daily_et0_fao_evapotranspiration = daily.Variables(0).ValuesAsNumpy()

    daily_data = {"date": pd.date_range(
      start = pd.to_datetime(daily.Time() + response.UtcOffsetSeconds(), unit = "s", utc = True),
      end =  pd.to_datetime(daily.TimeEnd() + response.UtcOffsetSeconds(), unit = "s", utc = True),
      freq = pd.Timedelta(seconds = daily.Interval()),
      inclusive = "left"
    )}

    # save et0 to a csv
    daily_data["et0_fao_evapotranspiration"] = daily_et0_fao_evapotranspiration

    daily_dataframe = pd.DataFrame(data = daily_data)
    daily_dataframe = daily_dataframe.set_index("date")
    daily_dataframe.to_csv("app/data/running_et0_values.csv")

    # Ensure time awareness and get current time
    hourly_dataframe['date'] = pd.to_datetime(hourly_dataframe['date']).dt.tz_convert('America/New_York')
    now = pd.Timestamp.now(tz='America/New_York')
    current = hourly_dataframe.iloc[(hourly_dataframe['date'] - now).abs().argsort()[:1]]

    create_features(current).to_csv("app/data/running_soil_precipitation.csv")


# function for getting date
def create_features(df):
    df = df.copy()
    df = df.set_index("date")
    # gets all time information
    df["hour"] = df.index.hour
    df["day"] = df.index.dayofweek
    df["month"] = df.index.month
    df["year"] = df.index.year
    df["quarter"] = df.index.quarter
    return df
  
  
# def append_to_data(sp, et0):
#     sp_df = pd.read_csv("app/data/running_soil_precipitation.csv")
#     et0_df = pd.read_csv("app/data/running_et0_values.csv")
#     if sp.index > sp_df.tail(1).index:
#         sp.to_csv("app/data/running_soil_precipitation.csv", mode='a', header=False, index=True)
#     if et0.index > et0_df.tail(1).index:
#         sp.to_csv("app/data/running_et0_values.csv", mode='a', header=False, index=True)

api_call()