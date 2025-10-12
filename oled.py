"""
This module manages the OLED display, showing time, sensor, and weather data.

It uses global variables to share state between timer callbacks, as MicroPython's
Timer objects do not support passing arguments to callbacks.
"""

# Standard Library
import time

# Third-Party
from machine import Pin, SoftI2C

# Local Application
import dht11
import ssd1306_driver as ssd1306
import weather

# --- Global Variables ---
# These variables are used to share state between the timer callbacks.
temp_val = "N/A"
hum = "N/A"
weather_data = None
show_weather = False

# --- Hardware Setup ---
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# --- Functions ---


def update_sensor_readings(timer):
    """Reads sensor data from dht11 and updates global variables."""
    global temp_val, hum
    temp_val, hum = dht11.get_data()


def update_weather_data(timer):
    """Fetches weather data from the API and stores it globally."""
    global weather_data
    weather_data = weather.get_data()


def oled_time(timer):
    """
    Updates the OLED display with the current date, time, and sensor readings.
    """
    now = time.localtime()
    date_str = f"{now[0]:04d}.{now[1]:02d}.{now[2]:02d}"
    time_str = f"{now[3]:02d}:{now[4]:02d}"

    oled.fill(0)
    oled.text(date_str, 0, 0)
    oled.text(time_str, 0, 20)

    if temp_val is not None and temp_val != "N/A":
        temp_str = f"Temp: {temp_val:.1f}"
        oled.text(temp_str, 0, 40)
        text_width = len(temp_str) * 8
        oled.blit(ssd1306.DEGREE, text_width, 40)
        oled.text("C", text_width + 8, 40)
    else:
        oled.text("Temp: N/A", 0, 40)

    if hum is not None and hum != "N/A":
        oled.text(f"Hum: {hum:.1f} %", 0, 50)
    else:
        oled.text("Hum: N/A", 0, 50)
    oled.show()


def oled_weather(timer):
    """
    Displays weather data on the OLED screen, handling missing data gracefully.
    """
    oled.fill(0)
    oled.text("Weather:", 0, 0)

    if weather_data and all(val is not None for val in weather_data):
        # weather_data is a tuple: (temp, pressure, humidity, wind_speed, wind_deg, weather_desc)

        # Description
        oled.text(str(weather_data[5]), 0, 10)

        # Temperature
        temp_str = f"Temp: {weather_data[0]:.1f}"
        oled.text(temp_str, 0, 20)
        text_width = len(temp_str) * 8
        oled.blit(ssd1306.DEGREE, text_width, 20)
        oled.text("C", text_width + 8, 20)

        # Pressure
        oled.text(f"Press: {weather_data[1]} hPa", 0, 30)

        # Humidity
        oled.text(f"Hum: {weather_data[2]:.1f} %", 0, 40)

        # Wind Speed
        oled.text(f"Wind: {weather_data[3]:.1f} m/s", 0, 50)
    else:
        oled.text("Data not", 0, 20)
        oled.text("available", 0, 30)
        oled.text("(Network Error)", 0, 40)

    oled.show()


def display_handler(timer):
    """Switches between the time/sensor display and the weather display."""
    global show_weather
    if show_weather:
        oled_weather(timer)
    else:
        oled_time(timer)

    # Toggle for the next cycle, but only if there is weather data
    if weather_data and all(val is not None for val in weather_data):
        show_weather = not show_weather
