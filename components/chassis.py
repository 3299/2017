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
        print(self.gyro.getAngle())
        powerY = (leftY + rightY) / 2 # average of Y axis for going forward/backward
        powerX = (leftX + rightX) / 2 # average of X axis for strafing
        rotate = (leftY - rightY) / -2

        if (squared == True):
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
        else:
            # deadband on rotate 20% only when not squarring inputs
            if (rotate < 0.2 and rotate > -0.2):
                rotate = 0
            if (powerX < 0.2 and powerX > -0.2):
                powerX = 0

        if (reverse == True):
            powerY = - powerY
            powerX = - powerX

        # snap the outputs to a standard angle
        #direction = helpers.snap(8, powerX, powerY)
        #self.drive.mecanumDrive_Polar((powerX + powerY) / 2, direction, rotate)

        self.drive.mecanumDrive_Cartesian(powerX, powerY, rotate * 0.75, 0)

    def arcadeDrive(self, x, y):
        self.drive.arcadeDrive(x, y)

    def set(self, power, direction, rotation):
        self.drive.mecanumDrive_Polar(power, direction, rotation)

    def cartesian(self, x, y, rotate):
        self.drive.mecanumDrive_Cartesian(x, y, rotate, 0)
