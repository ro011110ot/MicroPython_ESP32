from machine import Timer
import oled
import wifi


def weather_dht11_wrapper(timer):
    """
    Timer callback to periodically update sensor and weather data.

    This function is called by a timer to:
    1. Trigger a new reading from the local DHT11 sensor.
    2. Check for a WiFi connection.
    3. If WiFi is available, trigger a new fetch of weather data from the API.
    """
    oled.update_sensor_readings(timer)
    wifi_on = wifi.check_wifi()
    if wifi_on:
        oled.update_weather_data(timer)

def start_timer():
    """
    Initializes and starts the timers for updating the display
    and reading sensor data.
    """
    oled.update_sensor_readings(None)
    oled.update_weather_data(None)  # Initial fetch

    # Timer to switch between displays every 5 seconds
    display_timer = Timer(0)
    display_timer.init(
        period=5000, mode=Timer.PERIODIC, callback=oled.display_handler
    )

    # Timer to read local sensor data every 15 minutes
    sensor_timer = Timer(1)
    sensor_timer.init(
        period=900000, mode=Timer.PERIODIC, callback=weather_dht11_wrapper
    )