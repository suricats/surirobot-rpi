#!/usr/bin/python
import time

import RPi.GPIO as GPIO
from dotenv import load_dotenv, find_dotenv
import time
import redis
import sys
import os
# Load .env
load_dotenv(find_dotenv())
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
RELAY_PIN = 4
GPIO.setup(RELAY_PIN, GPIO.OUT)

# One shot mode
if sys.argv and len(sys.argv) > 1:
    if sys.argv[1] == "up":
        GPIO.output(RELAY_PIN, GPIO.HIGH)
    elif sys.argv[1] == "down":
        GPIO.output(RELAY_PIN,GPIO.LOW)
elif os.environ.get('REDIS_SERVER_URL'):
    # Redis connection mode
    port = int(os.environ.get('REDIS_SERVER_PORT'))
    r = redis.StrictRedis(host=os.environ.get('REDIS_SERVER_URL'), port=port if port else 6379)
    p = r.pubsub()
    channel = 'slack'
    if not r.exists(channel):
        r.set(channel, True)
    p.subscribe(channel)
    while True:
        try:
            message = p.get_message()
            if message:
                command = message['data']
                if type(command) == bytes:
                    command = command.decode('utf-8')
                print(command)
                if command == 'up':
                    GPIO.output(RELAY_PIN, GPIO.HIGH)
                elif command == 'down':
                    GPIO.output(RELAY_PIN, GPIO.LOW)
            time.sleep(0.5)
        except KeyboardInterrupt:
            break