"""
Helper class for ultrasonic sensor
"""
import statistics

class Sonic(object):
    def __init__(self, sensor):
        self.sensor = sensor

    def getCm(self, side):
        averageVoltage = self.sensor[side].getAverageVoltage()

        return (averageVoltage * 1000)/4.9
