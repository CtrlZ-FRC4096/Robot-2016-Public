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

from commands.shooter.run_shooter import Run_Shooter
from commands.shooter.stop_shooter import Stop_Shooter
from commands.shooter.wait_for_rate import Wait_For_Rate
from commands.indexer.forward_indexer import Forward_Indexer
from commands.indexer.reverse_indexer import Reverse_Indexer
from commands.indexer.stop_indexer import Stop_Indexer

import networktables
import wpilib
import const



		
class Manual_Shot( CommandGroup ):
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

		
		self.addSequential( On_Shooter( self.robot ) )		
		self.addSequential( WaitCommand( 4.0 ) )
		#self.addSequential( Wait_For_Rate( self.robot, const.SHOOTER_WHEEL_WAIT_FOR_RATE ), timeout = 10 )
		self.addSequential( Forward_Indexer( self.robot ), timeout = 3 )
		self.addSequential( Stop_Shooter( self.robot ) )
		self.addSequential( Stop_Indexer( self.robot ) )
