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

ID_VICTOR_BELTS		= 3


### CLASSES ###

class Feeder_Belts( wpilib.command.Subsystem ):

	def __init__( self, robot ):

		super( ).__init__( 'feeder_belts' )
		
		self.robot = robot
	
		if const.COMPETITION_ROBOT:
			self.victor_belts	= wpilib.Victor( ID_VICTOR_BELTS )
			self.victor_belts.setInverted( True )
		else:
			self.spikes = wpilib.Relay( 1 ) # both spike are connected to same input through a splitter
			self.spikes.setDirection( wpilib.Relay.Direction.kBoth )		
		
	def forward( self ):
		if const.COMPETITION_ROBOT:
			self.victor_belts.set( 1.0 )
		else:
			self.spikes.set( wpilib.Relay.Direction.kForward )

	def reverse( self ):
		if const.COMPETITION_ROBOT:
			self.victor_belts.set( -1.0 )
		else:
			self.spikes.set( wpilib.Relay.Direction.kReverse )	

	def stop( self ):
		if const.COMPETITION_ROBOT:
			self.victor_belts.set( 0.0 )
		else:
			self.spikes.stopMotor( )
		
	def log( self ):
		'''
		logs info about various things
		'''
		pass
		#wpilib.SmartDashboard.putString('Feeder Belts: ', '{0}'.format(self.current_shooter_angle))