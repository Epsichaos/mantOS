#!/usr/bin/env python
import rospy
import time
from manta.msg import Gps
from manta.msg import Imu

def general_callback(data):
	if hasattr(data, 'acc_x'):
		rospy.loginfo("Imu detected")
		rospy.loginfo(data.acc_x)
	else:
		rospy.loginfo("Gps detected")
		rospy.loginfo(data.latitude)

def gps_callback(gps_data):
	#rospy.loginfo(gps_data.latitude)
	#rospy.loginfo(gps_data.longitude)
	#rospy.loginfo(gps_data.speed)
	rospy.loginfo("NIQUE LE GPS")
	latitude = gps_data.latitude
	longitude = gps_data.longitude
	speed = gps_data.speed

def imu_callback(imu_data):
	#rospy.loginfo("acc_x = %f, acc_y = %f, acc_z = %f", imu_data.acc_x, imu_data.acc_y, imu_data.acc_z)
	#rospy.loginfo("gyro_x = %f, gyro_y = %f, gyro_z = %f", imu_data.gyro_x, imu_data.gyro_y, imu_data.gyro_z)
	#rospy.loginfo("magn_x = %f, magn_y = %f, magn_z = %f", imu_data.magn_x, imu_data.magn_y, imu_data.magn_z
	rospy.loginfo("NIQUE L'IMU")
	acc_x = imu_data.acc_x
	acc_y = imu_data.acc_y
	acc_z = imu_data.acc_z
	magn_x = imu_data.magn_x
	magn_y = imu_data.magn_y
	magn_z = imu_data.magn_z
	gyro_x = imu_data.gyro_x
	gyro_y = imu_data.gyro_y
	gyro_z = imu_data.gyro_z

def listener():
	rospy.init_node('listener', anonymous=True)
	rospy.Subscriber('gps', Gps, general_callback)
	rospy.Subscriber('imu', Imu, general_callback)
	rospy.spin()

if __name__ == '__main__':
	listener()

