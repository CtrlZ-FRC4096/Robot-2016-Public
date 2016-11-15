"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2016, "Stronghold"
Code for robot "Jaw-Z"
contact@team4096.org
"""

import math
import sys

import wpilib
import wpilib.command

import const
import time


### CONSTANTS ###

ID_MOTOR_FRONT_LEFT		= 9 
ID_MOTOR_REAR_LEFT		= 8
ID_MOTOR_FRONT_RIGHT	= 4
ID_MOTOR_REAR_RIGHT		= 5

DEFAULT_KP = 0.02
DEFAULT_KI = 0.01
DEFAULT_KD = 0.1


### CLASSES ###

class Drivetrain( wpilib.command.PIDSubsystem ):

	def __init__( self, robot ):
		
		super( ).__init__( DEFAULT_KP, DEFAULT_KI, DEFAULT_KD, name = 'drive' )
	
		self.robot = robot
	
		self.default_kP = DEFAULT_KP
		self.default_kI = DEFAULT_KI
		self.default_kD = DEFAULT_KD
	
		self.kP = DEFAULT_KP
		self.kI = DEFAULT_KI
		self.kD = DEFAULT_KD
		
		# Configure PID stuff
		self.setAbsoluteTolerance( 0.25 )
		self.getPIDController( ).setContinuous( False )

		self.drive = wpilib.RobotDrive( frontLeftMotor = const.ID_DRIVE_MOTOR_FRONT_LEFT,
		                                rearLeftMotor = const.ID_DRIVE_MOTOR_REAR_LEFT,
										frontRightMotor = const.ID_DRIVE_MOTOR_FRONT_RIGHT,
										rearRightMotor = const.ID_DRIVE_MOTOR_REAR_RIGHT )

		# Invert motors if necessary
		# Comp robot = Invert = True
		# Practice robot = Invert = False?
		self.drive.setInvertedMotor( self.drive.MotorType.kFrontLeft, False )
		self.drive.setInvertedMotor( self.drive.MotorType.kRearLeft, True )

		self.x = 0
		self.y = 0
		self.z = 0
		self.angle = 0

		self.drive_state = const.ID_TANK

		self.shift_solenoid_1 = wpilib.Solenoid( const.ID_DRIVE_SOLENOID_SHIFTER_1 )
		self.shift_solenoid_2 = wpilib.Solenoid( const.ID_DRIVE_SOLENOID_SHIFTER_2 )

		self._correction_start_angle = None


	def returnPIDInput( self ):
		return self.robot.gyro.getAngle( )
	
	
	def usePIDOutput( self, output ):
		# invert it
		output = -float( output )

		# Reduce the max output to 50%
		output = output / 2.0

		# Make sure we're outputing at least enough to move the robot at all
		if output < 0:
			output = min( output, -const.DRIVE_MIN_ROTATION_OUTPUT )
		elif output > 0:
			output = max( output, const.DRIVE_MIN_ROTATION_OUTPUT )
	
		#wpilib.SmartDashboard.putString( 'Drive Rotate PID Output: ', '{0:.3f}'.format( output ) )

		self.drive.mecanumDrive_Cartesian( 0, 0, output, 0 )
	
	
	def run( self, rotation ):
		self.drive.mecanumDrive_Cartesian( 0, 0, rotation, 0 )
		
	
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


	def set_drive_state( self, state ):
		"""
		Start of change state of drivetrain code. Changes the state by activating
		The solenoids which should push out/in the pistons.
		"""
		self.drive_state = state

		if state == const.ID_MECANUM:
			# Switch to mecanum
			self.shift_solenoid_1.set( True )
			self.shift_solenoid_2.set( False )
		else:
			# Switch to tank
			self.shift_solenoid_1.set( False )
			self.shift_solenoid_2.set( True )


	def _get_corrected_rotation( self, x, y, rotation ):
		"""
		If gyro drive correction is enabled, and the user isn't manually rotating the
		robot, let the gyro angle correct the rotation.
		"""
		if not const.DRIVE_CORRECTION_ENABLED:
			wpilib.SmartDashboard.putString( 'Drive Correction:  ', 'DISABLED' )
			self._correction_start_angle = None
			return rotation
		
		if ( abs( x ) > 0.1 or abs( y ) > 0.1 ) and rotation < const.DRIVE_CORRECTION_ROTATION_THRESHOLD:
			# This means driver is moving forward/back or strafing, but NOT rotating
			if self._correction_start_angle is None:
				# We were not correcting last time, so save gyro angle and start correcting to that
				self.robot.gyro.reset( )
				self._correction_start_angle = self.robot.gyro.getAngle( )
				return rotation

			else:
				# We're correcting so adjust rotation
				correction_amt = ( self._correction_start_angle - self.robot.gyro.getAngle( ) ) * const.DRIVE_CORRECTION_PROPORTION * -1
				rotation += correction_amt 
				wpilib.SmartDashboard.putString( 'Drive Correction:  ', 'ACTIVE - {0:.4f}'.format( correction_amt ) )
		else:
			wpilib.SmartDashboard.putString( 'Drive Correction:  ', 'INACTIVE' )
			self._correction_start_angle = None
		
		return rotation
			

	def get_drive_state( self ):
		return self.drive_state


	def toggle_drive_state( self ):
		if self.drive_state == const.ID_MECANUM:
			self.set_drive_state( const.ID_TANK )
			return const.ID_TANK
		else:
			self.set_drive_state( const.ID_MECANUM )
			return const.ID_MECANUM


	#start of code for driving
	def drive_with_mecanum( self, x, y, joy_rotation, gyro_angle ):
		val = '{0:.2f}, {1:.2f}'.format( x, joy_rotation )
		wpilib.SmartDashboard.putString( 'raw x,y:  ', val )
		
		# Sensitivity test - "squaring" the joystick values
		x *= abs(x)	
		y *= abs(y)
		val = '{0:.2f}, {1:.2f}'.format( x, y )
		wpilib.SmartDashboard.putString( 'cor x,y:  ', val )
		
		
		rotation = self._get_corrected_rotation( x, y, joy_rotation )

		# Actually drive
		# Fourth argument, angle, is always zero since we're not doing field-oriented driving
		self.drive.mecanumDrive_Cartesian( x, y, rotation, 0 )

		# Save values for use in log method below
		# changed to flip axes
		self.x = x
		self.y = y
		self.z = rotation
		self.angle = gyro_angle


	def drive_with_tank( self, left_axis, right_axis ):
		"""
		needs work, and support for correction
		"""
		self.drive.tankDrive( leftValue = left_axis( ), rightValue = right_axis( ) )
	

	def stop( self ):
		self.drive_with_mecanum( 0, 0, 0, 0 )
		self.drive.stopMotor( )


	def log( self ):
		'''
		logs various things about the robot
		'''
		if self.drive_state == const.ID_MECANUM:
			state_name = 'MECANUM'
			drive_values = '{0:.2f},{1:.2f},{2:.2f},{3:.2f}'.format( self.x, self.y, self.z, self.angle )
		else:
			state_name = 'TANK'
			drive_values = 'joy_left: ( {0:.2f}, {1:.2f} ), joy_right: ( {2:.2f}, {3:.2f} )'.format(
			    self.robot.oi.xbox_controller.getLeftX( ), self.robot.oi.xbox_controller.getLeftY( ), self.robot.oi.xbox_controller.getRightX( ), self.robot.oi.xbox_controller.getRightY( ), )

		wpilib.SmartDashboard.putString( 'Drive State:  ', state_name )
		wpilib.SmartDashboard.putString( 'Drive Values: ', drive_values )