#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
File name: invk2d_analytical.py
Author: Canopus Tong, Chen Li, Mohamed Ahmed
Date created: 9/10/2018
Python Version: 3.5
'''
from ev3dev.ev3 import *
from math import *
from move import *
from time import sleep

motor_i = LargeMotor(OUTPUT_A)
motor_o = LargeMotor(OUTPUT_B)

GEARRATIO = 56/24
L_I = 6.65
L_O = 18.3
global GEARRATIO,L_I, L_O

def main():
    x = float(input("Enter X: "))
    y = float(input("Enter Y: "))
    angles = find_angle_analytical(x,y) # [[a1,b1],[a2,b2]]
    angles = choose(angles[0],angles[1]) # 2d vector
    print("Calculated angle: ",angles)
    move(motor_i,angles[0],GEARRATIO)
    move(motor_o,angles[1]) 
    motor_o.run_timed(time_sp=30, speed_sp=0, stop_action='coast')
    motor_i.run_timed(time_sp=30, speed_sp=0, stop_action='coast')
    sleep(1)   
    print("Actual: ", [motor_i.position/-GEARRATIO,motor_o.position])
    

# Choose the set of angles closer to currect angles
# Args: [theta_i,theta_o],[theta_i,theta_o] in degree
# Return: [theta_i,theta_o]
def choose (v1,v2):
    current_i = motor_i.position/-GEARRATIO 
    current_o = motor_o.position
    if (abs(v1[0]-current_i)+abs(v1[1]-current_o))<=(abs(v2[0]-current_i)+abs(v2[1]-current_o)):
        return v1
    return v2
    

# Find the two joint angle analytically
# Args: x, y (float)
# Return: [theta_i,theta_o],[theta_i,theta_o] (two possible solns)
def find_angle_analytical(x,y):
    theta_o_1 = acos((x**2+y**2-L_I**2-L_O**2)/(2*L_I*L_O))
    theta_o_2 = -acos((x**2+y**2-L_I**2-L_O**2)/(2*L_I*L_O))
    theta_i_1 = atan2(y,x) - cosine_law_solve_angle(L_I,sqrt(x*x+y*y),L_O)
    theta_i_2 = atan2(y,x) + cosine_law_solve_angle(L_I,sqrt(x*x+y*y),L_O)
    return format_1([theta_i_1,theta_o_1]),format_1([theta_i_2,theta_o_2])

# Find angle using cosine law c^2 = a^2 + b^2 -2abcos(theta)
# Args: a,b,c
# Return: theta
def cosine_law_solve_angle(a,b,c):
    return acos((a*a+b*b-c*c)/(2*a*b))

# Convert radian to degree
# Args: float
# Return: float
def rad_to_deg(r):
    return r*(180/pi)

# Format output in from rad to degree @(-179,180)
# Args: [theta_i,theta_o]
# Return: [theta_i',theta_o']
def format_1(vector):
    vector[0] = round(rad_to_deg(vector[0]))%360
    vector[1] = round(rad_to_deg(vector[1]))%360
    for i in range(len(vector)):
        if vector[i] > 180:
            vector[i]-=360
    return vector
    
if __name__ == "__main__":
    main()
