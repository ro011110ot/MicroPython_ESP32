"""
This module configures and starts the hardware timers for periodic tasks.

Two timers are used:
- A display timer that cycles through different OLED screens.
- A sensor timer that periodically reads sensor data, fetches weather data,
  and logs everything.
"""

# Third-Party
from machine import Timer

# Local Application
import data_logger
import oled
import wifi


def weather_dht11_wrapper(timer):
    """
    Timer callback to periodically update sensor, weather data, and log it.

    This function is designed to be called by a `machine.Timer` instance.
    """
    # 1. Always update local sensor readings
    print("Task: Reading local DHT11 sensor...")
    oled.update_sensor_readings(timer)

    # 2. Check for Wi-Fi and update weather data if connected
    if wifi.is_connected():
        print("Task: Fetching weather data from API...")
        oled.update_weather_data(timer)

    # 3. Log the collected data to the CSV file
    print("Task: Logging data...")
    dht_data = (oled.temp_val, oled.hum)
    owm_data = oled.weather_data

    # Only log if we have valid DHT data
    if dht_data[0] is not None and dht_data[1] is not None:
        # If weather data is None (e.g., no Wi-Fi), create an empty tuple
        if owm_data is None:
            owm_data = (None, None, None, None, None, None)

        data_logger.log_data(dht_data, owm_data)


def start_timer_tasks():
    """
    Initializes and starts all hardware timers for the application.
    """
    # Perform an initial data fetch and log immediately on startup
    print("Performing initial data fetch and log...")
    weather_dht11_wrapper(None)

    # Timer to switch between OLED displays every 5 seconds
    display_timer = Timer(0)
    display_timer.init(period=5000, mode=Timer.PERIODIC, callback=oled.display_handler)

    # Timer to read sensors and log data every 15 minutes (900,000 ms)
    sensor_timer = Timer(1)
    sensor_timer.init(
        period=900000, mode=Timer.PERIODIC, callback=weather_dht11_wrapper
    )
