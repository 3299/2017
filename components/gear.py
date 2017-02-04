"""
Pops the gear onto the peg. Uses solenoids.
"""

class GearSol(object):
    def __init__(self, sol):
        self.sol = sol

    def run(self, trigger):
        if (trigger == True):
            self.sol.set(self.sol.Value.kForward)
        else:
            self.sol.set(self.sol.Value.kReverse)
