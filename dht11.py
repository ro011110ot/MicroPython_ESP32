"""
This module provides a function to read temperature and humidity from a DHT11 sensor.
It also logs the readings to a CSV file.
"""

import dht
from machine import Pin
import time
import os

# Initialize the sensor
sensor = dht.DHT11(Pin(14))


def measure() -> tuple:
    """
    Reads temperature and humidity from the DHT11 sensor, logs the data to a CSV file,
    and returns the values.

    The CSV file is stored in the '/temp_history' directory and named with the current date.
    If the directory or file doesn't exist, they are created.

    Returns:
        tuple: A tuple containing the temperature (float) and humidity (float).
               Returns (None, None) if the sensor reading fails.
    """
    try:
        time.sleep(2)  # Wait for sensor to stabilize
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
    except OSError as e:
        print(f"Failed to read sensor: {e}")
        return None, None

    now = time.localtime()
    date_str = f"{now[0]:04d}.{now[1]:02d}.{now[2]:02d}"
    time_str = f"{now[3]:02d}:{now[4]:02d}"

    log_dir = "/temp_history"
    filename = f"{log_dir}/{date_str}.temp.csv"

    try:
        # Create directory if it doesn't exist
        if "temp_history" not in os.listdir("/"):
            os.mkdir(log_dir)
        
        # Write header if file doesn't exist
        if f"{date_str}.temp.csv" not in os.listdir(log_dir):
            with open(filename, "w") as f:
                f.write("date;time;temperature;humidity\n")

        # Append data to file
        with open(filename, "a") as f:
            csv_line = f"{date_str};{time_str};{temp} °C;{hum} %\n"
            f.write(csv_line)
            
    except OSError as e:
        print(f"Failed to write to log file: {e}")

    return temp, hum
