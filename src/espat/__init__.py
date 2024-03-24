from adafruit_bus_device.spi_device import SPIDevice
from digitalio import DigitalInOut, Direction
import board
import busio
from enum import Enum, auto
from time import sleep

class ESPAT:

    class Mode(Enum):
        STATION_MODE = auto()
        SOFT_AP_MODE = auto()

    def _init_pin(self, board_pin, direction=Direction.OUTPUT, initial_value=False):
        pin = DigitalInOut(board_pin)
        pin.direction = direction
        if direction == Direction.OUTPUT:
            pin.value = initial_value

        return pin

    def __init__(self, mode=Mode.STATION_MODE):

        self.mode = mode

        self.wifi_handshake = DigitalInOut(board.ESP_HANDSHAKE)
        self.wifi_handshake.direction = Direction.OUTPUT

        self.wifi_reset = DigitalInOut(board.ESP_RESET)
        self.wifi_reset.direction = Direction.OUTPUT

        self.wifi_enable = DigitalInOut(board.ESP_ENABLE)
        self.wifi_enable.direction = Direction.OUTPUT

        self.wifi_power = DigitalInOut(board.ESP_POWER)
        self.wifi_power.direction = Direction.OUTPUT

        self.cs = DigitalInOut(board.ESP_CS)
        self.cs.direction = Direction.OUTPUT

    def activate(self, mode):

        self.power_on()
        self.wifi_init()

    def power_on(self):
        """
        https://github.com/IsQianGe/rp2040-spi/blob/master/ports/rp2/mod_wifi_spi.c#L349
        """

        self.wifi_handshake.value = True
        self.wifi_enable.value = True
        self.wifi_reset.value = True

        # select chip
        self.cs.value = False

        # enable (?) power
        self.wifi_power.value = False

        self.wifi_handshake.switch_to_input()
        self.cs.value = True

        self.spi_bus = busio.SPI(board.HSPI_CLK, MISO=board.HSPI_MISO, MOSI=board.HSPI_MOSI)
        self.spi_device = SPIDevice(self.spi_bus, self.cs, baudrate=200000)

    def _wifi_init(self):
        # https://github.com/IsQianGe/rp2040-spi/blob/master/ports/rp2/wifi_spi.c#L1339
        pass

    def power_off(self):
        raise NotImplementedError()

    class SPICommand(Enum):
        MASTER_WRITE_DATA_TO_SLAVE = 2
        MASTER_READ_DATA_FROM_SLAVE = 3
        MASTER_WRITE_STATUS_TO_SLAVE = 1
        MASTER_READ_STATUS_FROM_SLAVE = 4

    master_requests_send_to_slave = bytearray(b'\x01\x00\x00\xFE\x01\x04\x00')
    master_read_status_status_from_slave = bytearray(b'\x02\x04\x00\x00\x00\x00\x00')

    def send_at_command(self):

        # step 1 Master requests to send data
        with self.spi_device as spi:
            spi.write(self.master_requests_send_to_slave)

        # ESP pulls up handshake pin
        while not self.wifi_handshake.value:
            pass

        # ESP requests slave status and reads it
        with self.spi_device as spi:
            spi.write(self.master_read_status_status_from_slave)
            slave_read = bytearray(7)
            spi.readinto(slave_read)

            # check if slave status is ok (0x2)
            print(slave_read)

    def send_command(self):
        # https://github.com/IsQianGe/rp2040-spi/blob/master/ports/rp2/wifi_spi.c#L753
        raise NotImplementedError()

    def wifi_init(self):
        pass



