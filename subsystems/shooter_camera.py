"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2016, "Stronghold"
Code for robot "Jaw-Z"
contact@team4096.org
"""

import math
import sys
import time

import wpilib
import wpilib.command

import networktables


### CONSTANTS ###

### CLASSES ###

class Shooter_Camera( wpilib.command.Subsystem ):
	
	def __init__( self, robot ):
				
		super( ).__init__( 'shooter camera' )
		
		self.robot = robot
		
		
	def get_target_values( self ):
		values = {
			'centerX': 	networktables.NumberArray( ),
		    'centerY': 	networktables.NumberArray( ),
		    'width': 	networktables.NumberArray( ),
		    'height': 	networktables.NumberArray( ),
		    'area': 	networktables.NumberArray( ),		    
		}
		
		for key in values:
			try:
				self.robot.nt_grip.retrieveValue( key, values[ key ] )
			except:
				# No values found in NT for GRIP
				values[ key ] = [ ]
				
		return values


 		
	def log( self ):
		'''
		logs info about various things
		'''
		targets_visible = len( self.get_target_values( )[ 'area' ] ) > 0
		
		wpilib.SmartDashboard.putBoolean( '.', targets_visible )
		#wpilib.SmartDashboard.put( 'center_x', targets_visible )
		
		#wpilib.SmartDashboard.putString('Shooter Angle', '{0}'.format(self.current_shooter_angle))