import dht11
from machine import Pin, SoftI2C
import time
import ssd1306_driver as ssd1306
import weather


# --- Global Variables ---
# These variables are used to share state between the timer callbacks.
# This is necessary because timers in MicroPython do not support passing arguments to callbacks.
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
    temp_val, hum = dht11.measure()


def update_weather_data(timer):
    """Fetches weather data and stores it globally."""
    global weather_data
    weather_data = weather.call()


def oled_time(timer):
    """
    Updates the OLED display with the current date, time, and sensor readings.

    Display Layout:
    - Line 1: Date (YYYY.MM.DD)
    - Line 3: Time (HH:MM)
    - Line 5: Temperature (e.g., "Temp: 23.4 °C")
    - Line 6: Humidity (e.g., "Hum: 45.6 %")
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
    Displays weather data on the OLED screen.

    Display Layout:
    - Line 1: "Weather:"
    - Line 2: Weather description
    - Line 3: Temperature
    - Line 4: Pressure
    - Line 5: Humidity
    - Line 6: Wind speed
    """
    oled.fill(0)
    if weather_data:
        oled.text("Weather:", 0, 0)
        oled.text(weather_data["description"], 0, 10)

        temp_str = f'Temp: {weather_data["temperature"]:.1f}'
        oled.text(temp_str, 0, 20)
        text_width = len(temp_str) * 8
        oled.blit(ssd1306.DEGREE, text_width, 20)
        oled.text("C", text_width + 8, 20)

        oled.text(f'Press: {weather_data["pressure"]} hPa', 0, 30)
        oled.text(f'Hum: {weather_data["humidity"]:.1f} %', 0, 40)
        oled.text(f'Wind: {weather_data["wind"]}', 0, 50)
    else:
        oled.text("Weather data", 0, 20)
        oled.text("not available", 0, 30)
    oled.show()


def display_handler(timer):
    """Switches between time and weather display."""
    global show_weather
    if show_weather:
        oled_weather(timer)
    else:
        oled_time(timer)
    # Toggle for the next cycle, but only if there is weather data
    if weather_data:
        show_weather = not show_weather
