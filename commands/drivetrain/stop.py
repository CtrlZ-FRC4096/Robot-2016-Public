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


class Stop( Command ):

	def __init__( self, robot ):
		'''
		'''
		super( ).__init__( )

		self.robot = robot
		
		self.requires( self.robot.drive )
		self.setInterruptible( True )


	def initialize( self ):
		'''
		Called just before this Command runs the first time
		'''
		self.robot.drive.drive_with_mecanum( 0, 0, 0, 0 )


	def execute( self ):
		'''
		Called repeatedly when this Command is scheduled to run
		'''
		self.robot.drive.drive_with_mecanum( 0, 0, 0, 0 )
			

	def isFinished( self ):
		'''
		Return True when this Command no longer needs to run execute()
		'''
		return True
