"""
Main logic code
"""
import wpilib
from networktables import NetworkTables

from inits import Component
import helpers

from components.vision import Vision
from components.chassis import Chassis
from components.belt import Belt
from components.sonic import Sonic
from components.arduino import Arduino
from components.ledStrip import LedStrip
from guide import Guiding

class MyRobot(wpilib.SampleRobot):
    def robotInit(self):
        self.C = Component() # Components inits all connected motors, sensors, and joysticks. See components.py.

        # Network Table for Pi (for vision tracking)
        self.sd = NetworkTables.getTable("vision")

        # Setup subsystems
        self.drive    = Chassis(self.C.driveTrain, self.C.gyroS)
        self.belt     = Belt(self.C.beltM)
        self.sonic    = Sonic(self.C.sonic)
        self.ledStrip = LedStrip(self.C.ledStrip)

        self.guide    = Guiding(self.sd, self.sonic, self.drive)

    def operatorControl(self):
        self.C.driveTrain.setSafetyEnabled(True) # keeps robot from going crazy if connection with DS is lost

        # runs when robot is enabled
        while self.isOperatorControl() and self.isEnabled():
            # Left trigger turns on vision guiding
            if (self.C.leftJ.getRawButton(0) == True):
                self.guide.guideCamera()
            else:
                # Drive
                self.drive.run(self.C.leftJ.getX(), self.C.leftJ.getY(), self.C.middleJ.getDirectionDegrees())

                # Components
                self.belt.run(self.C.rightJ.getRawButton(4), self.C.rightJ.getRawButton(5))
                self.ledStrip.run({
                    'r': helpers.remap(self.C.leftJ.getY(), -1, 1, 0, 255),
                    'g': helpers.remap(self.C.leftJ.getX(), -1, 1, 0, 255),
                    'b': helpers.remap(self.C.middleJ.getY(), -1, 1, 0, 255)
                })

            wpilib.Timer.delay(0.002) # wait for a motor update time

    def autonomous(self):
        """This function is called periodically during autonomous."""

    def test(self):
        """This function is called periodically during test mode."""

if __name__ == "__main__":
    wpilib.run(MyRobot)
