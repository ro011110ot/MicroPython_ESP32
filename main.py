"""
Main entry point for the ESP32 application.

This script connects to the WiFi network and starts the OLED display timer.
"""
# Import own Functions

import oled
import wifi

wifi.connect()
oled.start_timer()
