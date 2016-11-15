"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2016, "Stronghold"
Code for robot "Jaw-Z"
contact@team4096.org
"""

import wpilib
from wpilib.command.commandgroup import CommandGroup

from commands.drivetrain.stop import Stop

### CLASSES ###

class Do_Nothing( CommandGroup ):
	"""
	This autonomous mode does... wait for it... nothing.
	"""

	def __init__( self, robot ):
		super( ).__init__( )

		self.robot = robot

		self.addSequential( Stop( self.robot ) )
