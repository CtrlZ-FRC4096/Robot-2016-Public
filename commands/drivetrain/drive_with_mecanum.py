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


class Drive_With_Mecanum( Command ):

	def __init__( self, robot, get_x, get_y, get_z ):
		'''
		initializes mecanum drive movement.
		:param robot: the robot object
		:param get_x: Used to get the x angle, function that determines y direction
		:param get_y: Used to get the y angle, function that determines the y value and direction
		:param get_z: Used to get the z angle, function that determines
		rotation and direction of rotation. Z value must be given if it separate from the joystick.
		'''
		super( ).__init__( )

		self.robot = robot
		
		self.requires( self.robot.drive )
		self.setInterruptible( True )

		self.get_x = get_x
		self.get_y = get_y
		self.get_z = get_z


	def initialize( self ):
		'''
		Called just before this Command runs the first time
		'''
		pass


	def execute( self ):
		'''
		Called repeatedly when this Command is scheduled to run
		'''

		# If in tank mode, still use mecanum drive code but force X/strafe to zero
		if self.robot.drive.drive_state == const.ID_TANK:
			x = 0
		else:
			x = self.get_x( ) if callable( self.get_x ) else self.get_x
			
		y = self.get_y( ) if callable( self.get_y ) else self.get_y
		z = self.get_z( ) if callable( self.get_z ) else self.get_z

		# Not doing field-centric, so always pass 0 for gyro value
		self.robot.drive.drive_with_mecanum( x, y, z, 0 )
			

	def isFinished( self ):
		'''
		Return True when this Command no longer needs to run execute()
		'''
		return False


	def end( self ):
		'''
		Called once after isFinished returns true
		'''
		self.robot.drive.stop( )


	def interrupted( self ):
		'''
		Called when another command which requires one or
		more of the same subsystems is scheduled to run
		'''
		self.end( )