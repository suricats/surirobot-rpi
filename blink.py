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
import threading

# Load .env
load_dotenv(find_dotenv())


def blink(pin, freq, init, stop_event):
    cpts = init
    print('blink')
    while not stop_event.is_set():
        GPIO.output(pin, cpts)
        cpts = (cpts + 1) % 2
        time.sleep(freq)


GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
stop = threading.Event()
BLUE_PIN = 4
BLUE_F = 0.1
BLUE_INITIAL = 0
GREEN_PIN = 17
GREEN_F = 0.11
GREEN_INITIAL = 1
RED_PIN = 27
RED_F = 0.12
RED_INITIAL = 1
GPIO.setup(BLUE_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(RED_PIN, GPIO.OUT)

try:
    t1 = threading.Thread(target=blink, args=(BLUE_PIN, BLUE_F, BLUE_INITIAL, stop))
    t2 = threading.Thread(target=blink, args=(GREEN_PIN, GREEN_F, GREEN_INITIAL, stop))
    t3 = threading.Thread(target=blink, args=(RED_PIN, RED_F, RED_INITIAL, stop))
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()
except KeyboardInterrupt:
    GPIO.cleanup()
    print("Exiting")
finally:
    stop.set()