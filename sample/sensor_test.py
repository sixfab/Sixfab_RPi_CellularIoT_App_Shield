'''
  sensor_test.py - This is basic sensor_test example for Cellular IoT Application Shield.
  WARNING: Running this script in the Cellular IoT HAT will lead to error.
  Created by Yasin Kaya (selengalp), August 28, 2018.
'''

from cellulariot import cellulariot
import time

node = cellulariot.CellularIoTApp()
node.setupGPIO()

node.disable()
time.sleep(1)
node.enable()

time.sleep(0.5)
print("Acceleration: "+str(node.readAccel()))
time.sleep(0.5)
print("Humidity: " + str(node.readHum()))
time.sleep(0.5)
print("Temperature: " + str(node.readTemp()))
time.sleep(0.5)
print("Lux: " + str(node.readLux()))
print("ADC1: " + str(node.readAdc(0)))
time.sleep(0.5)
print("ADC2: " + str(node.readAdc(1)))
time.sleep(0.5)
print("ADC3: " + str(node.readAdc(2)))
time.sleep(0.5)
print("ADC4: " + str(node.readAdc(3))) 
time.sleep(0.5)
node.turnOnRelay()
time.sleep(2)
node.turnOffRelay()
time.sleep(0.5)
node.turnOnUserLED()
time.sleep(2)
node.turnOffUserLED()
