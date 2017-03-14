"""
Pushes a bar out in front of the bumpers for aligning with the gear peg.
"""
import wpilib

class BumpPop(object):
    def __init__(self, output):
        self.output = output

    def run(self, trigger):
        if (trigger == True):
            self.output.set(wpilib.Relay.Value.kForward)
        else:
            self.output.set(wpilib.Relay.Value.kOff)
