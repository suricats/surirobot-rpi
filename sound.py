import json
import os

import pyaudio
import numpy as np
import time

import requests
from dotenv import load_dotenv, find_dotenv

# Load .env
load_dotenv(find_dotenv())

RATE = 44100
CHUNK = int(RATE / 20)  # RATE / number of updates per second
token = os.environ.get('MEMORY_TOKEN')
url = os.environ.get('MEMORY_URL')
headers = {'Authorization': 'Token {}'.format(token), 'Content-Type': 'application/json'}
data = {"location": "beaubourg"}

if __name__ == "__main__":
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    try:
        t1 = time.time()
        db_tab = []
        while True:
            if time.time() - t1 > 10:
                if db_tab:
                    average_db = np.average(db_tab)
                    print('Average dB : {:.2f} dB'.format(average_db))
                    data.update({'type': 'decibel', 'data': average_db})
                    r = requests.post(url='{}/api/memory/sensors/'.format(url), data=json.dumps(data), headers=headers)
                db_tab = []
                t1 = time.time()
            data_db = np.fromstring(stream.read(CHUNK), dtype=np.int16)
            average_amp = np.average(np.abs(data_db))
            if average_amp > 0:
                db = 20 * np.log10(average_amp * 2)
                db_tab.append(db)
    except KeyboardInterrupt:
        stream.stop_stream()
        stream.close()
        p.terminate()
