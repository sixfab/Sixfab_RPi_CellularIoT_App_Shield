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

node.setGSMBand(node.GSM_ANY)

node.setMode(node.GSM_MODE)

print ("Wait 10 seconds for network registration")
sleep(10)

print ("Checking Signal Quality")
node.getSignalQuality()

print ("Checking Attached operator")
node.getOperator()