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

# Load .env
load_dotenv(find_dotenv())

GPIO.setmode(GPIO.BCM)
BIG_SOUND_PIN = 7
GPIO.setup(BIG_SOUND_PIN, GPIO.IN)
try:
    while True:
        print(GPIO.input(BIG_SOUND_PIN))
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()
    print("Exiting")