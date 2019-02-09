#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
File name: PID.py
Author: Canopus Tong, Chen Li ,Mohamed Ahmed
Date created: 9/10/2018
Python Version: 3.5
Description: Assignment 2, question 1 of PID Control.
The controller multiplies the error by the Proportional Gain and adds the integral of error to proportional term. The integral term ensures the state error is zero.
'''
from ev3dev.ev3 import *
from time import sleep

motor = LargeMotor(OUTPUT_A)

# calibration, set position to zero
motor.position = 0
sleep(0.5)

# initialize default values
previous_error = 0
integral = 0
time = 0

# initialize setpt,Kp,Ki,Kd,dt
setpoint = 90
#Kp = float(input("Kp:"))
Kp = 3.95
Ki = float(input("Ki:"))
#Ki = 0
Kd = 0.00001
#Kd = float(input("Kd:"))
#dt = float(input("dt:"))
dt = 0.5

print("setpoint,Kp,Ki,Kd,dt: ",setpoint,Kp,Ki,Kd,dt)
while time <= 30: #run each test for 30 seconds
    pos = motor.position # motor angle
    error = setpoint - pos 
    integral = integral + error*dt
    derivative = (error - previous_error)/dt
    output = Kp*error + Ki*integral + Kd*derivative
    previous_error = error
    motor.run_timed(speed_sp=output, time_sp=dt*1000)
    sleep(dt)
    print("t,pos: ",time,pos)
    time += dt # increment time
