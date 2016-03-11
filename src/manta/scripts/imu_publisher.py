#!/usr/bin/env python
import rospy
#from manta.msg import Imu
#from sensor_msgs.msg import Imu
from manta.msg import Imu
from pyrr import *

import sys, getopt

sys.path.append('.')
import RTIMU
import os.path
import time
import math

def imuToQuaternion(magnetic_field, acceleration, angular_vel, dt):
	rotation_quaternion = Quaternion([0.0, 0.0, 0.0, 1.0])
#	rotation_quaternion.create(0.0, 0.0, 0.0, 1.0)
	correction = Vector3([0.0, 0.0, 0.0])
	
	# correspnd a rotation compass
	down = Vector3([-acceleration.x, -acceleration.y, -acceleration.z])
	east = Vector3.cross(down, magnetic_field)
	north = Vector3.cross(east, down)
	
	down.normalise()
	east.normalise()
	north.normalise()

	# m est le resultat de rotation compass
#	m = Matrix33()
	m = Matrix33([north, east, down])

#	m = Matrix33()
#	m = Matrix33([[north.x, north.y, north.z], [east.x, east.y, east.z], []])
	
	vector_norm = math.sqrt(acceleration.x*acceleration.x + acceleration.y*acceleration.y + acceleration.z*acceleration.z)
	test = abs(vector_norm - 1)	
	if(test <= 0.3):
		correction_strength = 1.0
		rotationCompass = m		
		rotationMatrix = rotation_quaternion.matrix33
		#colonnes de rotMat
		rotationMatrixC1 = Vector3([rotationMatrix.m11, rotationMatrix.m21, rotationMatrix.m31])
		rotationMatrixC2 = Vector3([rotationMatrix.m12, rotationMatrix.m22, rotationMatrix.m32])
		rotationMatrixC3 = Vector3([rotationMatrix.m13, rotationMatrix.m23, rotationMatrix.m33])
		#colonnes de rotComp
		rotationCompassC1 = Vector3([rotationCompass.m11, rotationCompass.m21, rotationCompass.m31])
		rotationCompassC2 = Vector3([rotationCompass.m12, rotationCompass.m22, rotationCompass.m32])
		rotationCompassC3 = Vector3([rotationCompass.m13, rotationCompass.m23, rotationCompass.m33]) 
		#prduit vectoriel
		prod1 = Vector3.cross(rotationCompassC1, rotationMatrixC1)
		prod2 = Vector3.cross(rotationCompassC2, rotationMatrixC2)
		prod3 = Vector3.cross(rotationCompassC3, rotationMatrixC3)
		#somme
		correction = (prod1 + prod2 + prod3)*correction_strength 
	angular_velocity_corrected = angular_vel + correction	
	temp = Quaternion([1.0, angular_velocity_corrected[0] * dt/2, angular_velocity_corrected[1] * dt/2, angular_velocity_corrected[2] * dt/2])	
	rotation_quaternion *= temp

	return rotation_quaternion

def talker():
	# ROS SETTINGS
	pub = rospy.Publisher("/imu/data", Imu, queue_size=10)
	rospy.init_node('talker', anonymous=True)
	rate = rospy.Rate(10)
	
	# IMU LIB SETTINGS
	SETTINGS_FILE = "RTIMULib"

	print("Using settings file " + SETTINGS_FILE + ".ini")
	if not os.path.exists(SETTINGS_FILE +".ini"):
		print("Settings file does not exist, will be created")

	s = RTIMU.Settings(SETTINGS_FILE)
	imu = RTIMU.RTIMU(s)

	print("IMU Name : " + imu.IMUName())

	if(not imu.IMUInit()):
		print("IMU Init Failed")
		sys.exit(1)
	else:
		print("IMU init succeeded")

	imu.setGyroEnable(True)
	imu.setAccelEnable(True)
	imu.setCompassEnable(True)

	#start time
	start = int(round(time.time()*1000))

	while not rospy.is_shutdown():
		last_start = start
		start = int(round(time.time()*1000))
		dt = (start - last_start)/1000.0
		if (dt<0):
			rospy.loginfo("PB TEMPS NIQUE")
		#read imu data
		imu.IMURead()
		data = imu.getIMUData()
		#define the vectors
		magnetic_field = Vector3([data["compass"][0], data["compass"][1], data["compass"][2]])
		acceleration = Vector3([data["accel"][0], data["accel"][1], data["accel"][2]])
		angular_vel = Vector3([data["gyro"][0], data["gyro"][1], data["gyro"][2]])
		#genere le quaternion
		rotation_quaternion = imuToQuaternion(magnetic_field, acceleration, angular_vel, dt)
		rospy.loginfo(rotation_quaternion)

		#initialize imu variable
		imu_data = Imu()
		#set time
		imu_data.header.stamp.secs = round(time.time())
		imu_data.linear_acceleration.x = acceleration.x
		imu_data.linear_acceleration.y = acceleration.y
		imu_data.linear_acceleration.z = acceleration.z
		imu_data.linear_acceleration_covariance[0] =  data["accel"][0]
		imu_data.linear_acceleration_covariance[1] = 0.0
		imu_data.linear_acceleration_covariance[2] = 0.0
		imu_data.linear_acceleration_covariance[3] = 0.0
		imu_data.linear_acceleration_covariance[4] = data["accel"][1]
		imu_data.linear_acceleration_covariance[5] = 0.0
		imu_data.linear_acceleration_covariance[6] = 0.0
		imu_data.linear_acceleration_covariance[7] = 0.0
		imu_data.linear_acceleration_covariance[8] = data["accel"][2]
		imu_data.angular_velocity.x = angular_vel.x
		imu_data.angular_velocity.y = angular_vel.y
		imu_data.angular_velocity.z = angular_vel.z
		imu_data.angular_velocity_covariance[0] = data["gyro"][0]
		imu_data.angular_velocity_covariance[1] = 0.0
		imu_data.angular_velocity_covariance[2] = 0.0
		imu_data.angular_velocity_covariance[3] = 0.0
		imu_data.angular_velocity_covariance[4] = data["gyro"][1]
		imu_data.angular_velocity_covariance[5] = 0.0
		imu_data.angular_velocity_covariance[6] = 0.0
		imu_data.angular_velocity_covariance[7] = 0.0
		imu_data.angular_velocity_covariance[8] = data["gyro"][2]
		imu_data.orientation.x = rotation_quaternion.x
		imu_data.orientation.y = rotation_quaternion.y
		imu_data.orientation.z = rotation_quaternion.z
		imu_data.orientation.w = rotation_quaternion.w
		imu_data.orientation_covariance[0] = 0.0
		imu_data.orientation_covariance[1] = 0.0
		imu_data.orientation_covariance[2] = 0.0
		imu_data.orientation_covariance[3] = 0.0
		imu_data.orientation_covariance[4] = 0.0
		imu_data.orientation_covariance[5] = 0.0
		imu_data.orientation_covariance[6] = 0.0
		imu_data.orientation_covariance[7] = 0.0
		imu_data.orientation_covariance[8] = 0.0

		rospy.loginfo('message sent')
		pub.publish(imu_data)
		rate.sleep()
		
if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass
