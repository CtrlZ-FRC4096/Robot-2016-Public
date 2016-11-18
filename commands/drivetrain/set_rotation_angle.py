"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2016, "Stronghold"
Code for robot "Jaw-Z"
contact@team4096.org
"""

import wpilib
from wpilib.command import Command


class Set_Rotation_Angle( Command ):

    def __init__( self, robot, angle ):
        super( ).__init__( )

        self.robot = robot

        self.requires( self.robot.drive ) 
        self.angle = angle
        self.setTimeout( 10 )
        

    def initialize( self ):
        self.robot.gyro.reset( )
        self.robot.drive.enable( )
        self.robot.drive.setSetpoint( self.angle )


    def execute( self ):
        """Called repeatedly"""


    def isFinished( self ):
        on_target = self.robot.drive.onTarget( )
        finished = self.robot.drive.onTarget( ) or self.isTimedOut( ) 

        return finished


    def end( self ):
        """
        Called once after isFinished returns true
        """
        self.robot.drive.disable( )


    def interrupted( self ):
        """
        Called when another thing which requires one or more of the same subsystem is scheduled to run
        """
        self.end( )
