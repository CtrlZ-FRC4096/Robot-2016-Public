"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2016, "Stronghold"
Code for robot "Jaw-Z"
contact@team4096.org
"""

import wpilib
from wpilib.command import Command


class Set_Feeder_Setpoint( Command ):

	def __init__( self, robot, setpoint ):
		super( ).__init__( )

		self.robot = robot

		self.requires( self.robot.feeder_lift ) 
		self.setpoint = setpoint
		self.setTimeout( 5 )


	def initialize( self ):
		self.robot.feeder_lift.enable( )
		self.robot.feeder_lift.setSetpoint( self.setpoint )


	def execute( self ):
		"""Called repeatedly"""


	def isFinished( self ):
		finished = self.robot.feeder_lift.onTarget( ) or self.isTimedOut( ) 
		#finished = False

		if finished:
			print( 'Set Feeder Setpoint we did it...!')

		#wpilib.SmartDashboard.putString( 'Feeder Lift PID Finished: ', '{0}'.format( finished ) )
		return finished


	def end( self ):
		"""
		Called once after isFinished returns true
		"""
		self.robot.feeder_lift.disable( )


	def interrupted( self ):
		"""
		Called when another thing which requires one or more of the same subsystem is scheduled to run
		"""
		self.end( )
