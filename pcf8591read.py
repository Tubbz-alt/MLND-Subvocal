#! /usr/bin/env python3
"""
This file is for gathering EMG data using the Q2W I2C PCF8591 ADC Breakout Board with a Raspberry PI. It's best used in conjunction with a script to control recording flow. See "simple_svr.py" for the actual control flow used. 
"""
import sys, time
from quick2wire.parts.pcf8591 import *
from quick2wire.i2c import I2CMaster
#from vis import volt_plot
from writefile import *
from tkinter import *

class adc_reader():

    def __init__(self):

        self.address = int(sys.argv[1]) if len(sys.argv) > 1 else BASE_ADDRESS
        self.pin_index1 = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        self.pin_index2 = int(sys.argv[3]) if len(sys.argv) > 3 else 1
        self.record = False



    def run(self, filename):

        with I2CMaster() as i2c:
            adc = PCF8591(i2c, THREE_DIFFERENTIAL)
            pin1 = adc.differential_input(1)
            count = 0
            start = time.time()

            with open(filename, 'w') as csvfile:

                fieldnames = ['time', 'count', 'voltage']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                while self.record:
                    reading = ''
                    voltage = pin1.value * 3.3
                    strength = ['-' for i in range(int(pin1.value*256))]
                    disp = ''
                    for dash in strength:
                        disp += dash
                    print (disp)
                    #sleep(0.1)
                    count += 1
                    current = time.time() - start
                    #data[count] = pin1.raw_value
                    #volt_plot(count, data)
                    writer.writerow({'time': current, 'count': count, 'voltage': voltage})
