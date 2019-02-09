#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
File name: distance.py
Author: Canopus Tong, Chen Li, Mohamed AhmedDate created: 9/10/2018
Python Version: 3.5
Description: Assignment 2, question 3 of forward kinematics part.
A user moves the positon of an end effector to a first point, then clicks a touch sensor for storing  
The user then moves the position of the end effector to a second point, the clicks a touch for storing. 
The program calculates the distance betweeen these two points, returns them and displayes on Ev3 screen..
'''

#imports
from time import sleep
from ev3dev.ev3 import *
from math import *

# Convert degree to radian
# Args: float
# Return: float
def deg_to_rad(d):
    return d*(pi/180)

def distance():
	# number 1 corresponds to the inner motor
	# number 2 corresponds to the outer motor
	#inner motor(bottom)
	motor_1 = LargeMotor(OUTPUT_A)
	#outer motor (top)
	motor_2 = LargeMotor(OUTPUT_B)

	#ev3 screen object
	lcd = Screen()
	#ev3 touch sensor object
	ts = TouchSensor()

	# between the two motors, we have a gear that moves the outer motor(motor_2) when the inner motor(motor_1) moves
	#thus, this ratio accounts for the rate at which the motor has to move in order to in the desired angle
	# for example if we need to move the arm at a 90 degrees, we need to move the inner motor at 90*gear_ratio.
	gear_ratio = 56/24 #number of teeth of the bigger gear over the number of teeth of the smaller gear
	#length of the first(inner) arm link
	length_1 = 6.65
	#lenght of the 2nd(outer) arm link
	length_2 = 18.3
	#initialize a list that records the motor positons
	motor_pos = [] 

	#A counter that countes the number of times a user presses the touch sensor
	counter = 0
	#it turns true whenever counter equals two
	pressed_twice = False
	#countinues until the user presses the touch sensor twice
	while not pressed_twice:
		if ts.is_pressed:
			#inner motor position
			motor_1_pos = motor_1.position
			#outer motor position
			motor_2_pos = motor_2.position
			#increment the couter
			counter +=1
			#sound beep when the touch sensor is pressed
			Sound.beep().wait()
			#append the motor positions to motor_pos list
			motor_pos.append(deg_to_rad(motor_1_pos))
			motor_pos.append(deg_to_rad(motor_2_pos))
			sleep(5) 

		# condition to terminate the loop	
		if counter == 2:
				pressed_twice = True
		sleep(1)
	# the x position of the first point
	first_point_x = length_2*cos((motor_pos[0]/-gear_ratio)+motor_pos[1])+length_1*cos(motor_pos[0]/-gear_ratio)
	print("first_point_x: ", first_point_x)
	# the y position of the first point
	first_point_y = length_2*sin((motor_pos[0]/-gear_ratio)+motor_pos[1])+length_1*sin(motor_pos[0]/-gear_ratio)
	print("first_point_y: ", first_point_y)
	#the x position of the second point		
	second_point_x = length_2*cos((motor_pos[2]/-gear_ratio)+motor_pos[3])+length_1*cos(motor_pos[2]/-gear_ratio)
	print("second_point_x: ", second_point_x)
	#the y position of the second point
	second_point_y = length_2*sin((motor_pos[2]/-gear_ratio)+motor_pos[3])+length_1*sin(motor_pos[2]/-gear_ratio)
	print("second_point_y: ", second_point_y)

	#distance between the two points
	d = sqrt((second_point_x - first_point_x)**2 + (second_point_y - first_point_y)**2)
	print("d: ",d)
	#display the distance on the Ev3 screen
	lcd.draw.text((48,13), str(d), fill='black')
	lcd.update()
	Sound.beep()
	sleep(3)
	return first_point_x,first_point_y,second_point_x,second_point_y

distance()



