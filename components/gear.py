"""
Pops the gear onto the peg. Uses solenoids.
"""

class GearSol(object):
    def __init__(self, sol):
        self.sol = sol
        self.state = 'DOWN'

    def run(self, trigger1, trigger2):
        '''
        if (trigger == True and self.state == 'UP'):
            self.sol['in'].set(True)
            self.sol['out'].set(False)
            self.state = 'DOWN'

        elif (trigger == True and self.state == 'DOWN'):
            self.sol['out'].set(True)
            self.sol['in'].set(False)
            self.state = 'UP'
        '''

        if (trigger1 == True):
            self.sol['in'].set(True)
        else:
            self.sol['in'].set(False)

        if (trigger2 == True):
            self.sol['out'].set(True)
        else:
            self.sol['out'].set(False)
