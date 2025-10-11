"""
This module handles the WiFi connection for the ESP32.
"""
import machine
import network
import ntp
import ntptime
import time
from secrets import secrets

# WLAN configuration
wlan = network.WLAN(network.WLAN.IF_STA)


def connect():
    """
    Connects to the WiFi network using credentials from the secrets file.

    If not connected, it will try to connect. If successful, it prints the
    network configuration and sets the real-time clock (RTC) from an NTP server.
    If it fails, it prints an error message.
    """
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
        print("Network is offline")
