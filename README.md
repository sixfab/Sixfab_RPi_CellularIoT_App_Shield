# Sixfab RPi CellularIoT Library
Repository of Python Library for [Sixfab RPi Cellular IoT HAT](https://sixfab.com/product/raspberry-pi-lte-m-nb-iot-egprs-cellular-hat/) and [Sixfab RPi Cellular IoT Application Shield](https://sixfab.com/product/raspberry-pi-cellular-iot-application-hat/)

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

# Library Documentation

## CellularIoT class

### vars
```
board = "" # shield name (Cellular IoT or Cellular IoT App.)
ip_address = "" # ip address       
domain_name = "" # domain name   
port_number = "" # port number 
timeout = TIMEOUT # default timeout for function and methods on this library.
response = "" # variable for modem self.responses
compose = "" # variable for command self.composes
```
#### Primary Functions

`setupGPIO` - Needs documentation

`clear_compose` - Function for clearing global compose variable 

`clearGPIOs` - Function for clearing GPIO's setup

`enable` - Function for enable BG96 module

`disable` - Function for powering down BG96 module and all peripherals from voltage regulator 

`powerUp` - Function for powering up or down BG96 module

`getModemStatus` - Function for getting modem power status

`getResponse` - Function for getting modem response

`sendDataCommOnce` - Function for sending data to module

`sendATCommOnce` - Function for sending at comamand to module

`sendDataComm` - Function for sending data to BG96_AT

`sendATComm` - Function for sending at command to BG96_AT

`resetModule` - Function for saving conf. and reset BG96_AT module

`saveConfigurations` - Function for save configurations that be done in current session

`getIMEI` - Function for getting IMEI number

`getFirmwareInfo` - Function for getting firmware info

`getHardwareInfo` - Function for getting hardware info

`setGSMBand` - Function for setting GSM Band

`setCATM1Band` - Function for setting Cat.M1 Band

`setNBIoTBand` - Function for setting NB-IoT Band

`getBandConfiguration` - Function for getting current band settings

`setScambleConf` - Function for setting scramble feature configuration 

`setMode` - Function for setting running mode

`getIPAddress` - Function for getting self.ip_address

`setIPAddress` - Function for setting self.ip_address

`getDomainName` - Function for getting self.domain_name

`setDomainName` - Function for setting domain name

`getPort` - Function for getting port

`setPort` - Function for setting port

`getTimeout` - Function for getting timout in ms

`setTimeout` - Function for setting timeout in ms  

#### Network Service Functions

`getSignalQuality` - Fuction for getting signal quality

`getQueryNetworkInfo` - Function for getting network information

`connectToOperator` - Function for connecting to base station of operator

#### SMS Functions

`sendSMS` - Function for sending SMS

#### GNSS Functions

`turnOnGNSS` - Function for turning on GNSS

`turnOffGNSS` - Function for turning of GNSS

`getLatitude` - Function for getting latitude

`getLongitude` - Function for getting longitude

`getSpeedMph` - Function for getting speed in MPH	

`getSpeedKph` - Function for getting speed in KPH

`getFixedLocation` - Function for getting fixed location 

#### TCP & UDP Protocols Functions

`activateContext` - Function for configurating and activating TCP context 

`deactivateContext` - Function for deactivating TCP context 

`connectToServerTCP` - Function for connecting to server via TCP (just buffer access mode is supported for now)

`sendDataTCP` - Fuction for sending data via tcp (just buffer access mode is supported for now)

`sendDataSixfabConnect` - Function for sending data to Sixfab connect

`sendDataIFTTT` - Function for sending data to IFTTT

`sendDataThingspeak` - Function for sending data to Thingspeak

`startUDPService` - Function for connecting to server via UDP

`sendDataUDP` - Fuction for sending data via udp

`closeConnection` - Function for closing server connection

#### Shield Peripheral Functions

`readUserButton` - Function for reading user button

`turnOnUserLED` - Function for turning on user LED

`turnOffUserLED` - Function for turning off user LED

## CellularIoTApp Class

### Primary Functions

`setupGPIO` - Needs documentation

`enable` - Function for enable BG96 module

`disable` - Function for powering down BG96 module and all peripherals from voltage regulator

`powerUp` - Function for powering up or down BG96 module

`getModemStatus` - Function for getting modem power status

`readAccel` - Function for reading accelerometer

`readAdc` - Function for reading ADC

`readTemp` - Function for reading temperature

`readHum` - Function for reading humidity

`readLux` - Function for reading light resolution	

`turnOnRelay` - Function for turning on RELAY

`turnOffRelay` - Function for turning off RELAY

`readUserButton` - Function for reading user button

`turnOnUserLED` - Function for turning on user LED

`turnOffUserLED` - Function for turning off user LED


# Pinouts
## Sixfab RPi Cellular IoT Application Shield
![Pinout Schematic](https://sixfab-com.exactdn.com/wp-content/uploads/2018/10/rpi_cellulariot_app_shield_pinout-e1545901898330.png?strip=all&w=1170&ssl=1)

## Sixfab RPi Cellular IoT HAT
![Pinout Schematic](https://sixfab.com/wp-content/uploads/2019/04/RPi_Cell_IoT_Hat_Pinout_2-e1555326552762.jpg)


# Attention
! All data pins work with 3.3V reference. Any other voltage level should harm your hat or RPI.

# Layouts
## Sixfab RPi Cellular IoT Application Shield
![Layout](https://sixfab.com/wp-content/uploads/2018/10/rpi_cellulariot_application_shield_layout-1.png)

## Sixfab RPi Cellular IoT HAT
![Layout](https://sixfab.com/wp-content/uploads/2019/04/RPi_Cell_IoT_Hat_Layout_2-e1555326485159.jpg)
