#!/usr/bin/python
# SCRIPT FOR KY-038 Big Sound
"""
PIN CONFIGURATION ON RPI 3
VCC | X | GND | X | ....... | USB   |
X   | X |  X  | SIGNAL | .. | PORTS |
"""
import time

import RPi.GPIO as GPIO
from dotenv import load_dotenv, find_dotenv
import time

# Load .env
load_dotenv(find_dotenv())

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
BIG_SOUND_PIN = 4
BLUE_LED_PIN = 17
GPIO.setup(BIG_SOUND_PIN, GPIO.IN)
GPIO.setup(BLUE_LED_PIN, GPIO.OUT)

try:
    GPIO.output(BLUE_LED_PIN, GPIO.LOW)
    while True:
        val = GPIO.input(BIG_SOUND_PIN)
        print(val)
        if val:
            GPIO.output(BLUE_LED_PIN, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(BLUE_LED_PIN, GPIO.LOW)
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()
    print("Exiting")
