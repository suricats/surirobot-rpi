#!/usr/bin/python
# SCRIPT FOR DHT11 SENSOR
"""
PIN CONFIGURATION ON RPI 3
VCC | X | GND | X | ....... | USB   |
X   | X |  X  | SIGNAL | .. | PORTS |
"""
from dotenv import load_dotenv, find_dotenv
import os
from time import sleep
import requests
import json

# Load .env
load_dotenv(find_dotenv())

try:
    import Adafruit_DHT
except ImportError:
    print('Adafruit_DHT not found. Please try : \n'
          '1. Enter this at the command prompt to download the library:\n'
          'git clone https://github.com/adafruit/Adafruit_Python_DHT.git\n'
          '2. Change directories with:\n'
          'cd Adafruit_Python_DHT\n'
          '3. Now enter this:\n'
          'sudo apt-get install build-essential python-dev\n'
          '4. Then install the library with:\n'
          'sudo python setup.py install\n')

token = os.environ.get('MEMORY_TOKEN')
url = os.environ.get('MEMORY_URL')
headers = {'Authorization': 'Token {}'.format(token), 'Content-Type': 'application/json'}
data = {"location": "beaubourg"}

while True:
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    print('Temp: {0:0.1f} C  Humidity: {1:0.1f}'.format(temperature, humidity))
    try:
        data.update({'type': 'temperature', 'data': temperature})
        r = requests.post(url=url, data=json.dumps(data), headers=headers)
        if r.status_code != 201 and r.status_code != 200:
            print(r.content)
            raise Exception("HTTP {} for temperature".format(r.status_code))
        print('Temperature added')
        data.update({'type': 'humidity', 'data': humidity})
        r = requests.post(url=url, data=json.dumps(data), headers=headers)
        if r.status_code != 201 and r.status_code != 200:
            print(r.content)
            raise Exception("HTTP {} for humidity".format(r.status_code))
        print('Humidity added')
        sleep(int(os.environ.get('TEMP_SLEEP', '60')))
    except Exception as e:
        print('{} : {}'.format(type(e).__name__, e))
        sleep(300)
