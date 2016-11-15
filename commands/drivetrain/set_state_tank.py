"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2016, "Stronghold"
Code for robot "Jaw-Z"
contact@team4096.org
"""

from wpilib.command import Command
import wpilib

import const
import subsystems.drivetrain


class Set_State_Tank( Command ):

	def __init__( self, robot ):
		super( ).__init__( )
		
		self.robot = robot
		
		self.requires( self.robot.drive )


	def initialize( self ):
		pass


	def execute( self ):
		new_state = self.robot.drive.set_drive_state( const.ID_TANK )


	def isFinished( self ):
		return True