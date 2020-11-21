# main.py
# DM1CR Nov 21, 2020
# Comparison of values from various CO2/VOC Sensors
# connected via I2C/UART to a ESP32 board
# with SSD1306 display
#
from VZ89TE import VZ89TE
from ssd1306 import SSD1306_I2C
from MHZ19B import *
from BME680 import *
from SCD30 import SCD30
import utime
from machine import Pin, I2C, UART

led = Pin(19, Pin.OUT)
led.on()

# Pin 16 is SSD1306 Display Enable
pin16 = Pin(16, Pin.OUT)
pin16.on()
displayi2c = I2C(scl=Pin(15), sda=Pin(4))
display = SSD1306_I2C(128, 64, displayi2c)
display.fill(0)

sensori2c = I2C(1,scl=Pin(22), sda=Pin(21), freq = 50000)
vz = VZ89TE(sensori2c)
bme = BME680_I2C(sensori2c)
scd = SCD30(sensori2c)
mhz = MHZ19B( UART(1, tx=32, rx=33, baudrate=9600, timeout=1000))

print("Display Width: ", display.width)
print("Display Height: ", display.height)
print("I2C slave(s) found at adr ")
for ad in sensori2c.scan():
    print("%x " % ad)
print("Revision: ", vz.getRevision())
print("Year: ", vz.getRevision()["Year"])
print("Month: ", vz.getRevision()["Month"])
print("Day: ", vz.getRevision()["Day"])

CO2DISPMAX = 1000
CO2DISPMIN = 400

scd.start()

while True:

    try:

         print("VZ89TE: ", vz.getData())
         print("BME680: Temp ", bme.temperature, " Hum ", bme.humidity, " Press ", bme.pressure, " Gas ", bme.gas)
         print("MHZ19: CO2 " + str(mhz.getCO2()))
    
    except ValueError:

         print("oops! crc error!")

    except OSError:

         print("oops! OS error!")
        
    success = scd.read()
    scdv={}
    if success == True:
        scdv = scd.values
        print("SCD30: ", scdv)
        #(s_co2, s_temperature, s_humidity, s_timestamp) = scd.values
        #print("SCD30: CO2 ", s_co2, " Temp ", s_temperature, " Hum ", s_humidity)
    else:
        print("SCD30 read failure")
    
    
    display.fill(0)
    pos = 0
    linincrement = 10
    display.text("m CO2: " + str(int(mhz.CO2)) + " ppm", 0, pos)
    pos += linincrement
    display.text("v CO2: " + str(int(vz.CO2)) + " ppm", 0, pos)
    pos += linincrement
    display.text("s CO2: " + str(scdv["co2"]), 0, pos)
    pos += linincrement
    display.text("b Res: " + str(int(bme.gas)), 0, pos)
    display.show()
    led.off()
    utime.sleep_ms(1000)
    led.on()
    utime.sleep_ms(1000)
