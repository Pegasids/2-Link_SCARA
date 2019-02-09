#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
File name: invk2d_newton.py
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
    angles = find_angle_newton(x,y) # 2d vector
    print("Calculated angle: ",angles)
    move(motor_i,angles[0],GEARRATIO)
    move(motor_o,angles[1])
    motor_o.run_timed(time_sp=30, speed_sp=0, stop_action='coast')
    motor_i.run_timed(time_sp=30, speed_sp=0, stop_action='coast')
    sleep(1)
    print("Actual: ", [motor_i.position/-GEARRATIO,motor_o.position])
    
# Find the two joint angle by Newton method
# Args: x, y (float)
# Return: [theta_i,theta_o]
def find_angle_newton(x,y):
    x0 = [deg_to_rad(motor_i.position),deg_to_rad(motor_o.position)] # [theta_inner, theta_outer]
    while norm2d(f(x,y,x0[0],x0[1])) >= 10**(-8):
        if (x0[1]==0) or (x0[1]%pi==0):
            x0[1]+=0.001
        jacobian = Jf(x0[0],x0[1]) # 2x2 2d list
        inv_jacobian = inv_matrix(jacobian) # 2x2 2d list
        v = f(x,y,x0[0],x0[1]) # vector 2x1 1d list
        temp = matrix_multi_2x2_2x1(inv_jacobian,v) # vector 2x1 1d list
        x0 = matrix_sub_2x1_2x1(x0,temp) # vector 2x1 1d list
    return format_1(x0)


# The f term of Newton method
# Args: x,y,theta_i, theta_o
# Return: [a,b]
def f(x,y,theta_i,theta_o):
    a = L_I*cos(theta_i) + L_O*cos(theta_i + theta_o) - x
    b = L_I*sin(theta_i) + L_O*sin(theta_i + theta_o) - y
    return [a,b]

# Find the Jacobian matrix Jf
# Args: theta_i, theta_o
# Return: [[a,b],[c,d]]
def Jf(theta_i,theta_o):
    dfxdti = -L_I*sin(theta_i) - L_O*sin(theta_i + theta_o)
    dfxdto = -L_O*sin(theta_i + theta_o)
    dfydti = L_I*cos(theta_i) + L_O*cos(theta_i + theta_o)
    dfydto = L_O*cos(theta_i + theta_o)
    return [[dfxdti,dfxdto],[dfydti,dfydto]]

# 2x2 matrix iversion
# Args: [[a,b],[c,d]]
# Return: [[a',b'],[c',d']]
def inv_matrix(matrix):
    det = determinant(matrix)
    a = matrix[1][1]
    b = -matrix[0][1]
    c = -matrix[1][0]
    d = matrix[0][0]
    k = 1/det
    return [[k*a,k*b],[k*c,k*d]]

# Product of 2x2 2x1
# Args: [[a,b],[c,d]],[i,s]
# Return: [a',b']
def matrix_multi_2x2_2x1(matrix,vector):
    r1 = (matrix[0][0]*vector[0]) + (matrix[0][1]*vector[1])
    r2 = (matrix[1][0]*vector[0]) + (matrix[1][1]*vector[1])
    return [r1,r2]

# 2x1 matrix subtraction
# Args: [a,b],[c,d]
# Return: [e,f]
def matrix_sub_2x1_2x1(v1,v2):
    r1 = v1[0] - v2[0]
    r2 = v1[1] - v2[1]
    return [r1,r2]

# Calculate det of 2x2
# Args: [[a,b],[c,d]]
# Return: float
def determinant(matrix):
    return (matrix[0][0]*matrix[1][1])-(matrix[0][1]*matrix[1][0])

# Calculate norm of 2d vector
# Args: [a,b]
# Return: float
def norm2d(vector):
    return sqrt((vector[0]*vector[0])+(vector[1]*vector[1]))

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
