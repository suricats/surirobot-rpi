# HAL-1 RPI Pack

Package of scripts to be used for collecting data on Raspberry Pi

## Features

* Blink : blinking LED test
* EnOcean Sensors : collecting data of enocean wireless sensors
* Mario : testing sound on buzzer
* Outlet : controlling a relay with redis/command
* Sound : collecting the decibel level of microphone
* Temperature : collecting  temperature and humidity of DHT11 sensor

## Installation 

```bash
sudo apt-get install -y --fix-missing python3-dev libatlas-base-dev portaudio19-dev
```
Install required python3 modules: `pip3 install -r requirements.txt`

```
## Configure the environment file
* Configure .env 
```shell
cp .env.example .env
```
If you want to use the default environment (WIP)
- Fill only the ```REMOTE_DATA_LOGIN```  and ```REMOTE_DATA_PASSWD``` fields
- Run the command : ```tools/get-env```

