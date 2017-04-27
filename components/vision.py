"""
Talks over NetworkTables to an instance
of RoboRealm running on the DS.
"""

from networktables import NetworkTable
import helpers
import wpilib
import time

class Vision(object):
    def __init__(self, drive, leds):
        self.sd = NetworkTable.getTable('SmartDashboard')
        self.drive = drive
        self.leds = leds
        self.direction = 1

        #PID (rotate)
        self.pidRotate = wpilib.PIDController(0.4, 0, 0.2, self.pidRotateInput, output=self.pidRotateOutput)
        self.pidRotate.setInputRange(-2.5, 2.5)
        self.pidRotate.setOutputRange(-1, 1)
        self.pidRotate.setAbsoluteTolerance(0)
        self.pidRotate.setContinuous(True)
        self.pidRotationRate = 0

        #PID (strafe)
        self.pidStrafe = wpilib.PIDController(1.5, 0, 0.1, self.pidStrafeInput, output=self.pidStrafeOutput)
        self.pidStrafe.setInputRange(0, 1)
        self.pidStrafe.setOutputRange(-1, 1)
        self.pidStrafe.setAbsoluteTolerance(0.001)
        self.pidStrafe.setContinuous(True)
        self.pidStrafeRate = 0

        #PID (distance)
        self.pidDistance = wpilib.PIDController(4, 0.1, 0.2, self.pidDistanceInput, output=self.pidDistanceOutput)
        self.pidDistance.setInputRange(0, 0.15)
        self.pidDistance.setOutputRange(-1, 1)
        self.pidDistance.setAbsoluteTolerance(0.03)
        self.pidDistance.setContinuous(False)
        self.pidDistanceRate = 0

    def getPegAngle(self):
        try:
            distance = self.sd.getNumber('DISTANCE_BETWEEN') * 1000

            if (self.getPegOffset() < 0.5):
                distance = distance * -1

            return distance
        except:
            return False

    def getPegOffset(self):
        try:
            x = self.sd.getNumber('PATTERN_X')
            return x
        except:
            return False

    def getPegDistance(self):
        try:
            return self.sd.getNumber('BLOBAREA')

        except:
            return False

    def alignToPeg(self, direction):
        try:
            # turn on LEDs
            self.leds.set(wpilib.Relay.Value.kForward)

            offset = self.getPegOffset()
            self.direction = direction

            # rotate
            self.pidRotate.setSetpoint(0)
            self.pidRotate.enable()
            # strafe
            self.pidStrafe.setSetpoint(0.5)
            self.pidStrafe.enable()

            # distance
            self.pidDistance.setSetpoint(0.1)
            self.pidDistance.enable()

            while (abs(self.pidStrafeInput() - 0.5) > 0.01 and self.pidDistanceInput() < 0.11 and self.sd.getNumber('BLOB_COUNT') != 0):
                self.drive.cartesian(self.pidStrafeRate*self.direction, 0.3 * self.direction, 0)#, self.pidRotationRate)

                wpilib.Timer.delay(0.002) # wait for a motor update time

            self.drive.cartesian(0, 0, 0)

            # small boost at the end to go all the way
            lastTime = time.clock()
            while (time.clock() - lastTime < 1):
                self.drive.cartesian(0, self.direction*0.4, 0)

            # turn off leds
            self.leds.set(wpilib.Relay.Value.kOff)
        except:
            return False

    def pidRotateInput(self):
        return self.getPegAngle()

    def pidRotateOutput(self, value):
        self.pidRotationRate = value

    def pidStrafeInput(self):
        return self.getPegOffset()

    def pidStrafeOutput(self, value):
        self.pidStrafeRate = value

    def pidDistanceInput(self):
        return self.getPegDistance()

    def pidDistanceOutput(self, value):
        self.pidDistanceRate = value
