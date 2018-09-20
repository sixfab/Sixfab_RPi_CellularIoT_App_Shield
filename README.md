# Sixfab RPi Cellular IoT Library 
Python Library for Sixfab RPi Cellular IoT Hat and [Sixfab RPi Cellular IoT Application Hat](https://sixfab.com/product/raspberry-pi-cellular-iot-application-hat/)

# Product Description
This is a hat that has combined LTE technologies Cat.M1, Cat.NB1 (NB-IoT) and eGPRS for Raspberry Pi, based on Quectel’s BG96 module. The hat has the power of new IoT phenomenon LPWA (Low Power Wide Area) with Cat.M1 and NB-IoT connection functionalities. Besides, it also provides the function of eGPRS that be enhanced version of classical GPRS.

The hat has GNSS (GPS, GLONASS etc.) functionality for the need of location, navigation, tracking, mapping and timing applications.

The design has built-in temperature, humidity, light sensors, 3-axis accelerometer, and a relay.

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
    * Disable "Login shell to be accessible over serial"
    * Enable "Serial port hardware"
5. Finish
6. Reboot
7. It's done.
```
cd sample
python3 sensor_test.py  #for testing sensor_test example
```

# Detailed Features
* BG96 Cat.M1 / Cat.NB1 (NB-IoT) / eGPRS (EDGE, GPRS)
* Supported Bands : Global – B1/ B2/ B3/ B4/ B5/ B8/ B12/ B13/ B18/ B19/ B20/ B26/ B28 and B39 ( for Cat M1 only )
* eGPRS Supported Frequencies: 850/900/1800/1900Mhz
* Embedded GNSS Functionality (GPS, GLONASS, BeiDou/Compass, Galileo, QZSS)
* Optional standalone use via USB interface
* ADS1015 12 Bit 4 Channel ADC
* Relay with optocoupler protection (24V DC, 120-220V AC Switching)
* Optocoupler (3-12 V DC switching)
* Built-in 3 axis accelerometer (MMA8452Q)
* Built-In HDC1080 temperature sensor (-40 +125 C)
* Built-In HDC1080 humidity sensor (0 100%)
* Built-In ALS-PT19 ambient light sensor()
* 1-Wire interface (3 male pins)(It can be used with DS18B20, DHT21 etc.)
* I2C interface (4 male pins)
* User button and LED
* Micro SIM Socket
* UFL sockets for external antennas

# Pinout
![Pinout Schematic](https://sixfab.com/wp-content/uploads/2018/09/RPiCellularIoTAppPinout.png)

# Attention
! All data pins work with 3.3V reference. Any other voltage level should harm your hat or RPI.

# Examples
** [basicUDP](https://github.com/sixfab/Sixfab_RPi_CellularIoT_Library/blob/master/sample/basicUDP.py)  
** [sensorTest](https://github.com/sixfab/Sixfab_RPi_CellularIoT_Library/blob/master/sample/sensor_test.py)

# Tutorials 
** [Basic UDP Communication Tutorial for Sixfab RPi Cellular IoT Application HAT](https://sixfab.com/basic-udp-communication-tutorial-for-sixfab-rpi-cellular-iot-application-hat/)  
** [Sensor Test Tutorial for Sixfab RPi Cellular IoT Application HAT](https://sixfab.com/sensor-test-tutorial-for-sixfab-rpi-cellular-iot-application-hat/)    

# Applications
* Smart farming sensor
* Smart cities sensor
* Smart home sensor
* Internet of Things (IoT) sensor
* Smart door lock
* Smart lightning
* Smart metering
* Bike sharing
* Smart parking
* Smart city
* Security and asset tracking
* Home appliances
* Agricultural and environmental monitoring
