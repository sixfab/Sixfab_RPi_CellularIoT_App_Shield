from cellulariot import cellulariot
import time

your_ip = "xx.xx.xx.xx" # change with your ip
your_port = "xxxx" # change with your port

#node = cellulariot.CellularIoT() # for Sixfab CellularIoT HAT
node = cellulariot.CellularIoTApp() # for Sixfab CellularIoT App. Shield
node.setupGPIO()

node.disable()
time.sleep(1)
node.enable()
time.sleep(1)
node.powerUp()

while True:
	if (node.readUserButton() == 1):
		node.turnOffUserLED()
	else:
		node.turnOnUserLED()
