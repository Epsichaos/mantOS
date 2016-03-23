#!/bin/sh

echo '------- LANCEMENT DU SCRIPT MANTA -------' 
sleep 1
echo '5'
sleep 1
echo '4'
sleep 1
echo '3'
sleep 1
echo '2'
sleep 1
echo '1'
sleep 1
echo ' Launch in progress...' 
screen -dmS roscore roscore
echo '[MANTA] Roscore executed'
echo '[MANTA] Waiting Roscore 10 seconds'
sleep 10
rosrun manta imu_publisher.py &
rosrun manta gps_publisher.py &
#rosrun hokuyo_node hokuyo_node &
rosrun manta echo_publisher &
rosrun manta position_subscriber.py 

