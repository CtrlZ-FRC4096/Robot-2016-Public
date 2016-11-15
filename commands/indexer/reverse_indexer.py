"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2016, "Stronghold"
Code for robot "Jaw-Z"
contact@team4096.org
"""

from wpilib.command import Command
import wpilib

import subsystems.indexer


class Reverse_Indexer( Command ):

	def __init__( self, robot ):
		super( ).__init__( )

		self.robot = robot
		
		self.requires( self.robot.indexer )
		self.interruptible = True


	def initialize( self ):
		wpilib.SmartDashboard.putString( 'Indexer: ', 'STOPPED' )


	def execute( self ):
		#print( 'reverse index')
		wpilib.SmartDashboard.putString( 'Indexer: ', 'REVERSE' )
		self.robot.indexer.run_reverse( )


	def isFinished( self ):
		return False


	def end( self ):
		#print( 'stop index')
		wpilib.SmartDashboard.putString( 'Indexer: ', 'STOPPED' )
		self.robot.indexer.stop( )


	def cancel( self ):
		"""
		If bound to a button using whileHeld, will be called once when button is released
		"""
		self.end( )
		super( ).cancel( )		