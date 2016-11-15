"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2016, "Stronghold"
Code for robot "Jaw-Z"
contact@team4096.org
"""

from wpilib.command import Command
import wpilib

import subsystems.shooter_wheel


class Stop_Shooter( Command ):

	def __init__( self, robot ):
		super( ).__init__( )

		self.robot = robot
		
		self.requires( self.robot.shooter_wheel )
		self.interruptible = True


	def initialize( self ):
		pass

	def execute( self ):
		wpilib.SmartDashboard.putString( 'Shooter Wheel: ', 'STOPPED' )
		wpilib.SmartDashboard.putString( 'Last Shot Wheel Speed: ', '{0:.2f}'.format( self.robot.shooter_wheel.wheel_speed ) )
		
		self.robot.shooter_wheel.stop( )

	def isFinished( self ):
		return True

	def end( self ):
		pass
		
	def interrupted( self ):
		"""
		Called when another thing which requires one or more of the same subsystem is scheduled to run
		"""
		self.end( )

	def cancel( self ):
		"""
		If bound to a button using whileHeld, will be called once when button is released
		"""
		self.end( )
		super( ).cancel( )		