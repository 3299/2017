"""
Drives. Can accept input from joysticks or values [-1, 1]. Uses the gyro for better steering.
"""
import math
import helpers

class Chassis(object):
    def __init__(self, drive, gyro):
        self.drive = drive
        self.gyro  = gyro

        self.Kp    = 0.03

    def run(self, leftX, leftY, rightAngle):
        if (rightAngle == 90 or rightAngle == 180 or rightAngle == 270 and leftX == 0):
            return

        self.drive.mecanumDrive_Polar(leftY, rightAngle, leftX)
