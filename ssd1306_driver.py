"""
MicroPython SSD1306 OLED driver, I2C and SPI interfaces.

This is a driver for the SSD1306 OLED display, originally created by Adafruit
and adapted for MicroPython.
"""

# Standard Library
import time

# Third-Party
import framebuf

# Register definitions
SET_CONTRAST = const(0x81)
SET_ENTIRE_ON = const(0xA4)
SET_NORM_INV = const(0xA6)
SET_DISP = const(0xAE)
SET_MEM_ADDR = const(0x20)
SET_COL_ADDR = const(0x21)
SET_PAGE_ADDR = const(0x22)
SET_DISP_START_LINE = const(0x40)
SET_SEG_REMAP = const(0xA0)
SET_MUX_RATIO = const(0xA8)
SET_COM_OUT_DIR = const(0xC0)
SET_DISP_OFFSET = const(0xD3)
SET_COM_PIN_CFG = const(0xDA)
SET_DISP_CLK_DIV = const(0xD5)
SET_PRECHARGE = const(0xD9)
SET_VCOM_DESEL = const(0xDB)
SET_CHARGE_PUMP = const(0x8D)

# Custom degree symbol character
p0 = bytearray([0x18, 0x24, 0x24, 0x18, 0x00, 0x00, 0x00, 0x00])
DEGREE = framebuf.FrameBuffer(p0, 8, 8, framebuf.MONO_HLSB)


class SSD1306:
    """Base class for SSD1306 OLED drivers."""

    def __init__(self, width, height, external_vcc):
        """Initialize the display."""
        self.width = width
        self.height = height
        self.external_vcc = external_vcc
        self.pages = self.height // 8
        self.poweron()
        self.init_display()

    def init_display(self):
        """Initialize the display registers."""
        for cmd in (
            SET_DISP | 0x00,  # off
            SET_MEM_ADDR,
            0x00,  # horizontal addressing mode
            SET_DISP_START_LINE | 0x00,
            SET_SEG_REMAP | 0x01,  # column addr 127 mapped to SEG0
            SET_MUX_RATIO,
            self.height - 1,
            SET_COM_OUT_DIR | 0x08,  # scan from COM[N-1] to COM0
            SET_DISP_OFFSET,
            0x00,
            SET_COM_PIN_CFG,
            0x02 if self.height == 32 else 0x12,
            SET_DISP_CLK_DIV,
            0x80,
            SET_PRECHARGE,
            0x22 if self.external_vcc else 0xF1,
            SET_VCOM_DESEL,
            0x30,  # 0.83*Vcc
            SET_CONTRAST,
            0xFF,  # maximum contrast
            SET_ENTIRE_ON,  # output follows RAM contents
            SET_NORM_INV,  # not inverted
            SET_CHARGE_PUMP,
            0x10 if self.external_vcc else 0x14,
            SET_DISP | 0x01,  # on
        ):
            self.write_cmd(cmd)
        self.fill(0)
        self.show()

    def poweron(self):
        """Power on the display."""
        raise NotImplementedError()

    def poweroff(self):
        """Power off the display."""
        self.write_cmd(SET_DISP | 0x00)

    def contrast(self, contrast):
        """Set the display contrast."""
        self.write_cmd(SET_CONTRAST)
        self.write_cmd(contrast)

    def invert(self, invert):
        """Invert the display colors."""
        self.write_cmd(SET_NORM_INV | (invert & 1))

    def show(self):
        """Update the display with the framebuffer contents."""
        x0 = 0
        x1 = self.width - 1
        if self.width == 64:
            # displays with width of 64 pixels are shifted by 32
            x0 += 32
            x1 += 32
        self.write_cmd(SET_COL_ADDR)
        self.write_cmd(x0)
        self.write_cmd(x1)
        self.write_cmd(SET_PAGE_ADDR)
        self.write_cmd(0)
        self.write_cmd(self.pages - 1)
        self.write_framebuf()

    def fill(self, col):
        """Fill the framebuffer with a color."""
        self.framebuf.fill(col)

    def pixel(self, x, y, col):
        """Set a pixel in the framebuffer."""
        self.framebuf.pixel(x, y, col)

    def scroll(self, dx, dy):
        """Scroll the framebuffer."""
        self.framebuf.scroll(dx, dy)

    def text(self, string, x, y, col=1):
        """Write text to the framebuffer."""
        self.framebuf.text(string, x, y, col)

    def blit(self, fbuf, x, y, key=-1, palette=None):
        """Bit-level copy from another framebuffer to this one."""
        self.framebuf.blit(fbuf, x, y, key, palette)


class SSD1306_I2C(SSD1306):
    """I2C-specific SSD1306 driver."""

    def __init__(self, width, height, i2c, addr=0x3C, external_vcc=False):
        """Initialize the I2C display."""
        self.i2c = i2c
        self.addr = addr
        self.temp = bytearray(2)
        self.buffer = bytearray(((height // 8) * width) + 1)
        self.buffer[0] = 0x40  # Co=0, D/C=1
        self.framebuf = framebuf.FrameBuffer1(
            memoryview(self.buffer)[1:], width, height
        )
        super().__init__(width, height, external_vcc)

    def write_cmd(self, cmd):
        """Write a command to the display."""
        self.temp[0] = 0x80  # Co=1, D/C#=0
        self.temp[1] = cmd
        self.i2c.writeto(self.addr, self.temp)

    def write_framebuf(self):
        """Write the framebuffer to the display."""
        self.i2c.writeto(self.addr, self.buffer)

    def poweron(self):
        """Power on the I2C display."""
        pass


class SSD1306_SPI(SSD1306):
    """SPI-specific SSD1306 driver."""

    def __init__(self, width, height, spi, dc, res, cs, external_vcc=False):
        """Initialize the SPI display."""
        self.rate = 10 * 1024 * 1024
        dc.init(dc.OUT, value=0)
        res.init(res.OUT, value=0)
        cs.init(cs.OUT, value=1)
        self.spi = spi
        self.dc = dc
        self.res = res
        self.cs = cs
        self.buffer = bytearray((height // 8) * width)
        self.framebuf = framebuf.FrameBuffer1(self.buffer, width, height)
        super().__init__(width, height, external_vcc)

    def write_cmd(self, cmd):
        """Write a command to the display."""
        self.spi.init(baudrate=self.rate, polarity=0, phase=0)
        self.cs.high()
        self.dc.low()
        self.cs.low()
        self.spi.write(bytearray([cmd]))
        self.cs.high()

    def write_framebuf(self):
        """Write the framebuffer to the display."""
        self.spi.init(baudrate=self.rate, polarity=0, phase=0)
        self.cs.high()
        self.dc.high()
        self.cs.low()
        self.spi.write(self.buffer)
        self.cs.high()

    def poweron(self):
        """Power on the SPI display."""
        self.res.high()
        time.sleep_ms(1)
        self.res.low()
        time.sleep_ms(10)
        self.res.high()
