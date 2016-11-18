#! python3
"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2016, "Stronghold"
Code for robot "Jaw-Z"
contact@team4096.org
"""

import logging
import time

import wpilib
import wpilib.sendablechooser
import wpilib.smartdashboard
import wpilib.command

import networktables

import robotpy_ext.autonomous
import robotpy_ext.control.xbox_controller

import subsystems.drivetrain
import subsystems.feeder_belts
import subsystems.feeder_lift
import subsystems.shooter_wheel
import subsystems.shooter_camera

import controls.xbox_controller
import oi
import const

from commands.drivetrain.set_state_tank import Set_State_Tank

log = logging.getLogger( 'robot' )

# Uncomment following line to deploy that GRIP config file to robot
# This requires use of Wing IDE and our custom deploy script
#GRIP_FILE_PATH = "shoptraining.grip"


class Robot( wpilib.IterativeRobot ):
	"""
	Main robot class.

	This is the central object, holding instances of all the robot subsystem
	and sensor classes.
	
	It also contains the init & periodic methods for autonomous and
	teloperated modes, called during mode changes and repeatedly when those
	modes are active.
	
	The one instance of this class is also passed as an argument to the
	various other classes, so they have full access to all its properties.
	"""
	def robotInit( self ):
		### Sensors ###

		# AndyMark Absolute Encoder
		# getValue method returns int value 0-3920
		self.feeder_lift_encoder = wpilib.AnalogInput( 1 )

		# Digital cim encoder - pinout:
		# 1 - +5vdc (orange)
		# 2 - Channel A
		# 3 - Ground (brown)
		# 4 - Channel B
		self.shooter_wheel_encoder = wpilib.Encoder( 0, 1, reverseDirection = True )
		self.shooter_wheel_encoder.setDistancePerPulse( const.SHOOTER_ENCODER_DISTANCE_PER_PULSE )
		self.shooter_wheel_encoder.reset( )

		# Pressure sensor (200 psi)
		self.pressure = wpilib.AnalogInput( 2 )

		# Gyro
		self.gyro = wpilib.AnalogGyro( 0 )

		# Accelerometer
		self.accel = wpilib.BuiltInAccelerometer( )

		# Ultrasonic
		self.ultra = wpilib.AnalogInput( 3 )


		### Subsystems ###

		# Drive for Xbox Controller
		self.drive = subsystems.drivetrain.Drivetrain( self )

		# Feeder Belts
		self.feeder_belts = subsystems.feeder_belts.Feeder_Belts( self )

		# Feeder Belts
		self.feeder_lift = subsystems.feeder_lift.Feeder_Lift( self )

		# Indexer
		self.indexer = subsystems.indexer.Indexer( self )
	
		# Shooter Camera
		self.shooter_camera = subsystems.shooter_camera.Shooter_Camera( self )

		# Shooter Wheel
		self.shooter_wheel = subsystems.shooter_wheel.Shooter_Wheel( self )


		### Misc ###

		# Operator Input
		self.oi = oi.OI( self )


		## Autonomous ##

		self.subsystems = {
			'drive':	self.drive,
			'feeder_lift': self.feeder_lift,
			'feeder_belts': self.feeder_belts,
			'shooter_wheel': self.shooter_wheel,
			'shooter_camera': self.shooter_camera,
			'indexer' : self.indexer,
		}


		### Logging ###

		# NetworkTables
		self.nt_smartdash = networktables.NetworkTable.getTable( 'SmartDashboard' )
		self.nt_grip = networktables.NetworkTable.getTable( 'GRIP/myContoursReport' )
		wpilib.SmartDashboard.putNumber( 'Cam Fudge: ', const.CAMERA_SHOOTER_PIXEL_OFFSET )

		wpilib.SmartDashboard.putBoolean( '.', False )
		wpilib.SmartDashboard.putBoolean( '..', False )

		# Timers for NetworkTables update so we don't use too much bandwidth
		self.log_timer = wpilib.Timer( )
		self.log_timer.start( )
		self.log_timer_delay = 0.1		# 10 times/second

		self.log( )


	### Disabled ###

	def disabledInit( self ):
		"""
		Runs once when disabled
		"""
		pass
	

	def disabledPeriodic( self ):
		"""
		Runs perodically when disabled
		"""		
		pass


	### Autonomous ###

	def autonomousInit( self ):
		'''
		Initializes our autonomous mode
		'''
		self.gyro.reset( )
		self.log_timer.reset( )

		# Get the driver-selected auto mode from SmartDashboard and start it
		self.oi.auto_choose.getSelected( ).start( )


	def autonomousPeriodic( self ):
		'''
		Periodically calls all autonomous based commands
		'''
		wpilib.command.Scheduler.getInstance( ).run( )
		self.log( )


	### Teleoperated ###

	def teleopInit( self ):
		'''
		Initializes our teleop mode
		'''
		const.DRIVE_CORRECTION_ENABLED = False

		# Stop auto mode commands
		self.oi.auto_choose.getSelected( ).cancel( )

		self.gyro.reset( )
		self.shooter_wheel_encoder.reset( )
		self.log_timer.reset( )


	def teleopPeriodic( self ):
		'''
		Periodically calls all teleop code
		'''
		wpilib.command.Scheduler.getInstance( ).run( )
		self.log( )


	### Misc ###

	def log( self ):
		'''
		Logs some info to the SmartDashboard, and standard output
		'''
		# Only every 1/10 second (or so) to avoid flooding networktables
		if not self.log_timer.running or not self.log_timer.hasPeriodPassed( self.log_timer_delay ):
			return

		self.drive.log( )
		self.feeder_lift.log( )
		self.feeder_belts.log( )
		self.shooter_wheel.log( )
		self.shooter_camera.log( )
		self.indexer.log( )

		voltage_pressure = self.pressure.getVoltage()
		drivetrain_pressure = ( 250 * voltage_pressure / 5 ) - 25

		wpilib.SmartDashboard.putString( 'pressure: ', '{0:.2f}'.format( drivetrain_pressure ) )
		wpilib.SmartDashboard.putBoolean( '..', drivetrain_pressure > 60 )

		wpilib.SmartDashboard.putBoolean( ',', False )

		wpilib.SmartDashboard.putNumber( 'Gyro Angle: ', self.gyro.getAngle( ) )



### MAIN ###

if __name__ == "__main__":
	wpilib.run( Robot )