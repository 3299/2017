"""
Runs the auto routine. Called once.
"""
from networktables import NetworkTable
import time

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
            while (time.clock() - startTime < 1.6):
                self.drive.driveToAngle(0.5, 0, True)

            # Stop
            self.drive.cartesian(0, 0, 0)

            # Turn 60 or -60 degrees
            if (self.sd.getBoolean('isLeft') == True):
                self.drive.driveToAngle(0, 60, False)
            else:
                self.drive.driveToAngle(0, 300, False)

        # Do vision
        self.vision.alignToPeg()

        # Activate back gear
        self.backGear.run(True, 'out')

        # Drive away
        startTime = time.clock()
        while (time.clock() - startTime < 0.5):
            self.drive.cartesian(-0.3, 0, 0)
        self.drive.cartesian(0, 0, 0)

        # Stop Randy
        self.randy.run(False)
