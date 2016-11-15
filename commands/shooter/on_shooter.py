from wpilib.command import Command
import wpilib

import subsystems.shooter_wheel


class On_Shooter( Command ):

	def __init__( self, robot ):
		super( ).__init__( )

		self.robot = robot

		self.requires( self.robot.shooter_wheel )
		self.interruptible = True


	def initialize( self ):
		pass

	def execute( self ):
		wpilib.SmartDashboard.putString( 'Shooter Wheel: ', 'RUNNING' )
		self.robot.shooter_wheel.run( 1.0 )

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