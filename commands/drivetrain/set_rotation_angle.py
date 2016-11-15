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
        
        #print( 'rotating to {0:.2f}'.format( self.angle ))


    def initialize( self ):
        self.robot.gyro.reset( )
        #print( 'gyro start = {0:.2f}'.format( self.robot.gyro.getAngle( )))
        self.robot.drive.enable( )
        self.robot.drive.setSetpoint( self.angle )


    def execute( self ):
        """Called repeatedly"""


    def isFinished( self ):
        on_target = self.robot.drive.onTarget( )
        #timed_out = self.isTimedOut( )
        
        #if timed_out:
            #print( 'Timed out!' )
        if on_target:
            print( 'On Target! {0:.2f}'.format( self.robot.gyro.getAngle( ) ) )
            
        finished = self.robot.drive.onTarget( ) or self.isTimedOut( ) 

        #wpilib.SmartDashboard.putString( 'Feeder Lift PID Finished: ', '{0}'.format( finished ) )
        return finished


    def end( self ):
        """
        Called once after isFinished returns true
        """
        #print( 'gyro end = {0:.2f}'.format( self.robot.gyro.getAngle( )))
        self.robot.drive.disable( )
        #not sure if this can just be self.robot.drive.stop()


    def interrupted( self ):
        """
        Called when another thing which requires one or more of the same subsystem is scheduled to run
        """
        self.end( )
