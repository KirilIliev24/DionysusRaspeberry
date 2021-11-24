import time
import RPi
import RPi.GPIO as GPIO
import datetime
import requests
import json
import decimal
import asyncio
from DHT11Driver import DHT11Driver

GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)

class HttpRequests:
    
    __url = ''
    
    def __init__(self, url):
            self.__url = url


    def __convertTimeFormat(self, timeNow):
        splitStr = timeNow.split();
        timeSplit = splitStr[1].split(".")
        cSharpTime = splitStr[0] + "T" + timeSplit[0]
        print(cSharpTime)
        return cSharpTime

    async def postInformation(self, temperature, humidity, date, pin):
        
                
        currentTime = self.__convertTimeFormat(str(date))
                
        readingObject = {
            "TemperatureReading": temperature,
            "HumidityReading": humidity,
            "dateTime": currentTime,
            "SensorPinNumber": pin,
            "BatchId": 1
        }
        
        headers = { "charset" : "utf-8", 'content-type': 'application/json'}  
        response = requests.post(self.__url, json=readingObject, headers = headers)
        print(response.status_code)
#         print(response.text)
        if(response.status_code == 200):
            return True;


    async def getCommand(self, tempPin, humPin):
        headers = {
            "charset" : "utf-8",
            'content-type': 'application/json',
            "temperaturePin": str(tempPin),
            "humidityPin": str(humPin)
        }  
        getCommand = requests.get(self.__url, headers = headers);
        print(getCommand)
        if(getCommand.status_code == 200):
            data = getCommand.json()
            print(getCommand.status_code)
            print(getCommand.text)
            return data;
        return 0
        
        
        
        



