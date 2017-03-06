"""
Runs the shooter wheel to shoot balls in the high goal.
"""

class Shooter(object):
    def __init__(self, motor, servos):
        self.motor = motor
        self.servos = servos

    def run(self, trigger1, trigger2):
        if (trigger1 == True):
            self.motor.set(1)
        else:
            self.motor.set(0)

        if (trigger2 == True):
            self.servos['servo1'].set(-1)
            self.servos['servo2'].set(1)
        else:
            self.servos['servo1'].set(1)
            self.servos['servo2'].set(-1)
