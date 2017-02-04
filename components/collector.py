"""
Runs the wheels on the front of the robot to pick up balls.
"""

class BallCollector(object):
    def __init__(self, motor):
        self.motor = motor

    def run(self, trigger):
        if (trigger == True):
            self.motor.set(1)
        else:
            self.motor.set(0)
