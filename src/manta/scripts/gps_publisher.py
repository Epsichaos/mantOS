#!/usr/bin/env python
import rospy
from manta.msg import NavSatFix

import os
from gps import *
from time import *
import time
import math

global gpsd
gpsd = None
gpsd = gps(mode=WATCH_ENABLE)

def talker():
	pub = rospy.Publisher("/gps/fix", NavSatFix, queue_size=10)
	rospy.init_node('talker', anonymous=True)
	rate = rospy.Rate(10)
	while not rospy.is_shutdown():
		#gps config
		gpsd.next()
		os.system('clear')
		gps_data = NavSatFix()
		#status of gps
#		gps_data.status.status = 0
#		gps_data.status.service = 1
		#time
		gps_data.header.stamp.secs = round(time.time())
		#position
		gps_data.latitude = gpsd.fix.latitude
		gps_data.longitude = gpsd.fix.longitude
		gps_data.altitude = 0
#		gps_data.position_covariance_type = 0
		#publication ros		
		pub.publish(gps_data)
		rate.sleep()
		
if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass
