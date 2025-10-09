from machine import Pin, SoftI2C, Timer
import ssd1306_driver as ssd1306
import time

# --- Global Variables ---
temp_val = "N/A"
hum = "N/A"

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
        # Keep default "N/A" values if file doesn't exist
        # or if there's an error reading it.
        temp_val = "N/A"
        hum = "N/A"


def oled_time(timer):
    """
    Updates the OLED display with the current time and the last known
    sensor readings from the global variables.
    """
    # Get current time
    now = time.localtime()
    date_str = "{:04d}.{:02d}.{:02d}".format(now[0], now[1], now[2])
    time_str = "{:02d}:{:02d}:{:02d}".format(now[3], now[4], now[5])

    oled.fill(0)
    oled.text(date_str, 0, 0)
    oled.text(time_str, 0, 20)

    # Display Temperature from global variable
    temp_str = f"Temp: {temp_val}"
    oled.text(temp_str, 0, 40)

    # Add degree symbol and 'C' if temp is available
    if temp_val != "N/A":
        text_width = len(temp_str) * 8
        oled.blit(ssd1306.DEGREE, text_width, 40)
        oled.text("C", text_width + 8, 40)

    # Display Humidity from global variable
    oled.text(f"Hum: {hum}", 0, 50)

    oled.show()


def start_timer():
    """
    Initializes and starts the timers for updating the display
    and reading sensor data.
    """
    # Perform an initial read of the sensor data so we don't
    # have to wait for the first timer interval.
    update_sensor_readings(None)

    # Start a 1-second timer to update the time on the display
    time_timer = Timer(0)
    time_timer.init(period=1000, mode=Timer.PERIODIC, callback=oled_time)

    # Start a 5-minute (300,000 ms) timer to read the temp.csv file
    sensor_timer = Timer(1)
    sensor_timer.init(
        period=300000, mode=Timer.PERIODIC, callback=update_sensor_readings
    )
