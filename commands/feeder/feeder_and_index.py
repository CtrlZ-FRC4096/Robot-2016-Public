"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2016, "Stronghold"
Code for robot "Jaw-Z"
contact@team4096.org
"""

from wpilib.command import CommandGroup
from commands.indexer.index_with_feeder import Index_With_Feeder
from commands.feeder.reverse_feeder import Reverse_Feeder
from commands.feeder.forward_feeder import Forward_Feeder

class Feeder_And_Index( CommandGroup ):
	
	def __init__( self, robot ):
		super( ).__init__( )

		self.robot = robot

		self.addParallel( Forward_Feeder( self.robot ) )
		self.addSequential( Index_With_Feeder( self.robot ) )


	def end( self ):
		self.robot.feeder_belts.stop( )
		self.robot.indexer.stop( )


	def cancel( self ):
		"""
		If bound to a button using whileHeld, will be called once when button is released
		"""
		self.end( )
		super( ).cancel( )		