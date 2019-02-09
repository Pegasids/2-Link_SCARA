#!/usr/bin/env python3

'''
File name: find_xy.py
Author: Canopus Tong, Chen Li, Mohamed Ahmed
Date created: 9/10/2018
Python Version: 3.5
Description:  Assignment 2, question 2 of forward kinematics part.
Given two angles as an input, this program moves the robot arm to the corresponding 
join angles then returns the position of the end effector and displayes on Ev3 screen.
'''
#imports
from ev3dev.ev3 import *
from time import sleep
from move import *
from math import *
# number 1 corresponds to the inner motor
# number 2 corresponds to the outer motor

#inner motor(bottom)
motor_1 = LargeMotor(OUTPUT_A)
#outer motor (top)
motor_2 = LargeMotor(OUTPUT_B)

#ev3 screen object
lcd = Screen()
# between the two motors, we have a gear that moves the outer motor(motor_2) when the inner motor(motor_1) moves
#thus, this ratio accounts for the rate at which the motor has to move in order to in the desired angle
# for example if we need to move the arm at a 90 degrees, we need to move the inner motor at 90*gear_ratio.
gear_ratio = 56/24 #number of teeth of the bigger gear over the number of teeth of the smaller gear


#angle_ = input("Enter the angle you want the first motor to move: ")
#angle_2 = input("Enter the angle you want the second motor to move: ")

# Convert degree to radian
# Args: float
# Return: float
def deg_to_rad(d):
    return d*(pi/180)

# Convert radian to degree
# Args: float
# Return: float
def rad_to_deg(r):
    return r*(180/pi)

#function begins here
def find_xy(angle_1, angle_2):
	# m1_angle and m2_angle both call on move function, giving the two motors and their angles as parameters.
	# I addition, m1_angle also gives gear_ratio as parameters, which then moves the arms at their given angles
	# and returns the current position of the motors 
	m1_angle = deg_to_rad(move(motor_1,angle_1,gear_ratio))
	m2_angle = deg_to_rad(move(motor_2,angle_2))

	print("m1_angle: ", rad_to_deg(m1_angle))
	print("m2_angle: ", rad_to_deg(m2_angle))


	#length of the first arm link
	length_1 = 6.65
	#lenght of the 2nd arm link
	length_2 = 18.3
	#We used this x_pos_ther and y_pos_ther to know where the end effector supposed to be theoretically
	#it uses the given angles to calclute the x,y positon of the end effector
	#by doing this we can compare the actual to the theoretical x,y positons of the end effector
	x_pos_ther = length_1*cos(deg_to_rad(angle_1)) + length_2*cos((deg_to_rad(angle_1))+deg_to_rad(angle_2))
	y_pos_ther = length_1*sin(deg_to_rad(angle_1)) + length_2*sin((deg_to_rad(angle_1))+deg_to_rad(angle_2)) 
	print("x_pos_ther: ", x_pos_ther)
	print("y_pos_ther: ", y_pos_ther)

	#usign the positions returned by the move functioon,
	#calculate the x positioin of the end effector 
	x_pos_cal = length_1*cos(m1_angle/-gear_ratio) + length_2*cos((m1_angle/-gear_ratio)+m2_angle)

	# usign the positions returned by the move functioon,
	# calculate the y positioin of the end effector 
	y_pos_cal = length_1*sin(m1_angle/-gear_ratio) + length_2*sin((m1_angle/-gear_ratio)+m2_angle)

	print("x_pos_cal", x_pos_cal)
	print("y_pos_cal", y_pos_cal)

	#draw the x and y positions of the end effector on the screen 
	lcd.draw.text((48,13), str(x_pos_cal), fill='white')
	lcd.draw.text((36,80), str(y_pos_cal))
	lcd.update()
	Sound.beep()
	sleep(3)
	return x_pos_cal, y_pos_cal
#angles required the robot arms to move
a1 = float(input("Enter the angle you'd want the first motor to move: "))
a2 = float(input("Enter the angle you'd want the second motor to move: "))
find_xy(a1,a2)




