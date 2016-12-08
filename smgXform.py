#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Copyright © 2016 Spencer Duncan <spencerjduncan@gmail.com>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

# SolidWorks Composer is probably a registered trademark or something of Dassault Systèmes
# The author of this software is in no affiliated with Dassault Systèmes
# Dassault Systèmes has not condoned, approved of, or probably even seen this script
# If any one at Dassault cares I'll remove any reference to their products upon request.

useage ="""
smgXform.py
Tool for applying linear transforms to SolidWorks Composer camera views.
useage: smgXform.py [X offset] [Y offset] [Z offset] [Input smgView file]
Writes transformed file to output.smgView"""

import re
import numpy as np
from sys import argv, stdin

reg = re.compile(r"""(?P<Q1><Anchor\.1.*?X=\")					#Begin XML Block
					 (?P<X1>[-,0-9,.,e]*)						#Anchor 1 X
					 (?P<Q2>.*?Y=\")(?P<Y1>[-,0-9,.,e]*)		#Anchor 1 Y
					 (?P<Q3>.*?Z=\")(?P<Z1>[-,0-9,.,e]*)		#Anchor 1 Z
					 (?P<Q4>.*?X=\")(?P<VX>[-,0-9,.,e]*)		#Anchor VXX
					 (?P<Q5>.*?Y=\")(?P<VY>[-,0-9,.,e]*)		#Anchor VXY
					 (?P<Q6>.*?Z=\")(?P<VZ>[-,0-9,.,e]*)		#Anchor VXZ
					 (?P<Q7>.*?X=\")(?P<UX>[-,0-9,.,e]*)		#Anchor VYX
					 (?P<Q8>.*?Y=\")(?P<UY>[-,0-9,.,e]*)		#Anchor VYY
					 (?P<Q9>.*?Z=\")(?P<UZ>[-,0-9,.,e]*)		#Anchor VYZ
					 (?P<QA>.*?<Anchor\.2.*?X=\")				#Anchor 2 Head
					 (?P<X2>[-,0-9,.,e]*)						#Anchor 2 X
					 (?P<QB>.*?Y=\")(?P<Y2>[-,0-9,.,e]*)		#Anchor 2 Y
					 (?P<QC>.*?Z=\")(?P<Z2>[-,0-9,.,e]*)		#Anchor 2 Z
					 (?P<QD>.*?\.DistCOI.*?)(?P<D>[-,0-9,.,e]*) #Camera Distance
					 (?P<QE>\"\/>)"""							#End XML Block
					 , re.X | re.S) 

def applytransform(m):
	ones = np.array([float(m.group('X1')), float(m.group('Y1')), float(m.group('Z1'))])
	twos = np.array([float(m.group('X2')), float(m.group('Y2')), float(m.group('Z2'))])
	VX   = np.array([float(m.group('VX')), float(m.group('VY')), float(m.group('VZ'))])
	VY   = np.array([float(m.group('UX')), float(m.group('UY')), float(m.group('UZ'))])
	VZ   = np.cross(VX, VY)

	dist  = abs(float(m.group('D')) - np.dot(VZ,xform))

	nTwos = twos + xform
	nOnes = nTwos + dist*VZ

	return ( m.group('Q1') + str(nOnes[0]) + m.group('Q2') + str(nOnes[1]) + m.group('Q3') + str(nOnes[2])
		   + m.group('Q4') + m.group('VX') + m.group('Q5') + m.group('VY') + m.group('Q6') + m.group('VZ')
		   + m.group('Q7') + m.group('UX') + m.group('Q8') + m.group('UY') + m.group('Q9') + m.group('UZ')
		   + m.group('QA') + str(nTwos[0]) + m.group('QB') + str(nTwos[1]) + m.group('QC') + str(nTwos[2])
		   + m.group('QD') + str(dist)     + m.group('QE'))

if len(argv) != 5:
	print(useage)
	exit()

try:
	xform = np.array([float(argv[1]),float(argv[2]),float(argv[3])])
except:
	print("Bad transform values")
	print(usage)
	exit()

try:
	string = open(argv[4], 'r').read()
except:
	print("Couldn't open " + argv[4])
	print(usage)
	exit()

print("Generating...")
output = reg.sub(applytransform, string)

f = open("output.smgView", 'w')
f.write(output)
f.close()
