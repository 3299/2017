"""
Defines port numbers for motors and sensors.
"""

class Map(object):
    def __init__(self):
        # Joysticks have suffix 'J'
        self.leftJ       = 0
        self.middleJ     = 1
        self.rightJ      = 2

        # Motors have suffix 'M'. All motors us e PWM.
        self.frontLeftM  = 0
        self.frontRightM = 1
        self.backLeftM   = 2
        self.backRightM  = 3

        self.climbM      = 4

        self.collectorM  = 5
        self.shooterM    = 6

        self.servo1      = 7
        self.servo2      = 8

        # Soldinoids
        self.gearSol     = {'in': 2, 'out': 0}

        # Sensors have suffix 'S'. Gyro and sonar use analog in, everything else uses the DIO.
        self.gyroS       = 0
        self.sonicS      = {'left': 1, 'right': 2} # pin 4 on both sensors is also connected to the same DIO pin
        self.allienceS   = 0

        # LED strip
        self.ledStrip    = {'r': 7, 'g': 8, 'b': 9}

        pass
