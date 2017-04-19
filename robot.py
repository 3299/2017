"""
Main logic code
"""
import wpilib
import time
from networktables import NetworkTable

from inits import Component
import helpers

from components.chassis import Chassis
from components.gear import GearSol
from components.climber import Climber
from components.bumpPop import BumpPop
from components.groundGear import GroundGear
from components.ledStrip import LedStrip

from components.vision import Vision
from autonomous import Autonomous

class Randy(wpilib.SampleRobot):
    def robotInit(self):
        # init cameras
        wpilib.CameraServer.launch('cameras.py:main')

        self.C = Component() # Components inits all connected motors, sensors, and joysticks. See inits.py.

        # Setup subsystems
        self.drive             = Chassis(self.C.driveTrain, self.C.gyroS)
        self.climb             = Climber(self.C.climbM)
        self.bumpPop           = BumpPop(self.C.bumpPopR)
        self.groundGear        = GroundGear(self.C.groundSol, self.C.groundGearM)
        self.ledStrip          = LedStrip(self.C.ledStrip)
        self.gearSol           = GearSol(self.C.gearSol)
        self.vision            = Vision(self.drive)
        self.autonomousRoutine = Autonomous(self.drive, self.bumpPop, self.gearSol, self.groundGear, self.vision)

        # Smart Dashboard
        self.sd = NetworkTable.getTable('SmartDashboard')
        self.sd.putBoolean('autoAngle', True)
        self.sd.putBoolean('isLeft', True)

    def operatorControl(self):
        # runs when robot is enabled
        while self.isOperatorControl() and self.isEnabled():

            if (self.C.middleJ.getRawButton(8) == True):
                self.drive.driveToAngle(0.5, 60, continuous=False)
                #self.vision.alignToPeg()

            else:
                self.C.gyroS.reset()
                # Drive
                self.drive.run(self.C.leftJ.getX(),
                               self.C.leftJ.getY(),
                               self.C.middleJ.getX(),
                               self.C.leftJ.getRawButton(4),
                               self.C.leftJ.getRawButton(3),
                               self.C.leftJ.getRawButton(5),
                               self.C.leftJ.getRawButton(2))

                # Components
                if (self.C.middleJ.getRawButton(1) == True and self.C.middleJ.getRawButton(2) == True):
                    self.gearSol.run(True)
                else:
                    self.gearSol.run(False)
                self.groundGear.run(self.C.leftJ.getRawButton(1), self.C.middleJ.getRawButton(4))
                self.climb.run(self.C.rightJ.getRawButton(1))

            wpilib.Timer.delay(0.002) # wait for a motor update time

    def test(self):
        """This function is called periodically during test mode."""

    def autonomous(self):
        """Runs once during autonomous."""
        self.autonomousRoutine.run() # see autonomous.py

if __name__ == "__main__":
    wpilib.run(Randy)
