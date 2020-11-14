# main.py
# DM1CR Nov 14, 2020
# CO2 sensor comparison
# for micropython on a ESP32
#
from VZ89TE import VZ89TE
import utime
from machine import Pin, I2C

def mapvalue(x, in_min, in_max, out_min, out_max):
    if (x > in_max):
        x = inmax
    if (x < in_min):
        x = in_min
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

led = Pin(23, Pin.OUT)
led.on()

sensori2c = I2C(1,scl=Pin(22), sda=Pin(21), freq = 100000)
vz89te = VZ89TE(sensori2c)

mhz19uart = machine.UART(1, tx=32, rx=33, baudrate=9600, timeout=1000)
mhz19 = MHZ19(mhz19uart)

print("I2C slave found at adr ", hex(sensori2c.scan()[0]) )
print("Revision: ", vz89te.getRevision())
print("Year: ", vz89te.getRevision()["Year"])
print("Month: ", vz89te.getRevision()["Month"])
print("Day: ", vz89te.getRevision()["Day"])

CO2DISPMAX = 1000
CO2DISPMIN = 400
co2 = 0

while True:

    try:

#        co2 = vz89te.getData()["CO2"]
#        print(co2)
         print("VZ89TE: " + str(sensor.getData()))
         
         print("MHZ19: " + str(mhz19.getCO2()))

    except ValueError:

         print("oops! crc error!")

    except OSError:

         print("oops! OS error!")

    led.off()
    utime.sleep_ms(500)
    led.on()
    utime.sleep(2)
