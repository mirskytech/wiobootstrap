import board
import busio
import digitalio
from adafruit_bus_device.spi_device import SPIDevice
import time
from time import sleep

wifi_handshake = digitalio.DigitalInOut(board.ESP_HANDSHAKE)
wifi_handshake.direction = digitalio.Direction.OUTPUT


wifi_reset = digitalio.DigitalInOut(board.ESP_RESET)
wifi_reset.direction = digitalio.Direction.OUTPUT
wifi_reset.value = False

wifi_enable = digitalio.DigitalInOut(board.ESP_ENABLE)
wifi_enable.direction = digitalio.Direction.OUTPUT


wifi_power = digitalio.DigitalInOut(board.ESP_POWER)
wifi_power.direction = digitalio.Direction.OUTPUT

cs = digitalio.DigitalInOut(board.ESP_CS)
cs.direction = digitalio.Direction.OUTPUT


wifi_handshake.value = True
wifi_enable.value = True
wifi_reset.value = True

cs.value = False
wifi_power.value = False

wifi_handshake.direction = digitalio.Direction.INPUT
cs.value = True


spi_bus = busio.SPI(board.HSPI_CLK, MISO=board.HSPI_MISO, MOSI=board.HSPI_MOSI)
spi_device = SPIDevice(spi_bus, cs, baudrate=200000)
time.sleep(1)

print(f"handshake is {'high' if handshake.value else 'low'}")

print("\n\nstart command sequence...")

master_requests_send = bytearray(b'\x01\x00\x00\xFE\x01\x04\x00')
master_read_status = bytearray(b'\x02\x04\x00\x00\x00\x00\x00')



with spi_device as spi:
    spi.write(master_requests_send)

sleep(0.1)

with spi_device as spi:
    spi.write(master_read_status)

print("request to send complete, wait for handshake...")

while not handshake.value:
    pass

print("handshake received")

print("checking slave status")


with spi_device as spi:
    spi.write(master_read_status)

with spi_device as spi:
    slave_read = bytearray(7)
    spi.readinto(slave_read)
    print(slave_read)

print("done")



# wifi=busio.UART(board.WIFI_TX, board.WIFI_RX, baudrate=115200, receiver_buffer_size=2048)
# wrst = digitalio.DigitalInOut(board.WIFI_RST)
# wmde = digitalio.DigitalInOut(board.WIFI_HANDSHAKE)
# wrst.direction = digitalio.Direction.OUTPUT
# wmde.direction = digitalio.Direction.OUTPUT
# wrst.value = 0
# wmde.value = 1
# wrst.value = 1

# print(wifi.read())
# wifi.write(bytearray('ATrn', 'utf-8'))
# print(wifi.read())
