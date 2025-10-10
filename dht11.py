import dht
from machine import Pin
import time
import os

sensor = dht.DHT11(Pin(14))


def dht11():
    # Get current time to create filename and timestamp
    now = time.localtime()
    date_str = "{:04d}.{:02d}.{:02d}".format(now[0], now[1], now[2])
    time_str = "{:02d}:{:02d}".format(now[3], now[4])
    filename = f"{date_str}.temp.csv"

    # Check if file exists, if not create it with header
    try:
        os.stat(filename)
    except OSError:
        with open(filename, "w") as f:
            f.write("date;time;temperature;humidity\n")

    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()

        # Format data for CSV
        csv_line = f"{date_str};{time_str};{temp} °C;{hum} %\n"
        # Write to CSV
        try:
            with open(filename, "a") as f:
                f.write(csv_line)
        except OSError:
            print(f"Failed to write to {filename}")
    except OSError:
        print("Failed to read sensor.")
