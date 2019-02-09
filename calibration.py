
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
File name: calibration.py
Author: Canopus Tong, Chen Li, Mohamed AhmedDate created: 9/10/2018
Python Version: 3.5
Description: To calibrate the angles of the motors to zero
'''
from ev3dev.ev3 import *

motor_i = LargeMotor(OUTPUT_A)
motor_o = LargeMotor(OUTPUT_B)

input("Move motor to starting position and press enter.")
motor_i.position = 0
motor_o.position = 0
