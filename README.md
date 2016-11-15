# Ctrl-Z FRC Team 4096 - Robot Code 2016

The codebase for Jaw-Z, the Ctrl-Z robot used in FRC 2016 Stronghold competition season.

## Overview

The code is written in Python 3.4, using the [robotpy](http://robotpy.readthedocs.io/en/latest/) libraries. It uses the command-based
structure. Subsystems and commands are in dedicated folders, as are the autonomous modes.

Jaw-Z has a vision system using a Raspberry Pi 2, connected to the roboRIO. The Pi runs
mjpg-streamer, turning the USB camera into an IP camera stream.  The Pi also runs GRIP,
which uses the deployed configuration file to identify targets and publish the contour
data to NetworkTables. This data is then used as-needed by the robot code running on
the roboRIO.

This repo contains the robot code last used in July at the Rock River Offseason
Competition (R2OC), as well as the GRIP configuration files for each competition venue.

## Requirements

Driver Station:
- Python 3.4
- [robotpy](https://github.com/robotpy/robotpy-wpilib)
- [pyfrc](https://github.com/robotpy/pyfrc)

roboRIO:
- [robotpy](https://github.com/robotpy/robotpy-wpilib) ([docs](http://robotpy.readthedocs.io/en/latest/))

Please see the [robotpy docs](http://robotpy.readthedocs.io/en/latest/) and [pyfrc docs](http://pyfrc.readthedocs.io/en/latest/) for installation instructions.

## Questions?

Feel free to email us:
contact@team4096.org