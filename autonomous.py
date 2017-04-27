"""
Runs the auto routine. Called once.
"""
from networktables import NetworkTable
import time
import wpilib

class Autonomous(object):
    def __init__(self, drive, randy, frontGear, backGear, vision):
        self.drive     = drive
        self.randy     = randy
        self.frontGear = frontGear
        self.backGear  = backGear
        self.vision    = vision
        self.sd        = NetworkTable.getTable('SmartDashboard')

    def run(self):
        self.randy.run(True) # deploy Randy

        if (self.sd.getBoolean('autoAngle') == True):
            # Drive forward
            startTime = time.clock()
            while (time.clock() - startTime < 2):
                self.drive.driveToAngle(-0.5, 0, True)

            # Stop
            self.drive.cartesian(0, 0, 0)

            # Turn 60 or -60 degrees
            if (self.sd.getBoolean('isLeft') == True):
                self.drive.driveToAngle(0, -60, False)
            else:
                self.drive.driveToAngle(0, 60, False)

            # Do vision
            if (self.vision.alignToPeg(direction=1) == False): # if returns an error, stop auto
                return False

            # Stop
            self.drive.cartesian(0, 0, 0)

        '''
        Center peg
        '''
        startTime = time.clock()
        while (time.clock() - startTime < 4.25):
            self.drive.cartesian(0, -0.3, 0.025)
        self.drive.cartesian(0, 0, 0)

        # Activate front gear
        self.frontGear.run(True)

        '''
        wpilib.Timer.delay(3)

        self.backGear.run(False, False)
        wpilib.Timer.delay(2)

        # Drive away
        startTime = time.clock()
        while (time.clock() - startTime < 2):
            self.drive.cartesian(0, -0.4, 0)
        self.drive.cartesian(0, 0, 0)
        '''

        # Stop Randy
        self.randy.run(False)
