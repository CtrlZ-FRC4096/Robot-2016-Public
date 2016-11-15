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

class Shooter_Wheel( wpilib.command.Subsystem ):

	def __init__( self, robot ):

		super( ).__init__( name = 'shooter_wheel' )

		self.robot = robot

		self.victor_wheel_1	= wpilib.Victor( const.ID_VICTOR_WHEEL_1 )
		self.victor_wheel_2	= wpilib.Victor( const.ID_VICTOR_WHEEL_2 )
		
		self.victor_wheel_1.setInverted( True )
		self.victor_wheel_2.setInverted( True )
		
		self.time_start = 0
		self.value_start = 0
		self.wheel_rate = 0

		self.at_target_rate = False


	def get_output_for_target_rate( self, target_rate ):
		wheel_rate = self.robot.shooter_wheel_encoder.getRate( )

		output = 1.0

		if wheel_rate > target_rate:
			# Too fast, slow it down
			output = 0.80
		elif wheel_rate < target_rate and wheel_rate > ( target_rate * 0.9 ):
			# Below target rate, but close to target, so slow it down a bit
			output = output * 0.9
		else:
			# Below target rate & not close
			# But make sure the change in output/power isn't too drastic
			if wheel_rate / target_rate < 0.20:
				output = output * 0.5

		# Never let motor go negative
		if output < 0:
			output = 0

		# If within tolerance of target rate, consider it on-target
		self.at_target_rate = abs( target_rate - wheel_rate ) < target_rate * const.SHOOTER_WHEEL_TARGET_RATE_TOLERANCE

		wpilib.SmartDashboard.putString( 'Shooter Wheel Output: ', '{0:.3f}'.format( float( output ) ) )

		return output


	def run( self, output ):
		self.victor_wheel_1.set( output )
		self.victor_wheel_2.set( output )


	def stop( self ):
		self.victor_wheel_1.set( 0 )
		self.victor_wheel_2.set( 0 )


	def log( self ):
		'''
		logs info about various things
		'''
		if not self.time_start:
			self.time_start = time.time( )

		# Get current encoder value
		value = self.robot.shooter_wheel_encoder.getRate( )

		# How much time has passed since we last checked?
		time_diff = time.time( ) - self.time_start

		if time_diff > 1.0:
			# How much has value changed since 1 second ago?
			value_diff = value - self.value_start

			# Calculate wheel speed, in revolutions per second
			self.wheel_speed = value_diff / time_diff / const.SHOOTER_ENCODER_DISTANCE_PER_PULSE

			# Reset the enc value and time
			self.value_start = value
			self.time_start = time.time( )

			wpilib.SmartDashboard.putString( 'Shooter Wheel Enc Val/Sec: ', '{0:.2f} revs/sec'.format( self.wheel_speed ) )

		wpilib.SmartDashboard.putString( 'Shooter Wheel Enc: ', '{0:.2f}'.format( value ) )