#! /usr/bin/python3

import statistics
import time
import argparse
import RPi.GPIO as GPIO



class UltraSonicSensor:
    def __init__(self, gpio_trigger, gpio_echo):
        self.gpio_trigger = gpio_trigger
        self.gpio_echo = gpio_echo
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.gpio_trigger, GPIO.OUT)
        GPIO.setup(self.gpio_echo, GPIO.IN)

    @property
    def distance(self):
        GPIO.output(self.gpio_trigger, True)    # set Trigger to HIGH
        time.sleep(0.00001)                     # sleep for 0.01ms
        GPIO.output(self.gpio_trigger, False)   # set trigger to LOW

        # save StartTime (after start of echo pulse)
        while GPIO.input(self.gpio_echo) == 0:
            start_time = time.time()

        # save time of arrival
        while GPIO.input(self.gpio_echo) == 1:
            stop_time = time.time()

        # time difference between start and arrival
        elapsed_time = stop_time - start_time
        distance     = (elapsed_time * 34300) / 2

        return round(distance,2)

    def avg_distance(self):

        def average(lst):
            return sum(lst) / len(lst)

        samples = []
        measurement = 0
        while measurement < 5:
                time.sleep(0.1)
                measurement += 1
                samples.append(self.distance)
        average = average(samples)
        print(str(round(average))+' cm')
        
if __name__ == "__main__":
    trigger = 24
    echo    = 23
    HCSR04 = UltraSonicSensor(trigger, echo)
    for i in range(0,100):
        HCSR04.avg_distance()
