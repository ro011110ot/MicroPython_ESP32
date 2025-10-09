import dht
from machine import Pin
from time import sleep

sensor = dht.DHT11(Pin(14))


# noinspection PyUnusedLocal
def dht11():
    while True:
        try:

            sensor.measure()
            temp = sensor.temperature()
            hum = sensor.humidity()
            # temp_f = temp * (9 / 5) + 32.0
            # print('Temperature: %3.1f F' % temp_f)
            print('Temperature: %3.1f C' % temp)
            print('Humidity: %3.1f %%' % hum)

            sleep(30)
        except OSError as e:
            print('Failed to read sensor.')