'''
  Sixfab_RPi_CellularIoT_Library 
  -
  Library for Sixfab RPi CellularIoT Application Shield.
  -
  Created by Yasin Kaya (selengalp), August 28, 2018.
'''

import time
import serial
import RPi.GPIO as GPIO
from Adafruit_ADS1x15 import ADS1015
from .SDL_Pi_HDC1000 import *
from .MMA8452Q import MMA8452Q

# global variables
TIMEOUT = 3 # seconds
ser = serial.Serial()

###########################################
### Private Methods #######################
###########################################

# Function for printing debug message 
def debug_print(message):
	print(message)

# Function for getting time as miliseconds
def millis():
	return int(time.time())

# Function for delay as miliseconds
def delay(ms):
	time.sleep(float(ms/1000.0))


###########################################
### Cellular IoT App Shield Class #############
###########################################

class CellularIoT:
	board = "" # shield name (Cellular IoT or Cellular IoT App.)
	ip_address = "" # ip address       
	domain_name = "" # domain name   
	port_number = "" # port number 
	timeout = TIMEOUT # default timeout for function and methods on this library.
	
	response = "" # variable for modem self.responses
	compose = "" # variable for command self.composes
	
	USER_BUTTON = 22
	USER_LED = 27
	BG96_ENABLE = 17
	BG96_POWERKEY = 24 
	STATUS = 23

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
	LTE_NO_CHANGE = "0"

	# GSM Bands
	GSM_NO_CHANGE = "0"
	GSM_900 = "1"
	GSM_1800 = "2"
	GSM_850 = "4"
	GSM_1900 = "8"
	GSM_ANY = "F"

	SCRAMBLE_ON = "0"
	SCRAMBLE_OFF = "1"
	
	# Special Characters
	CTRL_Z = '\x1A'
	
	# Initializer function
	def __init__(self, serial_port="/dev/ttyS0", serial_baudrate=115200, board="Sixfab Raspberry Pi Cellular IoT Shield"):
		
		self.board = board
    	
		ser.port = serial_port
		ser.baudrate = serial_baudrate
		ser.parity=serial.PARITY_NONE
		ser.stopbits=serial.STOPBITS_ONE
		ser.bytesize=serial.EIGHTBITS
			
		debug_print(self.board + " Class initialized!")
	
	def setupGPIO(self):
		GPIO.setmode(GPIO.BCM)
		#GPIO.setwarnings(False)
		GPIO.setup(self.BG96_ENABLE, GPIO.OUT)
		GPIO.setup(self.BG96_POWERKEY, GPIO.OUT)
		GPIO.setup(self.STATUS, GPIO.IN)
		GPIO.setup(self.USER_BUTTON, GPIO.IN)
		GPIO.setup(self.USER_LED, GPIO.OUT)
			
	def __del__(self): 
		self.clearGPIOs()
		
 	# Function for clearing global compose variable 
	def clear_compose(self):
		self.compose = ""
	
	# Function for clearing GPIO's setup
	def clearGPIOs(self):
		GPIO.cleanup()
	
	# Function for enable BG96 module
	def enable(self):
		GPIO.output(self.BG96_ENABLE,0)
		debug_print("BG96 module enabled!")

	# Function for powering down BG96 module and all peripherals from voltage regulator 
	def disable(self):
		GPIO.output(self.BG96_ENABLE,1)
		debug_print("BG96 module disabled!")

	# Function for powering up or down BG96 module
	def powerUp(self):
		GPIO.output(self.BG96_POWERKEY,1)
		
		while self.getModemStatus():
			pass
		debug_print("BG96 module powered up!")
		
		GPIO.output(self.BG96_POWERKEY,0)
		

		
	# Function for getting modem power status
	def getModemStatus(self):
		return GPIO.input(self.STATUS)
	
	# Function for getting modem response
	def getResponse(self, desired_response):
		if (ser.isOpen() == False):
			ser.open()
			
		while 1:	
			self.response =""
			while(ser.inWaiting()):
				self.response += ser.read(ser.inWaiting()).decode('utf-8', errors='ignore')
			if(self.response.find(desired_response) != -1):
				debug_print(self.response)
				break
	
	# Function for sending data to module
	def sendDataCommOnce(self, command):
		if (ser.isOpen() == False):
			ser.open()		
		self.compose = ""
		self.compose = str(command)
		ser.reset_input_buffer()
		ser.write(self.compose.encode())
		debug_print(self.compose)

	# Function for sending at comamand to module
	def sendATCommOnce(self, command):
		if (ser.isOpen() == False):
			ser.open()		
		self.compose = ""
		self.compose = str(command) + "\r"
		ser.reset_input_buffer()
		ser.write(self.compose.encode())
		debug_print(self.compose)
		
	# Function for sending data to BG96_AT.
	def sendDataComm(self, command, desired_response, timeout = None):
		
		if timeout is None:
			timeout = self.timeout
        
		self.sendDataCommOnce(command)
		
		timer = millis()
		while 1:
			if( millis() - timer > timeout): 
				self.sendDataCommOnce(command)
				timer = millis()
			
			self.response =""
			while(ser.inWaiting()):
				self.response += ser.read(ser.inWaiting()).decode('utf-8', errors='ignore')
			if(self.response.find(desired_response) != -1):
				debug_print(self.response)
				break

	# Function for sending at command to BG96_AT.
	def sendATComm(self, command, desired_response, timeout = None):
		
		if timeout is None:
			timeout = self.timeout
			
		self.sendATCommOnce(command)
		
		f_debug = False
		
		timer = millis()
		while 1:
			if( millis() - timer > timeout): 
				self.sendATCommOnce(command)
				timer = millis()
				f_debug = False
			
			self.response =""
			while(ser.inWaiting()):
				try: 
					self.response += ser.read(ser.inWaiting()).decode('utf-8', errors='ignore')
					delay(100)
				except Exception as e:
					debug_print(e.Message)
				# debug_print(self.response)
					
			if(self.response.find(desired_response) != -1):
				debug_print(self.response)
				break

	# Function for saving conf. and reset BG96_AT module
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
		self.compose = "AT+QCFG=\"band\","
		self.compose += str(gsm_band)
		self.compose += ","
		self.compose += str(self.LTE_NO_CHANGE)
		self.compose += ","
		self.compose += str(self.LTE_NO_CHANGE)

		self.sendATComm(self.compose,"OK\r\n")
		self.clear_compose()

	# Function for setting Cat.M1 Band
	def setCATM1Band(self, catm1_band):
		self.compose = "AT+QCFG=\"band\","
		self.compose += str(self.GSM_NO_CHANGE)
		self.compose += ","
		self.compose += str(catm1_band)
		self.compose += ","
		self.compose += str(self.LTE_NO_CHANGE)

		self.sendATComm(self.compose,"OK\r\n")
		self.clear_compose()

	# Function for setting NB-IoT Band
	def setNBIoTBand(self, nbiot_band):
		self.compose = "AT+QCFG=\"band\","
		self.compose += str(self.GSM_NO_CHANGE)
		self.compose += ","
		self.compose += str(self.LTE_NO_CHANGE)
		self.compose += ","
		self.compose += str(nbiot_band)

		self.sendATComm(self.compose,"OK\r\n")
		self.clear_compose()

	# Function for getting current band settings
	def getBandConfiguration(self):
		return self.sendATComm("AT+QCFG=\"band\"","OK\r\n")


	# Function for setting scramble feature configuration 
	def setScrambleConf(self, scramble):
		self.compose = "AT+QCFG=\"nbsibscramble\","
		self.compose += scramble

		self.sendATComm(self.compose,"OK\r\n")
		self.clear_compose()

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

	# Function for getting self.ip_address
	def getIPAddress(self):
		return self.ip_address

	# Function for setting self.ip_address
	def setIPAddress(self, ip):
		self.ip_address = ip


	# Function for getting self.domain_name
	def getDomainName(self):
		return self.domain_name

	# Function for setting domain name
	def setDomainName(self, domain):
		self.domain_name = domain

	# Function for getting port
	def getPort(self):
		return self.port_number

	# Function for setting port
	def setPort(self, port):
		self.port_number = port

	# Function for getting timout in ms
	def getTimeout(self):
		return self.timeout

	# Function for setting timeout in ms    
	def setTimeout(self, new_timeout):
		self.timeout = new_timeout


	#******************************************************************************************
	#*** Network Service Functions ************************************************************
	#****************************************************************************************** 

	# Fuction for getting signal quality
	def getSignalQuality(self):
		return self.sendATComm("AT+CSQ","OK\r\n")

	# Function for getting network information
	def getQueryNetworkInfo(self):
		return self.sendATComm("AT+QNWINFO","OK\r\n")

	# Function for connecting to base station of operator
	def connectToOperator(self):
		debug_print("Trying to connect base station of operator...")
		self.sendATComm("AT+CGATT?","+CGATT: 1\r\n")
		self.getSignalQuality()

	
	#******************************************************************************************
	#*** SMS Functions ************************************************************************
	#******************************************************************************************
	
	# Function for sending SMS
	def sendSMS(self, number, text):
		self.sendATComm("AT+CMGF=1","OK\r\n") # text mode	
		delay(500)
		
		self.compose = "AT+CMGS=\""
		self.compose += str(number)
		self.compose += "\""

		self.sendATComm(self.compose,">")
		delay(1000)
		self.clear_compose()
		delay(1000)
		self.sendATCommOnce(text)
		self.sendATComm(self.CTRL_Z,"OK",8) # with 8 seconds timeout
		

	#******************************************************************************************
	#*** GNSS Functions ***********************************************************************
	#******************************************************************************************

	# Function for turning on GNSS
	def turnOnGNSS(self):
		self.sendATComm("AT+QGPS=1","OK\r\n")

	# Function for turning of GNSS
	def turnOffGNSS(self):
		self.sendATComm("AT+QGPSEND","OK\r\n")
	
	# Function for getting latitude
	def getLatitude(self):

		self.sendATComm("ATE0","OK\r\n")
		self.sendATCommOnce("AT+QGPSLOC=2")
		
		timer = millis()
		while 1:
			self.response = ""

			while(ser.inWaiting()):
				self.response += ser.readline().decode('utf-8')
				
				if( self.response.find("QGPSLOC") != -1 and self.response.find("OK") != -1 ):
					self.response = self.response.split(",")
					ser.close()
					return Decimal(self.response[1])
					
				if(self.response.find("\r\n") != -1 and self.response.find("ERROR") != -1 ):
					debug_print(self.response)
					ser.close()
					return 0
	
	# Function for getting longitude		
	def getLongitude(self):

		self.sendATComm("ATE0","OK\r\n")
		self.sendATCommOnce("AT+QGPSLOC=2")
		
		timer = millis()
		while 1:
			self.response = ""

			while(ser.inWaiting()):
				self.response += ser.readline().decode('utf-8')
				
				if( self.response.find("QGPSLOC") != -1 and self.response.find("OK") != -1 ):
					self.response = self.response.split(",")
					ser.close()
					return Decimal(self.response[2])
					
				if(self.response.find("\r\n") != -1 and self.response.find("ERROR") != -1 ):
					debug_print(self.response)
					ser.close()
					return 0
	
	# Function for getting speed in MPH			
	def getSpeedMph(self):

		self.sendATComm("ATE0","OK\r\n")
		self.sendATCommOnce("AT+QGPSLOC=2")
		
		timer = millis()
		while 1:
			self.response = ""

			while(ser.inWaiting()):
				self.response += ser.readline().decode('utf-8')
				
				if( self.response.find("QGPSLOC") != -1 and self.response.find("OK") != -1 ):
					self.response = self.response.split(",")
					ser.close()
					return round(Decimal(self.response[7])/Decimal('1.609344'), 1)
					
				if(self.response.find("\r\n") != -1 and self.response.find("ERROR") != -1 ):
					debug_print(self.response)
					ser.close()
					return 0
	
	# Function for getting speed in KMPH			
	def getSpeedKph(self):

		self.sendATComm("ATE0","OK\r\n")
		self.sendATCommOnce("AT+QGPSLOC=2")
		
		timer = millis()
		while 1:
			self.response = ""

			while(ser.inWaiting()):
				self.response += ser.readline().decode('utf-8')
				
				if( self.response.find("QGPSLOC") != -1 and self.response.find("OK") != -1 ):
					self.response = self.response.split(",")
					ser.close()
					return Decimal(self.response[7])
					
				if(self.response.find("\r\n") != -1 and self.response.find("ERROR") != -1 ):
					debug_print(self.response)
					ser.close()
					return 0

	# Function for getting fixed location 
	def getFixedLocation(self):
		return self.sendATComm("AT+QGPSLOC?","+QGPSLOC:")


	#******************************************************************************************
	#*** TCP & UDP Protocols Functions ********************************************************
	#******************************************************************************************

	# Function for configurating and activating TCP context 
	def activateContext(self):
	  self.sendATComm("AT+QICSGP=1","OK\r\n") 
	  delay(1000)
	  self.sendATComm("AT+QIACT=1","\r\n")

	# Function for deactivating TCP context 
	def deactivateContext(self):
	  self.sendATComm("AT+QIDEACT=1","\r\n")

	# Function for connecting to server via TCP
	# just buffer access mode is supported for now.
	def connectToServerTCP(self):
		self.compose = "AT+QIOPEN=1,1"
		self.compose += ",\"TCP\",\""
		self.compose += str(self.ip_address)
		self.compose += "\","
		self.compose += str(self.port_number)
		self.compose += ",0,0"

		self.sendATComm(self.compose,"OK\r\n")
		self.clear_compose()
		self.sendATComm("AT+QISTATE=0,1","OK\r\n")

	# Fuction for sending data via tcp.
	# just buffer access mode is supported for now.
	def sendDataTCP(self, data):
		self.compose = "AT+QISEND=1,"
		self.compose += str(len(data))

		self.sendATComm(self.compose,">")
		self.sendATComm(data,"SEND OK")
		self.clear_compose()
	
	# Function for sending data to Sixfab connect
	def sendDataSixfabConnect(self, server, token, data):
	
		self.compose = "AT+QHTTPCFG=\"contextid\",1"
		self.sendATComm(self.compose,"OK")
		self.clear_compose()
		
		self.compose = "AT+QHTTPCFG=\"requestheader\",1"
		self.sendATComm(self.compose,"OK")
		self.clear_compose()
		
		url = str("https://"+ server+ "/sixfabStage/")
		self.compose = "AT+QHTTPURL="
		self.compose += str(len(url))
		self.compose += ",80"
		self.setTimeout(20)
		self.sendATComm(self.compose,"CONNECT")
		self.clear_compose()
		self.sendDataComm(url,"OK")
	
		payload = "POST /sixfabStage/ HTTP/1.1\r\nHost: "+server+"\r\nx-api-key: "+ token +"\r\nContent-Type: application/json\r\nContent-Length: "+str(len(data))+"\r\n\r\n"
		payload += data
		
		print("POSTED DATA")
		print(payload)
		print("----------------")
	
		self.compose = "AT+QHTTPPOST="
		self.compose += str(len(payload))
		self.compose += ",60,60"
		
		self.sendATComm(self.compose,"CONNECT")
		self.clear_compose()
		self.sendDataComm(payload,"OK")
	
	# Function for sending data to IFTTT	
	def sendDataIFTTT(self, eventName, key, data):
		
		self.compose = "AT+QHTTPCFG=\"contextid\",1"
		self.sendATComm(self.compose,"OK")
		self.clear_compose()
		
		self.compose = "AT+QHTTPCFG=\"requestheader\",1"
		self.sendATComm(self.compose,"OK")
		self.clear_compose()
		
		self.compose = "AT+QHTTPCFG=\"self.responseheader\",1"
		self.sendATComm(self.compose,"OK")
		self.clear_compose()
		
		url = str("https://maker.ifttt.com/trigger/" + eventName + "/with/key/"+ key)
		self.compose = "AT+QHTTPURL="
		self.compose += str(len(url))
		self.compose += ",80"
		self.setTimeout(20)
		self.sendATComm(self.compose,"CONNECT")
		self.clear_compose()
		self.sendDataComm(url,"OK")
		
		payload = "POST /trigger/" + eventName + "/with/key/"+ key +" HTTP/1.1\r\nHost: maker.ifttt.com\r\nContent-Type: application/json\r\nContent-Length: "+str(len(data))+"\r\n\r\n"
		payload += data
	
		self.compose = "AT+QHTTPPOST="
		self.compose += str(len(payload))
		self.compose += ",60,60"
		
		self.sendATComm(self.compose,"CONNECT")
		self.clear_compose()
		self.sendDataComm(payload,"OK")
		
		delay(5000)
		
		self.sendATComm("AT+QHTTPREAD=80","+QHTTPREAD: 0")
	
	# Function for sending data to Thingspeak
	def sendDataThingspeak(self, key, data):
	
		self.compose = "AT+QHTTPCFG=\"contextid\",1"
		self.sendATComm(self.compose,"OK")
		self.clear_compose()
		
		self.compose = "AT+QHTTPCFG=\"requestheader\",0"
		self.sendATComm(self.compose,"OK")
		self.clear_compose()
		
		url = str("https://api.thingspeak.com/update?api_key=" + key + "&"+ data)
		self.compose = "AT+QHTTPURL="
		self.compose += str(len(url))
		self.compose += ",80"
		self.setTimeout(20)
		self.sendATComm(self.compose,"CONNECT")
		self.clear_compose()
		self.sendDataComm(url,"OK")
	
		delay(3000)
		
		self.sendATComm("AT+QHTTPGET=80","+QHTTPGET")

	# Function for connecting to server via UDP
	def startUDPService(self):
		port = "3005"

		self.compose = "AT+QIOPEN=1,1,\"UDP SERVICE\",\""
		self.compose += str(self.ip_address)
		self.compose += "\",0,"
		self.compose += str(port)
		self.compose += ",0"

		self.sendATComm(self.compose,"OK\r\n")
		self.clear_compose()
		self.sendATComm("AT+QISTATE=0,1","\r\n")

	# Fuction for sending data via udp.
	def sendDataUDP(self, data):
		self.compose = "AT+QISEND=1,"
		self.compose += str(len(data))
		self.compose += ",\""
		self.compose += str(self.ip_address)
		self.compose += "\","
		self.compose += str(self.port_number)

		self.sendATComm(self.compose,">")
		self.clear_compose()
		self.sendATComm(data,"SEND OK")

	# Function for closing server connection
	def closeConnection(self):
		self.sendATComm("AT+QICLOSE=1","\r\n")

	
	#******************************************************************************************
	#*** Shield Peripheral Functions **********************************************************
	#******************************************************************************************

	# Function for reading user button
	def readUserButton(self):
		return GPIO.input(self.USER_BUTTON)

	# Function for turning on user LED
	def turnOnUserLED(self):
		GPIO.output(self.USER_LED, 1)

	# Function for turning off user LED
	def turnOffUserLED(self):
		GPIO.output(self.USER_LED, 0)
		

