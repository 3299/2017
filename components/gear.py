"""
Pops the gear onto the peg. Uses solenoids.
"""

class GearSol(object):
    def __init__(self, sol):
        self.sol = sol

    def run(self, trigger):
        self.sol['in'].set(trigger)
        self.sol['out'].set(not trigger)
