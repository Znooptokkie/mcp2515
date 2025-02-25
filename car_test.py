from machine import Pin, PWM
import time

# Motor A
IN1 = Pin(2, Pin.OUT)
IN2 = Pin(3, Pin.OUT)
ENA = PWM(Pin(4))
ENA.freq(1000)  # 1 kHz PWM-frequentie

# Motor B
IN3 = Pin(6, Pin.OUT)
IN4 = Pin(7, Pin.OUT)
ENB = PWM(Pin(8))
ENB.freq(1000)

def motor_forward(speed=30000):
    """ Laat beide motoren vooruit draaien """
    IN1.high()
    IN2.low()
    IN3.high()
    IN4.low()
    ENA.duty_u16(speed)
    ENB.duty_u16(speed)

def motor_backward(speed=30000):
    """ Laat beide motoren achteruit draaien """
    IN1.low()
    IN2.high()
    IN3.low()
    IN4.high()
    ENA.duty_u16(speed)
    ENB.duty_u16(speed)

def motor_stop():
    """ Stopt beide motoren """
    IN1.low()
    IN2.low()
    IN3.low()
    IN4.low()
    ENA.duty_u16(0)
    ENB.duty_u16(0)

# Test motors
print("Motor vooruit")
motor_forward()
time.sleep(2)

print("Motor achteruit")
motor_backward()
time.sleep(2)

print("Motor stoppen")
motor_stop()