###########################################
### Cellular IoT Application Shield Class #
###########################################

class CellularIoTApp(CellularIoT):
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
	LUX_CHANNEL = 3
	
	def __init__(self):
		super(CellularIoTApp, self).__init__(board="Sixfab Cellular IoT Application Hat")
		
	def __init__(self, serial_port="/dev/ttyS0", serial_baudrate=115200, board="Sixfab Raspberry Pi Cellular IoT Application Shield"):
		self.serial_port = serial_port
		self.serial_baudrate = serial_baudrate
		self.board = board
		super(CellularIoTApp, self).__init__(serial_port=self.serial_port, serial_baudrate=self.serial_baudrate, board=self.board)
	
	def __del__(self):
		self.clearGPIOs()
	
	def setupGPIO(self):
		GPIO.setmode(GPIO.BCM)
		#GPIO.setwarnings(False)
		GPIO.setup(self.BG96_ENABLE, GPIO.OUT)
		GPIO.setup(self.BG96_POWERKEY, GPIO.OUT)
		GPIO.setup(self.STATUS, GPIO.IN)
		GPIO.setup(self.RELAY, GPIO.OUT)
		GPIO.setup(self.USER_BUTTON, GPIO.IN)
		GPIO.setup(self.USER_LED, GPIO.OUT)
		
	# Function for enable BG96 module
	def enable(self):
		GPIO.output(self.BG96_ENABLE,1)
		debug_print("BG96 module enabled!")

	# Function for powering down BG96 module and all peripherals from voltage regulator 
	def disable(self):
		GPIO.output(self.BG96_ENABLE,0)
		debug_print("BG96 module disabled!")

	# Function for powering up or down BG96 module
	def powerUp(self):
		GPIO.output(self.BG96_POWERKEY,1)
		delay(1000)
		GPIO.output(self.BG96_POWERKEY,0)
		delay(2000)
		debug_print("BG96 module powered up!")
		
	# Function for getting modem power status
	def getModemStatus(self):
		return GPIO.input(self.STATUS)
		
	# Function for reading accelerometer
	def readAccel(self):
		mma = MMA8452Q()
		return mma.readAcc()
 
	# Function for reading ADC
	def readAdc(self, channelNumber):
		''' Only use 0,1,2,3(channel Number) for readAdc(channelNumber) function '''
		adc=ADS1015(address=0x49, busnum=1)
		adcValues = [0] * 4
		adcValues[channelNumber] = adc.read_adc(channelNumber, gain=1)
		return adcValues[channelNumber]

	# Function for reading temperature
	def readTemp(self):
		hdc1000 = SDL_Pi_HDC1000()
		hdc1000.setTemperatureResolution(HDC1000_CONFIG_TEMPERATURE_RESOLUTION_14BIT)
		return  hdc1000.readTemperature()

	# Function for reading humidity
	def readHum(self):
		hdc1000 = SDL_Pi_HDC1000()
		hdc1000.setHumidityResolution(HDC1000_CONFIG_HUMIDITY_RESOLUTION_14BIT)
		return hdc1000.readHumidity()

	# Function for reading light resolution	
	def readLux(self):
		adc=ADS1015(address=0x49, busnum=1)
		rawLux = adc.read_adc(self.LUX_CHANNEL, gain=1)
		lux = (rawLux * 100) / 1580
		return lux

	# Function for turning on RELAY
	def turnOnRelay(self):
		GPIO.output(self.RELAY, 1)

	# Function for turning off RELAY
	def turnOffRelay(self):
		GPIO.output(self.RELAY, 0)
	
		# Function for reading user button
	def readUserButton(self):
		return GPIO.input(self.USER_BUTTON)

	# Function for turning on user LED
	def turnOnUserLED(self):
		GPIO.output(self.USER_LED, 1)

	# Function for turning off user LED
	def turnOffUserLED(self):
		GPIO.output(self.USER_LED, 0)

