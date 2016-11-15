"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2016, "Stronghold"
Code for robot "Jaw-Z"
contact@team4096.org
"""

from commands.feeder.set_feeder_setpoint import Set_Feeder_Setpoint

# Sensor value for lift at center position



class Move_Feeder_To_Setpoint( Set_Feeder_Setpoint ):
    """
    Centers the feeder
    """
   
    def __init__( self, robot, value ):
        
        self.robot = robot
        
        super( ).__init__( self.robot, value )
         
        
    def isFinished( self ):
        return super( ).isFinished( ) #or self.feeder_lift.lift_encoder.getValue( ) > STALL_POINT
