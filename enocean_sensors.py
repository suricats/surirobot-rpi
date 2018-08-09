#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
import sys
import traceback
import requests
import json
import enocean.utils
from enocean.communicators.serialcommunicator import SerialCommunicator
from enocean.consolelogger import init_logging
from enocean.protocol.constants import PACKET, RORG
from enocean.protocol.packet import RadioPacket
from dotenv import load_dotenv, find_dotenv

try:
    import queue
except ImportError:
    import Queue as queue


def assemble_radio_packet(transmitter_id):
    return RadioPacket.create(rorg=RORG.BS4, rorg_func=0x20, rorg_type=0x01,
                              sender=transmitter_id,
                              CV=50,
                              TMP=21.5,
                              ES='true')

# Load .env
load_dotenv(find_dotenv())

# Request
token = os.environ.get('MEMORY_TOKEN')
url = os.environ.get('MEMORY_URL')
headers = {'Authorization': 'Token {}'.format(token), 'Content-Type': 'application/json'}
data = {"location": "beaubourg"}

# enOcean Serial
init_logging()
communicator = SerialCommunicator(port='/dev/ttyUSB0')
communicator.start()
try:
    print('The Base ID of your module is %s.' % enocean.utils.to_hex_string(communicator.base_id))
except TypeError:
    print("Can't get id hex value : {}".format(communicator.base_id))
if communicator.base_id is not None:
    print('Sending example package.')
    communicator.send(assemble_radio_packet(communicator.base_id))

# endless loop receiving radio packets
while communicator.is_alive():
    try:
        # Loop to empty the queue...
        packet = communicator.receive.get(block=True, timeout=1)
        if packet.packet_type == PACKET.RADIO and packet.rorg == RORG.BS4:
            # parse packet with given FUNC and TYPE
            for k in packet.parse_eep(0x02, 0x05):
                # Case : temperature
                if k == 'TMP':
                    temperature = float(packet.parsed[k]['value'])
                    print(u'{}: {:2f}{}'.format(k, temperature, packet.parsed[k]['unit']))
                    data.update({'type': 'temperature', 'data': temperature})
                    r = requests.post(url='{}/api/memory/sensors/'.format(url), data=json.dumps(data), headers=headers)
                    if r.status_code != 201 and r.status_code != 200:
                        print(r.content)
                        print("Error - HTTP {} for temperature".format(r.status_code))
                    else:
                        print('Temperature sended.')
                else:
                    print(u'{}: {}'.format(k, packet.parsed[k]))
        if packet.packet_type == PACKET.RADIO and packet.rorg == RORG.BS1:
            # alternatively you can select FUNC and TYPE explicitely
            packet.select_eep(0x00, 0x01)
            # parse it
            packet.parse_eep()
            for k in packet.parsed:
                # Case : magnetic contact
                if k == 'CO':
                    contact = int(packet.parsed[k]['raw_value'])
                    print(u'{}: {}{}'.format(k, packet.parsed[k]['value'], packet.parsed[k]['unit']))
                    data.update({'type': 'magnetic-contact', 'data': contact})
                    r = requests.post(url='{}/api/memory/sensors/'.format(url), data=json.dumps(data), headers=headers)
                    if r.status_code != 201 and r.status_code != 200:
                        print(r.content)
                        print("Error - HTTP {} for magnetic contact".format(r.status_code))
                    else:
                        print('Magnetic contact sended.')
        if packet.packet_type == PACKET.RADIO and packet.rorg == RORG.RPS:
            for k in packet.parse_eep(0x02, 0x02):
                print('%s: %s' % (k, packet.parsed[k]))
    except queue.Empty:
        continue
    except KeyboardInterrupt:
        break
    except Exception:
        traceback.print_exc(file=sys.stdout)
        break

if communicator.is_alive():
    communicator.stop()
