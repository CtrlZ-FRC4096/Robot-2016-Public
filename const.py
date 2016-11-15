"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2016, "Stronghold"
Code for robot "Jaw-Z"
contact@team4096.org
"""

import wpilib

### CONSTANTS ###

# Which robot is this?  Used to flip PWM values around.
# Next year, let's use same inputs on both robots?
COMPETITION_ROBOT					= True

# PWM port IDs

#Roborio Accelerometer
NEGATIVE_ACCEL_VALUE = 0

# Drivetrain
ID_DRIVE_MOTOR_FRONT_LEFT			= 9
ID_DRIVE_MOTOR_REAR_LEFT			= 8

ID_DRIVE_MOTOR_FRONT_RIGHT			= 4
ID_DRIVE_MOTOR_REAR_RIGHT			= 5

ID_DRIVE_SOLENOID_SHIFTER_1			= 0
ID_DRIVE_SOLENOID_SHIFTER_2			= 1

DRIVE_CORRECTION_ENABLED			= True
DRIVE_CORRECTION_ROTATION_THRESHOLD	= 0.05
DRIVE_CORRECTION_PROPORTION			= 0.04

DRIVE_MIN_ROTATION_OUTPUT			= 0.15   # Min power output required to rotate robot at all

# Feeder
ID_VICTOR_BELTS						= 3
ID_VICTOR_LIFT_1					= 7
ID_VICTOR_LIFT_2					= 1

FEEDER_HIGH_POINT					= 3604
FEEDER_CENTER_POINT					= 2380
FEEDER_LOW_POINT					= 2077

# Indexer
ID_VICTOR_INDEXER					= 2
INDEXER_POWER						= 1.0

# Shooter
ID_VICTOR_WHEEL_1					= 6
ID_VICTOR_WHEEL_2					= 0

# This was measured by observing 289 pulses per full wheel revolution, 1.0 / 289 = 0.00346
SHOOTER_ENCODER_DISTANCE_PER_PULSE	= 0.00346
SHOOTER_WHEEL_TARGET_RATE			= 90
SHOOTER_WHEEL_WAIT_FOR_RATE			= 100
SHOOTER_WHEEL_TARGET_RATE_TOLERANCE	= 0.0

# IDs for state of drive shifter
ID_MECANUM							= 0
ID_TANK								= 1

# Camera constants
CAMERA_RES_X						= 320
CAMERA_RES_Y						= 240
CAMERA_FOV							= 68	# used to be 84 when nolan was dumb
CAMERA_ALIGN_THRESHOLD				= 1		# degrees

CAMERA_SHOOTER_PIXEL_OFFSET			= 10	# Fudge factor used to adjust camera vs. shooter alignment, in pixels
											# greater the pos value = aim more left