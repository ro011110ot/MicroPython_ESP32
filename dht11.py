import dht
from machine import Pin
import time
import os

sensor = dht.DHT11(Pin(14))


def dht11():
    # Check if temp.csv exists, if not create it with header
    try:
        os.stat("temp.csv")
    except OSError:
        with open("temp.csv", "w") as f:
            f.write("date;time;temperature;humidity\n")

    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()

        # Get current time
        now = time.localtime()
        date_str = "{:04d}.{:02d}.{:02d}".format(now[0], now[1], now[2])
        time_str = "{:02d}:{:02d}".format(now[3], now[4])

        # Format data for CSV
        csv_line = f"{date_str};{time_str};{temp} °C;{hum} %\n"
        # Write to CSV
        try:
            with open("./temp.csv", "a") as f:
                f.write(csv_line)
        except OSError:
            print("Failed to write to temp.csv")
    except OSError:
        print("Failed to read sensor.")
