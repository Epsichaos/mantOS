#!/usr/bin/env python
import rospy
import time
from manta.msg import NavSatFix
from manta.msg import Imu
from sensor_msgs.msg import LaserScan

def general_callback(data):
	if hasattr(data, 'linear_acceleration'):
		rospy.loginfo("Imu detecte")
		rospy.loginfo(data)
	elif hasattr(data, 'latitude'):
		rospy.loginfo("Gps detecte")
		rospy.loginfo(data)
	else:
		rospy.loginfo("Telemetre detecte")
		rospy.loginfo(data)
def listener():
	rospy.init_node('listener', anonymous=True)
	#rospy.Subscriber('/gps/fix', Gps, general_callback)
	rospy.Subscriber('/imu/data', Imu, general_callback)
	rospy.Subscriber('scan', LaserScan, general_callback)
	rospy.spin()

if __name__ == '__main__':
	listener()
