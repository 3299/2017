"""
Drives. Can accept input from joysticks or values [-1, 1]. Uses the gyro for better steering.
"""
import helpers

class Chassis(object):
    def __init__(self, drive, gyro):
        self.drive = drive
        self.gyro  = gyro
        self.jDeadband = 0.05

    def run(self, leftX, leftY, rightX, rightY, squared, reverse):
        powerY = (leftY + rightY) / 2 # average of Y axis for going forward/backward
        powerX = (leftX + rightX) / 2 # average of X axis for strafing
        rotate = (leftY - rightY) / -2

        if (squared == False):
            if (powerY < 0):
                powerY = powerY**2
                powerY = powerY * -1
            else:
                powerY = powerY**2
            if (powerX < 0):
                powerX = powerX**2
                powerX = powerX * -1
            else:
                powerX = powerX**2
            if (rotate < 0):
                rotate = rotate**2
                rotate = rotate * -1
            else:
                rotate = rotate**2
            powerY = helpers.curve(powerY)
            powerX = helpers.curve(powerX)

        # deadband on rotate
        if (rotate < 0.75 and rotate > -0.75):
            rotate = 0

        if (reverse == True):
            powerY = - powerY
            powerX = - powerX

        self.drive.mecanumDrive_Cartesian(powerX, powerY, rotate * 0, 0)

    def arcadeDrive(self, x, y):
        self.drive.arcadeDrive(x, y)

    def set(self, power, direction, rotation):
        self.drive.mecanumDrive_Polar(power, direction, rotation)

    def cartesian(self, x, y, rotate):
        self.drive.mecanumDrive_Cartesian(x, y, rotate, 0)
