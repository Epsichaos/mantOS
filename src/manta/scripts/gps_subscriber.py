#!/usr/bin/env python
import rospy
from manta.msg import NavSatFix

def gps_callback(gps_data):
	rospy.loginfo(gps_data)

def listener():
	rospy.init_node('listener', anonymous=True)
	rospy.Subscriber("/gps/fix", NavSatFix, gps_callback)
	rospy.spin()

if __name__ == '__main__':
	listener()

