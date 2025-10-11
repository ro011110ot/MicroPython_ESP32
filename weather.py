"""
This module provides a function to fetch weather data from the OpenWeatherMap API.
"""

import os
import urequests as requests
from secrets import secrets
import time

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


def call():
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

        now = time.localtime()
        date_str = f"{now[0]:04d}.{now[1]:02d}.{now[2]:02d}"
        time_str = f"{now[3]:02d}:{now[4]:02d}"

        log_dir = "/temp_history"
        filename = f"{log_dir}/{date_str}.weather.csv"

        try:
            # Create directory if it doesn't exist
            if "temp_history" not in os.listdir("/"):
                os.mkdir(log_dir)

            # Write header if file doesn't exist
            if f"{date_str}.weather.csv" not in os.listdir(log_dir):
                with open(filename, "w") as f:
                    f.write(
                        "date;time;description;temperature;pressure;humidity;wind\n"
                    )

            # Append data to file
            with open(filename, "a") as f:
                csv_line = f"{date_str};{time_str};{description};{temperature:.1f} °C;{pressure} hPa;{humidity} %;{wind_speed_kmh} km/h\n"
                f.write(csv_line)

        except OSError as e:
            print(f"Failed to write to log file: {e}")

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
