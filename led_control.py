from machine import Pin

led = Pin(15, Pin.OUT)  # GPIO 15 voor externe LED

def led_aan():
    led.value(1)

def led_uit():
    led.value(0)
