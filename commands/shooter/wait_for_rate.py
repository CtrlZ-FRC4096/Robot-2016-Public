"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2016, "Stronghold"
Code for robot "Jaw-Z"
contact@team4096.org
"""

from wpilib.command import Command
import wpilib

import subsystems.shooter_wheel


class Wait_For_Rate( Command ):
	"""
	Waits until shooter encoder is at the specified rate, then finishes.
	"""

	def __init__( self, robot, target_rate ):
		super( ).__init__( )

		self.robot = robot

		#self.requires( self.robot.shooter_wheel )
		self.interruptible = True

		self.target_rate = target_rate
		
	def initialize( self ):
		pass

	def execute( self ):
		pass

	def isFinished( self ):
		# As soon as the shooter encoder is at/above target rate,
		# this command is finished
		return self.robot.shooter_wheel_encoder.getRate( ) >= self.target_rate
