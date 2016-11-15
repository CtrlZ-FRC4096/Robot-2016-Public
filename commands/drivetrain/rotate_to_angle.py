"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2016, "Stronghold"
Code for robot "Jaw-Z"
contact@team4096.org
"""

from commands.drivetrain.set_rotation_angle import Set_Rotation_Angle



class Rotate_To_Angle( Set_Rotation_Angle ):
	"""
	Centers the feeder
	"""

	def __init__( self, robot, value ):

		self.robot = robot

		super( ).__init__( self.robot, value )


	def isFinished( self ):
		return super( ).isFinished( )
