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
    try:
        weather_data = requests.get(open_weather_map_url)
        data = weather_data.json()

        # Weather Description
        description = data.get("weather")[0].get("main")

        # Temperature in Celsius
        raw_temperature = data.get("main").get("temp") - 273.15
        temperature = f"{raw_temperature:.1f}"

        # Pressure
        pressure = f'{data.get("main").get("pressure")}hPa'

        # Humidity
        humidity = f'{data.get("main").get("humidity")}%'

        # Wind
        # in mps
        # wind = f'{data.get("wind").get("speed")}mps {data.get("wind").get("deg")}*'
        # in km/h
        wind = f'{(data.get("wind").get("speed") * 3.6):.1f} km/h'
        return {
            "description": description,
            "temperature": temperature,
            "pressure": pressure,
            "humidity": humidity,
            "wind": wind,
        }
    except Exception as e:
        print(f"Error getting weather: {e}")
        return None
