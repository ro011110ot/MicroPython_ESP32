"""
Main entry point for the ESP32 weather and sensor monitoring station.

This script initializes the application by performing the following steps:
1. Connecting to the configured WiFi network.
2. Starting the timers that handle:
   - Reading temperature and humidity from the DHT11 sensor.
   - Fetching current weather data from the OpenWeatherMap API.
   - Updating the OLED display with time, sensor, and weather information.
"""
# Import own Functions
import own_timers
import wifi

wifi.connect()
own_timers.start_timer()
