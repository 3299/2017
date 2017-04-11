"""
Defines port numbers for motors and sensors.
"""

class Map(object):
    def __init__(self):
        # Joysticks have suffix 'J'
        self.leftJ       = 0
        self.middleJ     = 1
        self.rightJ      = 2

        # Motors have suffix 'M'. All motors use PWM.
        self.frontLeftM  = 3
        self.frontRightM = 1
        self.backLeftM   = 7
        self.backRightM  = 0

        self.climbM      = 2

        self.collectorM  = 5
        self.shooterM    = 6
        self.groundGearM = 4

        # Soleniods
        self.gearSol     = {'in': 3, 'out': 4}
        self.groundGearSol = {'in': 2, 'out': 0}

        # Sensors have suffix 'S'. Gyro uses analog in, everything else uses the DIO.
        self.gyroS       = 1
        self.allienceS   = 0

        # Relays
        self.bumpPopR    = 0

        # LED strip (connected to DIO).
        self.ledStrip    = {'r': 9, 'g': 7, 'b': 8}
