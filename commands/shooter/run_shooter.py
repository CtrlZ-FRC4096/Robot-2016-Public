"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2016, "Stronghold"
Code for robot "Jaw-Z"
contact@team4096.org
"""

from wpilib.command import Command
import wpilib

import subsystems.shooter_wheel


class Run_Shooter( Command ):

	def __init__( self, robot, target_rate ):
		super( ).__init__( )

		self.robot = robot

		self.requires( self.robot.shooter_wheel )
		self.interruptible = True
		self.timeout = None

		self.target_rate = target_rate

		self._running = False


	def initialize( self ):
		wpilib.SmartDashboard.putString( 'Shooter Wheel: ', 'STOPPED' )

		# Acts as a toggle
		if self._running:
			self.end( )


	def execute( self ):
		self._running = True
		wpilib.SmartDashboard.putString( 'Shooter Wheel: ', 'RUNNING' )

		output = self.robot.shooter_wheel.get_output_for_target_rate( self.target_rate )
		self.robot.shooter_wheel.run( output )


	def isFinished( self ):
		return False


	def end( self ):
		self.robot.shooter_wheel.stop( )

		wpilib.SmartDashboard.putString( 'Shooter Wheel: ', 'STOPPED' )
		self._running = False


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