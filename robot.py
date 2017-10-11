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
from components.shooter import Shooter
from components.groundGear import GroundGear

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
        self.gearSol           = GearSol(self.C.gearSol)
        self.shooter           = Shooter(self.C.shooterM, self.C.hopperM, self.C.shooterS, self.C.hopperS)
        self.vision            = Vision(self.drive, self.C.greenLEDR)
        self.autonomousRoutine = Autonomous(self.drive, self.bumpPop, self.gearSol, self.groundGear, self.vision)

        # Smart Dashboard
        self.sd = NetworkTable.getTable('SmartDashboard')
        self.sd.putBoolean('autoAngle', False)
        self.sd.putBoolean('isLeft', False)

        # Joysticks or xBox controller?
        self.controller = 'joysticks' # || joysticks

        if (self.controller == 'joysticks'):
            self.C.leftJ = wpilib.Joystick(0)
            self.C.middleJ = wpilib.Joystick(1)
            self.C.rightJ = wpilib.Joystick(2)
        elif (self.controller == 'xbox'):
            self.C.joystick = wpilib.XboxController(0)

    def operatorControl(self):
        # runs when robot is enabled
        while self.isOperatorControl() and self.isEnabled():
            '''
            Components
            '''
            # Drive
            if (self.controller == 'joysticks'):
                self.drive.run(self.C.leftJ.getX(),
                               self.C.leftJ.getY(),
                               self.C.middleJ.getX(),
                               self.C.leftJ.getRawButton(4),
                               self.C.leftJ.getRawButton(3),
                               self.C.leftJ.getRawButton(5),
                               self.C.leftJ.getRawButton(2))

            elif (self.controller == 'xbox'):
                self.drive.arcade(self.C.joystick.getRawAxis(0), self.C.joystick.getRawAxis(1), self.C.joystick.getRawAxis(4))

            # Back gear
            if (self.controller == 'joysticks'):
                if (self.C.middleJ.getRawButton(4)):
                    self.groundGear.run(True, 'out')
                elif (self.C.middleJ.getRawButton(5)):
                    self.groundGear.run(True, 'in')
                else:
                    self.groundGear.run(False, False)

            elif (self.controller == 'xbox'):
                if (self.C.joystick.getBumper(wpilib.GenericHID.Hand.kLeft)):
                    self.groundGear.run(True, 'out')
                elif (self.C.joystick.getTriggerAxis(wpilib.GenericHID.Hand.kLeft) > 0.5):
                    self.groundGear.run(True, 'in')
                else:
                    self.groundGear.run(False, False)

            # Front gear
            if (self.controller == 'joysticks'):
                if (self.C.middleJ.getRawButton(1) == True and self.C.middleJ.getRawButton(2) == True):
                    self.gearSol.run(True)
                else:
                    self.gearSol.run(False)

            elif (self.controller == 'xbox'):
                if (self.C.joystick.getTriggerAxis(wpilib.GenericHID.Hand.kRight) > 0.5):
                    self.gearSol.run(True)
                else:
                    self.gearSol.run(False)

            # LEDs
            if (self.controller == 'xbox'):
                if (self.C.joystick.getStickButton(wpilib.GenericHID.Hand.kRight)):
                    self.C.greenLEDR.set(wpilib.Relay.Value.kForward)
                else:
                    self.C.greenLEDR.set(wpilib.Relay.Value.kOff)
            elif (self.controller == 'joysticks'):
                if (self.C.middleJ.getRawButton(3)):
                    self.C.greenLEDR.set(wpilib.Relay.Value.kForward)
                else:
                    self.C.greenLEDR.set(wpilib.Relay.Value.kOff)

            # Climb
            if (self.controller == 'joysticks'):
                self.climb.run(self.C.rightJ.getRawButton(1))
            elif (self.controller == 'xbox'):
                self.climb.run(self.C.joystick.getBumper(wpilib.GenericHID.Hand.kRight))

            wpilib.Timer.delay(0.002) # wait for a motor update time

    def test(self):
        """This function is called periodically during test mode."""

    def autonomous(self):
        """Runs once during autonomous."""
        self.autonomousRoutine.run() # see autonomous.py

if __name__ == "__main__":
    wpilib.run(Randy)
