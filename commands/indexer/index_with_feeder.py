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


MODE_IDLE		= 0
MODE_INTAKE		= 1
MODE_SHOOT		= 2


class Index_With_Feeder( Command ):

	def __init__( self, robot ):
		super( ).__init__( )

		self.robot = robot

		self.requires( self.robot.indexer )
		self.interruptible = True
		
		self.indexer_timer = wpilib.Timer( )

		self.mode = MODE_IDLE


	def initialize( self ):
		wpilib.SmartDashboard.putString( 'Indexer: ', 'STOPPED' )


	def execute( self ):
		"""
		Based on ultrasonic sensor, indicating boulder is held under indexer or not,
		manage what to do when this command is run.  If boulder was held when this
		starts, run indexer forward in SHOOT mode until the switch opens.  If boulder
		was not held when this executes, run in INTAKE mode until switch closes.
		"""
		self.robot.indexer.run_forward( )
		#print( 'execute')


	def isFinished( self ):
		boulder_held = self.robot.indexer.is_boulder_indexed()	
		#print( 'boulder_held', boulder_held )
		
		return boulder_held
	
		# Incomplete code
		if not boulder_held:
			return False
		
		if not self.indexer_timer.hasPeriodPassed( const.INDEXER_HELD_DELAY ):
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