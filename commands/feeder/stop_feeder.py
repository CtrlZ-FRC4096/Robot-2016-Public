"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2016, "Stronghold"
Code for robot "Jaw-Z"
contact@team4096.org
"""

from wpilib.command import Command
import wpilib


class Stop_Feeder( Command ):

	def __init__( self, robot ):
		super( ).__init__( )
	
		self.robot = robot
		self.requires( self.robot.feeder_belts )
		self.interruptible = True


	def initialize( self ):
		wpilib.SmartDashboard.putString( 'Feeder Belts: ', 'STOPPED' )


	def execute( self ):
		wpilib.SmartDashboard.putString( 'Feeder Belts: ', 'STOPPED' )
		self.robot.feeder_belts.stop( )


	def isFinished( self ):
		return True


	def end( self ):
		wpilib.SmartDashboard.putString( 'Feeder Belts: ', 'STOPPED' )
		self.robot.feeder_belts.stop( )


	def cancel( self ):
		"""
		If bound to a button using whileHeld, will be called once when button is released
		"""
		self.end( )
		super( ).cancel( )		