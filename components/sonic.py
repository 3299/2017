"""
Helper class for ultrasonic sensor
"""
import statistics

class Sonic(object):
    def __init__(self, sensor):
        self.sensor = sensor
        self.sensor.setAutomaticMode(True)

        self.popping = []

    def getFeet(self):
        distance = self.sensor.getRangeInches()
        distance = distance / 12

        distance = distance + 1.91 # account for the fact that the sensor is not on front of robot

        return distance

    def getAverage(self):
        distance = self.getFeet()

        if (len(self.popping) > 9):
            self.popping.pop(0) # remove first measurement if there are 10 measurements

        self.popping.append(distance) # append measurement to end of list

        return statistics.median_grouped(self.popping)
