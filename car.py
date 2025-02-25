import time

class Wheel():

    def __init__(self, side):
        self.side = side # Motor A of B
        self.direction_1_pin = 0 # Vooruit Pin - IN1 A/B
        self.direction_2_pin = 0 # Achteruit Pin - IN2 A/B
        self.speed_pin = 0 # PWM signaal

        self.init_wheel()

    def speed(self):
        pass

    def direction(self):
        pass

    def brake(self):
        pass

    def init_wheel(self):
        
        if self.side == "A":
            self.direction_1_pin = 2 # GPIO2 - Pico
            self.direction_2_pin = 3 # GPIO3 - Pico
            self.speed_pin = 4 # GPIO4 - Pico
        elif self.side == "B":
            self.direction_1_pin = 6 # GPIO6 - Pico
            self.direction_2_pin = 7 # GPIO7 - Pico
            self.speed_pin = 8 # GPIO8 - Pico

    def __repr__(self):
        return f"Wheel(side={self.side}, direction_1_pin={self.direction_1_pin}, direction_2_pin={self.direction_2_pin}, speed_pin={self.speed_pin})"



if __name__ == "__main__":
    
    wheel_A = Wheel("A")
    print(wheel_A)
    
    wheel_b = Wheel("B")
    print(wheel_b)