"""
Talks over NetworkTables to an instance
of RoboRealm running on the DS.
"""

from networktables import NetworkTable
import helpers
import wpilib

class Vision(object):
    def __init__(self, drive):
        self.sd = NetworkTable.getTable('SmartDashboard')
        self.drive = drive

        #PID (rotate)
        self.pidRotate = wpilib.PIDController(0.3, 0.1, 0.2, self.pidRotateInput, output=self.pidRotateOutput)
        self.pidRotate.setInputRange(-1, 1)
        self.pidRotate.setOutputRange(-1, 1)
        self.pidRotate.setAbsoluteTolerance(0.001)
        self.pidRotate.setContinuous(False)
        self.pidRotationRate = 0

        #PID (distance)
        self.pidDistance = wpilib.PIDController(3, 0.5, 0.4, self.pidDistanceInput, output=self.pidDistanceOutput)
        self.pidDistance.setInputRange(0, 0.15)
        self.pidDistance.setOutputRange(-1, 1)
        self.pidDistance.setAbsoluteTolerance(0)
        self.pidDistance.setContinuous(False)
        self.pidDistanceRate = 0

    def getPegOffset(self):
        try:
            middleX = (self.sd.getNumber('LEFTX') + self.sd.getNumber('RIGHTX')) / 2
            width = self.sd.getNumber('IMAGE_WIDTH')

            offset = ((middleX - width / 2) / width)
            return offset
        except:
            return False

    def getPegDistance(self):
        try:
            return self.sd.getNumber('BLOBAREA')

        except:
            return False

    def alignToPeg(self):
        offset = self.getPegOffset()

        if (offset != False):
            # rotate
            self.pidRotate.setSetpoint(0)
            self.pidRotate.enable()
            # distance
            self.pidDistance.setSetpoint(0.10)
            self.pidDistance.enable()
            #print(self.pidDistanceRate)
            self.drive.cartesian(offset*0.5, -self.pidDistanceRate, self.pidRotationRate)
        else:
            self.drive.cartesian(0, 0, 0)
            self.pidRotate.disable()
            self.pidDistance.disable()

    def pidRotateInput(self):
        return self.getPegOffset()

    def pidRotateOutput(self, value):
        self.pidRotationRate = value

    def pidDistanceInput(self):
        return self.getPegDistance()

    def pidDistanceOutput(self, value):
        self.pidDistanceRate = value
