"""
Main entry point for the ESP32 Sensor Station application.

This script initializes the system, connects to Wi-Fi, synchronizes time, and
starts all necessary background tasks and timers before entering the main loop.
"""

# Standard Library
import utime

# Local Application
from ntp import set_rtc_from_ntp
from own_timers import start_timer_tasks
from secrets import secrets
from system_tasks import run_system_tasks
from wifi import connect_wifi, is_connected


def main():
    """The main entry point and logic for the application."""
    print("--- Starting MicroPython ESP32 Sensor Station ---")

    # 1. Initial Wi-Fi Connection
    connect_wifi(secrets["ssid"], secrets["password"])

    if not is_connected():
        print("FATAL: Initial WiFi connection failed. System will halt.")
        # In a real-world scenario, you might want to add a delay and then
        # machine.reset() to attempt a full reboot.
        return

    # 2. Initial NTP Time Synchronization
    print("Performing initial NTP synchronization...")
    set_rtc_from_ntp()

    # 3. Start Hardware Timer Tasks
    # These handle periodic data collection and display updates.
    print("Starting hardware timer-based tasks...")
    start_timer_tasks()

    # 4. Main Application Loop
    # This loop is responsible for running non-time-critical system tasks.
    print("Entering main application loop...")
    while True:
        run_system_tasks()

        # Sleep to prevent the loop from hogging the CPU
        utime.sleep_ms(50)


if __name__ == "__main__":
    main()
