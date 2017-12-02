# Steamworks
3299's code for the 2017 season. Programmed in Python with [RobotPy](https://robotpy.github.io).

## Notable features
- A Raspberry Pi on the robot does vision tracking with OpenCV and [GRIP](https://github.com/WPIRoboticsProjects/GRIP). It then publishes the results on Network Tables for the robot to use.
- Organized in a convoluted system that separates logic, actuators, and other components. It uses neither MagicBot or the Command framework.  Don't ask.
