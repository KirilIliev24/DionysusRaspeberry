import time
import RPi
import RPi.GPIO as GPIO
import datetime
import json
import requests


class DHT11Driver:
    __pin = 0
    __temperature = -1
    __humidity = -1


    def __init__(self, pin):
        self.__pin = pin

    async def readData(self):
        RPi.GPIO.setup(self.__pin, RPi.GPIO.OUT)

        # send initial high
        GPIO.output(self.__pin, GPIO.HIGH)
        time.sleep(0.05)

        # pull down to low
        GPIO.output(self.__pin, GPIO.LOW)
        time.sleep(0.02)

        # change to input using pull up
        RPi.GPIO.setup(self.__pin, RPi.GPIO.IN, RPi.GPIO.PUD_UP)

        # collect data into an array
        data = self.collect_data()

        # parse lengths of all data pull up periods
        pull_up_lengths = self.measure_high_data_lenghts(data)
       

        # if bit count mismatch, return error (4 byte data + 1 byte checksum)
        if len(pull_up_lengths) != 40:
            return 0

        # calculate bits from lengths of the pull up periods
        bits = self.convert_data_lenght_to_binary(pull_up_lengths)

        # we have the bits, calculate bytes
        all_bytes = self.convert_bits_to_bytes(bits)

        # calculate checksum and check
        checksum = self.calculate_checksum(all_bytes)
        
        #if the checksum is not equal to the 5th byte, then the data is incorect
        if all_bytes[4] != checksum:
            return 0

        temperature = all_bytes[2] + float(all_bytes[3]) / 10
        humidity = all_bytes[0] + float(all_bytes[1]) / 10

        #print(len(data))
        #print(data)
        return [temperature, humidity]

    def collect_data(self):
        # collect the data while unchanged found
        unchanged_count = 0

        # this is used to determine where is the end of the data
        max_unchanged_count = 50

        last = -1
        data = []
        while True:
            current = GPIO.input(self.__pin)
            data.append(current)
            if last != current:
                unchanged_count = 0
                last = current
            else:
                unchanged_count += 1
                if unchanged_count > max_unchanged_count:
                    break
        return data

    def measure_high_data_lenghts(self, data):
        
        high_period_lengths = [] # stores the lenght of the hight period
        current_length = 0 # last period
        
        for i in range(len(data)):

            if data[i] == GPIO.HIGH:
                current_length += 1
            elif data[i] == GPIO.LOW and data[i + 1] != GPIO.LOW:
                high_period_lengths.append(current_length)
                current_length = 0;
                
        #print(len(high_period_lengths))
        #print(high_period_lengths)
        if len(high_period_lengths) > 40:
            #remove first 2 bits, because they signal that the data is comming
            del high_period_lengths[0]
            del high_period_lengths[0]
            
        #print(len(high_period_lengths))
        #print(high_period_lengths)
        return high_period_lengths

    def convert_data_lenght_to_binary(self, pull_up_lengths):
        # find shortest and longest period
        shortest_pull_up = min(pull_up_lengths)
        longest_pull_up = max(pull_up_lengths)

        # using average will determine the lenght is for 0 or for 1
        average = (shortest_pull_up + longest_pull_up) / 2
        bits = []

        for i in range(len(pull_up_lengths)):
            bit = 0
            if pull_up_lengths[i] > average:
                bit = 1
            bits.append(bit)

        #print(bits)
        return bits

    def convert_bits_to_bytes(self, bits):
        all_bytes = []
        byte = 0

        for i in range(0, len(bits)):
            #move the byte to the left by 1 possition
            byte = byte << 1
            if (bits[i]):
                byte += 1
            else:
                byte += 0
                
            #check if this is the 8th bit, if yes then put in the array and start the next one     
            if ((i + 1) % 8 == 0):
                all_bytes.append(byte)
                byte = 0
        #print(the_bytes)
        return all_bytes

    def calculate_checksum(self, the_bytes):
        #summs the first 4 bytes
        return the_bytes[0] + the_bytes[1] + the_bytes[2] + the_bytes[3]
    
    
    
# # initialize GPIO
# GPIO.setwarnings(True)
# GPIO.setmode(GPIO.BCM)
# 
# instance = DHT11Driver(pin = 4)
# result = instance.readData()
# 
# try:
# 	while True:
# 	    result = instance.readData()
# 	    if result != 0:
# 	        print("Last valid input: " + str(datetime.datetime.now()))
# 
# 	        print("Temperature: %-3.1f C" % result[0])
# 	        print("Humidity: %-3.1f %%" % result[1])
# 
# 	    time.sleep(6)
# 
# except KeyboardInterrupt:
#     print("Cleanup")
#     GPIO.cleanup()    
