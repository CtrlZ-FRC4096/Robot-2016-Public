"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2016, "Stronghold"
Code for robot "Jaw-Z"
contact@team4096.org
"""

import wpilib
from wpilib.command import Command


class Set_Shooter_Wheel_Speed( Command ):

	def __init__( self, robot, target_speed ):
		super( ).__init__( )

		self.robot = robot

		self.requires( self.robot.shooter_wheel ) 
		
		# Speed in revolutions/second
		self.target_speed = target_speed
		
		#self.setTimeout( 30 )


	def initialize( self ):
		enabled = self.robot.shooter_wheel.getPIDController( ).isEnable( )
		
		if enabled:
			# Disable PID
			self.end( )
		else:
			# Enable PID
			self.robot.shooter_wheel.enable( )
			self.robot.shooter_wheel.setSetpoint( self.target_speed )			


	def execute( self ):
		"""Called repeatedly"""


	def isFinished( self ):
		finished = self.robot.shooter_wheel.onTarget( ) #or self.isTimedOut( ) 
		finished = False

		if finished:
			print( 'Finished!')

		#wpilib.SmartDashboard.putString( 'Shooter Wheel PID Finished: ', '{0}'.format( finished ) )
		return finished


	def end( self ):
		"""
		Called once after isFinished returns true
		"""
		self.robot.shooter_wheel.disable( )
		self.robot.shooter_wheel.setSetpoint( 0 )	


	def interrupted( self ):
		"""
		Called when another thing which requires one or more of the same subsystem is scheduled to run
		"""
		self.end( )
