"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2016, "Stronghold"
Code for robot "Jaw-Z"
contact@team4096.org
"""

import time

from wpilib.command import CommandGroup
from wpilib.command import Command
from wpilib.command import WaitCommand
from commands.shooter.on_shooter import On_Shooter

from commands.feeder.forward_feeder import Forward_Feeder
from commands.drivetrain.rotate_to_angle import Rotate_To_Angle
from commands.drivetrain.set_rotation_angle import Set_Rotation_Angle
from commands.shooter.run_shooter import Run_Shooter
from commands.shooter.stop_shooter import Stop_Shooter
from commands.shooter.wait_for_rate import Wait_For_Rate
from commands.indexer.forward_indexer import Forward_Indexer
from commands.indexer.reverse_indexer import Reverse_Indexer
from commands.indexer.stop_indexer import Stop_Indexer
from commands.feeder.stop_feeder import Stop_Feeder

import networktables
import wpilib
import const


def calculate_angle( robot ):
	target_values = robot.shooter_camera.get_target_values( )

	if len( target_values[ 'centerX' ] ) == 0:
		# No vision targets found
		return 0
	
	elif len( target_values[ 'centerX' ] ) == 1:
		center_x = target_values[ 'centerX' ][ 0 ]
		
	else:
		# Multiple targets found, so choose the best one
		
		if len( target_values[ 'area' ] ) != len( target_values[ 'centerX' ] ):
			# These two arrays must be same length for us to pick right one.
			# Sometimes GRIP finds 3 areas, but only 2 centerX values, for instance
			return 0
		
		# Find index of target with largest area
		largest_area_idx = 0

		for i in range( len( target_values[ 'area' ] ) ):
			if target_values[ 'area' ][ i ] > largest_area_idx:
				largest_area_idx = i
				
		center_x = target_values[ 'centerX' ][ largest_area_idx ]
		
	#target_x = const.CAMERA_RES_X / 2.0 + const.CAMERA_SHOOTER_PIXEL_OFFSET
	cam_fudge_value = wpilib.SmartDashboard.getNumber( 'Cam Fudge: ' )
	target_x = const.CAMERA_RES_X / 2.0 + cam_fudge_value

	pixel_offset = target_x - center_x
	degrees_per_pixel = const.CAMERA_FOV / const.CAMERA_RES_X
	degrees_offset = pixel_offset * degrees_per_pixel * -1.0

	return degrees_offset



class Rotate_To_Target( Rotate_To_Angle ):
	def __init__( self, robot ):

		self.robot = robot

		angle = 0	# gets set for real in initialize below
		super( ).__init__( self.robot, angle )


	def initialize( self ):
		angle = calculate_angle( self.robot )
		
		self.angle = angle
		
		super( ).initialize( )
		
	
	def execute( self ):
		pass


	def isFinished( self ):
		return super( ).isFinished( )
	


class Start_Shooter_And_Align( CommandGroup ):

	def __init__( self, robot ):
		super( ).__init__( )

		self.robot = robot
		

		self.addSequential( Rotate_To_Target( self.robot ) )
		self.addSequential( WaitCommand( 1.0 ) )
		self.addSequential( Rotate_To_Target( self.robot ) )
		self.addSequential( WaitCommand( 1.0 ) )

		self.addSequential( On_Shooter( self.robot ) )
		
		
class Auto_Shoot_2( CommandGroup ):
	"""
	(OUTDATED)
	Sequence goes like this:
	
	1. Run Start_Shooter_And_Align commandgroup
		1a. Rotate robot to vision target.
		1b. Rotate robot to target again, just to make sure we're on-target
		1c. Spin up the shooter, and at the same time:
		1d. Start 2 second timer
	2. Start indexer, which shoots the ball
	3. Wait 1 second, then...
	4. Stop shooter & indexer
	
	We use two commandgroups here because we have two commands to run in parallel
	(spin up the shooter and start the two-second timer), but those two commands together
	must complete before it continues to the next ones.
	"""
	def __init__( self, robot ):
		super( ).__init__( )

		self.robot = robot

		## This waits 3.0 secs before shooting
		#self.addSequential( Start_Shooter_And_Align( self.robot ) )
		#self.addSequential( WaitCommand( 5.0 ) )
		#self.addSequential( Forward_Indexer( self.robot ), timeout = 1 )
		#self.addSequential( Stop_Shooter( self.robot ) )
		#self.addSequential( Stop_Indexer( self.robot ) )

		# This waits until target rate is achieved on wheel before shooting
		self.addSequential( Rotate_To_Target( self.robot ) )
		self.addSequential( WaitCommand( 0.5 ) )
		self.addSequential( Rotate_To_Target( self.robot ) )
		self.addSequential( On_Shooter( self.robot ) )
		self.addSequential( WaitCommand( 3.00 ) )
		self.addSequential( Reverse_Indexer( self.robot ), .75 )
		#self.addSequential(Forward_Feeder( self.robot ), .25 ) 
		self.addParallel( Forward_Indexer( self.robot ), 3.00 )
		self.addSequential( WaitCommand (0.30))
		self.addSequential(Forward_Feeder( self.robot ), 3.00 )
		#self.addSequential( Wait_For_Rate( self.robot, const.SHOOTER_WHEEL_WAIT_FOR_RATE ), timeout = 10 )
		self.addSequential( Stop_Shooter( self.robot ) )
		self.addSequential( Stop_Indexer( self.robot ) )
		self.addSequential( Stop_Feeder( self.robot ) )
		
