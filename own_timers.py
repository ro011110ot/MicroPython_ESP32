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
import data_logger # For logging data
import dht11       # For reading the DHT11 sensor
import oled        # For updating the display
import weather     # For fetching weather data
import wifi        # For checking the connection status


def weather_dht11_wrapper(timer):
    """
    Timer callback to periodically update sensor, weather data, and log it.

    This function orchestrates the data flow:
    1. Fetches data from the DHT11 sensor and OpenWeatherMap API.
    2. Updates the OLED module with the new data.
    3. Logs the data to a CSV file.
    """
    # 1. Fetch data from sources
    print("Task: Reading local DHT11 sensor...")
    dht_data = dht11.get_data()  # Returns (temp, hum) or (None, None)

    owm_data = (None,) * 6  # Default to None tuple
    if wifi.is_connected():
        print("Task: Fetching weather data from API...")
        owm_data = weather.get_data()
    else:
        print("Task: Skipping weather data fetch, no WiFi.")

    # 2. Update the OLED module's state with the new data
    # The OLED display will use this data on its next refresh cycle.
    oled.set_sensor_data(dht_data)
    oled.set_weather_data(owm_data)

    # 3. Log the data
    print("Task: Logging data...")
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
