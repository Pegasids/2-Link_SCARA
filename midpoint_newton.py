#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
File name: midpoint_newton.py
Author: Canopus Tong, Chen Li, Mohamed Ahmed
Date created: 9/10/2018
Python Version: 3.5
'''
from ev3dev.ev3 import *
from math import *
from move import *
from invk2d_newton import *
from time import sleep


motor_i = LargeMotor(OUTPUT_A)
motor_o = LargeMotor(OUTPUT_B)
ts = TouchSensor()

GEARRATIO = 56/24
L_I = 6.65
L_O = 18.3
global GEARRATIO,L_I, L_O

def main():
    theta_i_1, theta_o_1 = get_angles_with_touch_sensor()
    x1,y1 = get_xy_given_angles(theta_i_1, theta_o_1) # get first position
    print("x1,y1: ",x1,y1)
    theta_i_2, theta_o_2 = get_angles_with_touch_sensor()
    x2,y2 = get_xy_given_angles(theta_i_2, theta_o_2) # get second position 
    print("x2,y2: ",x2,y2)   
    mx, my = midpoint(x1,y1,x2,y2) 
    print("mx,my: ",mx,my)
    angles = find_angle_newton(mx,my) # 2d vector
    move(motor_i,angles[0],GEARRATIO)
    move(motor_o,angles[1])    
    

# Find midpoint
# Args: x1,y1,x2,y2 (float)
# Return: x,y
def midpoint(x1,y1,x2,y2):
    return (x1+x2)/2, (y1+y2)/2

# Find theta_i, theta_o when touch sensor is pressed
# Return: theta_i, theta_o (radian)
def get_angles_with_touch_sensor():
    while True:
        if ts.is_pressed:
            theta_i = motor_i.position
            theta_o = motor_o.position
            Sound.beep()
            sleep(5)

            return deg_to_rad(theta_i), deg_to_rad(theta_o)

# Find x and y given two joint angles
# Args: theta_i, theta_o (radian)
# Return: x ,y
def get_xy_given_angles(theta_i, theta_o):
    x = L_I*cos(theta_i/-GEARRATIO) + L_O*cos((theta_i/-GEARRATIO)+theta_o)
    y = L_I*sin(theta_i/-GEARRATIO) + L_O*sin((theta_i/-GEARRATIO)+theta_o)
    return x,y

# Convert radian to degree
# Args: float
# Return: float
def rad_to_deg(r):
    return r*(180/pi)

# Convert degree to radian
# Args: float
# Return: float
def deg_to_rad(d):
    return d*(pi/180)

if __name__ == "__main__":
    main()
