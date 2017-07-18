# PTSprinkler driver module
import spidev

class PTDriver(object):
    """Low level driver object for the PTSprinkler driver board"""

    # Channels as defined on the PTSprinkler driver PCB
    CH1 = 0x02
    CH2 = 0x04
    CH3 = 0x08
    CH4 = 0x10
    CH5 = 0x20
    CH6 = 0x40
    CHALL = 0x7E

    # Channels as used with the pan/tilt stage and valves
    LEFT = CH1
    RIGHT = CH2
    UP = CH3
    DOWN = CH4
    VLV1 = CH5
    VLV2 = CH6

    def __init__(self):
        """Constructor: open and configure the SPI port
        The board uses a simple shift register with latching after load
        and on zero cross, but it works fine when driven by an SPI master"""
        self.spi = spidev.SpiDev()
        self.spi.open(0, 1)
        self.spi.max_speed_hz = 244000
        self.channels = 0

    def __del__(self):
        """Destructor: close the SPI port"""
        self.spi.close()

    def On(self, mask):
        """Turn the channels listed in the mask on"""
        self.channels = self.channels | mask
        self.spi.xfer([self.channels])

    def Off(self, mask):
        """Turn the channels listed in the mask off"""
        self.channels = self.channels & ~mask
        self.spi.xfer([self.channels])

    def PanLeft(self):
        """Pan the pan/tilt stage to the left"""
        self.channels = self.channels & ~self.RIGHT | self.LEFT
        self.spi.xfer([self.channels])

    def PanRight(self):
        """Pan the pan/tilt stage to the right"""
        self.channels = self.channels & ~self.LEFT | self.RIGHT
        self.spi.xfer([self.channels])

    def PanStop(self):
        """Stop panning the pan/tilt stage"""
        self.channels = self.channels & ~(self.LEFT|self.RIGHT)
        self.spi.xfer([self.channels])

    def TiltUp(self):
        """Tilt the pan/tilt stage up"""
        self.channels = self.channels & ~self.DOWN | self.UP
        self.spi.xfer([self.channels])

    def TiltDown(self):
        """Tilt the pan/tilt stage down"""
        self.channels = self.channels & ~self.UP | self.DOWN
        self.spi.xfer([self.channels])

    def TiltStop(self):
        """Stop tilting the pan/tilt stage"""
        self.channels = self.channels & ~(self.UP|self.DOWN)
        self.spi.xfer([self.channels])

    def Valve1(self, on):
        """Turn valve 1 on or off"""
        if on:
            self.channels = self.channels | self.VLV1
        else:
            self.channels = self.channels & ~self.VLV1
        self.spi.xfer([self.channels])

    def Valve2(self, on):
        """Turn valve 2 on or off"""
        if on:
            self.channels = self.channels | self.VLV2
        else:
            self.channels = self.channels & ~self.VLV2
        self.spi.xfer([self.channels])

