"""
Shoots balls using cardboard and
paper plates, tastefully decorated
with EDM artists.
"""

class Shooter(object):
    def __init__(self, shooterM, hopperM, shooterS, hopperS):
        self.shooterM = shooterM
        self.hopperM  = hopperM
        self.shooterS = shooterS
        self.hopperS  = hopperS

        self.hopperState = 'off'
        self.shooterState = 'off'
        self.hopperDirection = 1
        self.shooterDirection = -1

        self.limitSwitchTriggered = True

    def run(self, trigger):
        if (trigger == True):
            '''
            Shooter
            '''
            if (self.shooterState == 'off' and self.hopperState == 'off'):
                self.shooterState = 'running'
            elif (self.shooterState == 'running' or self.shooterState == 'pastlimitswitch'):
                # record when limit switch is no longer triggered
                if (self.shooterS.get() != self.limitSwitchTriggered):
                    self.shooterState == 'pastlimitswitch'

                # limit switch is triggered, stop the motor
                if (self.shooterS.get() == self.limitSwitchTriggered and self.shooterState == 'pastlimitswitch'):
                    self.shooterState = 'finished'
                else:
                    self.shooterM.set(self.shooterDirection) # otherwise keep running the motor

            # if 1 rev has completed, stop motor
            elif (self.shooterState == 'finished'):
                self.shooterState = 'off'
                self.hopperState = 'running'

            elif (self.shooterState == 'off'):
                self.shooterM.set(0)

            '''
            Hopper
            '''
            # inital turn on
            if (self.hopperState == 'off'):
                self.hopperM.set(0)

            # runs while plate makes 1 rev
            elif (self.hopperState == 'running' or self.hopperState == 'pastlimitswitch'):
                # record when limit switch is no longer triggered
                if (self.hopperS.get() != self.limitSwitchTriggered):
                    self.hopperState == 'pastlimitswitch'

                # limit switch is triggered, stop the motor
                if (self.hopperS.get() == self.limitSwitchTriggered and self.hopperState == 'pastlimitswitch'):
                    self.hopperState = 'finished'
                else:
                    self.hopperM.set(self.hopperDirection) # otherwise keep running the motor

            # if 1 rev has completed, stop the motor
            elif (self.hopperState == 'finished'):
                self.hopperM.set(0)

                # ball is now in shooter
                self.shooterState = 'running'


        else:
            self.hopperM.set(0)
            self.shooterM.set(0)
