"""
This module provides a function to fetch weather data from the OpenWeatherMap API.
"""
import gc
import json
import requests
from secrets import secrets

city = secrets["city"]
country_code = secrets["country_code"]


# set your unique OpenWeatherMap.org URL
open_weather_map_url = (
    "http://api.openweathermap.org/data/2.5/weather?q="
    + city
    + ","
    + country_code
    + "&APPID="
    + secrets["openweather_api_key"]
)


def weather():
    """
    Fetches weather data from the OpenWeatherMap API and returns it as a dictionary.

    Returns:
        dict: A dictionary containing weather information:
              {"description", "temperature", "pressure", "humidity", "wind"}
              Returns None if an error occurs.
    """
    try:
        weather_data = requests.get(open_weather_map_url)
        data = weather_data.json()

        description = data.get("weather")[0].get("main")
        temperature = data.get("main").get("temp") - 273.15
        pressure = data.get("main").get("pressure")
        humidity = data.get("main").get("humidity")
        wind_speed_mps = data.get("wind").get("speed")
        wind_speed_kmh = f"{(wind_speed_mps * 3.6):.1f}"

        return {
            "description": description,
            "temperature": temperature,
            "pressure": pressure,
            "humidity": humidity,
            "wind": f"{wind_speed_kmh} km/h",
        }
    except Exception as e:
        print(f"Error getting weather: {e}")
        return None
