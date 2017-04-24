'''
Launches the camera streamers in a seperate
thread to prevent the main robot thread
from being overloaded.
'''

from cscore import CameraServer

def main():
    cs = CameraServer.getInstance()
    cs.enableLogging()

    usb1 = cs.startAutomaticCapture(dev=0)
    #usb2 = cs.startAutomaticCapture(name='usb2', dev=1)

    usb1.setResolution(320, 240)
    #usb2.setResolution(320, 240)

    cs.waitForever()
