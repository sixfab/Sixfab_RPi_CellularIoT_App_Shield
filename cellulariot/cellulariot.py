'''
  Sixfab_RPi_CellularIoT_Library 
  -
  Library for Sixfab RPi CellularIoT Hat and 
  Sixfab RPi CellularIoT Application Hat.
  -
  Created by Yasin Kaya (selengalp), August 28, 2018.
'''

import time
import serial
import RPi.GPIO as GPIO
from .ADS1x15 import ADS1015
from .SDL_Pi_HDC1000 import *
from .MMA8452Q import MMA8452Q

# Peripheral Pin Definations
USER_BUTTON = 24
USER_LED = 27
BG96_ENABLE = 26
RELAY = 17
BG96_POWERKEY = 11 
STATUS = 20
AP_READY = 6
RING_INDICATOR = 13
OPTO1 = 10
OPTO2 = 18
LUX_CHANNEL = 0

# global variables
TIMEOUT = 3 # seconds
ser = serial.Serial()

###########################################
### Private Methods #######################
###########################################

# function for printing debug message 
def debug_print(message):
	print(message)

# function for getting time as miliseconds
def millis():
	return int(time.time())

# function for delay as miliseconds
def delay(ms):
	time.sleep(float(ms/1000.0))

###########################################
### Cellular IoT Hat Class ################
###########################################	
class CellularIoT:
	board = "" # hat name (Cellular IoT or Cellular IoT App.)
	ip_address = "" # ip address       
	domain_name = "" # domain name   
	port_number = "" # port number 
	timeout = TIMEOUT # default timeout for function and methods on this library.
	
	# Cellular Modes
	AUTO_MODE = 0
	GSM_MODE = 1
	CATM1_MODE = 2
	CATNB1_MODE = 3

	# LTE Bands
	LTE_B1 = "1"
	LTE_B2 = "2"
	LTE_B3 = "4"
	LTE_B4 = "8"
	LTE_B5 = "10"
	LTE_B8 = "80"
	LTE_B12 = "800"
	LTE_B13 = "1000"
	LTE_B18 = "20000"
	LTE_B19 = "40000"
	LTE_B20 = "80000"
	LTE_B26 = "2000000"
	LTE_B28 = "8000000"
	LTE_B39 = "4000000000" # catm1 only
	LTE_CATM1_ANY = "400A0E189F"
	LTE_CATNB1_ANY = "A0E189F"
	LTE_NO_CHANGE = "40000000"

	# GSM Bands
	GSM_NO_CHANGE = "00000000"
	GSM_900 = "00000001"
	GSM_1800 = "00000002"
	GSM_850 = "00000004"
	GSM_1900 = "00000008"
	GSM_ANY = "0000000F"

	SCRAMBLE_ON = "0"
	SCRAMBLE_OFF = "1"
	
	def __init__(self, serial_port="/dev/ttyS0", serial_baudrate=115200, board="Sixfab Cellular IoT Hat"):
		
		self.board = board
    	
		ser.port = serial_port
		ser.baudrate = serial_baudrate
		ser.parity=serial.PARITY_NONE
		ser.stopbits=serial.STOPBITS_ONE
		ser.bytesize=serial.EIGHTBITS
		
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(BG96_ENABLE, GPIO.OUT)
		GPIO.setup(BG96_POWERKEY, GPIO.OUT)
		GPIO.setup(STATUS, GPIO.IN)
			
		debug_print(self.board + " Class initialized!")
 
	def enable(self):
		GPIO.output(BG96_ENABLE,1)
		debug_print("BG96 module enabled!")

	# power down BG96 module and all peripherals from voltage regulator 
	def disable(self):
		GPIO.output(BG96_ENABLE,0)
		debug_print("BG96 module disabled!")

	# power up or down BG96 module
	def powerUp(self):
		GPIO.output(BG96_POWERKEY,1)
		time.sleep(0.3)
		GPIO.output(BG96_POWERKEY,0)
		time.sleep(3)
		
		while self.getModemStatus():
			pass
		
		debug_print("BG96 module powered up!")
		
	# get modem power status
	def getModemStatus(self):
		return GPIO.input(STATUS)

	# send at comamand to module
	def sendATCommOnce(self, command):
		if (ser.isOpen() == False):
			ser.open()		
		compose = ""
		compose = "\r\n" + str(command) + "\r\n"
		ser.reset_input_buffer()
		ser.write(compose.encode())
		debug_print(compose)

	# function for sending at command to BG96_AT.
	def sendATComm(self, command, desired_response):
		
		self.sendATCommOnce(command)
		
		timer = millis()
		while 1:
			if( millis() - timer > self.timeout): 
				self.sendATCommOnce(command)
				timer = millis()
			
			response =""
			while(ser.inWaiting()):
				response += ser.read(ser.inWaiting()).decode('utf-8')
			if(response.find(desired_response) != -1):
				debug_print(response)
				ser.close()
				break
	# function for saving conf. and reset BG96_AT module
	def resetModule(self):
		self.saveConfigurations()
		delay(200)
		self.disable()
		delay(200)
		self.enable()
		self.powerUp()

	# Function for save configurations that be done in current session. 
	def saveConfigurations(self):
		self.sendATComm("AT&W","OK\r\n")

	# Function for getting IMEI number
	def getIMEI(self):
		return self.sendATComm("AT+CGSN","OK\r\n")


	# Function for getting firmware info
	def getFirmwareInfo(self):
		return self.sendATComm("AT+CGMR","OK\r\n")

	# Function for getting hardware info
	def getHardwareInfo(self):
		return self.sendATComm("AT+CGMM","OK\r\n")


	# Function for setting GSM Band
	def setGSMBand(self, gsm_band):
		compose = "AT+QCFG=\"band\","
		compose += str(gsm_band)
		compose += ","
		compose += str(self.LTE_NO_CHANGE)
		compose += ","
		compose += str(self.LTE_NO_CHANGE)

		self.sendATComm(compose,"OK\r\n")

	# Function for setting Cat.M1 Band
	def setCATM1Band(self, catm1_band):
		compose = "AT+QCFG=\"band\","
		compose += str(self.GSM_NO_CHANGE)
		compose += ","
		compose += str(catm1_band)
		compose += ","
		compose += str(self.LTE_NO_CHANGE)

		self.sendATComm(compose,"OK\r\n")

	# Function for setting NB-IoT Band
	def setNBIoTBand(self, nbiot_band):
		compose = "AT+QCFG=\"band\","
		compose += str(self.GSM_NO_CHANGE)
		compose += ","
		compose += str(self.LTE_NO_CHANGE)
		compose += ","
		compose += str(nbiot_band)

		self.sendATComm(compose,"OK\r\n")

	# Function for getting current band settings
	def getBandConfiguration(self):
		return self.sendATComm("AT+QCFG=\"band\"","OK\r\n")


	# Function for setting scramble feature configuration 
	def setScrambleConf(self, scramble):
		compose = "AT+QCFG=\"nbsibscramble\","
		compose += scramble

		self.sendATComm(compose,"OK\r\n")

	# Function for setting running mode.
	def setMode(self, mode):
		if(mode == self.AUTO_MODE):
			self.sendATComm("AT+QCFG=\"nwscanseq\",00,1","OK\r\n")
			self.sendATComm("AT+QCFG=\"nwscanmode\",0,1","OK\r\n")
			self.sendATComm("AT+QCFG=\"iotopmode\",2,1","OK\r\n")
			debug_print("Modem configuration : AUTO_MODE")
			debug_print("*Priority Table (Cat.M1 -> Cat.NB1 -> GSM)")
		elif(mode == self.GSM_MODE):
			self.sendATComm("AT+QCFG=\"nwscanseq\",01,1","OK\r\n")
			self.sendATComm("AT+QCFG=\"nwscanmode\",1,1","OK\r\n")
			self.sendATComm("AT+QCFG=\"iotopmode\",2,1","OK\r\n")
			debug_print("Modem configuration : GSM_MODE")
		elif(mode == self.CATM1_MODE):
			self.sendATComm("AT+QCFG=\"nwscanseq\",02,1","OK\r\n")
			self.sendATComm("AT+QCFG=\"nwscanmode\",3,1","OK\r\n")
			self.sendATComm("AT+QCFG=\"iotopmode\",0,1","OK\r\n")
			debug_print("Modem configuration : CATM1_MODE")
		elif(mode == self.CATNB1_MODE):
			self.sendATComm("AT+QCFG=\"nwscanseq\",03,1","OK\r\n")
			self.sendATComm("AT+QCFG=\"nwscanmode\",3,1","OK\r\n")
			self.sendATComm("AT+QCFG=\"iotopmode\",1,1","OK\r\n")
			debug_print("Modem configuration : CATNB1_MODE ( NB-IoT )")

	# function for getting self.ip_address
	def getIPAddress(self):
		return self.ip_address

	# function for setting self.ip_address
	def setIPAddress(self, ip):
		self.ip_address = ip


	# function for getting self.domain_name
	def getDomainName(self):
		return self.domain_name

	# function for setting domain name
	def setDomainName(self, domain):
		self.domain_name = domain

	# function for getting port
	def getPort(self):
		return self.port_number

	# function for setting port
	def setPort(self, port):
		self.port_number = port

	# get timout in ms
	def getTimeout(self):
		return self.timeout

	# set timeout in ms    
	def setTimeout(self, new_timeout):
		self.timeout = new_timeout


	#******************************************************************************************
	#*** Network Service Functions ************************************************************
	#****************************************************************************************** 

	# 
	def getSignalQuality(self):
		return self.sendATComm("AT+CSQ","OK\r\n")


	#
	def getQueryNetworkInfo(self):
		return self.sendATComm("AT+QNWINFO","OK\r\n")

	# connect to base station of operator
	def connectToOperator(self):
		debug_print("Trying to connect base station of operator...")
		self.sendATComm("AT+CGATT?","+CGATT: 1\r\n")

		self.getSignalQuality()

	#******************************************************************************************
	#*** GNSS Functions ***********************************************************************
	#******************************************************************************************

	# Function for turning on GNSS
	def turnOnGNSS(self):
		self.sendATComm("AT+QGPS=1","OK\r\n")

	# Function for turning of GNSS
	def turnOffGNSS(self):
		self.sendATComm("AT+QGPSEND","OK\r\n")


	# Function for getting fixed location 
	def getFixedLocation(self):
		return self.sendATComm("AT+QGPSLOC?","+QGPSLOC:")

	#******************************************************************************************
	#*** TCP & UDP Protocols Functions ********************************************************
	#******************************************************************************************

	# function for configurating and activating TCP context 
	def activateContext(self):
	  self.sendATComm("AT+QICSGP=1","OK\r\n") 
	  delay(1000)
	  self.sendATComm("AT+QIACT=1","\r\n")

	# function for deactivating TCP context 
	def deactivateContext(self):
	  self.sendATComm("AT+QIDEACT=1","\r\n")

	# function for connecting to server via TCP
	# just buffer access mode is supported for now.
	def connectToServerTCP(self):
		compose = "AT+QIOPEN=1,1"
		compose += ",\"TCP\",\""
		compose += str(self.ip_address)
		compose += "\","
		compose += str(self.port_number)
		compose += ",0,0"

		self.sendATComm(compose,"OK\r\n")
		self.sendATComm("AT+QISTATE=0,1","OK\r\n")

	# fuction for sending data via tcp.
	# just buffer access mode is supported for now.
	def sendDataTCP(self, data):
		compose = "AT+QISEND=1,"
		compose += str(len(data))

		self.sendATComm(compose,">")
		self.sendATComm(data,"SEND OK")

	# function for connecting to server via UDP
	def startUDPService(self):
		port = "3005"

		compose = "AT+QIOPEN=1,1,\"UDP SERVICE\",\""
		compose += str(self.ip_address)
		compose += "\",0,"
		compose += str(port)
		compose += ",0"

		self.sendATComm(compose,"OK\r\n")
		self.sendATComm("AT+QISTATE=0,1","\r\n")

	# fuction for sending data via udp.
	def sendDataUDP(self, data):
		compose = "AT+QISEND=1,"
		compose += str(len(data))
		compose += ",\""
		compose += str(self.ip_address)
		compose += "\","
		compose += str(self.port_number)

		self.sendATComm(compose,">")
		self.sendATComm(data,"SEND OK")

	#function for closing server connection
	def closeConnection(self):
		self.sendATComm("AT+QICLOSE=1","\r\n")
			
