'''
  sendSMS.py - This is basic SMS Service example.
  Created by Yasin Kaya (selengalp), October 31, 2018.
'''
from cellulariot import cellulariot
import time

#node = cellulariot.CellularIoT() # for Sixfab CellularIoT HAT
node = cellulariot.CellularIoTApp() # for Sixfab CellularIoT App. Shield
node.setupGPIO()

node.disable()
time.sleep(1)
node.enable()
time.sleep(1)
node.powerUp()

node.sendATComm("ATE1","OK\r\n")

node.sendSMS("xxxxxxxxxxxxx","hello world!")
