"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2016, "Stronghold"
Code for robot "Jaw-Z"
contact@team4096.org
"""

import wpilib
from wpilib.command.commandgroup import CommandGroup

from commands.drivetrain.drive_with_mecanum import Drive_With_Mecanum
from commands.drivetrain.stop import Stop


### CLASSES ###

class Cross_Backward( CommandGroup ):
	"""
	This autonomous mode moves backwards fast, then slow, then stops.
	"""

	def __init__( self, robot ):
		super( ).__init__( )

		self.robot = robot

		self.addSequential( Drive_With_Mecanum( self.robot, 0, -1.0, 0 ), timeout = 3.5 )
		self.addSequential( Drive_With_Mecanum( self.robot, 0, -0.5, 0 ), timeout = 1.0 )
		self.addSequential( Stop( self.robot ) )
