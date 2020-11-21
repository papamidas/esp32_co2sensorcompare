# MHZ19B.py
# DM1CR Nov 14, 2020
# Class for CO2 Sensor
# for micropython on a ESP32
#

MHZ19B_CMD_READCO2 = bytes([0xFF,0x01,0x86,0,0,0,0,0,0x79])

class MHZ19B:
    
    def __init__(self, uart=None):
        self._uart = uart
        self._d = bytes(9)
        self._checksum = 0
        self.CO2 = 0
        if uart is None:
          raise ValueError('A UART object is required.')
    
    def getCheckSum(self):
        self._checksum = 0
        for _b in self._d[1:-1]:
            self._checksum += _b
            self._checksum = self._checksum & 0xff
        self._checksum = 0xff - self._checksum
        self._checksum += 1
        return self._checksum

    def getCO2(self):
        self._uart.write(MHZ19B_CMD_READCO2)
        self._d = self._uart.read(9)
        self.getCheckSum()
        
        #print("crc ist: " + str(self._d[-1]) + " soll: " + str(self._checksum))
        
        if(self._d[-1] != self._checksum):
            raise ValueError('crc error.')
        
        self.CO2 = self._d[2] * 256 + self._d[3]
        
        return self.CO2
        