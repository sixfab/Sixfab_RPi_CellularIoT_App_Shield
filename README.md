# Sixfab RPi CellularIoT App Shield
Repository of Python Library for Sixfab RPi Cellular IoT Shield and [Sixfab RPi Cellular IoT Application Shield](https://sixfab.com/product/raspberry-pi-cellular-iot-application-hat/)

# Library Installation
## Manual Installation
```
git clone https://github.com/sixfab/Sixfab_RPi_CellularIoT_Library.git
cd Sixfab_RPi_CellularIoT_Library
sudo python3 setup.py install
```

## Install with pip3
Use pip3 to install from PyPI.
```
sudo pip3 install sixfab-cellulariot
```

## Test
Enable `serial_hw` and `I2C` interfaces by following instructions below:  
1. Run `sudo raspi-config`
2. Select `5 Interfacing Options`
3. Enable `P5 I2C`
4. For `P6 Serial`
    * Disable `Login shell to be accessible over serial`
    * Enable `Serial port hardware`
5. Finish
6. Reboot
7. It's done.
```
cd sample
python3 sensor_test.py  #for testing sensor_test example
```

# Examples
** [basicUDP](https://github.com/sixfab/Sixfab_RPi_CellularIoT_Library/blob/master/sample/basicUDP.py)  
** [sensorTest](https://github.com/sixfab/Sixfab_RPi_CellularIoT_Library/blob/master/sample/sensor_test.py)

# Tutorials 
** [Basic UDP Communication Tutorial for Sixfab RPi Cellular IoT Application Shield](https://sixfab.com/basic-udp-communication-tutorial-for-sixfab-rpi-cellular-iot-application-hat/)  
** [Sensor Test Tutorial for Sixfab RPi Cellular IoT Application Shield](https://sixfab.com/sensor-test-tutorial-for-sixfab-rpi-cellular-iot-application-hat/) 

# Pinout
## Sixfab RPi Cellular IoT Application Shield
![Pinout Schematic](https://sixfab.com/wp-content/uploads/2018/09/RPiCellularIoTAppPinout.png)

# Attention
! All data pins work with 3.3V reference. Any other voltage level should harm your hat or RPI.

# Layout
## Sixfab RPi Cellular IoT Application Shield
![](https://sixfab.com/wp-content/uploads/2018/10/rpi_cellulariot_application_shield_layout-1.png)


