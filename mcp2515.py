import time
from machine import SPI, Pin

# MCP2515 SPI-opdrachten
CMD_RESET = 0xC0
CMD_READ = 0x03
CMD_WRITE = 0x02
CMD_RTS = 0x80
RXB0CTRL = 0x60
RXB0SIDH = 0x61
RXB0SIDL = 0x62
RXB0DLC = 0x65
RXB0D0 = 0x66

class MCP2515:
    def __init__(self, spi, cs):
        self.spi = spi
        self.cs = cs
        self.cs.init(Pin.OUT, value=1)

    def spi_transfer(self, command, data=[]):
        self.cs.value(0)
        self.spi.write(bytearray([command] + data))
        response = self.spi.read(len(data)) if data else None
        self.cs.value(1)
        return response

    def read_register(self, addr):
        self.cs.value(0)
        self.spi.write(bytearray([CMD_READ, addr]))
        data = self.spi.read(1)
        self.cs.value(1)
        return data[0]

    def write_register(self, addr, value):
        self.cs.value(0)
        self.spi.write(bytearray([CMD_WRITE, addr, value]))
        self.cs.value(1)

    def init_mcp2515(self):
        self.spi_transfer(CMD_RESET)
        time.sleep(0.1)

        # Baudrate instellen (500 kbps met 8MHz oscillator)
        self.write_register(0x2A, 0x00)  # CNF1
        self.write_register(0x29, 0x90)  # CNF2
        self.write_register(0x28, 0x02)  # CNF3

        # Zet alle maskers en filters uit (ontvang alle berichten)
        self.write_register(0x60, 0x00)  # RXB0CTRL
        self.write_register(0x70, 0x00)  # RXB1CTRL
        self.write_register(0x20, 0x00)  # RXM0SIDH
        self.write_register(0x24, 0x00)  # RXM1SIDH

        # Zet MCP2515 in normale modus
        self.write_register(0x0F, 0x00)

    def send_can_message(self, can_id, data):
        """Verzend een CAN-bericht met een ID en data-array."""
        self.write_register(0x31, (can_id >> 3) & 0xFF)
        self.write_register(0x32, (can_id << 5) & 0xE0)
        data_length = min(len(data), 8)
        self.write_register(0x35, data_length)

        for i in range(data_length):
            self.write_register(0x36 + i, data[i])

        self.spi_transfer(CMD_RTS | 0x01)

    def receive_can_message(self):
        """Ontvang een CAN-bericht als er een beschikbaar is."""
        interrupt_status = self.read_register(0x2C)  # CANINTF register
        if interrupt_status & 0x01 == 0:
            return None  # Geen bericht beschikbaar

        can_id_high = self.read_register(RXB0SIDH)
        can_id_low = self.read_register(RXB0SIDL)
        can_id = ((can_id_high << 3) | (can_id_low >> 5)) & 0x7FF

        data_length = self.read_register(RXB0DLC) & 0x0F
        data = [self.read_register(RXB0D0 + i) for i in range(data_length)]

        # Wis de RX0IF-flag zodat we nieuwe berichten kunnen ontvangen
        self.write_register(0x2C, interrupt_status & ~(0x01))

        return can_id, data
