"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2016, "Stronghold"
Code for robot "Jaw-Z"
contact@team4096.org
"""

import wpilib
from wpilib.joystick import Joystick
from wpilib.buttons.joystickbutton import JoystickButton
from wpilib.sendablechooser import SendableChooser
from wpilib.smartdashboard import SmartDashboard

import subsystems.drivetrain

from commands.autonomous.lowbar_and_shoot import Lowbar_And_Shoot
from commands.autonomous.cross_forward import Cross_Forward
from commands.autonomous.cross_backward import Cross_Backward
from commands.autonomous.do_nothing import Do_Nothing

from commands.drivetrain.drive_with_mecanum import Drive_With_Mecanum
from commands.drivetrain.set_state_tank import Set_State_Tank
from commands.drivetrain.set_state_mecanum import Set_State_Mecanum
from commands.drivetrain.rotate_to_angle import Rotate_To_Angle
from commands.shooter.auto_shoot import Rotate_To_Target
#from commands.shooter.auto_shoot import Start_Shooter_And_Align

from commands.shooter.manual_shot import Manual_Shot
from commands.shooter.run_shooter import Run_Shooter
from commands.shooter.auto_shoot import Auto_Shoot
from commands.shooter.auto_shoot_2 import Auto_Shoot_2
from commands.shooter.set_shooter_wheel_speed import Set_Shooter_Wheel_Speed
from commands.shooter.stop_shooter import Stop_Shooter

from commands.indexer.forward_indexer import Forward_Indexer
from commands.indexer.reverse_indexer import Reverse_Indexer

from commands.feeder.feeder_and_index import Feeder_And_Index
from commands.feeder.raise_feeder import Raise_Feeder
from commands.feeder.lower_feeder import Lower_Feeder
from commands.feeder.forward_feeder import Forward_Feeder
from commands.feeder.reverse_feeder import Reverse_Feeder
from commands.feeder.reverse_feeder_and_indexer import Reverse_Feeder_And_Indexer
from commands.feeder.move_feeder_to_setpoint import Move_Feeder_To_Setpoint

from controls.joystick_pov import Joystick_POV
from controls.xbox_button import Xbox_Button
from controls.xbox_trigger import Xbox_Trigger
from commands.command_call import Command_Call

from common.smartdashboard_update_trigger import SmartDashboard_Update_Trigger

import const

import controls.xbox_controller
from controls.joystick_pov import Joystick_POV


## CONSTANTS ##

# Joystick axes
JOY_AXIS_LEFT_X			= 0
JOY_AXIS_LEFT_Y			= 1
JOY_AXIS_LEFT_SLIDER	= 3
JOY_AXIS_RIGHT_X		= 0
JOY_AXIS_RIGHT_Y		= 1
JOY_AXIS_RIGHT_SLIDER	= 3

# Invert any axes?
INVERT_JOY_LEFT_X		= True
INVERT_JOY_LEFT_Y		= True
INVERT_JOY_RIGHT_X		= True
INVERT_JOY_RIGHT_Y		= True

# Dead band
JOY_DEAD_BAND = 0.1

# Joystick Buttons
JOY_BTN_1				= 1
JOY_BTN_2				= 2
JOY_BTN_3				= 3
JOY_BTN_4				= 4
JOY_BTN_5				= 5
JOY_BTN_6				= 6
JOY_BTN_7				= 7
JOY_BTN_8				= 8
JOY_BTN_9				= 9
JOY_BTN_10				= 10
JOY_BTN_11				= 11
JOY_BTN_12				= 12
JOY_BTN_13				= 13
JOY_BTN_14				= 14

# Gamepad axes
GP_AXIS_LEFT_X			= 0
GP_AXIS_LEFT_Y			= 1
GP_AXIS_RIGHT_X			= 2
GP_AXIS_RIGHT_Y			= 3

# Gamepad Buttons
GP_BTN_X				= 1
GP_BTN_A				= 2
GP_BTN_B				= 3
GP_BTN_Y				= 4
GP_BTN_BUMPER_L			= 5
GP_BTN_BUMPER_R			= 6
GP_BTN_TRIGGER_L		= 7
GP_BTN_TRIGGER_R		= 8
GP_BTN_BACK				= 9
GP_BTN_START			= 10
GP_BTN_STICK_L			= 11
GP_BTN_STICK_R			= 12

# Xbox Controller
# buttons
XBOX_BTN_A				= 1
XBOX_BTN_B				= 2
XBOX_BTN_X				= 3
XBOX_BTN_Y				= 4
XBOX_BTN_LEFT_BUMPER	= 5
XBOX_BTN_RIGHT_BUMPER	= 6
XBOX_BTN_BACK 			= 7
XBOX_BTN_START 			= 8

# axes
XBOX_BTN_TRIGGER_LEFT	= 2
XBOX_BTN_TRIGGER_RIGHT	= 3
#DPAD
JOY_POV_NONE        	= -1
JOY_POV_UP				= 0
JOY_POV_RIGHT			= 90
JOY_POV_DOWN			= 180

INVERT_XBOX_LEFT_X		= const.COMPETITION_ROBOT == True
INVERT_XBOX_LEFT_Y		= True
INVERT_XBOX_RIGHT_X		= True
INVERT_XBOX_RIGHT_Y		= True


class OI:
	"""
	Operator Input - This class ties together controls and commands
	"""
	def __init__( self, robot ):

		self.robot = robot

		# Controllers
		# Xbox
		self.xbox_controller = controls.xbox_controller.Xbox_Controller( 0 )

		## COMMANDS ##

		self.drive_command = Drive_With_Mecanum(
		    									self.robot,
	                                            self._get_axis(self.xbox_controller, controls.xbox_controller.XBOX_AXIS_LEFT_X, inverted = INVERT_XBOX_LEFT_X ),
	                                            self._get_axis(self.xbox_controller, controls.xbox_controller.XBOX_AXIS_LEFT_Y, inverted = INVERT_XBOX_LEFT_Y ),
	                                            self._get_axis(self.xbox_controller, controls.xbox_controller.XBOX_AXIS_RIGHT_X, inverted = INVERT_XBOX_RIGHT_X ),
	                                            )

		self.robot.drive.setDefaultCommand( self.drive_command )

		## Autonomous Mode Selector ###

		self.auto_choose = SendableChooser( )

		self.auto_choose.addObject( 'Lowbar and Shoot', Lowbar_And_Shoot( self.robot ) )
		self.auto_choose.addObject( 'Cross Forward', Cross_Forward( self.robot ) )
		self.auto_choose.addObject( 'Cross Backward', Cross_Backward( self.robot ) )
		self.auto_choose.addObject( 'Do Nothing', Do_Nothing( self.robot ) )

		SmartDashboard.putData( 'Autonomous Mode', self.auto_choose )


		## Buttons & Commands ##

		#self.drive_train_turn_90 = Xbox_Button( self.xbox_controller, XBOX_BTN_B )
		#self.drive_train_turn_90.whenPressed( Rotate_To_Angle( self.robot, 20.0 ) )

		# Auto rotation with camera
		#self.drive_train_turn_90 = Xbox_Button( self.xbox_controller, XBOX_BTN_B )
		#self.drive_train_turn_90.whenPressed( Rotate_To_Target( self.robot ) )

		self.auto_shoot = Xbox_Trigger( self.xbox_controller, XBOX_BTN_TRIGGER_RIGHT )
		self.auto_shoot.whenPressed( Auto_Shoot_2( self.robot ) )

		#self.auto_shoot = Xbox_Button( self.xbox_controller, XBOX_BTN_B )
		#self.auto_shoot.whenPressed( Set_Shooter_Wheel_Speed( self.robot, 70.0 ) )


		# Toggle Drive State
		self.button_drive_shift = Xbox_Trigger( self.xbox_controller, XBOX_BTN_TRIGGER_LEFT )
		self.button_drive_shift.whenPressed( Set_State_Mecanum( self.robot ) )
		self.button_drive_shift.whenReleased( Set_State_Tank( self.robot ) )

		##create pid update triggers
		#dp_trigger = SmartDashboard_Update_Trigger( 'Drive P: ', self.robot.drive.default_kP )
		#dp_trigger.whenActive(
			#Command_Call( lambda : self.robot.drive.update_pid( p = dp_trigger.get_key_value( ) ) )
		#)
		#di_trigger = SmartDashboard_Update_Trigger( 'Drive I: ', self.robot.drive.default_kI )
		#di_trigger.whenActive(
			#Command_Call( lambda : self.robot.drive.update_pid( i = di_trigger.get_key_value( ) ) )
		#)
		#dd_trigger = SmartDashboard_Update_Trigger( 'Drive D: ', self.robot.drive.default_kD )
		#dd_trigger.whenActive(
			#Command_Call( lambda : self.robot.drive.update_pid( d = dd_trigger.get_key_value( ) ) )
		#)

		#sp_trigger = SmartDashboard_Update_Trigger( 'Shooter P: ', self.robot.shooter_wheel.default_kP )
		#sp_trigger.whenActive(
			#Command_Call( lambda : self.robot.shooter_wheel.update_pid( p = sp_trigger.get_key_value( ) ) )
		#)
		#si_trigger = SmartDashboard_Update_Trigger( 'Shooter I: ', self.robot.shooter_wheel.default_kI )
		#si_trigger.whenActive(
			#Command_Call( lambda : self.robot.shooter_wheel.update_pid( i = si_trigger.get_key_value( ) ) )
		#)
		#sd_trigger = SmartDashboard_Update_Trigger( 'Shooter D: ', self.robot.shooter_wheel.default_kD )
		#sd_trigger.whenActive(
			#Command_Call( lambda : self.robot.shooter_wheel.update_pid( d = sd_trigger.get_key_value( ) ) )
		#)


		# Run shooter wheel
		self.button_run_shooter = Xbox_Button( self.xbox_controller, XBOX_BTN_X )
		self.button_run_shooter.whenPressed( Manual_Shot( self.robot ) )

		## Feeder lift setpoints
		self.feeder_angle_up = Xbox_Button( self.xbox_controller, XBOX_BTN_Y )
		self.feeder_angle_up.whenPressed( Move_Feeder_To_Setpoint( self.robot, const.FEEDER_HIGH_POINT ) )

		self.feeder_angle_middle = Xbox_Button( self.xbox_controller, XBOX_BTN_B )
		self.feeder_angle_middle.whenPressed( Move_Feeder_To_Setpoint( self.robot, const.FEEDER_CENTER_POINT ) )

		self.feeder_angle_down = Xbox_Button( self.xbox_controller, XBOX_BTN_A )
		self.feeder_angle_down.whenPressed( Move_Feeder_To_Setpoint( self.robot, const.FEEDER_LOW_POINT ) )

		# Feeder lift manual
		self.feeder_angle_up_manual = Joystick_POV( self.xbox_controller, controls.joystick_pov.JOY_POV_UP )
		self.feeder_angle_up_manual.whileHeld( Raise_Feeder( self.robot ) )
		self.feeder_angle_down_manual = Joystick_POV( self.xbox_controller, controls.joystick_pov.JOY_POV_DOWN )
		self.feeder_angle_down_manual.whileHeld( Lower_Feeder( self.robot ) )

		# Forward feeder
		self.button_forward_feeder = Xbox_Button( self.xbox_controller, XBOX_BTN_LEFT_BUMPER )
		self.button_forward_feeder.whileHeld( Feeder_And_Index( self.robot ) )

		# Reverse feeder
		self.button_reverse_feeder = Xbox_Button( self.xbox_controller, XBOX_BTN_RIGHT_BUMPER )
		self.button_reverse_feeder.whileHeld( Reverse_Feeder_And_Indexer( self.robot ) )

		# Forward indexer
		self.button_run_indexer = Xbox_Trigger( self.xbox_controller, XBOX_BTN_START )
		self.button_run_indexer.whileHeld( Forward_Indexer( self.robot ) )

		# Stop Shooter
		self.button_run_indexer = Xbox_Button( self.xbox_controller, XBOX_BTN_BACK)
		self.button_run_indexer.whenPressed( Stop_Shooter( self.robot ) )


	def _get_axis( self, joystick, axis, inverted = False ):
		"""
		Handles inverted joy axes and dead band
		"""
		def axis_func():
			val = joystick.getAxis(axis)

			if abs(val) < JOY_DEAD_BAND:
				val = 0

			if inverted:
				val *= -1

			return val

		return axis_func
