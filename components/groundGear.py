"""
Pops the gear onto the peg (from ground pickup). Uses solenoids.
"""

import wpilib

class GroundGear(object):
    def __init__(self, sol, rollers):
        self.sol = sol
        self.rollers = rollers

    def run(self, trigger, rollerTrigger):
        if (trigger == True):
            self.sol.set(self.sol.Value.kForward)
        else:
            self.sol.set(self.sol.Value.kReverse)

        if (rollerTrigger == True):
            self.rollers.set(1)
        else:
            self.rollers.set(0)
