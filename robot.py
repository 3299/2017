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
from components.collector import BallCollector
from components.climber import Climber
from components.shooter import Shooter
from components.bumpPop import BumpPop
from components.groundGear import GroundGear
from components.ledStrip import LedStrip
from guide import Guiding

class Randy(wpilib.SampleRobot):
    def robotInit(self):
        self.C = Component() # Components inits all connected motors, sensors, and joysticks. See inits.py.

        # Setup subsystems
        self.drive     = Chassis(self.C.driveTrain, self.C.encoders, self.C.gyroS)
        self.collector = BallCollector(self.C.collectorM)
        self.shooter   = Shooter(self.C.shooterM, self.C.ballServos)
        self.climb     = Climber(self.C.climbM)
        self.bumpPop   = BumpPop(self.C.bumpPopR)
        self.groundGear= GroundGear(self.C.groundSol, self.C.groundGearR)
        self.ledStrip  = LedStrip(self.C.ledStrip)
        self.gearSol   = GearSol(self.C.gearSol)

        # Smart Dashboard
        self.sd = NetworkTable.getTable('SmartDashboard')
        self.sd.putBoolean('autoAngle', False)

        self.lastTime = 0 # used in Auto

    def operatorControl(self):
        # runs when robot is enabled
        while self.isOperatorControl() and self.isEnabled():
            print(self.C.gyroS.getRate())
            # Drive
            self.drive.run(self.C.leftJ.getX(),
                           self.C.leftJ.getY(),
                           self.C.middleJ.getX(),
                           self.C.middleJ.getY(),
                           self.C.leftJ.getRawButton(4),
                           self.C.leftJ.getRawButton(3),
                           self.C.leftJ.getRawButton(5),
                           self.C.leftJ.getRawButton(2),
                           self.C.middleJ.getRawButton(2),
                           'arcade')

            # Components
            if (self.C.middleJ.getRawButton(1) == True and self.C.middleJ.getRawButton(2) == True):
                self.gearSol.run(True)
            else:
                self.gearSol.run(False)
            self.collector.run(self.C.rightJ.getRawButton(4), self.C.rightJ.getRawButton(5))
            self.shooter.run(self.C.rightJ.getRawButton(2), self.C.rightJ.getRawButton(3))
            self.bumpPop.run(self.C.leftJ.getRawButton(1))
            self.groundGear.run(self.C.leftJ.getRawButton(1), self.C.middleJ.getRawButton(4))
            self.climb.run(self.C.rightJ.getRawButton(1))

            self.ledStrip.run(self.C.allienceS.get(), self.C.middleJ.getRawButton(1), wpilib.Timer.getMatchTime())

            wpilib.Timer.delay(0.002) # wait for a motor update time

    def test(self):
        """This function is called periodically during test mode."""

    def autonomous(self):
        """Runs once during autonomous."""
        if (self.sd.getBoolean('autoAngle') == True):
            print('running alternative auto')
            runTime = 1.6
        else:
            print('running main auto')
            runTime = 1.4

        self.C.gyroS.reset()
        self.bumpPop.run(True) # deploy Randy
        self.lastTime = time.clock()
        while (time.clock() - self.lastTime < runTime):
            self.drive.polar(0.5, 180, 3 * helpers.remap(self.C.gyroS.getRate(), -360, 360, -1, 1)) # drive forward

        self.drive.polar(0, 0, 0)
        wpilib.Timer.delay(1.5)
        self.gearSol.run(True)
        wpilib.Timer.delay(1)
        self.gearSol.run(False)
        self.bumpPop.run(False)

if __name__ == "__main__":
    wpilib.run(Randy)
