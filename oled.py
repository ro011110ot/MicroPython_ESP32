from machine import Pin, SoftI2C, Timer
import ssd1306_driver as ssd1306
import time
import weather

# --- Global Variables ---
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


def oled_hello():
    """A simple test function to display text."""
    oled.text("Hello, World 1!", 0, 0)
    oled.text("Hello, World 2!", 0, 10)
    oled.text("Hello, World 3!", 0, 20)
    oled.show()


def update_sensor_readings(timer):
    """
    Reads the last line of temp.csv and updates the global
    temperature and humidity variables.
    """
    global temp_val, hum
    try:
        with open("temp.csv", "r") as f:
            lines = f.readlines()
        if lines:
            last_line = lines[-1]
            parts = last_line.strip().split(";")
            if len(parts) >= 4:
                temp_with_unit = parts[2].strip()
                temp_val = temp_with_unit.split(" ")[0]
                hum = parts[3].strip()
    except OSError:
        temp_val = "N/A"
        hum = "N/A"


def update_weather_data(timer):
    """Fetches weather data and stores it globally."""
    global weather_data
    weather_data = weather.weather()


def oled_time(timer):
    """
    Updates the OLED display with the current time and the last known
    sensor readings from the global variables.
    """
    now = time.localtime()
    date_str = "{:04d}.{:02d}.{:02d}".format(now[0], now[1], now[2])
    time_str = "{:02d}:{:02d}".format(now[3], now[4])

    oled.fill(0)
    oled.text(date_str, 0, 0)
    oled.text(time_str, 0, 20)

    temp_str = f"Temp: {temp_val}"
    oled.text(temp_str, 0, 40)

    if temp_val != "N/A":
        text_width = len(temp_str) * 8
        oled.blit(ssd1306.DEGREE, text_width, 40)
        oled.text("C", text_width + 8, 40)

    oled.text(f"Hum: {hum}", 0, 50)
    oled.show()


def oled_weather(timer):
    """Displays weather data on the OLED."""
    oled.fill(0)
    if weather_data:
        oled.text("Weather:", 0, 0)
        oled.text(weather_data["description"], 0, 10)

        temp_str = f'Temp: {weather_data["temperature"]}'
        oled.text(temp_str, 0, 20)
        text_width = len(temp_str) * 8
        oled.blit(ssd1306.DEGREE, text_width, 20)
        oled.text("C", text_width + 8, 20)

        oled.text(f'Press: {weather_data["pressure"]}', 0, 30)
        oled.text(f'Hum: {weather_data["humidity"]}', 0, 40)
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


def start_timer():
    """
    Initializes and starts the timers for updating the display
    and reading sensor data.
    """
    update_sensor_readings(None)
    update_weather_data(None)  # Initial fetch

    # Timer to switch between displays every 5 seconds
    display_timer = Timer(0)
    display_timer.init(
        period=5000, mode=Timer.PERIODIC, callback=display_handler
    )

    # Timer to read local sensor data every 5 minutes
    sensor_timer = Timer(1)
    sensor_timer.init(
        period=300000, mode=Timer.PERIODIC, callback=update_sensor_readings
    )

    # Timer to fetch weather data every 30 minutes
    weather_timer = Timer(2)
    weather_timer.init(
        period=1800000, mode=Timer.PERIODIC, callback=update_weather_data
    )
