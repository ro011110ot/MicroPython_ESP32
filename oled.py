from machine import Pin, SoftI2C, Timer
import ssd1306_driver as ssd1306
import time


# ESP32 Pin assignment
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)


def oled_hello():
    oled.text("Hello, World 1!", 0, 0)
    oled.text("Hello, World 2!", 0, 10)
    oled.text("Hello, World 3!", 0, 20)
    oled.show()


def oled_time(timer):
    # Get current time
    now = time.localtime()
    date_str = "{:04d}.{:02d}.{:02d}".format(now[0], now[1], now[2])
    time_str = "{:02d}:{:02d}:{:02d}".format(now[3], now[4], now[5])

    oled.fill(0)
    oled.text(date_str, 0, 0)
    oled.text(time_str, 0, 20)

    oled.show()


def start_time_display():
    timer = Timer(0)
    timer.init(period=1000, mode=Timer.PERIODIC, callback=oled_time)