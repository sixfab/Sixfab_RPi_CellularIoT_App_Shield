#! /usr/bin/env python3 

from cellulariot import cellulariot
from time import sleep

node = cellulariot.CellularIoT()

node.setupGPIO()

node.disable()
sleep(1)
node.enable()
sleep(1)
node.powerUp()

node.setMode(node.GSM_MODE)

print ("Wait 60 seconds for network registration\nWaiting Time:", end=" ")

for i in range(1,7):
    sleep(10)
    print(i*10, end=" ")
    print("sec")
    

print ("Checking Signal Quality")
node.getSignalQuality()

print ("Checking Attached operator")
node.getOperator()