"""
Drives. Can accept input from joysticks or values [-1, 1].
Uses the wheel-attached encoders as input for a threaded PID
loop on each wheel.
"""
import helpers
import wpilib
import math

from networktables import NetworkTable

class Chassis(object):
    def __init__(self, drive, gyro):
        self.drive          = drive
        self.gyro           = gyro
        self.jDeadband      = 0.05
        self.pidAngle       = wpilib.PIDController(0.015, 0, 0.02, self.anglePIDInput, output=self.anglePIDOutput)

        self.pidAngle.setInputRange(-180.0, 180.0)
        self.pidAngle.setOutputRange(-1.0, 1.0)
        self.pidAngle.setAbsoluteTolerance(1)
        self.pidAngle.setContinuous(False)
        self.pidRotateRate = 0

        self.sd = NetworkTable.getTable('SmartDashboard')
        self.sd.putNumber('p', 0.015)
        self.sd.putNumber('i', 0.0)
        self.sd.putNumber('d', 0.02)

    def run(self, leftX, leftY, rightX, microLeft, microTop, microRight, microBackward):
        self.arcade(helpers.raiseKeepSign(leftX, 2) + 0.4*(microRight - microLeft),
                    helpers.raiseKeepSign(leftY, 2) + 0.4*(microBackward - microTop),
                    rightX)

    def arcade(self, x1, y1, x2):
        # rotation deadzone
        if (-0.10 < x2 < 0.10):
            rotation = 0
        else:
            rotation = helpers.raiseKeepSign(-x2, 2) * 0.75

        direction = math.degrees(math.atan2(-x1, y1))

        # deadzone on power
        if (-0.1 < (abs(x1) + abs(y1))/2 < 0.1):
            power = 0
        else:
            if (abs(x1) > abs(y1)):
                power = abs(x1)
            elif (abs(x1) < abs(y1)):
                power = abs(y1)
            else:
                power = 1

        self.polar(power, direction, rotation)

    def cartesian(self, x, y, rotation):
        speeds = [0] * 4

        speeds[0] = -x + y + rotation
        speeds[1] = x + y - rotation
        speeds[2] = x + y + rotation
        speeds[3] = -x + y - rotation

        self.drive['frontLeft'].set(speeds[0])
        self.drive['frontRight'].set(speeds[1])
        self.drive['backLeft'].set(speeds[2])
        self.drive['backRight'].set(speeds[3])

    def polar(self, power, direction, rotation):
        power = power * math.sqrt(2.0)
        # The rollers are at 45 degree angles.
        dirInRad = math.radians(direction + 45)
        cosD = math.cos(dirInRad)
        sinD = math.sin(dirInRad)

        speeds = [0] * 4
        speeds[0] = sinD * power + rotation
        speeds[1] = cosD * power - rotation
        speeds[2] = cosD * power + rotation
        speeds[3] = sinD * power - rotation

        self.drive['frontLeft'].set(speeds[0])
        self.drive['frontRight'].set(speeds[1])
        self.drive['backLeft'].set(speeds[2])
        self.drive['backRight'].set(speeds[3])

    def driveToAngle(self, power, angle, continuous):
        self.pidAngle.setPID(self.sd.getNumber('p'), self.sd.getNumber('i'), self.sd.getNumber('d'))
        self.pidAngle.setSetpoint(angle)
        self.pidAngle.enable()
        self.pidAngle.setContinuous(continuous)

        if (continuous == True): # if true, runs continuously (for driving straight)
            self.cartesian(0, -power, -self.pidRotateRate)
        else:
            self.cartesian(0, 0, -self.pidRotateRate)

    def anglePIDInput(self):
        return helpers.normalizeAngle(self.gyro.getAngle())

    def anglePIDOutput(self, value):
        self.pidRotateRate = value

    def speedsToDirection(self, frontLeft, frontRight, backLeft, backRight):
    	x = (backLeft - frontLeft) / 2
    	y = (frontLeft + frontRight) / 2
    	rotation = (backLeft - frontRight) / 2

    	direction = math.degrees(math.atan2(x, -y))

    	return {'direction': -direction, 'rotation': rotation}
