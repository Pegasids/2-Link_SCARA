#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
File name: pathplanning.py
Author: Canopus Tong, Chen Li, Mohamed Ahmed
Date created: 9/10/2018
Python Version: 3.5
'''
from ev3dev.ev3 import *
from math import *
from invk2d_analytical import *
#from invk2d_newton import *
from move import *

motor_i = LargeMotor(OUTPUT_A)
motor_o = LargeMotor(OUTPUT_B)

GEARRATIO = 56/24
global GEARRATIO

def main():
    print("Select one of the following options:")
    print("1. Draw a straight line defined by two points.")
    print("2. Draw a straight line defined by a point, angle with respect to an horizontal axis and distance.")
    print("3. Draw an arc defined by n points.")
    task = int(input())
    if task == 1:
        x1 = float(input("Enter starting point x: "))
        y1 = float(input("Enter starting point y: "))
        x2 = float(input("Enter ending point x: "))
        y2 = float(input("Enter ending point y: "))
        n = int(input("Enter number of points: "))
        move_to_all_points(find_n_points_straight_line_by_two_points(x1,y1,x2,y2,n))
    elif task == 2:
        x1= float(input("Enter starting point x: "))
        y1 = float(input("Enter starting point y: "))
        theta = float(input("Enter angle with respect to an horizontal axis: (radian)"))
        d = float(input("Enter length of the straight: "))
        n = int(input("Enter number of points: "))
        move_to_all_points(find_n_points_straight_line_by_point_angle_distance(x1,y1,theta,d,n))
    elif task == 3:
        cx = float(input("Enter center of the arc x: "))
        cy = float(input("Enter center of the arc y: "))
        r = float(input("Enter radius of the arc: "))
        s = float(input("Enter arc length: "))
        n = int(input("Enter number of points: "))
        move_to_all_points(find_n_points_arc(cx,cy,r,s,n))

# Given a list of coordinates, move to these positions. 
# Args: [[x1,y1],...,[xn,yn]]
def move_to_all_points(lst):
    for pos in lst:
        print(pos)
        #angles = find_angle_newton(pos[0],pos[1])
        angles = find_angle_analytical(pos[0],pos[1]) # [[a1,b1],[a2,b2]]
        angles = choose(angles[0],angles[1]) # 2d vector
        print(angles)
        move(motor_i,angles[0],GEARRATIO)
        move(motor_o,angles[1])    

# Find n equidistant points of a straight line defined by two points.
# Args: x1,y1,x2,y2,number_of_points
# Return: [[x1,y1],...,[xn,yn]]
def find_n_points_straight_line_by_two_points(x1,y1,x2,y2,n):
    assert n>=2
    n_points = []
    deltaX = (x2-x1)/(n-1)
    deltaY = (y2-y1)/(n-1)
    for i in range(n):
        n_points.append([x1+i*deltaX, y1+i*deltaY])
    return n_points
    
# Find n equidistant points of a straight line defined by
# a point, angle with respect to an horizontal axis and distance.
# Args: x1,y1, angle_respect_to_x_axis, distance, number_of_points
# Return: [[x1,y1],...,[xn,yn]]
def find_n_points_straight_line_by_point_angle_distance(x1,y1,theta,d,n):
    x2 = x1 + d*cos(theta)
    y2 = y1 + d*sin(theta)
    return find_n_points_straight_line_by_two_points(x1,y1,x2,y2,n)

# Find n equidistant points of an arc defined by 
# center(x,y), radius, arclength.
# Args: center_x, center_y, radius, arc_length, number_of_points
# Return: [[x1,y1],...,[xn,yn]]
def find_n_points_arc(cx,cy,r,s,n):
    assert s<2*pi*r
    n_points = []
    theta = s/r
    deltaTheta = theta/(n-1)
    for i in range(n):
        n_points.append([cx+r*cos(i*deltaTheta), cy+r*sin(i*deltaTheta)])
    return n_points
    


if __name__ == "__main__":
    main()
