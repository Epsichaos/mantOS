#!/usr/bin/env python
import rospy
from pyrr import *
from manta.msg import Imu

def imu_callback(imu_data):
	print(imu_data)

def listener():
	rospy.init_node('listener', anonymous=True)
	rospy.Subscriber("/imu/data", Imu, imu_callback)
	rospy.spin()

if __name__ == '__main__':
	listener()
