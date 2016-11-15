"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2016, "Stronghold"
Code for robot "Jaw-Z"
contact@team4096.org
"""

from wpilib.command import Command
import wpilib

import subsystems.drivetrain
import const

class Set_State_Mecanum( Command ):

	def __init__( self, robot ):
		super( ).__init__( )
		
		self.robot = robot
		
		self.requires( self.robot.drive )
				
	
	def initialize( self ):
		pass
		
		
	def execute( self ):
		new_state = self.robot.drive.set_drive_state( const.ID_MECANUM )

		
	def isFinished( self ):
		return True