import time
import RPi
import RPi.GPIO as GPIO
import datetime
import requests
import json
import decimal
import asyncio
from DHT11Driver import DHT11Driver
from RegulatorDriver import RegulatorDriver
from HTTPRequests import HttpRequests

GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)


async def main():

    URL = 'http://e963-212-10-147-231.ngrok.io/api/RaspberryGateway'

    # read data using pin 4
    instance = DHT11Driver(pin = 4)
    humidityRegulator = RegulatorDriver(pin = 14)
    temperatureRegulator = RegulatorDriver(pin = 15)
    requests = HttpRequests(url = URL)


    while True:
        result = await instance.readData()
        if result != 0:
            print("Sending data")
            print(result)
            date = datetime.datetime.now()
            postTask = asyncio.create_task(requests.postInformation(result[0], result[1], date, 4))
            await postTask
            
        print("Getting command")
        getTask = asyncio.create_task(requests.getCommand(15, 14))
        command = await getTask
        if(command != 0):
            acticvateTemperature = command['activateTemperatureDevice']
            acticvateHumidity = command['activateHumidityDevice']
            temperatureRegulator.setRegulatorState(acticvateTemperature)
            humidityRegulator.setRegulatorState(acticvateHumidity)
        
        time.sleep(5)


asyncio.run(main())

