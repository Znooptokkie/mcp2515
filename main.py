import time
from machine import SPI, Pin
from mcp2515 import MCP2515

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
        
        # VOORBEELD voor ontvangen data te verwerken:
        if can_id == 0x200: # Maak id 0x200 LED aansturing
            if data[0] == 0x01:
                # led_aan()
                pass
            elif data[0] == 0x00:
                # led_uit()
                pass

    time.sleep(0.1)  # Voorkom overbelasting van de processor
