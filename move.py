#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
File name: move.py
Author: Canopus Tong, Chen Li ,Mohamed Ahmed
Date created: 9/10/2018
Python Version: 3.5
Description: Assignment 2, question B and C of forward and inverse kinematics.
The move.py is the called program for forward and inverse kinematics programs
It introduces the PID movement to the movement of motor in 
forward and inverse kinematics programs
'''
from ev3dev.ev3 import *
from time import sleep

# Move a motor to a specific angle using PID
# Args: motor,setpoint(deg)
# Return: motor's exact position
def move(motor,setpoint,gearratio=0):
    if gearratio!=0:
        setpoint = round(-setpoint*gearratio)

    # initialize default values
    previous_error = 0
    integral = 0
    # initialize Kp,Ki,Kd,dt
    Kp = 3.5; Ki = 0; Kd = 0
    dt = 0.1
    
    while True:
        pos = motor.position
        error = setpoint - pos
        
        # exit while loop if error within tolerance
        if abs(error) <= 2:
                motor.stop(stop_action='hold')
                motor.stop(stop_action='coast')
                break
                
        integral += error*dt
        derivative = (error - previous_error)/dt
        output = Kp*error + Ki*integral +Kd*derivative
        previous_error = error

        # contraint output to motor maximum capacity
        if output > 999:
            output = 999
        elif output < -999:
            output = -999
        #print('output',output)
        
        # adjust output when it is low, so robot can keep moving
        if (output <= 22) and (output >= -22):
            output = output*2.5
        
        # run the motor
        motor.run_timed(speed_sp=output, time_sp=dt*1000)
        sleep(dt)
        
    return motor.position # returns motor exact position


