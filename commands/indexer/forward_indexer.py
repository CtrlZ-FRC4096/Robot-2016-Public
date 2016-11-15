"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2016, "Stronghold"
Code for robot "Jaw-Z"
contact@team4096.org
"""

from wpilib.command import Command
import wpilib

import subsystems.indexer

import const


class Forward_Indexer( Command ):

	def __init__( self, robot ):
		super( ).__init__( )

		self.robot = robot

		self.requires( self.robot.indexer )
		self.requires( self.robot.shooter_wheel )
		self.interruptible = False


	def initialize( self ):
		wpilib.SmartDashboard.putString( 'Indexer: ', 'STOPPED' )


	def execute( self ):
		# this portion is for running the indexer without a switch
		self.robot.indexer.run_forward( )
		#self.robot.shooter_wheel.run( 1.0 )


	def isFinished( self ):
		return False


	def end( self ):
		wpilib.SmartDashboard.putString( 'Indexer: ', 'STOPPED' )
		self.robot.indexer.stop( )


	def cancel( self ):
		"""
		If bound to a button using whileHeld, will be called once when button is released
		"""
		self.end( )
		super( ).cancel( )