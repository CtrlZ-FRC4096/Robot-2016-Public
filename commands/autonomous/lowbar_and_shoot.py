"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2016, "Stronghold"
Code for robot "Jaw-Z"
contact@team4096.org
"""

import wpilib
from wpilib.command.commandgroup import CommandGroup

import const

from commands.drivetrain.drive_with_mecanum import Drive_With_Mecanum
from commands.drivetrain.rotate_to_angle import Rotate_To_Angle
from commands.shooter.auto_shoot_2 import Auto_Shoot_2
from commands.feeder.move_feeder_to_setpoint import Move_Feeder_To_Setpoint
from commands.shooter.manual_shot import Manual_Shot
from commands.drivetrain.stop import Stop


### CLASSES ###

class Lowbar_And_Shoot( CommandGroup ):
	"""
	This autonomous mode moves backwards, lowering the feeder as it
	approaches the low bar, goes under the low bar, then turns
	to face the tower.  It used to also take an auto shot but that's
	currently commented out.
	"""

	def __init__( self, robot ):
		super( ).__init__( )

		self.robot = robot

		self.addParallel( Move_Feeder_To_Setpoint( self.robot, const.FEEDER_CENTER_POINT ), 15 )
		self.addSequential( Drive_With_Mecanum( self.robot, 0, -0.7, 0 ), timeout = 3.5 ) #before 4 seconds
		self.addSequential( Drive_With_Mecanum( self.robot, 0, -0.7, -0.25 ), timeout = 2.0 ) #before 2.5
		#self.addSequential( Drive_With_Mecanum( self.robot, 0, -0.6, 0 ), timeout = 1.0 )
		#self.addSequential( Rotate_To_Angle( self.robot, 20.0 ) )
		#self.addSequential( Auto_Shoot_2( self.robot ) )
		self.addSequential( Stop( self.robot ) )
