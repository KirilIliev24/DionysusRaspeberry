import time
import RPi
import RPi.GPIO as GPIO
import datetime

GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM) 

class RegulatorDriver:
    
    __pin = 0;
    
    def __init__(self, pin):
        self.__pin = pin
        GPIO.setup(self.__pin, GPIO.OUT)
        GPIO.output(self.__pin, False)
        print(self.__pin)
        
        
    def setRegulatorState(self, activate):
        GPIO.output(self.__pin, activate)
        
    def cleanup(self):
        print("Cleanup")
        GPIO.cleanup()
        

# humidityRegulator = RegulatorDriver(pin = 14)
# temperatureRegulator = RegulatorDriver(pin = 15)
#         
# while True:
#     temperatureRegulator.setRegulatorState(True)
#     humidityRegulator.setRegulatorState(False)
#     time.sleep(1)
#     temperatureRegulator.setRegulatorState(False)
#     humidityRegulator.setRegulatorState(True)
#     time.sleep(1)


