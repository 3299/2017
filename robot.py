"""
Main logic code
"""
import wpilib
from networktables import NetworkTables

from inits import Component
import helpers

from components.chassis import Chassis
from components.sonic import Sonic
from components.gear import GearSol
from components.collector import BallCollector
from components.climber import Climber
from components.shooter import Shooter
from components.ledStrip import LedStrip
from guide import Guiding

class MyRobot(wpilib.SampleRobot):
    def robotInit(self):
        self.C = Component() # Components inits all connected motors, sensors, and joysticks. See components.py.

        # Network Table for Pi (for vision tracking)
        # TODO: move this elsewhere
        self.sd = NetworkTables.getTable("SmartDashboard")
        self.sd.putNumberArray('x', [])
        self.sd.putNumberArray('y', [])

        # Setup subsystems
        self.drive     = Chassis(self.C.driveTrain, self.C.gyroS)
        self.gearSol   = GearSol(self.C.gearSol)
        self.collector = BallCollector(self.C.collectorM)
        self.shooter   = Shooter(self.C.shooterM, self.C.ballServos)
        self.climb     = Climber(self.C.climbM)
        self.sonic     = Sonic(self.C.sonicS)
        self.ledStrip  = LedStrip(self.C.ledStrip)

        self.guide    = Guiding(self.sd, self.sonic, self.drive)

    def operatorControl(self):
        self.C.driveTrain.setSafetyEnabled(True) # keeps robot from going crazy if connection with DS is lost

        # runs when robot is enabled
        while self.isOperatorControl() and self.isEnabled():
            # Drive
            self.drive.run(self.C.leftJ.getX(), self.C.leftJ.getY(), self.C.middleJ.getX(), self.C.middleJ.getY(), self.C.leftJ.getRawButton(2), self.C.middleJ.getRawButton(2))

            # Components
            self.gearSol.run(self.C.middleJ.getRawButton(1))
            self.collector.run(self.C.rightJ.getRawButton(4))
            self.shooter.run(self.C.rightJ.getRawButton(2), self.C.rightJ.getRawButton(3))
            self.climb.run(self.C.rightJ.getRawButton(1))

            if (self.C.allienceS.get() == True):
                self.ledStrip.run({'r': True, 'g': False, 'b': False})
            else:
                self.ledStrip.run({'r': False, 'g': False, 'b': True})

            wpilib.Timer.delay(0.002) # wait for a motor update time

    def autonomous(self):
        """This function is called periodically during autonomous."""

    def test(self):
        """This function is called periodically during test mode."""

if __name__ == "__main__":
    wpilib.run(MyRobot)
