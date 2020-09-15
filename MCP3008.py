import time

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008


#Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))



def analogue(channel):
    
    
    # The read_adc function will get the value of the specified channel (0-7).
    return mcp.read_adc(channel)
while True:    
    print(analogue(0))
    time.sleep(0.5)


