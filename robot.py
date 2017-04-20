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
            '''
            Components
            '''
            # Drive
            self.drive.arcade(self.C.joystick.getRawAxis(0), self.C.joystick.getRawAxis(1), self.C.joystick.getRawAxis(2))

            # Back gear
            if (self.C.joystick.getBumper(wpilib.GenericHID.Hand.kLeft)):
                self.groundGear.run(True, 'out')
            elif (self.C.joystick.getTriggerAxis(wpilib.GenericHID.Hand.kLeft) > 0.5):
                self.groundGear.run(True, 'in')
            else:
                self.groundGear.run(False, False)

            # Front gear
            if (self.C.joystick.getTriggerAxis(wpilib.GenericHID.Hand.kRight) > 0.5):
                self.gearSol.run(True)
            else:
                self.gearSol.run(False)

            # Climb
            self.climb.run(self.C.joystick.getStickButton(wpilib.GenericHID.Hand.kRight))

            wpilib.Timer.delay(0.002) # wait for a motor update time

    def test(self):
        """This function is called periodically during test mode."""

    def autonomous(self):
        """Runs once during autonomous."""
        self.autonomousRoutine.run() # see autonomous.py

if __name__ == "__main__":
    wpilib.run(Randy)
