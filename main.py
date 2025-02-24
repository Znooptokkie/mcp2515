import time
from machine import SPI, Pin
from mcp2515 import MCP2515
from led_control import led_aan, led_uit

# LED-instellingen
led = Pin(15, Pin.OUT)  # GPIO 15 voor externe LED

# SPI-instellingen voor MCP2515
spi = SPI(0, baudrate=10000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19), miso=Pin(16))
cs = Pin(17, Pin.OUT)

# Initialiseer MCP2515
can = MCP2515(spi, cs)
can.init_mcp2515()

# Hoofdloop: Luister naar CAN-berichten en schakel LED op basis van data
while True:
    message = can.receive_can_message()
    
    if message:
        can_id, data = message
        
        if can_id == 0x200:  # LED-besturing via CAN
            if data[0] == 0x01:
                led_aan()
            elif data[0] == 0x00:
                led_uit()

    time.sleep(0.1)  # Voorkom overbelasting van de processor
