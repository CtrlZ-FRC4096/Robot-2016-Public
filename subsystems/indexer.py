"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2016, "Stronghold"
Code for robot "Jaw-Z"
contact@team4096.org
"""

import math
import sys
import time

import wpilib
import wpilib.command

import const


### CONSTANTS ###

### CLASSES ###

class Indexer( wpilib.command.Subsystem ):

	def __init__( self, robot ):

		super( ).__init__( 'indexer' )

		self.robot = robot

		self.victor_indexer	= wpilib.Victor( const.ID_VICTOR_INDEXER )
		self.victor_indexer.setInverted( True )


	def run_forward( self ):
		self.victor_indexer.set( const.INDEXER_POWER )
	
	def run_reverse( self ):
		self.victor_indexer.set( -const.INDEXER_POWER )	

	def stop( self ):
		self.victor_indexer.set( 0 )


	def get_ultrasonic_distance( self ):
		return self.robot.ultra.getVoltage( ) / ( 5 / 512 )


	def is_boulder_indexed( self ):
		"""
		Empty indexer returns values from 9-11 or so.
		So anything outside of that range means boulder is held/indexed
		"""

		distance = self.get_ultrasonic_distance( )
		boulder_indexed = distance < 8.5 or distance > 11.0

		return boulder_indexed


	def log( self ):
		'''
		logs info about various things
		'''
		wpilib.SmartDashboard.putBoolean( '...', self.is_boulder_indexed( ) )
		wpilib.SmartDashboard.putString( 'Ultra Distance: ', '{0:.3f}'.format( self.get_ultrasonic_distance( ) ) )
