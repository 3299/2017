"""
Runs the wheels on the front of the robot to pick up balls.
"""

class BallCollector(object):
    def __init__(self, motor):
        self.motor = motor

    def run(self, trigger1, trigger2):
        if (trigger1 == True):
            self.motor.set(1)
        elif (trigger2 == True):
            self.motor.set(-1)
        else:
            self.motor.set(0)
