# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# MMA8452Q
# This code is designed to work with the MMA8452Q_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Accelorometer?sku=MMA8452Q_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
##bus = smbus.SMBus(1)

# MMA8452Q address, 0x1C(28)
# Select Control register, 0x2A(42)
#		0x00(00)	StandBy mode
##bus.write_byte_data(0x1C, 0x2A, 0x00)
# MMA8452Q address, 0x1C(28)
# Select Control register, 0x2A(42)
#		0x01(01)	Active mode
##bus.write_byte_data(0x1C, 0x2A, 0x01)
# MMA8452Q address, 0x1C(28)
# Select Configuration register, 0x0E(14)
#		0x00(00)	Set range to +/- 2g
##bus.write_byte_data(0x1C, 0x0E, 0x00)

#time.sleep(0.5)

class MMA8452Q:
    
    def __init__(self):
        
        # Get I2C bus
        self.bus = smbus.SMBus(1)        
        # MMA8452Q address, 0x1C(28)
        # Select Control register, 0x2A(42)
        #		0x00(00)	StandBy mode
        self.bus.write_byte_data(0x1C, 0x2A, 0x00)
        # MMA8452Q address, 0x1C(28)
        # Select Control register, 0x2A(42)
        #		0x01(01)	Active mode
        self.bus.write_byte_data(0x1C, 0x2A, 0x01)
        # MMA8452Q address, 0x1C(28)
        # Select Configuration register, 0x0E(14)
        #		0x00(00)	Set range to +/- 2g
        self.bus.write_byte_data(0x1C, 0x0E, 0x00)  
    
        time.sleep(0.5)
    
        
    #public Function



    def readAcc(self):
        data = self.bus.read_i2c_block_data(0x1C, 0x00, 7)

        xAccl = (data[1] * 256 + data[2]) / 16
        if xAccl > 2047 :
            xAccl -= 4096

        yAccl = (data[3] * 256 + data[4]) / 16
        if yAccl > 2047 :
            yAccl -= 4096

        zAccl = (data[5] * 256 + data[6]) / 16
        if zAccl > 2047 :
            zAccl -= 4096

        return {'x': xAccl, 'y': yAccl, 'z': zAccl}
