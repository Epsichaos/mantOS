#!/usr/bin/env python
import rospy
import time
from sensor_msgs.msg import NavSatFix
from manta.msg import Imu
#from sensor_msgs.msg import Imu
from sensor_msgs.msg import LaserScan
from manta.msg	 import Echo
import numpy

isGpsWritten = False
#isTelemeterWritten = False
isEchosounderWritten = False
isImuWritten = False
isTimeWritten = False
currentTime = 0
tempTime = 0
fileName = "results"+str(round(time.time()*1000000000))+".txt"

def isClose(t1, t2):
	if(abs(t2-t1)<3000000000):
		return True
	else:
		return False

def resetAll():
	rospy.loginfo("---- RESET DATA ----")
	global isGpsWritten
	#global isTelemeterWritten
	global isEchosounderWritten	
	global isImuWritten
	global isTimeWritten
	global currentTime
	global tempTime
	
	isGpsWritten = False
	isImuWritten = False
	#isTelemeterWritten = False
	isEchosounderWritten = False	
	isTimeWritten = False

	results = open(fileName, "a")
	results.write("\n")
def general_callback(data):
	#use global variables
	global isGpsWritten
	#global isTelemeterWritten
	global isEchosounderWritten
	global isImuWritten
	global isTimeWritten
	global currentTime
	global tempTime

	results = open(fileName, "a")
	if(isGpsWritten == False and isEchosounderWritten == False and isImuWritten == False and isTimeWritten == False):
		currentTime = int(round(time.time()*1000000000))
		results.write("T ")
		# write time in milliseconds
		results.write(str(currentTime))
		isTimeWritten = True

	if hasattr(data, 'linear_acceleration'):
		tempTime = int(round(time.time()*1000000000))
		if(isGpsWritten == True and isImuWritten == False):
			if(isClose(currentTime, tempTime) == True):
				rospy.loginfo("---- IMU WRITE ----")				
				results.write(" OR ")
				results.write(str(data.direction))
				isImuWritten = True
			else:
				results.close()
				resetAll()
	elif hasattr(data, 'latitude'):
		tempTime = int(round(time.time()*1000000000))
		if(isGpsWritten == False):
			if(isClose(currentTime, tempTime) == True):
				rospy.loginfo("---- GPS WRITE ----")
				results.write(" GPS ")
				results.write(str(data.longitude*1000))
				results.write(" ")
				results.write(str(data.latitude*1000))
				isGpsWritten = True
			else:
				results.close()
				resetAll()
	else:
		tempTime = int(round(time.time()*1000000000))
		if(isGpsWritten == True and isImuWritten == True and isEchosounderWritten == False):
			if(isClose(currentTime, tempTime) == True):
				rospy.loginfo("---- ECHO SOUNDER WRITE ----")
				results.write(" PRO ")
				results.write(str(data.profondeur))
				isEchosounderWritten = True
			else:
				results.close()
				resetAll()
#		
#	else:
#		tempTime = int(round(time.time()*1000000000))	
#		if(isGpsWritten == True and isImuWritten == True and isTelemeterWritten == False): 
#			if(isClose(currentTime, tempTime) == True):
#				rospy.loginfo("---- TELEMETER WRITE ----")
#				tableLength = len(data.ranges)
#				results.write(" DI ")
#				results.write(str(data.ranges[tableLength-1]))
#				results.write(" ")
#				results.write(str(data.ranges[int(numpy.floor(tableLength/2))]))
#				results.write(" ")
#				results.write(str(data.ranges[0]))
#				isTelemeterWritten = True
#			else:
#				results.close()
#				resetAll()

	# all the data has been written	
	if(isGpsWritten == True and isImuWritten == True and isEchosounderWritten == True):
		rospy.loginfo("---- LINE WRITTEN ----")
		results.write("\n")		
		isGpsWritten = False
		isImuWritten = False
		isEchosounderWritten = False
		#isTelemeterWritten = False
		isTimeWritten = False
	# Close file	
	results.close()
def listener():
	rospy.init_node('listener', anonymous=True)
	rospy.Subscriber('/gps/fix', NavSatFix, general_callback)
	rospy.Subscriber('/imu/data', Imu, general_callback)
	rospy.Subscriber('echo/data', Echo, general_callback)	
	#rospy.Subscriber('scan', LaserScan, general_callback)
	rospy.spin()

if __name__ == '__main__':
	listener()