###########################################
### Cellular IoT Application Hat Class ####
###########################################
class CellularIoTApp(CellularIoT):
	def __init__(self):
		super(CellularIoTApp, self).__init__(board="Sixfab Cellular IoT Application Hat")

	# 
	def readAccel(self):
		mma = MMA8452Q()
		return mma.readAcc()
 
	#
	def readAdc(self, channelNumber):
		''' Only use 0,1,2,3(channel Number) for readAdc(channelNumber) function '''
		adc=ADS1015(address=0x49, busnum=1)
		adcValues = [0] * 4
		adcValues[channelNumber] = adc.read_adc(channelNumber, gain=1)
		return adcValues[channelNumber]

	#
	def readTemp(self):
		hdc1000 = SDL_Pi_HDC1000()
		hdc1000.setTemperatureResolution(HDC1000_CONFIG_TEMPERATURE_RESOLUTION_14BIT)
		return  hdc1000.readTemperature()

	# 
	def readHum(self):
		hdc1000 = SDL_Pi_HDC1000()
		hdc1000.setHumidityResolution(HDC1000_CONFIG_HUMIDITY_RESOLUTION_14BIT)
		return hdc1000.readHumidity()

	#	
	def readLux(self):
		adc=ADS1015(address=0x49, busnum=1)
		rawLux = adc.read_adc(LUX_CHANNEL, gain=1)
		lux = (rawLux * 100) / 1580
		return lux

	#
	def turnOnRelay(self):
		GPIO.setup(RELAY, GPIO.OUT)
		GPIO.output(RELAY, 1)

	#
	def turnOffRelay(self):
		GPIO.setup(RELAY, GPIO.OUT)
		GPIO.output(RELAY, 0)

	#
	def readUserButton(self):
		GPIO.setup(USER_BUTTON, GPIO.IN)
		return GPIO.input(USER_BUTTON)

	#
	def turnOnUserLED(self):
		GPIO.setup(USER_LED, GPIO.OUT)
		GPIO.output(USER_LED, 1)

	#
	def turnOffUserLED(self):
		GPIO.setup(USER_LED, GPIO.OUT)
		GPIO.output(USER_LED, 0)
