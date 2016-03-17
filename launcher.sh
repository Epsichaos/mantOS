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
echo '[MANTA] Waiting Roscore 7 seconds'
sleep 7
rosrun manta imu_publisher.py &
rosrun manta gps_publisher.py &
rosrun hokuyo_node hokuyo_node &
rosrun manta position_subscriber.py 
#screen -dm rosrun manta imu_publisher.py
#echo '[MANTA] Imu publisher executed'
#sleep 1
#screen -dmS gps rosrun manta gps_publisher.py
#echo '[MANTA] Gps publisher executed'
sleep 1
#screen -dmS telemeter rosrun hokuyo_node hokuyo_node
#echo '[MANTA] Hokuyo node executed'
#sleep 1
#rosrun manta position_subscriber.py
