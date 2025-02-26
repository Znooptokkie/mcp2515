import time
from machine import SPI, Pin, PWM
from mcp2515 import MCP2515

# SPI-instellingen voor MCP2515
spi = SPI(0, baudrate=10000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19), miso=Pin(16))
cs = Pin(17, Pin.OUT)

# Initialiseer MCP2515
can = MCP2515(spi, cs)
can.init_mcp2515()

# Motor A
IN1 = Pin(2, Pin.OUT)
IN2 = Pin(3, Pin.OUT)
ENA = PWM(Pin(4))
ENA.freq(1000)

# Motor B
IN3 = Pin(6, Pin.OUT)
IN4 = Pin(7, Pin.OUT)
ENB = PWM(Pin(8))
ENB.freq(1000)

def motor_forward(speed):
    IN1.high()
    IN2.low()
    IN3.high()
    IN4.low()
    ENA.duty_u16(speed)
    ENB.duty_u16(speed)

def motor_backward(speed):
    IN1.low()
    IN2.high()
    IN3.low()
    IN4.high()
    ENA.duty_u16(speed)
    ENB.duty_u16(speed)

def motor_stop():
    IN1.low()
    IN2.low()
    IN3.low()
    IN4.low()
    ENA.duty_u16(0)
    ENB.duty_u16(0)

# Luister naar CAN-berichten en bestuur motoren
while True:
    message = can.receive_can_message()
    
    if message:
        can_id, data = message

        if can_id == 0x200:  # ID 0x200 voor motorbesturing
            command = data[0]

            if command == 0x01:  # Vooruit
                snelheid = int(data[2]) * 65535 // 100  # 0-100% omzetten naar PWM-waarde
                print(f"Motor vooruit met snelheid: {snelheid}")
                motor_forward(snelheid)

            elif command == 0x02:  # Achteruit
                snelheid = int(data[2]) * 65535 // 100
                print(f"Motor achteruit met snelheid: {snelheid}")
                motor_backward(snelheid)

            elif command == 0x00:  # Stop
                print("Motor stoppen")
                motor_stop()

    time.sleep(0.1)  # CPU niet overbelasten
