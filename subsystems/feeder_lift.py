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

### CONSTANTS ###

ID_VICTOR_LIFT_1		= 7
ID_VICTOR_LIFT_2		= 1

DEFAULT_KP = 0.01
DEFAULT_KI = 0.0
DEFAULT_KD = 0.01


### CLASSES ###

class Feeder_Lift( wpilib.command.PIDSubsystem ):

	def __init__( self, robot ):
		super( ).__init__( DEFAULT_KP, DEFAULT_KI, DEFAULT_KD, name = 'feeder_lift' )

		self.robot = robot
		
		# Configure PID stuff
		self.default_kP = DEFAULT_KP
		self.default_kI = DEFAULT_KI
		self.default_kD = DEFAULT_KD
		
		self.kP = DEFAULT_KP
		self.kI = DEFAULT_KI
		self.kD = DEFAULT_KD
		
		self.setAbsoluteTolerance( 10.0 )
		self.getPIDController( ).setContinuous( False )
		
		
		self.victor_lift_1	= wpilib.Victor( ID_VICTOR_LIFT_1 )
		self.victor_lift_1.setInverted( False )
		self.victor_lift_2	= wpilib.Victor( ID_VICTOR_LIFT_2 )
		self.victor_lift_2.setInverted( False )
		

	def returnPIDInput( self ):
		return self.robot.feeder_lift_encoder.getValue( )


	def usePIDOutput( self, output ):
		# if lift is above target, reduce max output
		encoder_val = self.robot.feeder_lift_encoder.getValue( )
		
		output = float( output )
		#wpilib.SmartDashboard.putString( 'Feeder Lift PID Output: ', '{0:.3f}'.format( output ) )
		
		self.victor_lift_1.pidWrite( output )
		self.victor_lift_2.pidWrite( output )
		
	
	def run( self, speed ):
		self.victor_lift_1.set( speed )
		self.victor_lift_2.set( speed )


	def stop( self ):
		self.victor_lift_1.set( 0 )
		self.victor_lift_2.set( 0 )


	def update_pid( self, p = None, i = None, d = None ):
		'''
		Updates the PID coefficients
		'''
		if p: 
			self.kP = p
		if i: 
			self.kI = i
		if d: 
			self.kD = d

		self.getPIDController( ).setPID( self.kP, self.kI, self.kD )			


	def log( self ):
		'''
		logs info about various things
		'''
		pass
		wpilib.SmartDashboard.putString( 'Feeder Lift Encoder: ', '{0}'.format( self.robot.feeder_lift_encoder.getValue( ) ) )
		wpilib.SmartDashboard.putString( 'Feeder Lift PID Values: ', '{0}'.format( '{0:.3f},{1:.3f},{2:.3f}'.format( self.kP, self.kI, self.kD ) ) )
