import machine
import network
import ntp
import ntptime
import time
from secrets import secrets

# WLAN-Konfiguration
wlan = network.WLAN(network.WLAN.IF_STA)


# Funktion: WLAN-Verbindung
def connect():
    wlan.active(True)
    if not wlan.isconnected():
        print("connecting to network...")
        wlan.connect(secrets["ssid"], secrets["password"])
        while not wlan.isconnected():
            time.sleep(1)

    if wlan.isconnected():
        print("network config:", wlan.ipconfig("addr4"))
        ntptime.settime()
        rtc = machine.RTC()
        rtc.datetime(ntp.cettime())
        print("RTC set to:", time.localtime())
    else:
        print("Network ro011110ot is offline")
