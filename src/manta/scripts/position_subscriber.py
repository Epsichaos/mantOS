#!/usr/bin/env python
import rospy
import time
from manta.msg import NavSatFix
from manta.msg import Imu
from sensor_msgs.msg import LaserScan
import numpy

isGpsWritten = False
isTelemeterWritten = False
isImuWritten = False
isTimeWritten = False
currentTime = 0
tempTime = 0

def isClose(t1, t2):
	if(abs(t2-t1)<3000000000):
		return True
	else:
		return False

def resetAll():
	rospy.loginfo("---- RESET DATA ----")
	global isGpsWritten
	global isTelemeterWritten
	global isImuWritten
	global isTimeWritten
	global currentTime
	global tempTime
	
	isGpsWritten = False
	isImuWritten = False
	isTelemeterWritten = False
	isTimeWritten = False

	results = open("results.txt", "a")
	results.write("\n")
def general_callback(data):
	#use global variables
	global isGpsWritten
	global isTelemeterWritten
	global isImuWritten
	global isTimeWritten
	global currentTime
	global tempTime

	results = open("results.txt", "a")
	if(isGpsWritten == False and isTelemeterWritten == False and isImuWritten == False and isTimeWritten == False):
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
		if(isGpsWritten == True and isImuWritten == True and isTelemeterWritten == False): 
			if(isClose(currentTime, tempTime) == True):
				rospy.loginfo("---- TELEMETER WRITE ----")
				tableLength = len(data.ranges)
				results.write(" DI ")
				results.write(str(data.ranges[tableLength-1]))
				results.write(" ")
				results.write(str(data.ranges[int(numpy.floor(tableLength/2))]))
				results.write(" ")
				results.write(str(data.ranges[0]))
				isTelemeterWritten = True
			else:
				results.close()
				resetAll()
	# all the data has been written	
	if(isGpsWritten == True and isImuWritten == True and isTelemeterWritten == True):
		rospy.loginfo("---- LINE WRITTEN ----")
		results.write("\n")		
		isGpsWritten = False
		isImuWritten = False
		isTelemeterWritten = False
		isTimeWritten = False
	# Close file	
	results.close()
def listener():
	rospy.init_node('listener', anonymous=True)
	rospy.Subscriber('/gps/fix', NavSatFix, general_callback)
	rospy.Subscriber('/imu/data', Imu, general_callback)
	rospy.Subscriber('scan', LaserScan, general_callback)
	rospy.spin()

if __name__ == '__main__':
	listener()
