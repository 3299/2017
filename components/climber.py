"""
Runs the climber motor.
"""

class Climber(object):
    def __init__(self, motor):
        self.motor = motor

    def run(self, trigger):
        if (trigger == True):
            self.motor.set(-1)
        else:
            self.motor.set(0)
