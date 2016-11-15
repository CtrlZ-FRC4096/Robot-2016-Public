"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2016, "Stronghold"
Code for robot "Jaw-Z"
contact@team4096.org
"""

from wpilib.command import Command
import wpilib

import subsystems.indexer


class Stop_Indexer( Command ):

	def __init__( self, robot ):
		super( ).__init__( )

		self.robot = robot
		
		self.requires( self.robot.indexer )
		self.interruptible = True

	def execute( self ):
		wpilib.SmartDashboard.putString( 'Indexer: ', 'STOPPED' )
		self.robot.indexer.stop( )

	def isFinished( self ):
		return True
